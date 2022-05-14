from __main__ import app
from flask import request
from db import surveys
from flask_cors import cross_origin


@app.route("/surveys/<id>", methods=['PUT'])
@cross_origin()
def update_survey(id):
    title = request.json["title"]
    interests = request.json["interests"]
    questions = request.json["questions"]
    published = request.json["published"]

    for (i, question) in enumerate(questions):
        if len(question["alternatives"]) == 0:
            return {
                "status": "error",
                "message": f"La pregunta {i + 1} no tiene alternativas"
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
