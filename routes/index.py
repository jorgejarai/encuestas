from __main__ import app


@app.route('/')
def index():
    return {
        "status": "success",
    }
