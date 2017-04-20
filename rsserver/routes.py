
from flask import Flask, abort, redirect, url_for, render_template, \
        send_from_directory, request

app = Flask(__name__, static_url_path='/static', static_folder='../client/dist/')


@app.route('/users/', methods=['GET', 'POST'])
def users():
	uname = "No username provided"
	if (request.method == 'POST'):
		uname = request.form['username']
		# do something with this

	if (request.method == 'GET'):
		return uname


@app.route('/')
@app.route('/<path:path>')
def default(**path):
    # Note that path will be in a list here
    return send_from_directory('../client/src/', 'index.html')


if (__name__ == '__main__'):
	app.run(debug=True)
