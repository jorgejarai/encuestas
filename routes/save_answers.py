from __main__ import app
from flask import request
from db import surveys
from bson.objectid import ObjectId
from flask_cors import cross_origin

@app.route("/surveys/<id>/answers/<user_id>", methods=['PUT'])
@cross_origin()
def save_answers(id, user_id):
    answers = request.json["answers"]
    answers["user_id"] = ObjectId(answers["user_id"])

    try:
        surveys.Surveys().add_answers(id, answers)
    except ValueError as e:
        return {
            "status": "error",
            "message": str(e)
        }

    return {
        "status": "success",
    }
