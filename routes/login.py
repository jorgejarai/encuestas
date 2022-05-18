from __main__ import app
from flask import make_response, request
from flask_cors import cross_origin
import datetime
from auth import requires_auth
import jwt

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

    encoded_jwt = jwt.encode({
        "sub": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
        "iat": datetime.datetime.utcnow(),
    }, app.config["JWT_SECRET"], algorithm="HS256")

    return {
        "status": "success",
        "jwt": encoded_jwt
    }
