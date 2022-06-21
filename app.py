#!/usr/bin/env python3

from flask import Flask
from flask_cors import CORS
from db import Database

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb+srv://encuestas:encuestas@cluster0.m6eyi.mongodb.net/encuestas?retryWrites=true&w=majority"

cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

app.config['AUTH0_DOMAIN'] = 'probable-fortnight.us.auth0.com'
app.config['API_AUDIENCE'] = 'https://equipo3-is2-2022/api'
app.config['ALGORITHMS'] = ['RS256']

Database().setup(app)

import routes  # nopep8
import routes.create_survey  # nopep8
import routes.edit_survey  # nopep8
import routes.get_survey  # nopep8
import routes.login_link  # nopep8
import routes.get_respondents  # nopep8
import routes.edit_respondent  # nopep8
import routes.save_answers  # nopep8
import routes.create_respondent  # nopep8

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5003, debug=True)
