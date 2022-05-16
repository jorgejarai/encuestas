#!/usr/bin/env python3

from flask import Flask
from flask_cors import CORS
from db import Database

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb+srv://encuestas:encuestas@cluster0.m6eyi.mongodb.net/encuestas?retryWrites=true&w=majority"

cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

Database().setup(app)

import routes  # nopep8
import routes.create_survey  # nopep8
import routes.edit_survey  # nopep8
import routes.get_survey  # nopep8
import routes.login  # nopep8


if __name__ == '__main__':
    app.run(port=3001, debug=True)
