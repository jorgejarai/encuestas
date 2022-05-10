from __main__ import app
from db import surveys
from flask_cors import cross_origin


@app.route('/surveys', methods=['GET'])
@cross_origin()
def get_surveys():
    data = surveys.Surveys().get_all()

    if not data:
        return {
            "status": "error",
            "message": "No hay encuestas"
        }

    return {
        "status": "success",
        "data": data
    }


@app.route('/surveys/<id>', methods=['GET'])
@cross_origin()
def get_survey_by_id(id):
    data = surveys.Surveys().get_by_id(id)

    if not data:
        return {
            "status": "error",
            "message": "No se encontró la encuesta"
        }

    return {
        "status": "success",
        "data": data
    }
