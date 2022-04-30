from __main__ import app
from flask import flash, render_template, request, url_for, redirect
from db import surveys
import json
import pprint


@app.route('/edit')
def edit_survey():
    data = surveys.Surveys().get_all()
    return render_template("edit_survey.html", encuestas=data)


@app.route('/edit/<id>')
def get_surveyid(id):
    data = surveys.Surveys().get_by_id(id)
    questions = data.get('questions')

    num_questions = len(questions)
    num_alternatives = []

    for i in range(0, num_questions):
        num_alternatives.insert(i, len(questions[i].get('alternatives')))

    return render_template("edit_surveydata.html", encuesta=data, num_q=num_questions, num_a=num_alternatives)


@app.route('/update/<id>', methods=['POST'])
def update_survey(id):
    name = request.form['surveyName']
    interests = request.form['interests']

    payload = request.form["payload"]
    questions = json.loads(payload)["questions"]

    formatted_interests = [x for x in interests.strip().split(" ") if x]
    formatted_questions = [{"position": i,
                            "label": q["title"].strip(),
                            "type": "selection",
                            "alternatives":
                                [{"value": alternative.strip(),
                                    "label": alternative.strip()}
                                    for alternative in q["alternatives"]
                                    if alternative.strip() != ""]
                            } for i, q in enumerate(questions)]

    try:
        new_survey = {
            "title": name.strip(),
            "interests": formatted_interests,
            "questions": formatted_questions
        }
        surveys.Surveys().update(id, survey=new_survey)

    except ValueError as e:
        return {
            "status": "error",
            "message": str(e)
        }

    flash('{} se ha ingresado correctamente'.format(name.strip()))

    return redirect(url_for('edit_survey'))


@app.route('/delete/<string:id>')
def delete_surveyid(id):
    print(id)
    surveys.Surveys().delete(id)
    return redirect(url_for('edit_survey'))
