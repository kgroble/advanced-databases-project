import user_controller, question_controller
from flask import Flask, abort, redirect, url_for, render_template, \
    send_from_directory, request, jsonify, session, redirect
from pyArango.connection import *
from pymongo import MongoClient
from flask_api import status

app = Flask(__name__,
            static_url_path='/static',
            static_folder='../client/dist/')
arangoConn = Connection(arangoURL='http://cdk433.csse.rose-hulman.edu:8529',
                        username='root',
                        password='srirammohan')
arangoDB = arangoConn['RelationalSchema']
mongoConn = MongoClient("mongodb://cdk433.csse.rose-hulman.edu:27017", replicaset='cdk')
mongoDB = mongoConn.relational_schema


def logged_in(username):
    if username in session:
        return False
    return True


def not_logged_in():
    return redirect("/login", code=302)


@app.route('/login/', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    session['username'] = username
    return jsonify({'username': username}), status.HTTP_201_CREATED


@app.route('/logout/', methods=['POST'])
def logout():
    data = request.get_json()
    username = data['username']
    del session['username']
    return jsonify({'username': username}), status.HTTP_200_OK


@app.route('/users/', methods=['GET'])
def users():
    username = request.args.get('username')
    if not logged_in(username):
        return not_logged_in()
    if (request.method == 'GET'):
        return user_controller.getUsers(mongoDB)

@app.route('/questions/', methods=['GET'])
def questions():
    username = request.args.get('username')
    if not logged_in(username):
        return not_logged_in()
    if (request.method == 'GET'):
        return question_controller.getQuestions(mongoDB)

@app.route('/user/<username>/', methods=['GET', 'PATCH'])
def specific_user(username):
    if request.method == 'GET':
        if not logged_in(username):
            return not_logged_in()
        user = user_controller.get_user(arangoDB, mongoDB, username)
        if user == None:
            stat = status.HTTP_404_NOT_FOUND
            jsn = jsonify({'error': 'User not found.'})
        else:
            # user['_id'] = str(user['_id'])
            stat = status.HTTP_200_OK
            jsn = jsonify(user)
        return jsn, stat
    elif request.method == 'PATCH':
        return user_controller.updateUserAttributes(mongoDB, username, request.get_json())

@app.route('/user/<username>/answer/<code>', methods=['POST'])
def answerQuestion(username, code):
    if request.method == 'POST':
        if not logged_in(username):
            return not_logged_in()
        return question_controller.setAnswer(arangoDB, username, code)


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
