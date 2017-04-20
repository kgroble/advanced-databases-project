
from flask import Flask, abort, redirect, url_for, render_template, \
        send_from_directory, request

app = Flask(__name__, static_url_path='/static', static_folder='../client/dist/')

uname = "No username provided"

@app.route('/')
def hello_world():
    return send_from_directory('../client/src/', 'index.html')

@app.route('/users/', methods=['GET', 'POST'])
def users():
	global uname
	if (request.method == 'POST'):
		uname = request.form['username']
		# do something with this
		
	if (request.method == 'GET'):
		return uname

if (__name__ == '__main__'):
	app.run(debug=True)