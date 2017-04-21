import user_controller
from flask import Flask, abort, redirect, url_for, render_template, \
    send_from_directory, request
from pyArango.connection import *
from pymongo import MongoClient

app = Flask(__name__, static_url_path='/static', static_folder='../client/dist/')
arangoConn = Connection(arangoURL='http://127.0.0.1:8529', username='root', password='foobar')
arangoDB = arangoConn['RelationalSchema']
mongoConn = MongoClient()
mongoDB = mongoConn.relational_schema

@app.route('/users/', methods=['GET', 'POST'])
def users():
    if (request.method == 'POST'):
        data = request.get_json()
        return user_controller.createUser(arangoDB, mongoDB, data['username'])

    if (request.method == 'GET'):
        return user_controller.getUsers(arangoDB)


@app.route('/')
@app.route('/<path:path>')
def default(**path):
    # Note that path will be in a list here
    return send_from_directory('../client/src/', 'index.html')

if __name__ == '__main__':
    app.run()
