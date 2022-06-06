from __main__ import app
from flask import request
from db import surveys
from db.users import Users
from flask_cors import cross_origin
from io import TextIOWrapper
import csv

# Upload folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Get the upload files


@app.route("/respondents/new", methods=['POST'])
@cross_origin()
def create_respondents():
    if not "application/json" in request.content_type:
        csv_file = request.files['file']
        if csv_file.filename != '':
            csv_file = TextIOWrapper(csv_file, encoding='utf-8')
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            usuarios = []
            for row in csv_reader:
                nombre = row[0]
                correo = row[1]
                rol = row[2]
                intereses = row[3]
                intereses = intereses.split(" ")
                usuarios.append({
                    "Name": nombre,
                    "Email": correo,
                    "Role": rol,
                    "Interests": intereses,
                })
            import_users(usuarios)
        else:
            return {
                "status": "error",
                "message": "Se esperaba un archivo"
            }
    else:
        name = request.json['name']
        email = request.json['email']
        interests = request.json['interests']

        Users().create(name=name, email=email, role='respondent', interests=interests)

    return {"status": "success"}

# Parse CSV function


def import_users(usuarios):
    for user in usuarios:
        print(user['Interests'])
        Users().create(name=user['Name'], email=user['Email'],
                       role=user['Role'], interests=user['Interests'])
