from __main__ import app
from flask import render_template


@app.route('/survey')
def create_survey():
    return render_template("create_survey.html")
