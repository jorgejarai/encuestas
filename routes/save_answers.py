from __main__ import app
from flask import request
from db import surveys
from bson.objectid import ObjectId
from flask_cors import cross_origin


@app.route("/surveys/<id>/answers/<user_id>", methods=['PUT'])
@cross_origin()
def save_answers(id, user_id):
    user_id = ObjectId(request.json["user_id"])
    answers = request.json["responses"]

    for (i, resp) in enumerate(answers):
        if resp == "":
            return {
                "status": "error",
                "message": f"La pregunta {i + 1} no ha sido respondida"
            }

    try:
        surveys.Surveys().add_answers(id, {
            "user_id": user_id,
            "responses": answers
        })
    except ValueError as e:
        return {
            "status": "error",
            "message": str(e)
        }

    return {
        "status": "success",
    }
