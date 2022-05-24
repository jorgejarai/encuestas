from __main__ import app
from curses.ascii import US
from flask import request
from db import surveys
from flask_cors import cross_origin


from db.users import Users

@app.route('/respondents', methods=['GET'])
@cross_origin()
def get_respondents():
    data = Users().get_respondents()
    if not data:
        return {
            "status": "error",
            "message": "No hay encuestados"
        }

    return {
        "status": "success",
        "respondents": data
    }


@app.route('/respondents/<id>', methods=['GET'])
@cross_origin()
def get_respondents_by_id(id):
    data = Users().get_by_id(id)

    if not data:
        return {
            "status": "error",
            "message": "No se encontró al encuestado"
        }

    return {
        "status": "success",
        "respondents": data
    }