import user_controller
from flask import Flask, abort, redirect, url_for, render_template, \
    send_from_directory, request
from flask.ext.api import status
from pyArango.connection import *

app = Flask(__name__, static_url_path='/static', static_folder='../client/dist/')
conn = Connection(arangoURL='http://127.0.0.1:8529', username='root', password='foobar')
db = conn['RelationalSchema']

@app.route('/users/', methods=['GET', 'POST'])
def users():
    uname = "No username provided"
    print('test')
    if (request.method == 'POST'):
        data = request.get_json()
        return user_controller.createUser(db, data['username']), status.HTTP_201_CREATED

    if (request.method == 'GET'):
        return uname


@app.route('/')
@app.route('/<path:path>')
def default(**path):
    # Note that path will be in a list here
    return send_from_directory('../client/src/', 'index.html')


if (__name__ == '__main__'):
    app.run(debug=True)
