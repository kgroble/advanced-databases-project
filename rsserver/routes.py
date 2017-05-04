import user_controller, question_controller
from flask import Flask, abort, redirect, url_for, render_template, \
    send_from_directory, request, jsonify, session, redirect
from pyArango.connection import *
from pymongo import MongoClient
from flask_api import status
import socket
import redis


arango_username = 'root'
arango_password = 'srirammohan'
if 'cdk' in socket.gethostname():
    arango_url = 'http://cdk433.csse.rose-hulman.edu:8529'
    mongo_url = 'mongodb://cdk433.csse.rose-hulman.edu:27017'
    mongoConn = MongoClient(mongo_url,
                        replicaset='cdk')
else:
    arango_url = 'http://127.0.0.1:8529'
    mongo_url = 'mongodb://127.0.0.1:27017'
    mongoConn = MongoClient(mongo_url)


app = Flask(__name__,
            static_url_path='/static',
            static_folder='../client/dist/')
arangoConn = Connection(arangoURL=arango_url,
                        username=arango_username,
                        password=arango_password)
arangoDB = arangoConn['RelationalSchema']
# mongoConn = MongoClient(mongo_url,
#                         replicaset='cdk')
mongoDB = mongoConn.relational_schema
redis_conn = redis.Redis()



def not_logged_in():
    return jsonify({}), status.HTTP_401_UNAUTHORIZED



@app.route('/login/', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    key = data['key']
    if user_controller.log_in(username, key, mongoDB, redis_conn):
        return jsonify({}), status.HTTP_204_NO_CONTENT
    return not_logged_in()


@app.route('/logout/', methods=['POST'])
def logout():
    data = request.get_json()
    username = data['username']
    del session['username']
    return jsonify({'username': username}), status.HTTP_200_OK


@app.route('/users/', methods=['GET'])
def users():
    username = request.args.get('username')
    key = request.args.get('key')
    if not user_controller.is_logged_in(username, key, redis_conn):
        return not_logged_in()
    if (request.method == 'GET'):
        return user_controller.getUsers(mongoDB)


@app.route('/questions/', methods=['GET'])
def questions():
    username = request.args.get('username')
    key = request.args.get('key')
    if not user_controller.is_logged_in(username, key, redis_conn):
        return not_logged_in()
    if (request.method == 'GET'):
        return question_controller.getQuestions(mongoDB)


@app.route('/user/<username>/', methods=['GET', 'PATCH'])
def specific_user(username):
    if request.method == 'GET':
        key = request.args.get('key')
        auth_user = request.args.get('username')
        if not user_controller.is_logged_in(auth_user, key, redis_conn):
            return not_logged_in()
        user = user_controller.get_user(arangoDB, mongoDB, username)
        if user == None:
            stat = status.HTTP_404_NOT_FOUND
            jsn = jsonify({'error': 'User not found.'})
        else:
            stat = status.HTTP_200_OK
            del user['password']
            jsn = jsonify(user)
        return jsn, stat
    elif request.method == 'PATCH':
        return user_controller.updateUserAttributes(mongoDB,
                                                    username,
                                                    request.get_json())

@app.route('/user/<username>/matches/', methods=['GET'])
def matches(username):
    print(username)
    auth_user = request.args.get('username')
    key = request.args.get('key')
    if not user_controller.is_logged_in(auth_user, key, redis_conn):
        return not_logged_in()
    if (request.method == 'GET'):
        print(username)
        return user_controller.getMatches(arangoDB, mongoDB, username)

@app.route('/user/<username>/answer/<code>', methods=['POST'])
def answerQuestion(username, code):
    if request.method == 'POST':
        if not logged_in(username, key):
            return not_logged_in()
        return question_controller.setAnswer(arangoDB,
                                             username,
                                             code)


@app.route('/user/', methods=['POST'])
def user():
    data = request.get_json(force=True)
    username = data['username']
    new_user = user_controller.createUser(arangoDB,
                                          mongoDB,
                                          username)
    if not new_user:
        return jsonify({'error': 'User already exists.'}), \
            status.HTTP_400_BAD_REQUEST
    else:
        return jsonify(new_user._store), \
            status.HTTP_201_CREATED
