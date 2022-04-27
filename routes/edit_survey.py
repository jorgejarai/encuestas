from __main__ import app
from turtle import title
from flask import render_template
from db import surveys

@app.route('/edit')
def edit_survey():
    data = surveys.Surveys().get_all()
    return render_template("edit_survey.html", titles = data)
