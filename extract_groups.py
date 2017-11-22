
from collections import namedtuple
import json
import re
import argparse

from evaluations import status_string, rule_history
DEBUG = False

letters = ['F', 'F', 'D-', 'D', 'D+', 'C-', 'C', 'C+', 'B-', 'B', 'B+', 'A-', 'A', 'A+']

# _grade()
# -------------------------------------------------------------------------------------------------
def _grade(min_gpa, max_gpa):
  """ Convert numerical gpa range to description of required grade in letter-grade form
        below <letter> (when max < 4.0) (should check min < 0.7)
        <letter> or better (when min is > 0.7) (should check max >= 4.0)
        TODO Report anything that doesn't fit one of those two models
        GPA Letter 3×GPA
        4.3 A+      12.9
        4.0 A       12.0
        3.7 A-      11.1
        3.3 B+       9.9
        3.0 B        9.0
        2.7 B-       8.1
        2.3 C+       6.9
        2.0 C        6.0
        1.7 C-       5.1
        1.3 D+       3.9
        1.0 D        3.0
        0.7 D-       2.1
  """
  if max_gpa >= 4.0:
    letter = letters[int(round(min_gpa * 3))]
    return letter + ' or above'
  letter = letters[int(round(max_gpa * 3))]
  return 'below ' + letter

# _course_list()
# -------------------------------------------------------------------------------------------------
def _course_list(courses, is_source):
  """ Given a set of Course namedtuples, generate a display string for the contents of a
      table cell. Enclose segments of the string with spans giving course ids as title elements;
      update the global row_id_str with each course_id.
      Grade requirements and discipline abbreviations appear each time they change.
      If is_source, show grade requirements and sum of course credits
      If not, show sum of transfer_credits
  """
  row_id_str = ''
  # Sort the courss by grade requirement, discipline and course number
  courses = sorted(courses, key=lambda c: (c.grade, c.discipline, int(c.catalog_number)))

  transfer_credits = 0.0
  course_credits = 0.0
  grade = ''
  discipline = ''
  catalog_number = ''
  grade = ''
  string = ''

  for course in courses:
    row_id_str += '{}:'.format(course.course_id)
    if is_source:
      if course.grade != grade:
        if grade != '': string = string.strip('/') + '; '
        grade = course.grade
        string = string.strip('/') + ' {} in '.format(grade)

    if discipline != course.discipline:
      if discipline != '': string = string.strip('/') +'; '
      discipline = course.discipline
      discipline_str = '<apan title="{}">{}</apan>'.format(course.discipline_name, course.discipline)
      string = string.strip('/') + discipline_str + '-'

    if catalog_number != course.catalog_number:
      if not is_source and abs(float(course.course_credits) - float(course.transfer_credits)) > 0.1:
        note = '({:.1f} cr.)'.format(float(course.transfer_credits))
      else:
        note = ''
      catalog_number = course.catalog_number
      string += '<span title="course id: {}">{}{}</span>/'.format(course.course_id,
                                                                  course.catalog_number,
                                                                  note)
      course_credits += float(course.course_credits)
      transfer_credits += float(course.transfer_credits)

  string = string.strip('/')
  row_id_str = row_id_str.strip(':')
  suffix = 's'
  if is_source:
    if course_credits < 2.0 and course_credits > 0: suffix = ''
    return ('{} [{} credit{}]'.format(string, course_credits, suffix),
                              course_credits, row_id_str)
  else:
    if transfer_credits < 2.0 and transfer_credits > 0: suffix = ''
    return ('{} [{} credit{}]'.format(string, transfer_credits, suffix),
                              transfer_credits, row_id_str)


# The values in one row of the db query
# -------------------------------------------------------------------------------------------------
QueryRecord = namedtuple('QueryRecord', """
                          source_course_id
                          destination_course_id
                          priority rule_group
                          min_gpa max_gpa
                          transfer_credits
                          source_institution
                          source_institution_name
                          source_discipline
                          source_discipline_name
                          source_catalog_number
                          source_course_credits
                          destination_institution
                          destination_institution_name
                          destination_discipline
                          destination_discipline_name
                          destination_catalog_number
                          destination_course_credits
                          rule_status""")

# After the user has selected source and destination colleges, and source/destination
# disciplines, there is an array of records, which need to be sorted into rule groups.
# Hypothesis: need only look at source institution, source discipline, rule group, and
# destination institution to establish groups. For each group show courses, group prio
# and gpas.

# Group key: combination of properties that identiy a group
# -------------------------------------------------------------------------------------------------
GroupKey =namedtuple('GroupKey',"""
                      source_institution source_discipline rule_group
                     """)

# Group record: properties for one course-pair in a group. Some of this information is
# redundant across members of the group, so the issue is to sort out the common properties from the
# redundant properties.
# -------------------------------------------------------------------------------------------------
GroupRecord = namedtuple('GroupRecord', """
                          source_course_id
                          source_discipline
                          source_discipline_name
                          source_catalog_number
                          source_course_credits
                          rule_priority
                          transfer_credits
                          grade
                          destination_course_id
                          destination_discipline
                          destination_discipline_name
                          destination_catalog_number
                          destination_course_credits
                          rule_status
                          """)
# Course
# -------------------------------------------------------------------------------------------------
Course = namedtuple('Course', """
                    course_id
                    discipline
                    discipline_name
                    catalog_number
                    course_credits
                    grade
                    transfer_credits""")


def extract_groups(records):
  """ Generate HTML table with information about each rule group.
  """
  table = '<table>\n'
  groups = dict()

  # Process each row of the db query into arrays of courses matched to rule groups.
  # Min and max credits are retained, but will be discarded below because they seem to be
  # irrelevant.
  # Min and max GPA are converted to letter grade requirement text.
  for record in records:
    qr = QueryRecord._make(record)
    key = GroupKey._make((qr.source_institution,
                          qr.source_discipline,
                          qr.rule_group))
    value = GroupRecord._make((qr.source_course_id,
                              qr.source_discipline,
                              qr.source_discipline_name,
                              qr.source_catalog_number.strip(),
                              qr.source_course_credits,
                              qr.priority,
                              qr.transfer_credits,
                              _grade(qr.min_gpa, qr.max_gpa),
                              qr.destination_course_id,
                              qr.destination_discipline,
                              qr.destination_discipline_name,
                              qr.destination_catalog_number.strip(),
                              qr.destination_course_credits,
                              qr.rule_status))
    if key in groups.keys():
      groups[key].append(value)
    else:
      groups[key] = [value]

  # Generate a HTML table row for each group
  # The db query should have produced the keys in institution/discipline/course order. If not, they
  # would have to be sorted here.
  if DEBUG: print('found {} groups'.format(len(groups)))
  for key in groups.keys():
    source_courses = set()
    destination_courses = set()
    rule_status = set()
    first = True

    if DEBUG: print('{} ['.format(key), end='')
    for rule_part in groups[key]:
      if DEBUG:
        if not first:
          print(', ', end='')
        first = False
        print(rule_part, end='')

      # Populate the sets of source and destination courses for this group
      source_courses.add(Course._make((rule_part.source_course_id,
                                       rule_part.source_discipline,
                                       rule_part.destination_discipline_name,
                                       rule_part.source_catalog_number,
                                       rule_part.source_course_credits,
                                       rule_part.grade,
                                       rule_part.transfer_credits)))
      destination_courses.add(Course._make((rule_part.destination_course_id,
                                            rule_part.destination_discipline,
                                            rule_part.destination_discipline_name,
                                            rule_part.destination_catalog_number,
                                            rule_part.destination_course_credits,
                                            rule_part.grade,
                                            rule_part.transfer_credits)))
      rule_status.add(rule_part.rule_status)
    if DEBUG: print(']')

    # All parts of the rule group must have the same reveiw_status. Failure indicates a bug.
    assert len(rule_status) == 1, 'Rule group with mixed review_status values'
    rule_status = rule_status.pop()

    # The id for the row will be a colon-separated list of course_ids, with source and destinations
    # separated by a hyphen
    source_course_list, source_credits, id_str = _course_list(source_courses, True)
    row_id_str = id_str + '-'
    destination_course_list, destination_credits, id_str = _course_list(destination_courses, False)
    row_id_str += id_str
    row_class = 'rule'
    if source_credits != destination_credits:
      row_class = 'rule credit-mismatch'

    # If the rule has been evaluated, the last column is a link to the review history. But if it
    # hasn't been evaluated yet, the last column is just the text that says so.
    status_cell = status_string(rule_status)
    if rule_status != 0:
      status_cell = '<a href="/history/{}" target="_blank">status_cell</a>'.format(key)
    row = """ <tr id="{}" class="{}">
                <td title="{}">{}</td>
                <td>{}</td>
                <td>=></td>
                <td title="{}">{}</td>
                <td>{}</td>
                <td>{}</td>
              </tr>"""\
            .format(row_id_str, row_class,
                    qr.source_institution_name,
                    qr.source_institution,
                    source_course_list,
                    qr.destination_institution_name,
                    qr.destination_institution,
                    destination_course_list,
                    status_cell)
    table += '  {}\n'.format(row)

  table += '\n</table>'
  return table

if __name__ == "__main__":
  parser = argparse.ArgumentParser('Testing transfer rule groups')
  parser.add_argument('--debug', '-d', action='store_true', default=False)
  args = parser.parse_args()

  if args.debug: DEBUG = true

  fp = open('qbcc-ph.json', 'r')
  records = json.load(fp)
  fp.close()
  table = extract_groups(records)
  html = """
  <head>
    <title>Testing Transfer Rule Groups</title>
    <style>
      table {border-collapse: collapse;}
      td, th {border: 1px solid #ccc; padding:0.25em;}
    </style>
  </head>
  <body>
    {}
  </body>
  """.format(table)
  with open('rules.html', 'w') as r:
    r.write(html)
