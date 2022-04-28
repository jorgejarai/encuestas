from __main__ import app
from flask import render_template
from db import surveys

@app.route('/edit')
def edit_survey():
    data = surveys.Surveys().get_all()
    print(data)
    return render_template("edit_survey.html", encuestas = data)

@app.route('/edit/<string:id>')
def edit_surveyid(id):
    return (id)

@app.route('/delete/<string:id>')
def delete_surveyid(id):
    return (id)