from __main__ import app
from flask import request
from db import surveys
from flask_cors import cross_origin
from auth import requires_auth


@app.route("/surveys/<id>", methods=['PUT'])
@cross_origin()
@requires_auth
def update_survey(id):
    title = request.json["title"]
    interests = request.json["interests"]
    questions = request.json["questions"]
    published = request.json["published"]

    if published == True:
        return {
            "status": "error",
            "message": "No se puede editar una encuesta que ha sido publicada."
        }
    if len(title) == 0:
        return {
            "status": "error",
            "message": "La encuesta no tiene título."
        }
    if interests == ['']:
        return {
            "status": "error",
            "message": "La encuesta no tiene intereses."
        }
    if len(questions) == 0:
        return {
            "status": "error",
            "message": "La encuesta no tiene preguntas."
        }

    for (i, question) in enumerate(questions):
        if question["label"] == "":
            return {
                "status": "error",
                "message": f"La pregunta {i + 1} no tiene texto."
            }
        if len(question["alternatives"]) == 0:
            return {
                "status": "error",
                "message": f"La pregunta {i + 1} no tiene alternativas."
            }
        for (j, alt) in enumerate(question["alternatives"]):
            if alt["label"] == "":
                return {
                    "status": "error",
                    "message": f"La pregunta {i + 1} no tiene texto en la alternativa {j+1}."
                }

    formatted_questions = [{
        "label": q["label"].strip(),
        "type": "selection",
        "alternatives": q["alternatives"]
    } for q in questions]

    try:
        new_survey = {
            "title": title.strip(),
            "interests": interests,
            "questions": formatted_questions,
            "published": published
        }
        surveys.Surveys().update(id, survey=new_survey)
    except ValueError as e:
        return {
            "status": "error",
            "message": str(e)
        }

    return {
        "status": "success",
    }


@app.route('/surveys/<id>', methods=['DELETE'])
@cross_origin()
@requires_auth
def delete_surveyid(id):
    try:
        surveys.Surveys().delete(id)
    except ValueError as e:
        return {
            "status": "error",
            "message": str(e)
        }

    return {
        "status": "success",
    }

@app.route('/surveys/<id>/<status>', methods=['PUT'])
@cross_origin()
@requires_auth
def update_status_survey(id, status):
    if status == "publicada":
        new_survey = {
            "published": False
        }
        surveys.Surveys().update(id, survey=new_survey)
        return {
            "status": "success"
        }
    if status == "cerrada":
        new_survey = {
            "published": True,
            "answers": []
        }
        surveys.Surveys().update(id, survey=new_survey)
        return {
            "status": "success"
        }
