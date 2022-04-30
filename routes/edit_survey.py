from __main__ import app
from re import I
from turtle import title
from flask import flash, render_template, request, url_for, redirect
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
        num_alternatives.insert(i, len(questions[i].get('alternatives')))
    

    return render_template("edit_surveydata.html", encuesta = data, num_q = num_questions, num_a = num_alternatives)

@app.route('/update/<id>' , methods = ['POST'])
def update_survey(id):
    inter = []
    title = request.form['surveyName']
    inter.append(request.form['interests']) 
    i = 0
    p_id = []
    
    while "p"+str(i) in request.form.keys(): #se obtienen las preguntas, pero sin alternativas
        p_id.append(request.form["p"+str(i)])
        i +=1
    
    print(p_id)

    surveys.Surveys().update(id,{"title": title,"interests": inter})

    return redirect(url_for('edit_survey'))

@app.route('/delete/<string:id>')
def delete_surveyid(id):
    print(id)
    surveys.Surveys().delete(id)
    return redirect(url_for('edit_survey'))