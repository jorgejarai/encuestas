from __main__ import app
from flask import make_response, request
from flask_cors import cross_origin

from db.users import Users


@app.route('/login')
@cross_origin()
def login():
    email = request.json["email"]
    password = request.json["password"]

    if not email or not password:
        return {
            "status": "error",
            "message": "Necesita un email y una contraseña"
        }

    if not Users().login(email, password):
        return {
            "status": "error",
            "message": "Email o contraseña incorrectos"
        }

    res = make_response({
        "status": "success",
    })

    # TODO: Generar token JWT y adjuntarlo a la respuesta con una cookie

    return res
