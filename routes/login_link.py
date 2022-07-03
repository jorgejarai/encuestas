from __main__ import app
from flask import request, make_response, redirect
from flask_cors import cross_origin
from auth import requires_auth

from db.link_sessions import LinkSessions


@app.route('/login_link', methods=['POST'])
@cross_origin()
@requires_auth
def generate_link():
    email = request.json["email"]
    survey = request.json["survey"]

    if not email:
        return {
            "status": "error",
            "message": "Necesita un email"
        }

    link = LinkSessions().add(email, survey)

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

    link_session = LinkSessions().check(secret)

    if not link_session:
        return {
            "status": "error",
            "message": "Secreto inválido"
        }

    ret = make_response(
        redirect(f'localhost:3000/answerSurvey/{link_session["survey_id"]}/{link_session["user_id"]}'))
    ret.set_cookie("link_secret", secret)

    return ret
