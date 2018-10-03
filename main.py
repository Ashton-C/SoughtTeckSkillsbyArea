import requests
from bs4 import BeautifulSoup
from jobsiteclass import JobSite
from languages import *
from flask import Flask, render_template
from flask_bootstrap import Bootstrap


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
    combine_like_terms()
    to_remove = []
    for word in field:
        if field[word] == 0:
            to_remove.append(word)
    for word in to_remove:
        field.pop(word)


fields = [all_languages, all_frameworks, all_databases, all_platforms]


def sort_list(field):
    pass
    

def prettify_output(field):
    for word in field:
        print("{}% of job postings asked for skills in {}.".format(round(((field.get(word)/(x + y)) * 100.0), 2), word))


def combine(field):
    remove_empty(field)
    sort_list(field)
#    prettify_output(field)

stackoverflow = JobSite("stackoverflow")
indeed = JobSite("indeed")

location = "Portland, OR"

x = 0
#x = stackoverflow.get_listings("Software Developer", location)
y = indeed.get_listings("Software Developer", location)
for field in fields:
    combine(field)

@app.route('/', methods=["GET", "POST"])
def welcome():
    # if "go" in request.form:
    #     get_data()
    #     consolidate(field, fields)
    #     return render_template('home_with_data.html', fields=fields, x=x, y=y, loc=location)
    # else:
        return render_template('home_with_data.html', fields=fields, x=x, y=y, loc=location)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    