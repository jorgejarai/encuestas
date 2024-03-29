from __main__ import app
from flask import request, make_response, redirect
from flask_cors import cross_origin
from auth import requires_auth
from db import surveys
from db.link_sessions import LinkSessions
import sys


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
        if len(sys.argv) > 1 and sys.argv[1] == 'prod':
            return redirect("https://encuestas-frontend.vercel.app/error")
        else:
            return redirect("http://localhost:6003/error")

    link_session = LinkSessions().check(secret)

    if not link_session:
        if len(sys.argv) > 1 and sys.argv[1] == 'prod':
            return redirect("https://encuestas-frontend.vercel.app/error")
        else:
            return redirect("http://localhost:6003/error")

    ret = None

    if len(sys.argv) > 1 and sys.argv[1] == 'prod':
        ret = make_response(
            redirect(f'https://encuestas-frontend.vercel.app/answerSurvey/{link_session["survey_id"]}/{link_session["user"]}?secret={secret}'))
    else:
        ret = make_response(
            redirect(f'http://localhost:6003/answerSurvey/{link_session["survey_id"]}/{link_session["user"]}?secret={secret}'))

    return ret
