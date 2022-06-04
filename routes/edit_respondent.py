from __main__ import app
from flask import request
from db.users import Users
from flask_cors import cross_origin


@app.route("/respondents/<id>", methods=['PUT'])
@cross_origin()
def update_respondent(id):
    name = request.json["name"]
    email = request.json["email"]
    interests = request.json["interests"]
    
    if len(name) == 0:
        return {
                "status": "error",
                "message": "Falta el nombre."
            }
    if len(email) == 0:
        return {
                "status": "error",
                "message": "Falta el email."
            }
    if len(interests) == ['']:
        return {
                "status": "error",
                "message": "Faltan intereses."
            }
    try:
        new_respondent = {
            "name": name,
            "interests": interests,
            "email": email,
        }

        Users().update(id, user=new_respondent)
    except ValueError as e:
        return {
            "status": "error",
            "message": str(e)
        }

    return {
        "status": "success",
    }


@app.route('/respondents/<id>', methods=['DELETE'])
@cross_origin()
def delete_respondentid(id):
    try:
        Users().delete(id)
    except ValueError as e:
        return {
            "status": "error",
            "message": str(e)
        }

    return {
        "status": "success",
    }
