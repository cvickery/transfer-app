# CUNY Transfer App
# C. Vickery

import sys
import os
import re
import socket

import json
import uuid
import datetime
import time

from pgconnection import pgconnection

from collections import namedtuple
from collections import defaultdict
from collections import Counter

from course_lookup import lookup_courses, lookup_course
from mysession import MySession
from sendemail import send_token, send_message
from reviews import process_pending
from rule_history import rule_history
from format_rules import format_rule, format_rules, format_rule_by_key, institution_names, \
    Transfer_Rule, Source_Course, Destination_Course
from course_lookup import course_attribute_rows, course_search

from known_institutions import known_institutions

from system_status import app_available, app_unavailable, get_reason, \
    start_update_db, end_update_db, start_maintenance, end_maintenance

from flask import Flask, url_for, render_template, make_response,\
    redirect, send_file, Markup, request, jsonify

from propose_rules import _propose_rules

from program_requirements import Requirements

app = Flask(__name__)
app.secret_key = os.urandom(24)

# During local development, enable more detailed log messages from the app.
if os.getenv('DEVELOPMENT') is not None:
  DEBUG = True
else:
  DEBUG = False


# Overhead URIs
# =================================================================================================
@app.route('/favicon.ico')
def favicon():
  return send_file('favicon.ico', mimetype="image/x-icon")


@app.route('/image/<file_name>')
def image_file(file_name):
  return send_file('static/images/' + file_name + '.png')


# _STATUS
# -------------------------------------------------------------------------------------------------
@app.route('/_status/<command>')
def _status(command):
  """ Start/End DB Update / Maintenance
      TODO: Need to add user authentication to this.
  """

  dispatcher = {
      'start_update': start_update_db,
      'end_update': end_update_db,
      'start_maintenance': start_maintenance,
      'end_maintenance': end_maintenance,
      'check': app_available
  }

  if command in dispatcher.keys():
    current_status = dispatcher[command]()
    if current_status:
      return top_menu()
    else:
      return make_response(render_template('app_unavailable.html', result=Markup(get_reason())))
  else:
    return ''


# date2str()
# --------------------------------------------------------------------------------------------------
def date2str(date_str):
  """Takes a string in YYYY-MM-DD form and returns a text string with the date in full English form.
  """
  return datetime.datetime.fromisoformat(date_str).strftime('%B %e, %Y').replace('  ', ' ')


# fix_title()
# -------------------------------------------------------------------------------------------------
def fix_title(str):
  """ Create a better titlecase string, taking specifics of the registered_programs dataset into
      account.
  """
  return (str.strip(' *')
             .title()
             .replace('Cuny', 'CUNY')
             .replace('Mhc', 'MHC')
             .replace('Suny', 'SUNY')
             .replace('\'S', '’s')
             .replace('1St', '1st')
             .replace('6Th', '6th')
             .replace(' And ', ' and ')
             .replace(' Of ', ' of '))


#
# Transfer App Functions
# =================================================================================================
# Map Courses: Look at rules for courses across campuses.
# Review Rules: A sequence of pages for reviewing transfer rules.
# Courses Page: Display the complete catalog of currently active courses for any college.

# REVIEW RULES PAGES
# -------------------------------------------------------------------------------------------------
#   Not posted: display form_1, which displays email prompt, source, and destination lists. User
#   must provide email and select exactly one institution from one of the lists and 1+ institutions
#   from the other list.
#   Posted form_1: display form_2, which provides list of disciplines for the single institution.
#   The user may select 1+ of them.
#   Posted form_2: display form_3, which provides matching transfer rules for all discipline pairs
#   selected. For each one, display a "verified" checkbox and a "notation" text box.
#   Posted form_3: enter all verified/notation data, along with person's email into db; send email
#   for confirmation. When user replies to the email, mark all matching items as confirmed and
#   notify the proper authorities. If confirmation email says no, notify OUR, who can delete them.
#   (This allows people to accidentally deny their work without losing it.)

@app.route('/propose_rules', methods=['POST', 'GET'])
def propose_rules():
  return make_response(render_template('propose_rules.html', result=Markup(_propose_rules())))


# INDEX PAGE: Top-level Menu
# =================================================================================================
# This is the entry point for the transfer application
@app.route('/', methods=['POST', 'GET'])
@app.route('/index/', methods=['POST', 'GET'])
def top_menu():
  if app_unavailable():
    return make_response(render_template('app_unavailable.html', result=Markup(get_reason())))

  """ Display menu of available features.
  """
  conn = pgconnection('dbname=cuny_courses')
  cursor = conn.cursor()
  cursor.execute("select count(*) from transfer_rules")
  num_rules = cursor.fetchone()[0]
  cursor.execute("select * from updates")
  updates = cursor.fetchall()
  catalog_date = 'unknown'
  rules_date = 'unknown'
  for update in updates:
    if update.table_name == 'courses':
      catalog_date = date2str(update.update_date)
    if update.table_name == 'transfer_rules':
      rules_date = date2str(update.update_date)
  cursor.close()
  conn.close()
  # You can put messages for below the menu here:
  result = """
  <div id="update-info">
    <p><sup>&dagger;</sup>{:,} transfer rules as of {}.</p>
  </div>
            """.format(num_rules, rules_date)
  return make_response(render_template('top-menu.html', result=Markup(result)))


# REVIEW_RULES PAGE
# =================================================================================================
@app.route('/review_rules/', methods=['POST', 'GET'])
def review_rules():
  if app_unavailable():
    return make_response(render_template('app_unavailable.html', result=Markup(get_reason())))

  """ (Re-)establish user's mysession and dispatch to appropriate function depending on which form,
      if any, the user submitted.
  """
  if DEBUG:
    print('*** {} / ***'.format(request.method))
  mysession = MySession(request.cookies.get('mysession'))

  # Dispatcher for forms
  dispatcher = {
      'do_form_1': do_form_1,
      'do_form_2': do_form_2,
      'do_form_3': do_form_3,
  }

  if request.method == 'POST':
    # User has submitted a form.
    return dispatcher.get(request.form['next-function'], lambda: error)(request, mysession)

  # Form not submitted yet, so call do_form_0 to generate form_1
  else:
    # clear institutions, subjects, and rules from the session before restarting
    mysession.remove('source_institutions')
    mysession.remove('destination_institutions')
    mysession.remove('source_disciplines')
    mysession.remove('destination_disciplines')
    keys = mysession.keys()
    return do_form_0(request, mysession)


# do_form_0()
# -------------------------------------------------------------------------------------------------
def do_form_0(request, session):
  """
      No form submitted yet; generate the Step 1 page.
      Display form_1 to get aource and destination institutions; user's email.
  """
  if DEBUG:
    print('*** do_form_0({})'.format(session))
  conn = pgconnection('dbname=cuny_courses')
  cursor = conn.cursor()

  cursor.execute("select count(*) from transfer_rules")
  num_rules = cursor.fetchone()[0]
  cursor.execute("select * from updates")
  updates = cursor.fetchall()
  catalog_date = 'unknown'
  rules_date = 'unknown'
  for update in updates:
    if update.table_name == 'courses':
      catalog_date = date2str(update.update_date)
    if update.table_name == 'transfer_rules':
      rules_date = date2str(update.update_date)
  cursor.close()
  conn.close()

  source_prompt = """
    <fieldset id="sending-field"><legend>Sending College(s)</legend>
    <div id="source-college-list">
    """
  n = 0
  for code in institution_names:
    n += 1
    source_prompt += """
        <div class='institution-select'>
          <input type="checkbox" name="source" class="source" id="source-{}" value="{}">
          <label for="source-{}">{}</label>
        </div>
    """.format(n, code, n, institution_names[code])
  source_prompt += """
  </div>
  <div>
    <button type="button" id="all-sources">Select All Sending Colleges</button>
    <button type="button"  id="no-sources">Clear All Sending Colleges</button>
    </div>
  </fieldset>
  """

  destination_prompt = """
    <fieldset id="receiving-field"><legend>Receiving College(s)</legend>
    <div id="destination-college-list">
    """
  n = 0
  for code in institution_names:
    n += 1
    destination_prompt += """
        <div class='institution-select'>
          <input type="checkbox" name="destination" class="destination" id="dest-{}" value="{}">
          <label for="dest-{}">{}</label>
        </div>
    """.format(n, code, n, institution_names[code])
  destination_prompt += """
    </div>
    <div>
    <button type="button" id="all-destinations">Select All Receiving Colleges</button>
    <button type="button"  id="no-destinations">Clear All Receiving Colleges</button>
    </div>
  </fieldset>
  """

  email = ''
  if request.cookies.get('email') is not None:
    email = request.cookies.get('email')
  remember_me = ''
  if request.cookies.get('remember-me') is not None:
    remember_me = 'checked="checked"'

  # Return Form 1
  result = """
    <h1>Step 1: Select Colleges</h1>
    <details class="instructions">
      <summary>
        This is the first step for reviewing the {:,}<sup>&dagger;</sup> existing course
        transfer rules at CUNY.
      </summary>
      <hr>
      <p>
        To see just the rules you are interested in, start here by selecting exactly one sending
        college and at least one receiving college, or exactly one receiving college and one or more
        sending colleges.
        <br/>
        In the next step you will select just the discipline(s) you are interested in, and in the
        last step you will be able to review the rules that match your selections from the first two
        steps.
      </p>
      <p>
        Background information and more detailed instructions are available in the
        <a  target="_blank"
            href="https://docs.google.com/document/d/141O2k3nFCqKOgb35-VvHE_A8OV9yg0_8F7pDIw5o-jE">
            Reviewing CUNY Transfer Rules</a> document.
      </p>
    </details>
    <fieldset>
      <form method="post" action="#" id="form-1">
          {}
          {}
        <fieldset>
          <legend>Your email address</legend>
          <p>
            To record your reviews of transfer rules, you need to supply a valid CUNY email address
            for verification purposes.<br/>If you just want to view the rules, you can use a dummy
            address: <em>nobody@cuny.edu</em>
          </p>
          <label for="email-text">Enter a valid CUNY email address:</label>
          <div>
            <input type="text" name="email" id="email-text" value="{}"/>
            <div>
              <input type="checkbox" name="remember-me" id="remember-me" {}/>
              <label for="remember-me"><em>Remember me on this computer.</em></label>
            </div>
          </div>
          <div id="error-msg" class="error"> </div>
          <input type="hidden" name="next-function" value="do_form_1" />
          <div>
            <button type="submit" id="submit-form-1">Next</button>
          </div>
        </fieldset>
      </form>
    </fieldset>
    <p><a href="/" class="button">Main Menu</a></p>
    <div id="update-info">
      <p><sup>&dagger;</sup>Catalog information last updated {}</p>
      <p>Transfer rules information last updated {}</p>
    </div>
    """.format(num_rules,
               source_prompt,
               destination_prompt,
               email,
               remember_me,
               catalog_date,
               rules_date)

  response = make_response(render_template('review_rules.html', result=Markup(result)))
  response.set_cookie('mysession',
                      session.session_key)

  return response


# do_form_1()
# -------------------------------------------------------------------------------------------------
def do_form_1(request, session):
  """
      Collect source institutions, destination institutions and user's email from Form 1, and add
      them to the session.
      Generate Form 2 to select discipline(s)
  """
  if DEBUG:
     print('*** do_form_1({})'.format(session))

  # Add institutions selected to user's session
  session['source_institutions'] = request.form.getlist('source')
  session['destination_institutions'] = request.form.getlist('destination')

  # Database lookups
  # ----------------
  conn = pgconnection('dbname=cuny_courses')
  cursor = conn.cursor()

  # The CUNY Subjects table, for getting subject descriptions from their abbreviations
  cursor.execute("select * from cuny_subjects order by subject")
  subject_names = {row.subject: row.subject_name for row in cursor}

  # Generate table headings for source and destination institutions
  sending_is_singleton = False
  sending_heading = 'Sending Colleges’'
  receiving_is_singleton = False
  receiving_heading = 'Receiving Colleges’'
  criterion = ''
  if len(session['source_institutions']) == 1:
    sending_is_singleton = True
    criterion = 'the sending college is ' + institution_names[session['source_institutions'][0]]
    sending_heading = '{}’s'.format(institution_names[session['source_institutions'][0]])
  if len(session['destination_institutions']) == 1:
    receiving_is_singleton = True
    receiving_heading = '{}’s'.format(institution_names[session['destination_institutions'][0]])
    if sending_is_singleton:
      criterion += ' and '
    criterion += 'the receiving college is ' + \
        institution_names[session['destination_institutions'][0]]

  # Look up all {source_institution, source_discipline, cuny_subject}
  #         and {destination_institution, destination_discipline, cuny_subject}
  # tuples for the selected source and destination institutions.

  source_institution_params = ', '.join('%s' for i in session['source_institutions'])
  q = """
  select *
     from cuny_disciplines
    where institution in ({})
    """.format(source_institution_params)
  cursor.execute(q, session['source_institutions'])
  source_disciplines = cursor.fetchall()

  destination_institution_params = ', '.join('%s' for i in session['destination_institutions'])
  q = """
  select *
     from cuny_disciplines
    where institution in ({})
    """.format(destination_institution_params)
  cursor.execute(q, session['destination_institutions'])
  destination_disciplines = cursor.fetchall()

  # The CUNY subjects actually used by the source and destination disciplines.
  cuny_subjects = set([d.cuny_subject for d in source_disciplines])
  cuny_subjects |= set([d.cuny_subject for d in destination_disciplines])
  cuny_subjects.discard('')  # empty strings don't match anything in the subjects table.
  cuny_subjects = sorted(cuny_subjects)

  cursor.close()
  conn.close()

  # Build selection list. For each cuny_subject found in either sending or receiving disciplines,
  # list all disciplines for that subject, with checkboxes for selecting either the sending or
  # receiving side.
  # The user sees College: discipline(s) in the table (source_disciplines_str), and that info is
  # encoded as a colon-separated list of college-discipline pairs (source_disciplines_val) as the
  # value of the corresponding cbox. *** TODO *** and then parse the value in do_form_2() ***
  # ===============================================================================================
  selection_rows = ''
  num_rows = 0
  for cuny_subject in cuny_subjects:

    # Sending College(s)’ Disciplines
    #   Both the college and discipline names will be displayed for each cuny_subject, unless there
    #   is only one college involved ("singleton"), in which case only the discipline name is shown.
    source_disciplines_str = ''
    source_disciplines_val = ''
    source_disciplines_set = set()
    for discipline in source_disciplines:
      if discipline.cuny_subject == cuny_subject:
        if sending_is_singleton:
          source_disciplines_set.add(discipline.discipline)
        else:
          source_disciplines_set.add((discipline.institution, discipline.discipline))
    source_disciplines_set = sorted(source_disciplines_set)

    if sending_is_singleton:
      if len(source_disciplines_set) > 1:
        source_disciplines_str = '<div>' + '</div><div>'.join(source_disciplines_set) + '</div>'
      else:
        source_disciplines_str = ''.join(source_disciplines_set)
    else:
      colleges = {}
      for discipline in source_disciplines_set:
        if discipline[0] not in colleges.keys():
          colleges[discipline[0]] = []
        colleges[discipline[0]].append(discipline[1])
      for college in colleges:
        source_disciplines_str += '<div>{}: <em>{}</em></div>'.format(institution_names[college],
                                                                      ', '.join(colleges[college]))

    # Receiving College Disciplines
    destination_disciplines_str = ''
    destination_disciplines_set = set()
    for discipline in destination_disciplines:
      if discipline.cuny_subject == cuny_subject:
        if receiving_is_singleton:
          destination_disciplines_set.add(discipline.discipline)
        else:
          destination_disciplines_set.add((discipline.institution, discipline.discipline))
    destination_disciplines_set = sorted(destination_disciplines_set)

    if receiving_is_singleton:
      destination_disciplines_str = ''
      if len(destination_disciplines_set) > 1:
        destination_disciplines_str = '<div>' + \
                                      '</div><div>'.join(destination_disciplines_set) + '</div>'
      else:
        destination_disciplines_str = ''.join(destination_disciplines_set)
    else:
      colleges = {}
      for discipline in destination_disciplines_set:
        if discipline[0] not in colleges.keys():
          colleges[discipline[0]] = []
        colleges[discipline[0]].append(discipline[1])
      for college in colleges:
        destination_disciplines_str += '<div>{}: <em>{}</em></div>'.\
            format(institution_names[college], ', '.join(colleges[college]))

    # We are showing disciplines, but reporting cuny_subjects.
    source_label = ''
    source_box = ''
    if source_disciplines_str != '':
      source_label = f"""
      <label for="source-subject-{cuny_subject}">{source_disciplines_str}</label>"""
      source_box = """
        <input type="checkbox" id="source-subject-{}" name="source_subject" value="{}"/>
        """.format(cuny_subject, cuny_subject)
    destination_box = ''
    destination_label = ''
    if destination_disciplines_str != '':
      destination_box = """
        <input  type="checkbox"
                checked="checked"
                id="destination-subject-{}"
                name="destination_subject"
                value="{}"/>
        """.format(cuny_subject, cuny_subject)
      destination_label = f"""
      <label for="destination-subject-{cuny_subject}">{destination_disciplines_str}</label>"""
    selection_rows += """
    <tr>
      <td class="source-subject">{}</td>
      <td class="source-subject f2-cbox">{}</td>
      <td><strong title="{}">{}</strong></td>
      <td class="destination-subject f2-cbox">{}</td>
      <td class="destination-subject">{}</td>
    </tr>
    """.format(source_label,
               source_box,

               cuny_subject, subject_names[cuny_subject],

               destination_box,
               destination_label)
    num_rows += 1

  shortcuts = """
              <h2 class="error">
                There are no disciplines that match the combination of colleges you selected.
              </h2>
              """
  if num_rows > 1:
    shortcuts = """
    <table id="f2-shortcuts">
    <tr>
      <td f2-cbox" colspan="2">
        <div>
          <label for="all-source-subjects"><em>Select All Sending Disciplines: </em></label>
          <input  type="checkbox"
                  id="all-source-subjects"
                  name="all-source-subjects" />
        </div>
        <div>
          <label for="no-source-subjects"><em>Clear All Sending Disciplines: </em></label>
          <input type="checkbox" id="no-source-subjects" checked="checked"/>
        </div>
      </td>
      <td f2-cbox" colspan="2">
        <div>
          <label for="all-destination-subjects"><em>Select All Receiving Disciplines: </em>
          </label>
          <input  type="checkbox"
                  id="all-destination-subjects"
                  name="all-destination-subjects"
                  checked="checked"/>
        </div>
        <div>
          <label for="no-destination-subjects"><em>Clear All Receiving Disciplines: </em></label>
          <input type="checkbox" id="no-destination-subjects" />
        </div>
      </td>
    </tr>
    </table>
    """

  # set or clear email-related cookies based on form data
  email = request.form.get('email')
  session['email'] = email  # always valid for this session
  # The email cookie expires now or later, depending on state of "remember me"
  expire_time = datetime.datetime.now()
  remember_me = request.form.get('remember-me')
  if remember_me == 'on':
    expire_time = expire_time + datetime.timedelta(days=90)

  # Return Form 2
  result = """
  <h1>Step 2: Select Sending &amp; Receiving Disciplines</h1>
  <details>
  <summary>Instructions</summary>
  <div class="instructions">
    <p>There are {:,} disciplines where {}.</p>
    Disciplines are grouped by CUNY subject area.<br/>
    Select at least one sending discipline and at least one receiving discipline.<br/>
    By default, all receiving disciplines are selected to account for all possible equivalencies,
    including electives and blanket credit.<br/>
    The next step will show all transfer rules for courses in the corresponding pairs of
    disciplines.
  </div>
  </details>
  <form method="post" action="#" id="form-2">
    <a href="/" class="restart button">Main Menu</a>
    <a href="/review_rules" class="restart">Restart</a>
    <button type="submit">Next</button>
    <input type="hidden" name="next-function" value="do_form_2" />
    {}
    <div id="subject-table-div" class="selection-table-div">
      <table id="subject-table">
        <thead>
          <tr>
            <th class="source-subject">{} Discipline(s)</th>
            <th class="source-subject">Select Sending</th>
            <th>CUNY Subject</th>
            <th class="destination-subject">Select Receiving</th>
            <th class="destination-subject">{} Discipline(s)</th>
          </tr>
        </thead>
        <tbody>
        {}
        </tbody>
      </table>
    </div>
  </form>
  """.format(len(source_disciplines) + len(destination_disciplines), criterion,
             shortcuts, sending_heading, receiving_heading, selection_rows)
  response = make_response(render_template('review_rules.html', result=Markup(result)))
  response.set_cookie('email', email, expires=expire_time)
  response.set_cookie('remember-me', 'on', expires=expire_time)
  return response


# do_form_2()
# -------------------------------------------------------------------------------------------------
def do_form_2(request, session):
  """
      Process CUNY Subject list from form 2.
      Generate form_3: the selected transfer rules for review
  """
  if DEBUG:
    print(f'*** do_form_2()')
    elapsed = time.perf_counter()
  conn = pgconnection('dbname=cuny_courses')
  cursor = conn.cursor()

  # Look up transfer rules where the sending course belongs to a sending institution and is one of
  # the source disciplines and the receiving course belongs to a receiving institution and is one of
  # the receiving disciplines.
  try:
    source_institution_params = ', '.join('%s' for i in session['source_institutions'])
    destination_institution_params = ', '.join('%s' for i in session['destination_institutions'])
  except KeyError:
    # the session is expired or invalid. Go back to Step 1.
    return render_template('review_rules.html', result=Markup("""
                                                           <h1>Session Expired</h1>
                                                           <p>
                                                             <a href="/" class="button">
                                                                Main Menu</a>
                                                             <a href="/review_rules"
                                                                  class="restart button">Restart
                                                              </a>
                                                           </p>

                                                           """))

  # Be sure there is the possibility there will be some rules
  source_subject_list = request.form.getlist('source_subject')
  destination_subject_list = request.form.getlist('destination_subject')

  if len(source_subject_list) < 1:
    return render_template('review_rules.html', result=Markup(
                           '<h1 class="error">No sending disciplines selected.</h1>'))
  if len(destination_subject_list) < 1:
    return render_template('review_rules.html', result=Markup(
                           '<h1 class="error">No receiving disciplines selected.</h1>'))

  # Prepare the query to get the set of rules that match the institutions and cuny_subjects
  # selected.
  if request.form.get('all-source-subjects'):
    source_subjects_clause = ''
  else:
    source_subjects_str = '|'.join(f':{s}:' for s in source_subject_list)
    source_subjects_clause = f"  and '{source_subjects_str}' ~ source_subjects"
    source_subjects = ', '.join(f"'{s}'" for s in source_subject_list)
    source_subjects_clause = f"""
      and id in (select rule_id from subject_rule_map where subject in ({source_subjects}))"""

  # Get all the rules where,
  #  - The source and destination institutions have been selected
  #  and
  #  - The source_subjects have been selected
  q = f"""
  select *
    from transfer_rules
   where source_institution in ({source_institution_params})
     and destination_institution in ({destination_institution_params})
     {source_subjects_clause}
  order by source_institution, destination_institution, subject_area, group_number"""
  cursor.execute(q, (session['source_institutions'] + session['destination_institutions']))
  if cursor.rowcount < 1:
    return render_template('review_rules.html', result=Markup(
                           '<h1 class="error">There are no matching rules.</h1>'))

  all_rules = cursor.fetchall()
  selected_rules = []
  # Get the source and destination course lists from the above set of rules where the destination
  # subject was selected. It's possible to have selected rules that don’t transfer to any of the
  # selected destination subjects, so those rules are dropped while building the selected-rules
  # list.
  if request.form.get('all-destination-subjects'):
    destination_subjects_clause = ''
  else:
    # Create a clause that makes sure the destination course has one of the destination subjects
    destination_subject_list = request.form.getlist('destination_subject')
    destination_subject_params = ', '.join(f"'{s}'" for s in destination_subject_list)
    destination_subjects_clause = f" and dc.cuny_subject in ({destination_subject_params})"

  for rule in all_rules:
    # It’s possible some of the selected rules don’t have destination courses in any of the selected
    # disciplines, so that has to be checked first.
    cursor.execute(f"""
      select  dc.course_id,
              dc.offer_count,
              dc.discipline,
              dc.catalog_number,
              dc.cat_num,
              dc.cuny_subject,
              dc.transfer_credits,
              dn.discipline_name
      from destination_courses dc, cuny_disciplines dn
      where dc.rule_id = %s
        and dn.institution = %s
        and dn.discipline = dc.discipline
        {destination_subjects_clause}
       order by discipline, cat_num
    """, (rule.id, rule.destination_institution))
    if cursor.rowcount > 0:
      destination_courses = [Destination_Course._make(c) for c in cursor.fetchall()]
      cursor.execute("""
        select  sc.course_id,
                sc.offer_count,
                sc.discipline,
                sc.catalog_number,
                sc.cat_num,
                sc.cuny_subject,
                sc.min_credits,
                sc.max_credits,
                sc.min_gpa,
                sc.max_gpa,
                dn.discipline_name
        from source_courses sc, cuny_disciplines dn
        where sc.rule_id = %s
          and dn.institution = %s
          and dn.discipline = sc.discipline
        order by discipline, cat_num
        """, (rule.id, rule.source_institution))
      if cursor.rowcount > 0:
        source_courses = [Source_Course._make(c)for c in cursor.fetchall()]

      # Create the Transfer_Rule tuple suitable for passing to format_rules, and add it to the
      # list of rules to pass.
      selected_rules.append(Transfer_Rule._make(
          [rule.id,
           rule.source_institution,
           rule.destination_institution,
           rule.subject_area,
           rule.group_number,
           rule.source_disciplines,
           rule.source_subjects,
           rule.review_status,
           source_courses,
           destination_courses]))
  cursor.close()
  conn.close()

  if len(selected_rules) == 0:
    num_rules = 'No matching transfer rules found.'
  if len(selected_rules) == 1:
    num_rules = 'There is one matching transfer rule.'
  if len(selected_rules) > 1:
    num_rules = 'There are {:,} matching transfer rules.'.format(len(selected_rules))

  rules_table = format_rules(selected_rules)

  result = f"""
  <h1>Step 3: Review Transfer Rules</h1>
    <details class="instructions">
      <summary>{num_rules}</summary>
      <hr>
      Rules that are <span class="credit-mismatch">highlighted like this</span> have a different
      number of credits taken from the number of credits transferred.
      Hover over the “=>” to see the numbers of credits.<br/>
      Credits in parentheses give the number of credits transferred where that does not match the
      nominal number of credits for a course.<br/>
      Rules that are <span class="evaluated">highlighted like this</span> are ones that you have
      reviewed but not yet submitted.<br/>
      Click on a rule to review it.<br/>
    </details>
    <p>
      <a href="/" class="button">Main Menu</a>
      <a href="/review_rules" class="restart button">Restart</a>
    </p>
    <fieldset id="verification-fieldset"><legend>Review Reviews</legend>
        <p id="num-pending">You have not reviewed any transfer rules yet.</p>
        <button type="text" id="send-email" disabled="disabled">
        Review Your Reviews
      </button>
      <form method="post" action="#" id="review-form">
        Waiting for rules to finish loading ...
      </form>
    </fieldset>
    <div id="rules-table-div" class="selection-table-div">
    {rules_table}
    </div>
  """
  return render_template('review_rules.html', result=Markup(result))


# do_form_3()
# -------------------------------------------------------------------------------------------------
def do_form_3(request, session):
  if DEBUG:
      print('*** do_form_3({})'.format(session))
  reviews = json.loads(request.form['reviews'])
  kept_reviews = [e for e in reviews if e['include']]
  email = session['email']
  if len(kept_reviews) == 0:
    result = '<h1>There are no reviews to confirm.</h1>'
  else:
    message_tail = 'review'
    if len(kept_reviews) > 1:
      num_reviews = len(kept_reviews)
      if num_reviews < 13:
        num_reviews = ['', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten',
                       'eleven', 'twelve'][num_reviews - 1]
      message_tail = '{} reviews'.format(num_reviews)

    # Insert these reviews into the pending_reviews table of the db.
    conn = pgconnection('dbname=cuny_courses')
    cursor = conn.cursor()
    token = str(uuid.uuid4())
    reviews = json.dumps(kept_reviews)
    q = "insert into pending_reviews (token, email, reviews) values(%s, %s, %s)"
    cursor.execute(q, (token, email, reviews))
    conn.commit()
    conn.close()

    # Description message templates
    review_dict = dict()
    review_dict['ok'] = '{}: OK'
    review_dict['not-ok'] = '{}: {}'
    review_dict['other'] = 'Other: {}'

    # Generate description messages
    style_str = ' style="border:1px solid #666;vertical-align:top; padding:0.5em;"'
    suffix = 's'
    if len(kept_reviews) == 1:
      suffix = ''
    review_rows = """
                      <table style="border-collapse:collapse;">
                        <tr>
                          <th colspan="5"{}>Rule</th>
                          <th{}>Your Review{}</th>
                        </tr>
                        """.format(style_str, style_str, suffix)
    for review in kept_reviews:
      event_type = review['event_type']
      if event_type == 'src-ok':
          description = review_dict['ok'].format(re.sub(r'\d+', '',
                                                        review['source_institution']))
      elif event_type == 'dest-ok':
        description = review_dict['ok'].format(re.sub(r'\d+', '',
                                                      review['destination_institution']))
      elif event_type == 'src-not-ok':
        description = review_dict['not-ok'].format(re.sub(r'\d+', '',
                                                          review['source_institution']),
                                                   review['comment_text'])
      elif event_type == 'dest-not-ok':
        description = review_dict['not-ok'].format(re.sub(r'\d+', '',
                                                          review['destination_institution']),
                                                   review['comment_text'])
      else:
        description = review_dict['other'].format(review['comment_text'])

      rule_str = re.sub(r'</tr>',
                        """<td>{}</td></tr>
                        """.format(description), review['rule_str'])
      review_rows += re.sub('<td([^>]*)>', '<td\\1{}>'.format(style_str), rule_str)
    review_rows += '</table>'
    # Send the email
    hostname = os.environ.get('HOSTNAME')
    if hostname and hostname.endswith('.local'):
      hostname = 'http://localhost:5000'
    else:
      hostname = 'https://transfer-app.qc.cuny.edu'
    url = hostname + '/confirmation/' + token

    response = send_token(email, url, review_rows)
    if response.status_code != 202:
      result = 'Error sending email: {}'.format(response.body)
    else:
      result = """
      <h1>Step 4: Respond to Email</h1>
      <p>
        Check your email at {}.<br/>Click on the 'activate these reviews' button in that email to
        confirm that you actually wish to have your {} recorded.
      </p>
      <p>
        Thank you for your work!
      </p>
      <a href="/" class="button">Main Menu</a>
      <a href="/review_rules" class="restart">Restart</a>

      """.format(email, message_tail)
  return render_template('review_rules.html', result=Markup(result))


# PENDING PAGE
# -------------------------------------------------------------------------------------------------
@app.route('/pending')
def pending():
  """ Display pending reviews.
      TODO: Implement login option so defined users can manage this table.
  """
  if app_unavailable():
    return make_response(render_template('app_unavailable.html', result=Markup(get_reason())))

  conn = pgconnection('dbname=cuny_courses')
  cursor = conn.cursor()
  cursor.execute("""
    select email, reviews, to_char(when_entered, 'Month DD, YYYY HH12:MI am') as when_entered
      from pending_reviews""")
  if cursor.rowcount == 0:
    return render_template('review_rules.html', result=Markup("""
        <h1>There are no pending reviews.</h1>
        <p>
          <a href="/"><button>main menu</button></a>
          <a href="/review_rules"><button>Review Transfer Rules</button></a>
        </p>
        """))
  result = '<h1>Pending Reviews</h1>'
  for pending in cursor.fetchall():
    reviews = json.loads(pending.reviews)
    suffix = 's'
    if len(reviews) == 1:
      suffix = ''
    result += f"""
    <details>
      <summary>{len(reviews)} review{suffix} by {pending.email} on {pending.when_entered}</summary>
      <table>
        <tr><th>Rule</th><th>Type</th><th>Comment</th></tr>"""
    for review in reviews:
      result += f"""
                    <tr>
                      <td>{review['rule_key']}</td>
                      <td>{review['event_type']}</td>
                      <td>{review['comment_text']}</td>
                    </tr>"""
    result += '</table></details>'
  cursor.close()
  conn.close()

  result += """
  <p>
    <a href="/" class="button">Main Menu</a>
    <a href="/review_rules" class="button">Review Transfer Rules</a>
  </p>"""
  return render_template('review_rules.html', result=Markup(result))


# CONFIRMATION PAGE
# -------------------------------------------------------------------------------------------------
# This is the handler for clicks in the confirmation email.
# Notifications go to university_registrar, webmaster, and anyone identified with any sending or
# receiving college in the covered rules.
@app.route('/confirmation/<token>', methods=['GET'])
def confirmation(token):
  if app_unavailable():
    return make_response(render_template('app_unavailable.html', result=Markup(get_reason())))

  conn = pgconnection('dbname=cuny_courses')
  cursor = conn.cursor()
  # Get list of colleges involved in the reviews
  #
  q = 'select * from person_roles where role'
  # Make sure the token is received and is in the pending table.
  msg = ''
  q = 'select * from pending_reviews where token = %s'
  cursor.execute(q, (token,))
  if cursor.rowcount == 0:
    msg = '<p class="error">This report has either expired or already been recorded.</p>'
  elif cursor.rowcount != 1:
    msg = f'<p class="error">Program Error: {cursor.rowcount} pending_reviews.</p>'
  else:
    msg, colleges = process_pending(cursor.fetchone())
    # Get list of people to notify
    q = """ select * from person_roles
            where role in ('cuny_registrar', 'webmaster')
               or institution in ({})""".format(', '.join([f"'{c}'" for c in colleges]))
    cursor.execute(q)
    to_people = set()
    cc_people = set()
    bc_people = set()
    for person_role in cursor.fetchall():
      if person_role.role == 'cuny_registrar':
        cc_people.add(person_role)
      elif person_role.role == 'webmaster':
        bc_people.add(person_role)
      else:
        to_people.add(person_role)
    to_list = [{'email': p.email, 'name': p.name} for p in to_people]
    cc_list = [{'email': p.email, 'name': p.name} for p in cc_people]
    bcc_list = [{'email': p.email, 'name': p.name} for p in bc_people]
    try:
     from_person = bc_people.pop()
     from_addr = {'email': from_person.email, 'name': 'CUNY Transfer App'}
    except KeyError:
      from_addr = {'email': 'cvickery@qc.cuny.edu', 'name': 'CUNY Transfer App'}
    # Embed the html table in a complete web page
    html_body = """ <html><head><style>
                      table {border-collapse: collapse;}
                      td, th {
                        border: 1px solid blue;
                        padding:0.25em;
                      }
                    </style></head><body>
                """ + msg.replace('/history', request.url_root + 'history') + '</body></html>'
    response = send_message(to_list,
                            from_addr,
                            subject='Transfer Rule Evaluation Received',
                            html_msg=html_body,
                            cc_list=cc_list,
                            bcc_list=bcc_list)
    if response.status_code != 202:
      msg += f'<p>Error sending notifications: {response.body}</p>'
  cursor.close()
  conn.close()

  result = f"""
  <h1>Confirmation</h1>
  <p>Review Report ID: {token}</p>
  {msg}
  <p><a href="/"><button>main menu</button></a></p>
  """

  return render_template('review_rules.html', result=Markup(result))


# HISTORY PAGE
# -------------------------------------------------------------------------------------------------
# Display the history of review events for a rule.
#
@app.route('/history/<rule>', methods=['GET'])
def history(rule):
  if app_unavailable():
    return make_response(render_template('app_unavailable.html', result=Markup(get_reason())))

  """ Look up all events for the rule, and report back to the visitor.
  """
  result = rule_history(rule)
  return render_template('review_rules.html', result=Markup(result))


# MAP_COURSES PAGE
# -------------------------------------------------------------------------------------------------
# Map courses at one instituition to all other other institutions, or vice-versa.
@app.route('/map_courses', methods=['GET'])
def map_courses():
  """ Prompt for a course (or set of courses in a discipline) at an institution, and display
      view-only information about rules that involve that or those courses.
      Display a CSV-downloadable table.
  """
  if app_unavailable():
    return make_response(render_template('app_unavailable.html', result=Markup(get_reason())))

  conn = pgconnection('dbname=cuny_courses')
  cursor = conn.cursor()
  cursor.execute('select code, prompt from institutions order by prompt')
  options = ['<option value="{}">{}</option>'.format(x[0], x[1]) for x in cursor.fetchall()]
  conn.close()
  institution_select = """
  <select id="institution" name="institution">
    <option value="none" selected="selected">Select a College</option>
    {}
  </select>
  """.format('\n'.join(options))
  # Supply colleges from db now, but use ajax to get a college's disciplines

  result = """
  <h1>Map Course Transfers</h1>
  <div id="setup-div">
    <details>
    <summary>Instructions</summary>
    <div class="instructions">
      <p>
        Select courses of interest in the “Which Courses” section. The number of courses selected
        will be shown.
      </p>
      <p>
        Then use the <span class="pseudo-button">show sending rules</span> button if you want to map
        how these courses transfer <em>to</em> courses at other institutions, or use the <span
        class="pseudo-button">show receiving rules</span> button if you want to map how these
        courses transfer <em>from</em> other institutions.
      </p>
      <p>
        If it takes too long to load the transfer map, reduce the number of courses selected. You
        can also limit the set of colleges mapped to senior, community, or comprehensives using the
        options in the “Which Colleges” section.
      </p>
  </div>
    </details>
    <form action="#" method="POST">
      <fieldset><legend>Which Courses</legend>
        <h2>
          Select one or more of the following groups of courses.
        </h2>
        <div id="grouping-div">
          <label for="course-groups">Groups:</label>
          <select multiple id="course-groups" size="9">
            <option value="all">All course levels</option>
            <option value="below">Below 100-level courses</option>
            <option value="100">100-level courses</option>
            <option value="200">200-level courses</option>
            <option value="300">300-level courses</option>
            <option value="400">400-level courses</option>
            <option value="500">500-level courses</option>
            <option value="600">600-level courses</option>
            <option value="above">Above 600-level courses</option>
          </select>
          <p>
            <em>Note:</em> Catalog numbers greater than 999 will be divided by ten until they are
            in the range 0 to 999 for grouping purposes.
          </p>
        </div>
        <h2>
          Select a college and the discipline for the courses you are interested in.
        </h2>
        <div>
          <label for="institution">College:</label>
          {}
          <span id="discipline-span">
            <label for="discipline">Discipline:</label>
            <input type="text" id="discipline" />
          </span>
        </div>
        <p>
          <strong id="num-courses">No courses</strong> selected.
        </p>
      </fieldset>
      <div>
        <button id="show-sending">show sending rules</button>
        <strong>or</strong>
        <button id="show-receiving">show receiving rules</button>
        <span id="loading">Loading
          <span class="one">.</span>
          <span class="two">.</span>
          <span class="three">.</span>
        </span>
      </div>
      <fieldset><legend>Which Colleges To Map</legend>
          <input  type="checkbox"
                  id="associates"
                  name="which-colleges"
                  value="associates"
                  checked>
          <label for="associates" class="radio-label">Include Associates Degree Colleges</label>
          <input  type="checkbox"
                  id="bachelors"
                  name="which-colleges"
                  value="bachelors"
                  checked>
          <label for="bachelors" class="radio-label">Include Bachelor’s Degree Colleges</label>
      </fieldset>
    </form>
  </div>
  <div id="transfers-map-div">
    <h2>Transfers Map</h2>
    <details class="instructions">
      <summary>
        Each row of the table below shows the number of ways each course listed on the
        <span class="left-right">left</span> transfers <span class="to-from">to</span> other CUNY
        colleges.
      </summary>
      <hr>
      <p>
        If a cell contains zero, there are no rules for transferring the course
        <span class="to-from">to</span> that college. Values greater than one occur when there are
        multiple rules, for example when a course transfers as a particular destination course only
        if the student earned a minimum grade.
      </p>
      <p>
        If a course is <span class="inactive-course">highlighted like this</span>, it is inactive,
        and non-zero rule counts are <span class="bogus-rule">highlighted like this</span>. For
        sending courses, it is possible the rule would be used for students who completed the course
        before it became inactive. But for receiving courses, the rule is definitely an error.
      </p>
      <p>
        If the table is empty, it means that all the courses selected are inactive and there are no
        rules for transferring them from any college. This is correct for inactive courses.
      </p>
      <p>
        If a course is active but has zero values for some colleges, they are <span
        class="missing-rule">highlighted like this</span>.
      </p>
      <p>
        If a course transfers only as blanket credit, it is <span class="blanket-credit">highlighted
        like this</span>.
      </p>
      <p>
        If there are any rules that maps courses to their own institution, they are <span
        class="self-rule">highlighted like this</span>.
      </p>
      <p>
        Hover on courses on the <span class="left-right">left</span> to see their titles. Click on
        them to see complete catalog information.
      </p>
      <p>
        Click on non-zero cells to see details about those rules. (Hovering gives information for
        locating them in CUNYfirst.)
      </p>
    </details>
    <table id="transfers-map-table">
    </table>
    <div>
      <a href="/" class="button">main menu</a>
      <button id="show-setup">change courses or direction</button>
    </div>
  </div>
  <div id="pop-up-div">
    <div id="pop-up-container">
      <div id="dismiss-bar">x</div>
      <div id="pop-up-content"></div>
    </div>
  </div>
  """.format(institution_select)
  return render_template('map-courses.html', result=Markup(result))


# /_INSTITUTIONS
# =================================================================================================
# AJAX access to the institutions table.
@app.route('/_institutions')
def _institutions():
  Institution = namedtuple('Institution', 'code, prompt, name, associates, bachelors')
  conn = pgconnection('dbname=cuny_courses')
  cursor = conn.cursor()
  cursor.execute("""select code, prompt, name, associates, bachelors
                      from institutions order by code
                 """)
  institutions = [Institution._make(x)._asdict() for x in cursor.fetchall()]

  conn.close()
  return jsonify(institutions)


# /_DISCIPLINES
# =================================================================================================
# AJAX access to disciplines offered at a college
#
# Look up the disciplines and return the HTML for a select element named discipline.
@app.route('/_disciplines')
def _disciplines():
  institution = request.args.get('institution', 0)
  conn = pgconnection('dbname=cuny_courses')
  cursor = conn.cursor()
  cursor.execute("""select discipline
                      from disciplines
                      where cuny_subject != 'MESG'
                        and institution = %s
                      order by discipline""", (institution,))
  disciplines = ['<option value="{}">{}</option>'.format(x[0], x[0]) for x in cursor.fetchall()]
  conn.close()
  return jsonify("""<select name="discipline" id="discipline">
    <option value="none" selected="selected">Select a Discipline</option>
    {}
    </select>""".format('\n'.join(disciplines)))


# /_FIND_COURSE_IDS
# ================================================================================================
# AJAX course_id lookup.
@app.route('/_find_course_ids')
def _find_course_ids():
  """ Given an institution and discipline, get all the matching course_ids. Then use range strings
      to select only the ones wanted (100-level, etc.)
      Return an array of {course_id, catalog_number} tuples.
      Cross-listing info (offer_nbr) is not included here because rules don’t know about them.
  """
  institution = request.args.get('institution')
  discipline = request.args.get('discipline')
  ranges_str = request.args.get('ranges_str')
  conn = pgconnection('dbname=cuny_courses')
  cursor = conn.cursor()
  cursor.execute("""select course_id, numeric_part(catalog_number) as cat_num
                    from courses
                    where institution = %s and discipline = %s
                 """, (institution, discipline))
  courses = [[c.course_id, c.cat_num] for c in cursor.fetchall()]

  # Filter out the deplorables
  # Range string syntax: all | min:max [;...]
  range_strings = ranges_str.split(';')
  ranges = []
  for range_string in range_strings:
    min, max = range_string.split(':')
    ranges.append((float(min), float((max))))

  # Keep courses whose numeric part is within one of the ranges
  keepers = []
  for course in courses:
    for range in ranges:
      if 'all' in ranges_str or course[1] >= range[0] and course[1] < range[1]:
        keepers.append(course)
        continue

  # The keepers list included the numeric part of catalog_number as a float so it could be sorted
  # before returning just the array of course_ids.
  keepers.sort(key=lambda c: c[1])
  return jsonify([c[0] for c in keepers])


# /_MAP_COURSE
# =================================================================================================
# AJAX generator of course_map table.
#
# Create a table row for each course_id in course_id_list; a column for each element in colleges.
# Table cells show how many rules there are for transferring that course to or from the institutions
# listed, with the title attribute of each cell being a colon-separated list of rule_keys (if any),
# and class attributes for bogus rules, etc.
# Request type tells which type of request: show-sending or show-receiving.
#
@app.route('/_map_course')
def _map_course():
  # Note to self: there has to be a cleaner way to pass an array from JavaScript
  course_ids = json.loads(request.args.getlist('course_list')[0])
  discipline = request.args.get('discipline')
  colleges = json.loads(request.args.getlist('colleges')[0])

  request_type = request.args.get('request_type', default='show-sending')

  table_rows = []
  conn = pgconnection('dbname=cuny_courses')
  cursor = conn.cursor()
  for course_id in course_ids:
    cursor.execute("""select  course_id,
                              institution,
                              discipline,
                              catalog_number,
                              title,
                              course_status,
                              designation
                      from courses
                      where course_id = %s
                      and discipline = %s
                   """, (course_id, discipline))
    if cursor.rowcount == 0:
      continue
    course_info = cursor.fetchone()
    class_info = 'selected-course'
    if course_info.course_status != 'A':
      class_info = 'selected-course inactive-course'
    course_info_cell = """
                         <th class="clickable {}" title="course_id {}: {} {}"{}>{} {} {}</th>
                       """.format(class_info,
                                  course_info.course_id,
                                  course_info.institution,
                                  course_info.title,
                                  class_info,
                                  course_info.institution.rstrip('0123456789'),
                                  course_info.discipline,
                                  course_info.catalog_number)
    # Collect rules where the selected course is a sending course
    if request_type == 'show-sending':
      row_template = '<tr>' + course_info_cell + '{}</tr>'
      cursor.execute("""select distinct *
                        from transfer_rules r
                        where r.id in (select rule_id from source_courses where course_id = %s)
                        order by source_institution, subject_area, destination_institution
                    """, (course_info.course_id, ))

    else:
      # Collect rules where the selected course is a destination course
      row_template = '<tr>{}' + course_info_cell + '</tr>'
      cursor.execute("""select distinct *
                        from transfer_rules r
                        where r.id in (select rule_id from destination_courses where course_id = %s)
                        order by source_institution, subject_area, destination_institution
                    """, (course_info.course_id, ))
    all_rules = cursor.fetchall()

    # For each destination/source institution, need the count of number of rules and a list of the
    # rules.
    rule_counts = Counter()
    rules = defaultdict(list)
    for rule in all_rules:
      rule_key = '{}-{}-{}-{}'.format(rule.source_institution,
                                      rule.destination_institution,
                                      rule.subject_area,
                                      rule.group_number)
      if request_type == 'show-sending':
        rule_counts[rule.destination_institution] += 1
        rules[rule.destination_institution].append(rule_key)
      else:
        rule_counts[rule.source_institution] += 1
        rules[rule.source_institution].append(rule_key)

    # Ignore inactive courses for which there are no rules
    if sum(rule_counts.values()) == 0 and course_info.course_status != 'A':
      continue

    # Fill in the data cells for each college
    data_cells = ''
    for college in colleges:
      class_info = ''
      num_rules = rule_counts[college]
      if num_rules > 0:
        class_info = 'clickable '
      rules_str = ':'.join(rules[college])
      if course_info.course_status == 'A' and num_rules == 0 and college != course_info.institution:
        class_info += 'missing-rule'
      if num_rules == 1 and (course_info.designation == 'MLA' or course_info.designation == 'MNL'):
        class_info += 'blanket-credit'
      if course_info.course_status != 'A' and num_rules > 0 and college != course_info.institution:
        class_info += 'bogus-rule'
      if num_rules > 0 and college == course_info.institution:
        class_info += 'self-rule'
      class_info = class_info.strip()
      if class_info != '':
        class_info = f' class="{class_info}"'
      data_cells += '<td title="{}"{}>{}</td>'.format(rules_str, class_info, num_rules)
    table_rows.append(row_template.format(data_cells))

  conn.close()
  return jsonify('\n'.join(table_rows))


# /_LOOKUP_RULES
# =================================================================================================
# AJAX access to the rules applicable to a course or set of courses.
#
# Returns up to two HTML strings, one for rules where the course(s) are a sending course, the other
# where it/they are a receiving course.
@app.route('/_lookup_rules')
def lookup_rules():
  institution = request.args.get('institution')
  discipline = request.args.get('discipline')
  original_catalog_number = request.args.get('catalog_number')
  # Munge the catalog_number so it makes a good regex and doesn't get tripped up by whitespace in
  # the CF catalog numbers.
  catalog_number = r'^\s*' + \
      original_catalog_number.strip(' ^').replace(r'\.', r'\\\.').replace(r'\\\\', r'\\')
  # Make sure it will compile when it gets to the db
  try:
    re.compile(catalog_number)
  except re.error:
    return jsonify("""
                   <p class="error">Invalid regular expression:
                   Unable to use "{}" as a catalog number.</p>""".format(original_catalog_number))
  type = request.args.get('type')
  # Get the course_ids
  conn = pgconnection('dbname=cuny_courses')
  cursor = conn.cursor()
  query = """
  select distinct course_id
    from courses
   where institution = %s
     and discipline = %s
     and catalog_number ~* %s
     and course_status = 'A'
     and discipline_status = 'A'
     and can_schedule = 'Y'
     and cuny_subject != 'MESG'
     """

  rules = ''
  cursor.execute(query, (institution, discipline, catalog_number))
  if cursor.rowcount > 0:
    course_ids = ', '.join(['{}'.format(x[0]) for x in cursor.fetchall()])

    # Get the rules
    if type == 'sending':
      source_dest = 'source'
    else:
      source_dest = 'destination'

    query = """
    select distinct
        source_institution||'-'||source_discipline||'-'||group_number||'-'||destination_institution
      from {}_courses
     where course_id in ({})
     order by source_institution||'-'||discipline||'-'||group_number||'-'||destination_institution
    """.format(source_dest, course_ids)
    cursor.execute(query)
    rules = ['<div>{}</div>'.format(format_rule(x[0])) for x in cursor.fetchall()]
    credit_mismatch = False
    for rule in rules:
      if 'credit-mismatch' in rule:
        credit_mismatch = True
        break
    if credit_mismatch:
      rules.insert(0, """<p class="credit-mismatch">Rules higlighted like this have different
                   numbers of credits at the sending and receiving colleges.</p>""")
    rules.insert(0, '<p><em>Hover over catalog numbers for course details.</em></p>')
  if len(rules) == 0:
    if type == 'sending':
      rules = '<p>No sending rules</p>'
    else:
      rules = '<p>No receiving rules</p>'

  return jsonify(rules)


# /_RULES_TO_HTML
# =================================================================================================
# AJAX utility for converting a colon-separated list of rule keys into displayable description of
# the rules. Acts as an interface to format_rule().
@app.route('/_rules_to_html')
def _rules_to_html():
  rule_keys = request.args.get('rule_keys').split(':')
  return jsonify('<hr>'.join([format_rule_by_key(rule_key)[0] for rule_key in rule_keys]))


# /_COURSES
# =================================================================================================
# This route is for AJAX access to course catalog information.
#
# The request object has a course_ids field, which is a colon-separated list of course_ids.
# Look up each course, and return a list of html-displayable objects.
@app.route('/_courses')
def _courses():
  return_list = []
  course_ids = request.args.get('course_ids', 0)
  already_done = set()
  for course_id in course_ids.split(':'):
    if course_id in already_done:
      continue
    already_done.add(course_id)
    course, html = lookup_course(int(course_id), active_only=False)
    if course is not None:
      return_list.append({'course_id': course.course_id,
                          'institution': course.institution,
                          'department': course.department,
                          'discipline': course.discipline,
                          'catalog_number': course.catalog_number,
                          'title': course.title,
                          'html': html})
  return jsonify(return_list)


# /_COURSE_SEARCH
# =================================================================================================
#   AJAX search for a course, given the institution, discipline, and catalog number.
#   May return multiple matching courses, so return a list of html rather than just "the one".
@app.route('/_course_search')
def _course_search():
  search_str = request.args.get('search_string')
  return course_search(search_str)


# /_SESSIONS
# =================================================================================================
# This route is intended as a utility for pruning dead "mysession" entries from the db. A periodic
# script can access this url to prevent db bloat when millions of people start using the app. Until
# then, it's just here in case it's needed.
@app.route('/_sessions')
def _sessions():
  conn = pgconnection('dbname=cuny_courses')
  cursor = conn.cursor()
  q = 'select session_key, expiration_time from sessions order by expiration_time'
  cursor.execute(q)
  result = '<table>'
  now = datetime.datetime.now()
  num_expired = 0
  for row in cursor.fetchall():
    ts = datetime.datetime.fromtimestamp(row['expiration_time'])
    ts_str = ts.strftime('%Y-%m-%d %H:%M:%S')
    status = 'active'
    if ts < now:
      status = 'expired'
      num_expired += 1
    result += '<tr><td>{}</td><td>{}</td><td>{}</td></tr>'.format(row['session_key'],
                                                                  ts_str,
                                                                  status)
  msg = '<p>There were no expired sessions to delete.</p>'
  if num_expired > 0:
    cursor.execute("delete from sessions where expiration_time < {}".format(now.timestamp()))
    conn.commit()
    cursor.close()
    conn.close()

    if num_expired == 1:
      msg = '<p>Deleted one expired session.</p>'
    else:
      msg = '<p>Deleted {} expired sessions.</p>'.format(num_expired)
  return result + '</table>' + msg


# COURSES PAGE
# =================================================================================================
# Pick a college, and see catalog descriptions of all courses currently active there.
# Allow institution to come from the URL
@app.route('/courses/', methods=['POST', 'GET'])
def courses():
  if app_unavailable():
    return make_response(render_template('app_unavailable.html', result=Markup(get_reason())))

  conn = pgconnection('dbname=cuny_courses')
  cursor = conn.cursor()
  institution_code = None
  discipline_code = None
  department_code = None
  institution_name = 'Unknown'
  date_updated = 'Unknown'
  num_active_courses = 0
  discipline_clause = ''
  discipline_name = ''
  department_clause = ''
  department_str = ''
  if request.method == 'POST':
    institution_code = request.form['inst']
  else:
    institution_code = request.args.get('college', None)
    discipline_code = request.args.get('discipline', None)
    department_code = request.args.get('department', None)
    if institution_code is not None:
      if not re.search(r'\d\d$', institution_code):
        institution_code += '01'
      institution_code = institution_code.upper()
      if discipline_code is not None:
        discipline_code = discipline_code.upper()
        discipline_clause = f"and discipline = '{discipline_code}'"
        cursor.execute(f"""select description
                            from disciplines
                           where institution = '{institution_code}'
                             and discipline = '{discipline_code}'
                        """)
        if cursor.rowcount == 1:
          discipline_name = cursor.fetchone().description
      if department_code is not None:
        department_code = department_code.upper()
        department_clause = f"and department = '{department_code}'"
        cursor.execute(f"""select description
                             from cuny_departments
                            where institution = '{institution_code}'
                              and department = '{department_code}'
                        """)
        if cursor.rowcount == 1:
          department_str = f'Offered By the {cursor.fetchone().description} Department'

  if institution_code is not None:
    cursor.execute("""
              select name, date_updated
                from institutions
               where code ~* %s
               """, (institution_code,))
    if cursor.rowcount == 1:
      # Found a college: find out if it offers some courses
      row = cursor.fetchone()
      institution_name = row.name
      date_updated = row.date_updated.strftime('%B %d, %Y')
      cursor.execute(f"""
          select count(*) from courses
           where institution ~* %s {discipline_clause} {department_clause}
             and course_status = 'A'
             and can_schedule = 'Y'
             and discipline_status = 'A'
          """, (institution_code,))
      num_active_courses = cursor.fetchone()[0]

    if discipline_name == '' and department_str == '':
      quantifier = 'All'
    else:
      quantifier = ''
    result = f"""
      <h1>{quantifier} {institution_name} {discipline_name} Courses {department_str}</h1>
      <details><summary style="border:1px solid #ccc;">Legend and Details</summary>
        <div class="instructions">
          <p>{num_active_courses:,} active courses as of {date_updated}</p>
          <p>
            <em>
              The following course properties are shown in parentheses following the catalog
              description:
            </em>
          </p>
          <ul>
            <li title="CUNYfirst uses “career” to mean undergraduate, graduate, etc.">Career;</li>
            <li title="CUNY-standard name for the academic discipline">CUNY Subject;</li>
            <li title="Each course has exactly one Requirement Designation (RD).">
              Requirement Designation;</li>
            <li id="show-attributes"
                title="A course can have any number of attributes. Click here to see descriptions.">
              Course Attributes (a comma-separated list of name:value attribute pairs).
            </li>
          </ul>
          <em>Hover over above list for more information.</em>
          <div id="pop-up-div">
            <div id="pop-up-inner">
              <div id="dismiss-bar">x</div>
              <table>
                <tr><th>Name</th><th>Value</th><th>Description</th></tr>
                {course_attribute_rows}
              </table>
            </div>
          </div>
        </div>
      </details>
      <p id="need-js" class="error">Loading catalog information ...</p>
      """
    result = result + lookup_courses(institution_code,
                                     department=department_code,
                                     discipline=discipline_code)

  if num_active_courses == 0:
    # No courses yet (bogus or missing institution): prompt user to select an institution
    if (institution_code is not None or discipline_code is not None or department_code is not None):
      msg = '<p class="error">No Courses Found</p>'
    else:
      msg = ''
    result = f"""
    <h1>List Active Courses</h1>{msg}
    <p id="need-js" class="error">This app requires JavaScript.</p>
    <p>Pick a college and say “Please”.</p>
    <form method="post" action="#">
    <fieldset><legend>Select a College</legend>"""
    cursor.execute("select * from institutions order by code")
    n = 0
    college_list = ''
    for row in cursor:
      n += 1
      college_list += """
      <div class='institution-select'>
        <input type="radio" name="inst" id="inst-{}" value="{}"/>
        <label for="inst-{}">{}</label>
      </div>
      """.format(n, row.code, n, row.name)
    cursor.close()
    conn.close()
    result += f"""
      {college_list}
      <div>
        <button type="submit">Please</button>
      </div>
    </fieldset></form>
    """
  return render_template('courses.html', result=Markup(result))


# REGISTERED PROGRAMS PAGE
# =================================================================================================
#
@app.route('/download_csv/<filename>')
def download_csv(filename):
  """ Download csv file with the registered programs information for a college.
      THIS IS FRAGILE: The project directory for scraping the NYS DOE website must be located in
      the same folder as this app’s project directory, and it must be named registered_programs.
  """
  return send_file(os.path.join(app.root_path,
                                f'../registered_programs/csv_files/{filename}'))


@app.route('/registered_programs/', methods=['GET'], defaults=({'institution': None}))
def registered_programs(institution, default=None):
  """ Show the academic programs registered with NYS Department of Education for any CUNY college.
  """
  if institution is None:
    institution = request.args.get('institution', None)

  # Allow users to supply the institution in QNS01 or qns01 format; force to internal format ('qns')
  if institution is not None:
    institution = institution.lower().strip('10')
  else:
    institution = 'none'

  # See when the db was last updated
  conn = pgconnection('dbname=cuny_courses')
  cursor = conn.cursor()
  plan_cursor = conn.cursor()
  dgw_conn = pgconnection('dbname=cuny_programs')
  dgw_cursor = dgw_conn.cursor()
  try:
    cursor.execute("select update_date from updates where table_name='registered_programs'")
    update_date = date2str(cursor.fetchone().update_date)
  except (KeyError, ValueError):
    update_date = '<em>None (or in progress)</em>'
  try:
    dgw_cursor.execute("select last_update from updates where institution = %s", (institution, ))
    dgw_update_date = 'was last updated on ' + date2str(str(dgw_cursor.fetchone().last_update))
  except (KeyError, ValueError, AttributeError) as e:
    if institution == 'none':
      dgw_update_date = 'is not available until you select a college.'
    elif institution == 'all':
      dgw_update_date = 'is not available when “All CUNY Colleges” is selected.'
    else:
      dgw_update_date = 'is not available.'

  # Find out what CUNY colleges are in the db
  cursor.execute("""
                 select distinct r.target_institution as inst, i.name
                 from registered_programs r, institutions i
                 where i.code = upper(r.target_institution||'01')
                 order by i.name
                 """)

  if cursor.rowcount < 1:
    result = """
    <h1>There is no registered-program information for CUNY colleges available at this time.</h1>
    """
    return render_template('registered_programs.html', result=Markup(result))

  cuny_institutions = dict([(row.inst, row.name) for row in cursor.fetchall()])
  cuny_institutions['all'] = 'All CUNY Colleges'
  options = '\n'.join([f'<option value="{inst}">{cuny_institutions[inst]}</option>'
                      for inst in cuny_institutions])
  csv_link = ''
  if institution is None or institution not in cuny_institutions.keys():
    h1 = '<h1>Select a CUNY College</h1>'
    table = ''
  else:
    # Complete the page heading
    institution_name = cuny_institutions[institution]

    # Link to the current csv file, if there is one.
    csv_dir = '../registered_programs/csv_files'
    all_clause = ' (<em>Does not include the “CUNY Program(s)” column.</em>)'
    for filename in os.listdir(csv_dir):
      if filename.startswith(institution.upper()):
        if institution == 'all':
          all_clause = ''
        csv_link = f"""<a download class="button" href="/download_csv/{filename}">
                       Download {filename}</a>{all_clause}<br/>"""
        break
    h1 = f'<h1>Registered Academic Programs for {institution_name}</h1>'

    # Generate the HTML table: headings
    headings = ['Program Code',
                'Registration Office',
                'Institution',
                'Title',
                """<a href="http://www.nysed.gov/college-university-evaluation/format-definitions">
                   Formats</a>""",
                'HEGIS',
                'Award',
                'CUNY Program(s)',
                'Certificate or License',
                'Accreditation',
                'First Reg. Date',
                'Latest Reg. Action',
                '<span title="Tuition Assistance Program">TAP</span>',
                '<span title="Aid for Part-Time Study">APTS</span>',
                '<span title="Veteran’s Tuition Assistance">VVTA</span>']
    heading_row = '<thead><tr>' + ''.join([f'<th>{head}</th>' for head in headings])
    heading_row += '</tr></thead>\n'

    # Generate the HTML table: data rows
    if institution == 'all':
      institution = ''  # regex will match all values
    cursor.execute("""
                   select program_code,
                          unit_code,
                          institution,
                          title,
                          formats,
                          hegis,
                          award,
                          certificate_license,
                          accreditation,
                          first_registration_date,
                          last_registration_action,
                          tap, apts, vvta,
                          is_variant
                   from registered_programs
                   where target_institution ~ %s
                   order by title, program_code
                   """, (institution,))
    data_rows = []
    for row in cursor.fetchall():
      if row.is_variant:
        class_str = ' class="variant"'
      else:
        class_str = ''

      values = list(row)
      values.pop()  # Don’t display is_variant value: it is indicated by the row’s class.

      # If the institution column is a numeric string, it’s a non-CUNY partner school, but the
      # name is available in the known_institutions dict.
      if values[2].isdecimal():
        values[2] = fix_title(known_institutions[values[2]][1])

      # Insert list of all CUNY “plans” for this program code
      plan_cursor.execute('select * from academic_plans where program_id = %s', (values[0],))
      plans = plan_cursor.fetchall()
      # If there is a dgw requirement block for the plan, use link to it
      plan_items = []
      for plan in plans:
        dgw_cursor.execute("""
                           select *
                             from requirement_blocks
                            where institution = %s
                              and block_value = %s
                           """, (institution, plan.academic_plan))
        if dgw_cursor.rowcount == 0:
          plan_items.append(plan.academic_plan)
        else:
          plan_items.append('<a href="/academic_plan/{}/{}">{}</a>'
                            .format(institution, plan.academic_plan, plan.academic_plan))
      values.insert(7, ', '.join(plan_items))
      cells = ''.join([f'<td>{value}</td>' for value in values])
      data_rows.append(f'<tr{class_str}>{cells}</tr>')
    table_rows = heading_row + '<tbody>' + '\n'.join(data_rows) + '</tbody>'
    table = f'<div class="table-height"><table class="scrollable">{table_rows}</table></div>'
  result = f"""
      {h1}
        <form action="/registered_programs/" method="GET" id="select-institution">
          <select name="institution">
          <option value="none">No College Selected</option>
          {options}
          </select>
        <p>
          <button id="submit-button" type="submit" form="select-institution">
          Show Selected College</button> or
          <a href="/" class="button">Return to Main Menu</a>
        </p>
      </form>
      <details>
        <summary>Instructions and Options</summary>
        <p>
          <span class="variant">Highlighted rows</span> are for programs with more than one variant,
          such as multiple institutions and/or multiple awards.
        </p>
        <p>
          The Registration Office is either the Department of Education’s Office of the Professions
          (OP) or its Office of College and University Evaluation (OCUE).
        </p>
        <p>
          The last three columns show financial aid eligibility. (Hover over the headings for
          full names.)
        </p>
        <p>
          Latest NYS Department of Education access was on {update_date}.
        </p>
        <p>
          The CUNY Programs column shows matching programs from CUNYfirst. Links in that column
          show the program’s requirements as given in Degreeworks. Degreeworks information
          {dgw_update_date}
        </p>
        <p>
          {csv_link}
        </p>
        <hr>
      </details>
      {table}
"""
  conn.close()
  return render_template('registered_programs.html', result=Markup(result))


@app.route('/academic_plan/<institution>/<plan>/',
           methods=['GET'],
           defaults=({'catalog_year': 'current'}))
def academic_plan(institution, plan, catalog_year):
  conn = pgconnection('dbname=cuny_courses')
  cursor = conn.cursor()
  cursor.execute("""
                 select distinct r.target_institution as inst, i.name
                 from registered_programs r, institutions i
                 where i.code = upper(r.target_institution||'01')
                 order by i.name
                 """)
  cuny_institutions = dict([(row.inst, row.name) for row in cursor.fetchall()])

  conn = pgconnection('dbname=cuny_programs')
  cursor = conn.cursor()

  cursor.execute('select last_update from updates where institution = %s', (institution, ))
  last_update = cursor.fetchone().last_update.strftime('%B %d, %Y')

  cursor.execute("""select *
                      from requirement_blocks
                     where institution = %s
                       and block_value = %s
                  order by period_start desc
                  """, (institution, plan.upper()))
  result = f'<h1>Program Requirements for {plan} at {cuny_institutions[institution]}</h1>'
  result += f'<p>DegreeWorks information as of {last_update}</p>'
  # for row in cursor.fetchall():
  #   start = row.period_start.strip('UG').replace('-20', '-')
  #   stop = row.period_stop.strip('UG').replace('-20', '-')
  #   stop = re.sub('9{3,}', 'Now', stop)
  #   result += f'<h2>Academic Years {start} to {stop}</h2>'
  #   requirement_text = [line.replace('(CLOB)', '').strip()
  #                       for line in row.requirement_text.splitlines()
  #                       if line.strip() != '' and not line.lower().startswith('log:')]
  #   result += f"<pre>{'<br>'.join(requirement_text)}</pre>"
  row = cursor.fetchone()
  requirements = Requirements(row.requirement_text, row.period_start, row.period_stop)
  conn.close()
  result += requirements.html()
  return render_template('academic_program.html', result=Markup(result))


@app.errorhandler(500)
def server_error(e):
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='0.0.0.0', port=5000, debug=True)
