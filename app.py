from flask import Flask, render_template, request
from scripts.sql_query_simulator import search_transferable_course_from_cc
from scripts.search_list import extract_uc_course_names
import os

app = Flask(__name__)

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(CURR_DIR, 'data')
course_name_csv_path = os.path.join(DATA_DIR, 'course_name.csv')
# read csv file's first column to a list
uc_course_names = extract_uc_course_names()


@app.route('/')
def index():
    return render_template('index.html', courses=uc_course_names)


@app.route('/search')
def search():
    query = request.args.get('query').strip()
    print('query: ', query)
    try:
        results = search_transferable_course_from_cc(query)
    except ValueError as e:
        error_message = str(e)
        return render_template('error.html', error_message=error_message)
    else:
        num_results = len(results)
        return render_template('search.html', results=results, num_results=num_results, courses=uc_course_names)


if __name__ == '__main__':
    app.run(debug=True)
