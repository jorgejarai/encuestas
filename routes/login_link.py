from __main__ import app
from flask import request
from flask_cors import cross_origin
from auth import generate_token, requires_auth

from db.link_sessions import LinkSessions


@app.route('/login_link', methods=['POST'])
@cross_origin()
@requires_auth(role='editor')
def generate_link():
    email = request.json["email"]

    if not email:
        return {
            "status": "error",
            "message": "Necesita un email"
        }

    link = LinkSessions().add(email)

    return {
        "status": "success",
        "link": link
    }


@app.route('/login_link', methods=['GET'])
@cross_origin()
def link_login():
    secret = request.args.get('secret')

    if not secret:
        return {
            "status": "error",
            "message": "Necesita un secreto"
        }

    email = LinkSessions().check(secret)

    if not email:
        return {
            "status": "error",
            "message": "Secreto inválido"
        }

    return {
        "status": "success",
        "jwt": generate_token(email)
    }
