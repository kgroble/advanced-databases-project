import user_controller, question_controller, message_controller
from flask import Flask, abort, redirect, url_for, render_template, \
    send_from_directory, request, jsonify, session, redirect
from pyArango.connection import *
from pymongo import MongoClient
from flask_api import status
import socket
import redis
import re


arango_username = 'root'
arango_password = 'srirammohan'
if 'cdk' in socket.gethostname():
    arango_url = 'http://cdk433.csse.rose-hulman.edu:8529'
    mongo_url = 'mongodb://cdk433.csse.rose-hulman.edu:27017'
    mongoConn = MongoClient(mongo_url,
                            replicaset='cdk',
                            serverSelectionTimeoutMS=1000)
elif 'JCG' in socket.gethostname():
    arango_url = 'http://127.0.0.1:8530'
    mongo_url = 'mongodb://127.0.0.1:27017'
    mongoConn = MongoClient(mongo_url, serverSelectionTimeoutMS=1000)
else:
    arango_url = 'http://127.0.0.1:8529'
    mongo_url = 'mongodb://127.0.0.1:27017'
    mongoConn = MongoClient(mongo_url, serverSelectionTimeoutMS=1000)


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
local_redis_conn = redis.Redis()
redis_info = local_redis_conn.info()
if 'master_host' in redis_info:
    redis_conn = redis.Redis(redis_info['master_host'])
else:
    redis_conn = local_redis_conn



"""
HELPER FUNCTIONS
"""


def not_logged_in():
    return jsonify({}), status.HTTP_401_UNAUTHORIZED


p = re.compile('^\\w+$')
def valid_username(uname):
    return not not p.match(uname)


"""
API ENDPOINTS
"""


@app.route('/login/', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    key = data['key']
    token = user_controller.log_in(username, key, mongoDB, redis_conn)
    if token:
        print(token)
        return jsonify({'key': token}), status.HTTP_201_CREATED
    return not_logged_in()


@app.route('/logout/', methods=['POST'])
def logout():
    data = request.get_json()
    username = data['username']
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
        user = user_controller.get_user(arangoDB, mongoDB, username, redis_conn)
        if user == None:
            stat = status.HTTP_404_NOT_FOUND
            jsn = jsonify({'error': 'User not found.'})
        else:
            stat = status.HTTP_200_OK
            jsn = jsonify(user)
        return jsn, stat

    elif request.method == 'PATCH':
        data = request.get_json()
        auth_user = data['username']
        key = data['key']
        if not user_controller.is_logged_in(auth_user, key, redis_conn):
            return not_logged_in()
        return user_controller.updateUserAttributes(mongoDB,
                                                    username,
                                                    data)


@app.route('/user/<username>/matches/', methods=['GET'])
def matches(username):
    auth_user = request.args.get('username')
    key = request.args.get('key')
    if not user_controller.is_logged_in(auth_user, key, redis_conn):
        return not_logged_in()
    if (request.method == 'GET'):
        return user_controller.getMatches(arangoDB, mongoDB, username, redis_conn)

@app.route('/user/<username>/answer/<code>', methods=['POST'])
def answerQuestion(username, code):
    data = request.get_json()
    auth_user = data['username']
    key = data['key']
    if request.method == 'POST':
        if not user_controller.is_logged_in(username, key, redis_conn):
            return not_logged_in()
        return question_controller.setAnswer(arangoDB,
                                             username,
                                             code,
                                             redis_conn)


@app.route('/user/<username>/messages/', methods=['GET'])
def getMessages(username):
    auth_user = request.args.get('username')
    key = request.args.get('key')
    if not user_controller.is_logged_in(auth_user, key, redis_conn):
        return not_logged_in()
    if (request.method == 'GET'):
        return message_controller.getMessages(mongoDB, username)


@app.route('/user/<username>/message/<recipient>/', methods=['POST'])
def sendMessage(username, recipient):
    data = request.get_json()
    auth_user = data['username']
    key = data['key']
    if request.method == 'POST':
        if not user_controller.is_logged_in(username, key, redis_conn):
            return not_logged_in()
        return message_controller.sendMessage(mongoDB,
                                              username,
                                              recipient,
                                              data['body'])


@app.route('/user/', methods=['POST'])
def user():
    data = request.get_json(force=True)
    username = data['username']

    if not valid_username(username):
        return jsonify({'error': 'Bad username.'}), \
            status.HTTP_400_BAD_REQUEST

    password = data['password']
    name = data['name']
    description = data['description']
    new_user = user_controller.createUser(
        username,
        name,
        description,
        password,
        arangoDB,
        mongoDB,
        redis_conn,
    )
    if not new_user:
        return jsonify({'error': 'User already exists.'}), \
            status.HTTP_400_BAD_REQUEST
    else:
        return jsonify(new_user), \
            status.HTTP_201_CREATED
