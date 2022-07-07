#!/usr/bin/env python3

from flask import Flask
from flask_cors import CORS
from db import Database
import sys

app = Flask(__name__)
if len(sys.argv) > 1 and sys.argv[1] == 'prod':
    app.config['MONGO_URI'] = "mongodb://localhost:27017/encuestas"
else:
    app.config['MONGO_URI'] = "mongodb+srv://encuestas:encuestas@cluster0.m6eyi.mongodb.net/encuestas?retryWrites=true&w=majority"

# mongodb+srv://encuestas:encuestas@cluster0.m6eyi.mongodb.net/encuestas?retryWrites=true&w=majority
# mongodb://localhost:27017/encuestas
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
import routes.send_email  # nopep8
import routes.get_statistics  # nopep8

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'prod':
        app.run(host="0.0.0.0", port=5003,
                ssl_context=('cert.pem', 'key.pem'))
    else:
        app.run(host="0.0.0.0", port=5003, debug=True)
