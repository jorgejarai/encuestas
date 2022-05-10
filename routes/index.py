from __main__ import app
from flask_cors import cross_origin


@app.route('/')
@cross_origin()
def index():
    return {
        "status": "success",
    }
