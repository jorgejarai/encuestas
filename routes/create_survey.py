from __main__ import app
from db.surveys import Surveys
from flask import request
import json
from flask_cors import cross_origin


@app.route('/surveys', methods=["POST"])
@cross_origin()
def create_question():
    name = request.form['surveyName']
    interests = request.form['interests']
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

    return {
        "status": "success",
    }
