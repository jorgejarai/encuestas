from __main__ import app
from db.surveys import Surveys
from flask import render_template, request, url_for, flash, redirect 
import json
import time
app.secret_key = 'my_key'

@app.route('/survey')
def create_survey():
    
    return render_template("create_survey.html")


@app.route('/survey', methods=["POST"])
def create_question():
    name = request.form['surveyName']
    interests = request.form['interests']
    num_q = int(request.form['questions'])
    num_a = []
    if "Finalizar" in request.form.keys():
        
        payload = request.form["payload"]
        questions = json.loads(payload)["questions"]

        for (i, question) in enumerate(questions):
            if len(question["alternatives"]) == 0:
                return {
                    "status": "error",
                    "message": f"La pregunta {i + 1} no tiene alternativas"
                }

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
            Surveys().create(title=name.strip(),
                             interests=formatted_interests,
                             questions=formatted_questions)
            
        except ValueError as e:
            return {
                "status": "error",
                "message": str(e)
            }

        
        flash('{} se ha ingresado correctamente'.format(name.strip()))
        return redirect(url_for("create_survey"))

    for i in range(num_q):
        num_a.append(0)

    apretaAlt = False
    i = 0

    for k in request.form.keys():
        if "agrega_A" in k:
            apretaAlt = True
            i = int(k.replace('agrega_A', ''))
            break

    if apretaAlt:
        for j in range(num_q):
            v = request.form['num_alt'+str(j)]
            num_a[j] = int(v)
        num_a[i] += 1

    return render_template("create_questions.html", name=name, interests=interests, num_q=num_q, num_a=num_a)