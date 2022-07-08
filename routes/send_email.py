from __main__ import app
from flask import request
from db.users import Users
from bson.objectid import ObjectId
from flask_cors import cross_origin
from src.email_API import Email



@app.route("/postSurvey/<id>", methods=['POST'])
@cross_origin()
def send_email(id):
    try:
        emails = Users().get_respondents()
        correos = []
        for email in emails:
            correos.append(email['email'])
        email= Email()
        with open('static/email_template.html', 'r') as f:
            html_string = f.read()
        email.send_email(correos,'Answer survey',message_format=html_string.format(),format ='html',id_encuesta =id)
        
    except ValueError as e:
        return {
            "status": "error",
            "message": str(e)
        }

    return {
        "status": "success",
    }
    

       