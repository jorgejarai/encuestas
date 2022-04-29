from __main__ import app
from flask import flash, render_template, url_for, redirect
from db import surveys

@app.route('/edit')
def edit_survey():
    data = surveys.Surveys().get_all()
    print(data)
    return render_template("edit_survey.html", encuestas = data)

@app.route('/edit/<id>')
def get_surveyid(id):
    data = surveys.Surveys().get_by_id(id)
    print(data)
    return render_template("edit_surveydata.html", encuesta = data)

@app.route('/delete/<string:id>')
def delete_surveyid(id):
    print(id)
    surveys.Surveys().delete(id)
    return redirect(url_for('edit_survey'))