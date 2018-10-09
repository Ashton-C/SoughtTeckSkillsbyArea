import requests
from bs4 import BeautifulSoup
from jobsiteclass import JobSite
from languages import *
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import operator


app = Flask(__name__)
Bootstrap(app)


def combine_like_terms():
    try:
        all_languages["JavaScript"] += all_languages.get("JS")
        all_languages["JavaScript"] += all_languages.get("Javascript")
        all_languages["C/C++"] += all_languages.get("C++")
        all_languages[" Go "] += all_languages.get("Golang")
    except TypeError:
        pass
    try:
        all_languages.pop("JS")
        all_languages.pop("Javascript")
        all_languages.pop("C++")
        all_languages.pop("Golang")
    except KeyError:
        pass

def remove_empty(field):
    if field == all_languages:
        combine_like_terms()
    to_remove = []
    for word in field:
        if field[word] == 0:
            to_remove.append(word)
    for word in to_remove:
        field.pop(word)


fields = [all_languages, all_frameworks, all_databases, all_platforms]


def sort_list(field):
    sorted_field = sorted(field.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_field


def combine(field):
    remove_empty(field)
    field = sort_list(field)
    return field


def data_collect(fields):
    temp = []
    for field in fields:
        field = combine(field)
        temp.append(field)
    return temp
    

stackoverflow = JobSite("stackoverflow")
indeed = JobSite("indeed")

# Change location here (for now :/).
############################
location = "Salt Lake City, UT"
############################

# test variable
x = 0

# this starts the data collection methods and processes it.
x = stackoverflow.get_listings("Software Developer", location)
y = indeed.get_listings("Software Developer", location)
postings = x + y
fields = data_collect(fields)


@app.route('/', methods=["GET", "POST"])
def welcome():
        return render_template('home.html', fields=fields, postings=postings, loc=location)

@app.route('/data', methods=["GET", "POST"])
def data():
    return render_template('home_with_data.html', fields=fields, postings=postings, loc=location)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    