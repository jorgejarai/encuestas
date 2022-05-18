from __main__ import app
from flask import request
from flask_cors import cross_origin
from auth import generate_token

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

    return {
        "status": "success",
        "jwt": generate_token(email)
    }
