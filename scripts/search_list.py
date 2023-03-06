"""Script to generate search list to help prompt user when searching
"""
from scripts.sql_query_simulator import COURSE_DATA, SCHOOL_DATA


UC_COURSE_CODE = set()
# read uc id from school table
for row in SCHOOL_DATA:
    # 0 is id, 1 is code, 2 is name, 3 is type
    if 'University of California' in row[2]:
        UC_COURSE_CODE.add(row[1])


def extract_uc_course_names():
    """Extract course names from COURSE_DATA
    """
    uc_course_names = []
    for row in COURSE_DATA:
        # 0 is id, 1 is name
        split_id = row[0].split('_')
        if split_id[0] in UC_COURSE_CODE:
            uc_course_names.append(row[0])
    return uc_course_names
