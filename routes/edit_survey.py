from __main__ import app
from flask import flash, render_template, url_for, redirect
from db import surveys

@app.route('/edit')
def edit_survey():
    data = surveys.Surveys().get_all()
    return render_template("edit_survey.html", encuestas = data)

@app.route('/edit/<id>')
def get_surveyid(id):
    data = surveys.Surveys().get_by_id(id)
    questions = data.get('questions')
    print(questions)
    num_questions = len(questions)
    num_alternatives = []
    
    for i in range(0,num_questions):
        print(questions[i].get('alternatives'))
        num_alternatives.insert(i, len(questions[i].get('alternatives')))
    
    print(num_alternatives)

    return render_template("edit_surveydata.html", encuesta = data, num_q = num_questions, num_a = num_alternatives)

@app.route('/delete/<string:id>')
def delete_surveyid(id):
    print(id)
    surveys.Surveys().delete(id)
    return redirect(url_for('edit_survey'))
