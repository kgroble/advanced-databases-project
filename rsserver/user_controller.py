from pyArango.connection import *
from pyArango.graph import Graph, EdgeDefinition
from flask import jsonify
from flask_api import status
import bcrypt

user_hashes = 'hashes'

class UserGraph(Graph):
    _edgeDefinitions = [EdgeDefinition('Match',
                                       fromCollections = ['Users'],
                                       toCollections = ['Users'])]
    _orphanedCollections = []


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


def createUser(uname, name, description, password, arangoDB, mongoDB):
    userGraph = arangoDB.graphs['UserGraph']
    try:
        newUser = userGraph.createVertex('Users',
                                         {'uname': uname})
        mongoUser = mongoDB.users.insert_one({
            'uname': uname,
            'password': password,
            'name': name,
            'description': description,
        })
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
    del user['password']
    return user

def getMatches(arango, mongo, uname):
    uid = arango['Users'].fetchFirstExample({'uname': uname},
                                            rawResults=True)[0]['_id']
    aql = "FOR v IN 2..2 ANY @user GRAPH 'UserGraph' RETURN v"
    bindVars = {'user': uid}
    query = arango.AQLQuery(aql, bindVars = bindVars)

    matches = {}
    for u in query:
        if u['uname']:
            other = u['uname']
            if other in matches:
                matches[other] = matches[other] + 1
            else:
                matches[other] = 1

    print(matches)
    return jsonify(matches), status.HTTP_200_OK

def getUsers(db):
    users = db.users.find(projection={'_id': False})
    userArray = []
    for u in users:
        del u['password']
        userArray.append(u)
    return jsonify(userArray), status.HTTP_200_OK


def updateUserAttributes(mongo, uname, data):
    no_good = [ 'key', 'username', 'password', 'uname' ]
    for x in no_good:
        if x in data:
            del data[x]
    if data['remove']:
        del data['remove']
        mongo.users.update_one({'uname' : uname}, {'$unset': data}, upsert=True)
    else:
        del data['remove']
        mongo.users.update_one({'uname' : uname}, {'$set': data}, upsert=True)
    return jsonify({}), status.HTTP_204_NO_CONTENT
