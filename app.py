#!/usr/bin/env python3

from flask import Flask

from db import Database

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb+srv://encuestas:encuestas@cluster0.m6eyi.mongodb.net/encuestas?retryWrites=true&w=majority"

Database().setup(app)

import routes.index  # nopep8
import routes.create_survey  # nopep8
import routes.edit_survey #nopep8
import routes.api_survey #nopep8


if __name__ == '__main__':
    app.run(port=3000, debug=True)
