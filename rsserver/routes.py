from flask import Flask, abort, redirect, url_for
app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello world!'

@app.route('/anotherpage/', methods=['GET', 'POST'])
def another_page():

	
	
	return 'Another page!'