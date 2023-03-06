import sqlite3
import re
import os
import csv

# Define the paths to the CSV files
CURR_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(CURR_DIR, '..', 'data')

# Load the CSV files into pandas DataFrames
COURSE_PATH = os.path.join(DATA_DIR, 'course_name.csv')
TRANSFERABLE_COURSE_PATH = os.path.join(DATA_DIR, 'transferable_course.csv')
SCHOOL_PATH = os.path.join(DATA_DIR, 'school.csv')

# Load the data from CSV files
with open(TRANSFERABLE_COURSE_PATH, 'r') as f:
    next(f)  # Skip the header line
    TRANSFERABLE_COURSE_DATA = list(csv.reader(f))

with open(SCHOOL_PATH, 'r') as f:
    next(f)  # Skip the header line
    SCHOOL_DATA = list(csv.reader(f))

with open(COURSE_PATH, 'r') as f:
    next(f)  # Skip the header line
    COURSE_DATA = list(csv.reader(f))


def search_transferable_course_from_cc(search_term: str) -> list:
    if not validate_search_term(search_term):
        raise ValueError('Invalid search term')

    # Create a SQLite database in memory
    conn = sqlite3.connect(':memory:')
    cur = conn.cursor()

    # Create tables in the database
    cur.execute('''
        CREATE TABLE transferable_course (
            uc_course_id TEXT,
            cc_course_id TEXT
        )
    ''')
    cur.execute('''
        CREATE TABLE school (
            id INTEGER,
            code TEXT,
            name TEXT,
            type TEXT
        )
    ''')

    # Load data into the tables
    cur.executemany('INSERT INTO transferable_course VALUES (?, ?)', TRANSFERABLE_COURSE_DATA)
    cur.executemany('INSERT INTO school VALUES (?, ?, ?, ?)', SCHOOL_DATA)

    # Run the query
    query = f'''
        WITH tmp AS (
            SELECT uc_course_id, cc_course_id, suc.name as uc_name, scc.name as cc_name
            FROM transferable_course tc
            JOIN school suc ON suc.code = SUBSTR(uc_course_id, 0, INSTR(uc_course_id, '_'))
            JOIN school scc ON scc.code = SUBSTR(cc_course_id, 0, INSTR(cc_course_id, '_'))
        )
        SELECT uc_name || SUBSTR(uc_course_id, INSTR(uc_course_id, '_')),
               cc_name || SUBSTR(cc_course_id, INSTR(cc_course_id, '_'))
        FROM tmp
        WHERE uc_course_id = '{search_term}'
            AND cc_course_id NOT LIKE '%No Course Articulated%'
            AND cc_course_id NOT LIKE '%This course must be taken at the university%'
            AND cc_course_id NOT LIKE '%Never Articulated%'
        LIMIT 1000;
    '''
    cur.execute(query)
    results = cur.fetchall()
    # sort the results by uc course name alphabetically
    results.sort(key=lambda x: x[1])

    # Close the connection and cursor objects
    cur.close()
    conn.close()

    return results


def validate_search_term(search_term: str) -> bool:
    """Check if the search term is valid. Important to prevent SQL injection attacks.
    Can not be totally number, to ensure don't seach for course id.
    """
    if not isinstance(search_term, str):
        return False
    if re.search(r'[;\'"]', search_term) or search_term.isnumeric():
        return False
    return True


# search_term = 'DATA C8'
# results = search_transferable_course_from_cc(search_term)
# print(results)
