from __main__ import app
import email
from flask import request
from db import surveys
from db.users import Users
from flask_cors import cross_origin
import os
import pandas as pd
from os.path import join,dirname, realpath
from io import TextIOWrapper
import csv
#Upload folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Get the upload files
@app.route("/respondents/new", methods=['POST'])
@cross_origin()
def create_respondents():
    if request.method == 'POST':
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
                    "Rol": rol,
                    "Interests": intereses,
                })
            print(usuarios)
            importUsers(usuarios)

    return {"status": "success"}
    
#Parse CSV function
def importUsers(usuarios):
    print("Importar usuarios")
    for user in usuarios:
        print(user['Name'])
        print(user['Email'])
        print(user['Rol'])
        print(user['Interests'])
        Users().create(name=user['Name'],email=user['Email'],role=user['Rol'],interests=user['Interests'],surveys=[])
      
    """Crea un usuario a partir de **kwargs.

        Ejemplo: Users().create(name="Perico Pérez", email="perico@udec.cl",
                       role="respondent", interests=["male", "18-25", "biking",
                                                     "women", "programming"],
                       surveys=[])
        """
