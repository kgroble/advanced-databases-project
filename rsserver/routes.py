import user_controller
from flask import Flask, abort, redirect, url_for, render_template, \
    send_from_directory, request, jsonify
from pyArango.connection import *
from pymongo import MongoClient
from flask_api import status

app = Flask(__name__,
            static_url_path='/static',
            static_folder='../client/dist/')
arangoConn = Connection(arangoURL='http://127.0.0.1:8529',
                        username='root',
                        password='foobar')
arangoDB = arangoConn['RelationalSchema']
mongoConn = MongoClient()
mongoDB = mongoConn.relational_schema


@app.route('/users/', methods=['GET'])
def users():
    if (request.method == 'GET'):
        return user_controller.getUsers(arangoDB)


@app.route('/user/<username>/', methods=['GET'])
def specific_user(username):
    user = user_controller.get_user(arangoDB, mongoDB, username)
    if user == None:
        stat = status.HTTP_404_NOT_FOUND
        jsn = jsonify({'error': 'User not found.'})
    else:
        user['_id'] = str(user['_id'])
        stat = status.HTTP_200_OK
        jsn = jsonify(user)
    return jsn, stat


@app.route('/user/', methods=['POST'])
def user():
    data = request.get_json(force=True)
    username = data['username']
    new_user = user_controller.createUser(arangoDB, mongoDB, username)
    if not new_user:
        return jsonify({'error': 'User already exists.'}), \
            status.HTTP_400_BAD_REQUEST
    else:
        return jsonify(new_user._store), \
            status.HTTP_201_CREATED



@app.route('/')
@app.route('/<path:path>')
def default(**path):
    return send_from_directory('../client/src/', 'index.html')
