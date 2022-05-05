from __main__ import app
from flask import request
from db import surveys


@app.route("/surveys/<id>", methods=['PUT'])
def update_survey(id):
    title = request.json["title"]
    interests = request.json["interests"]
    questions = request.json["questions"]

    formatted_questions = [{"position": i,
                            "label": q["label"].strip(),
                            "type": "selection",
                            "alternatives": q["alternatives"]
                            } for i, q in enumerate(questions)]

    try:
        new_survey = {
            "title": title.strip(),
            "interests": interests,
            "questions": formatted_questions
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
