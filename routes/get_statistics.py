from __main__ import app
from flask_cors import cross_origin
from auth import requires_auth

from db.surveys import Surveys

@app.route('/statistics/<id>', methods=['GET'])
@cross_origin()
@requires_auth
def get_statistics(id):
    print("STATISTICS")
    data = Surveys().get_by_id(id)
    preguntas=[]
    answers =[]
    for i,question in enumerate(data['questions']):
        preguntas.append([])
        for alternatives in question['alternatives']:
            preguntas[i].append(alternatives['value'])

    for i, answer in enumerate(data['answers']):
        answers.append(answer['responses'])
    
    total = [{},{}]
    for i, pregunta in enumerate(preguntas):
        for alternative in pregunta:
         total[i][alternative] = 0

    for answer in answers:
        for i, alternative in enumerate(answer):
            total[i][alternative] += 1

   

    if not data:
        return {
            "status": "error",
            "message": "No se encontró la encuesta"
        }

    return {
        "status": "success",
        "statistics": total
    }


def cont_answer(id):
    survey = Surveys().get_by_id(id)
    

    if(survey != 'None'):
        answers = {
            'total': len(survey["answers"]),

        }

        for answer in survey["answers"]:
            pass
        
        pass
    pass