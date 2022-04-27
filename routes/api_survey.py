from __main__ import app
from flask import request
from db import surveys

@app.route('/api/survey', methods = ['POST'])
def api_survey():
    encuesta = request.get_json()
    
    surveys.Surveys().create(
        title=encuesta['title'], 
        interests=encuesta['interests'],
        questions=encuesta['questions']
    )
    
    return {"result":"sucess", "survey":encuesta}
