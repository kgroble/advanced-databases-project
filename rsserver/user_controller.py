from pyArango.connection import *
from pyArango.graph import Graph, EdgeDefinition
from pyArango.collection import Collection, Field
from pyArango.collection import Edges
from flask import jsonify
from flask_api import status
import bcrypt

import pdb

user_hashes = 'hashes'

class UserGraph(Graph):
    _edgeDefinitions = [EdgeDefinition('Match',
                                       fromCollections = ['Users'],
                                       toCollections = ['Users'])]
    _orphanedCollections = []


# NOTE: These passwords are not secure
def is_logged_in(username, key, redis_conn):
    if not redis_conn.hexists(user_hashes, username):
        return False
    hashed = redis_conn.hget(user_hashes, username).decode()
    return hashed == key


def log_in(username, hpw, mongo_conn, redis_conn):
    user_doc = mongo_conn.users.find_one({'uname': username})
    if bcrypt.checkpw(hpw.encode(), user_doc['password'].encode()):
        # this should be set to a random key and returned to the user
        redis_conn.hset(user_hashes, username, hpw)
        return True
    return False


def log_out(username, key, redis_conn):
    if is_logged_in(username, key, redis_conn):
        redis_conn.hdel(user_hashes, username)
        return True
    return False


def createUser(arangoDB, mongoDB, uname, password):
    userGraph = arangoDB.graphs['UserGraph']
    try:
        newUser = userGraph.createVertex('Users',
                                         {'uname': uname})
        mongoUser = mongoDB.users.insert_one({'uname': uname,
                                              'password': password})
        return newUser
    except CreationError:
        return False


def get_user(arango, mongo, uname):
    userGraph = arango.graphs['UserGraph']
    users = arango['Users']
    arango_user = users.fetchFirstExample({'uname': uname})[0]

    # Getting responses to questions
    val = userGraph.traverse(arango_user,
                             maxDepth=1,
                             direction='any')
    trav = val['visited']['vertices']
    only_responses = filter(lambda x: x['_id'].startswith('Response'), trav)

    user = mongo.users.find_one({'uname': uname}, projection={'_id': False})
    user['answers'] = list(only_responses)
    return user


def getUsers(db):
    users = db.users.find(projection={'_id': False})
    userArray = []
    for u in users:
        userArray.append(u)
    return jsonify(userArray), status.HTTP_200_OK


def updateUserAttributes(mongo, uname, data):
    mongo.users.update_one({'uname' : uname}, {'$set': data}, upsert=True)
    return jsonify({}), status.HTTP_204_NO_CONTENT
