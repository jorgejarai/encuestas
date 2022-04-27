from __main__ import app
from flask import request
from db import surveys

@app.route('/api/survey', methods = ['POST'])
def create_survey():
    encuesta = request.get_json()
    surveys.Surveys().create(**encuesta)
    return {"result":"sucess"}

""" 
dejo esto comentado pq me duele y soy trol, mañana lo borro  

    info = request.json

    title = info['title']
    interests = info['interests']

    return surveys.Surveys().create(title, interests, q_id, q_pos, q_label, q_type, q_format)
    
    q_id = info['question']['id']
    q_pos = info['question']['position']
    q_label = info['question']['label']
    q_type = info['question']['type']
    
    if q_type == 'selection':
        q_opt_label = info['question']['options']['label']
        q_opt_value = info['question']['options']['value']
        return surveys.Surveys().create(title, interests, q_id, q_pos, q_label, q_type, q_opt_label, q_opt_value)
    elif q_type == 'score':
        q_rangeMin = info['question']['range']['min']
        q_rangeMax = info['question']['range']['max']
        return surveys.Surveys().create(title, interests, q_id, q_pos, q_label, q_type, q_rangeMin, q_rangeMax)
    elif q_type == 'freetext':
        q_text = info['question']['text']
        return surveys.Surveys().create(title, interests, q_id, q_pos, q_label, q_type, q_text)
    elif q_type == 'text':
        q_format = info['question']['format']
        return surveys.Surveys().create(title, interests, q_id, q_pos, q_label, q_type, q_format)
 """