from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html")
'''
@app.route('/crear_encuesta')
def crear_encuesta():

	return #logica de crear encuesta, agregar href en base.html

@app.route('/encuestas')
def ver_encuestas():
	return #logica de ver encuestas

@app.route('responder_encuestas')
def responder():
	return #logica de responde encuestas

'''
if __name__ == '__main__':
	app.run(port=3000,debug=True)