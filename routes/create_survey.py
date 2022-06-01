from __main__ import app
from db.surveys import Surveys
from flask import request
from flask_cors import cross_origin


@app.route('/surveys', methods=["POST"])
@cross_origin()
def create_question():
    title = request.json["title"]
    interests = request.json["interests"]
    questions = request.json["questions"]

    if len(title) == 0:
        return {
                "status": "error",
                "message": "La encuesta no tiene título"
            }
    if interests == ['']:
        return {
                "status": "error",
                "message": "La encuesta no tiene intereses"
            }
    if len(questions) == 0:
        return {
                "status": "error",
                "message": "La encuesta no tiene preguntas"
            }
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
        Surveys().create(title=title.strip(),
                         interests=interests,
                         questions=formatted_questions,
                         published=False)
    except ValueError as e:
        return {
            "status": "error",
            "message": str(e)
        }

    return {
        "status": "success",
    }
