"""
  Functions for creating evaluation events, updating rule statuses, and generating associated
  reports. Or maybe just for converting pending evaluations to events and statuses.
"""
import json
from datetime import datetime

from pgconnection import pgconnection
from cuny_course import CUNYCourse

event_type_bits = None
status_messages = None

def status_string(status):
  """
    Generate a string summarizing all bits that are set in status.
  """
  global status_messages
  if status == 0: return 'Not Evaluated'

  if status_messages == None:
    conn = pgconnection('dbname=cuny_courses')
    with conn.cursor() as cursor:
      status_messages = dict()
      cursor.execute('select * from transfer_rule_status')
      for row in cursor.fetchall():
        status_messages[row['value']] = row['description']
    conn.close()
  strings = []
  bit = 1
  for i in range(16):
    if status & bit: strings.append(status_messages[bit])
    bit += bit
  return '; '.join(strings)


def process_pending(row):
  """ Look up the token and generate events. Return as status message.
  """
  global event_type_bits, status_messages

  token = row['token']
  evaluations = json.loads(row['evaluations'])
  email = row['email']
  when_entered = row['when_entered']
  summaries = ''
  conn = pgconnection('dbname=cuny_courses')
  with conn.cursor() as cursor:

    event_type_bits = dict()
    cursor.execute('select * from event_types')
    for row in cursor.fetchall():
      event_type_bits[row['abbr']] = row['bitmask']

    status_messages = dict()
    cursor.execute('select * from transfer_rule_status')
    for row in cursor.fetchall():
      status_messages[row['value']] = row['description']

    for evaluation in evaluations:

      # Generate an event for this evaluation
      event_type = evaluation['event_type']
      src_id = evaluation['rule_src_id']
      dest_id = evaluation['rule_dest_id']
      what = evaluation['comment_text']
      q = """
      insert into events (event_type, src_id, dest_id, who, what, event_time)
                         values (%s, %s, %s, %s, %s, %s)"""
      cursor.execute(q, (event_type, src_id, dest_id, email, what, when_entered))

      # Update the evaluation state for this rule.
      source_course_id = evaluation['rule_src_id']
      destination_course_id = evaluation['rule_dest_id']
      cursor.execute("""
        select * from transfer_rules
         where source_course_id = %s
           and destination_course_id = %s
        """, (source_course_id, destination_course_id))
      rows = cursor.fetchall()
      if len(rows) != 1:
        summaries = """
        <tr><td class="error">Found {} transfer rules for {}:{}</td></tr>
        """.format(source_course_id, destination_course_id)
        break
      old_status = rows[0]['status']
      new_status = old_status | event_type_bits[event_type]
      q = """
        update transfer_rules set status = %s
        where source_course_id = %s
          and destination_course_id = %s
        """
      cursor.execute(q, (new_status, source_course_id, destination_course_id))

      # Generate a summary of this evaluation
      old_status_str = status_string(old_status)
      new_status_str = status_string(new_status)
      # Convert to event-history link for the rule
      new_status_str = """
      <a href="/history/{}" target="_blank">{}</a>""".format(evaluation['rule_index'],
                                                             new_status_str)
      summaries += """
      <tr>
        <td title="{} => {}">{}</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
      </tr>
      """.format(evaluation['rule_src_id'],
                 evaluation['rule_dest_id'],
                 evaluation['rule_str'],
                 evaluation['event_type'],
                 evaluation['comment_text'],
                 old_status_str, new_status_str)
    # Remove record from pending_evaluations
    cursor.execute('delete from pending_evaluations where token = %s', (token, ))

  conn.commit()
  cursor.close()
  conn.close()

  suffix = 's'
  if len(evaluations) == 1: suffix = ''
  return """
  <p>Recorded {} evaluation{} made by <em>{}</em> on {}.</p>
    <table>
      <tr>
      <th>Rule</th><th>Action</th><th>Note</th><th>Previous Status</th>
      <th>New Status<br/><em>Click for Evaluation History</em></th>
      </tr>
      {}
    </table>
    """.format(len(evaluations),
               suffix,
               email,
               when_entered.strftime('%B %d, %Y at %I:%M %p'), summaries)

# rule_history()
# -------------------------------------------------------------------------------------------------
def rule_history(rule):
  """ Generate HTML for the evaluation history of a transfer rule.
  """
  conn = pgconnection('dbname=cuny_courses')
  cursor = conn.cursor()
  return """
  <h1 class="error">Unable to provide evaluation history for transfer rule “{}” at this time.</h1>
  <p>
    Under development.
  </p>
         """.format(rule)
  cursor.execute("""
    select status from transfer_rules where source_course_id = %s and destination_course_id = %s
    """, (source_course_id, destination_course_id))
  rows = cursor.fetchall()
  if len(rows) == 0:
    return '<h1 class="error">{} is not a recognized transfer rule.</h1>'.format(rule)
  status = rows[0]['status']
  status_str = status_string(status)

  source_course = CUNYCourse(source_course_id)
  if not source_course.is_active:
    source_course.html += """
      <div class="warning"><strong>Note:</strong> Course is not active in CUNYfirst</div>"""
  destination_course = CUNYCourse(destination_course_id)
  if not destination_course.is_active:
    destination_course.html += """
      <div class="warning"><strong>Note:</strong> Course is not active in CUNYfirst</div>"""

  # Get the institutions, disciplines, numbers, and titles of the two courses
  result = """
  <h1>Transfer Rule Evaluation Details</h1>
  <h2>Sending Course</h2>
  <div>
    <h3>Course ID:  {:06d}</h3>
    <h3>Institution: {}</h3>
    <h3>Department: {}</h3>
    <h3>Catalog Number:</h3>{}
  </div>

  <h2>Receiving Course</h2>
  <div>
    <h3>Course ID {:06d}</h3>
    <h3>Institution: {}</h3>
    <h3>Department: {}</h3>
    <h3>Catalog Number:</h3>{}
  </div>
  """.format(
    int(source_course.course_id), source_course.institution, source_course.department,
    source_course.html,
    int(destination_course.course_id), destination_course.institution, destination_course.department,
    destination_course.html)
  result += """
    <h2>Transfer Rule Status</h2>
    <div><h3>{}</h3></div>
    <h2>Evaluation History</h2>
    """.format(status_str)
  # Get all the events for the transfer rule
  if status == 0:
    result += '<div class="warning">This rule has not been evaluated yet.</div>'
  else:
    result += '<div><table><tr><th>What</th><th>Comment</th><th>Who</th><th>When</th></tr>'
    q = 'select * from events where src_id = %s and dest_id = %s order by event_time'
    cursor.execute(q, (source_course_id, destination_course_id))
    for row in cursor.fetchall():
      result += """
      <tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>
      """.format(row['event_type'],
                 row['what'],
                 row['who'],
                 row['event_time'].strftime('%B %d, %Y at %I:%M %p'))
    result += '</table></div>'
  cursor.close()
  conn.close()
  return result