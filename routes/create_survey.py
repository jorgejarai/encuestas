from __main__ import app
from flask import render_template, request


@app.route('/survey')
def create_survey():
    return render_template("create_survey.html")

@app.route('/survey', methods = ["POST"])
def create_question():
    if "Finalizar" in request.form.keys():
        lista = request.form.getlist('a0')
        print(lista)
        return "si"     
    name = request.form['surveyName']
    interests = request.form['interests']
    num_q = int(request.form['questions'])
    num_a = []
    for i in range(num_q):
        num_a.append(0)
    apretaAlt = False
    i = 0
    for k in request.form.keys():
        if "agrega_A" in k:
            apretaAlt = True
            i = int(k.replace('agrega_A',''))
            break
    if apretaAlt:
        for j in range(num_q):
            v = request.form['num_alt'+str(j)]
            num_a[j] = int(v)
        #val = request.form['num_alt'+str(i)] #val actual de la cant de prgtas para el correspondiente indice
        num_a[i] +=1

    return render_template("create_questions.html", name=name, interests=interests, num_q = num_q, num_a = num_a)