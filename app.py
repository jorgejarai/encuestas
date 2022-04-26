from flask import Flask, render_template, request
from flask_pymongo import PyMongo

from db import Database

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb+srv://encuestas:encuestas@cluster0.m6eyi.mongodb.net/encuestas?retryWrites=true&w=majority"

Database().setup(app)


def database():
    '''
    funcion para conectar con la base de datos


    '''


def edit_surveys():
    """
            funcion para editar las encuestas
    """


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/CreateSurvey')
def create_survey():

    return render_template("create_survey.html")  # logica de crear encuesta


'''
@app.route('/encuestas')
def see_surveys():

@app.route('responder_encuestas')
def answer():
	return #logica de responde encuestas

'''
if __name__ == '__main__':
    app.run(port=3000, debug=True)
