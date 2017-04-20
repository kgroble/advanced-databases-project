from flask import Flask, abort, redirect, url_for, render_template, \
    send_from_directory, request
import server

app = Flask(__name__, static_url_path='/static', static_folder='../client/dist/')

@app.route('/users/', methods=['GET', 'POST'])
def users():
    if (request.method == 'POST'):
        data = request.get_json()
        server.addUser(data['username'])
        return "POST succeeded"

    if (request.method == 'GET'):
        return server.getUsernames()


@app.route('/')
@app.route('/<path:path>')
def default(**path):
    # Note that path will be in a list here
    return send_from_directory('../client/src/', 'index.html')