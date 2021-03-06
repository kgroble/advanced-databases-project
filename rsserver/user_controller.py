import uuid, json
from pyArango.connection import *
from pyArango.graph import Graph, EdgeDefinition
from flask import jsonify
from flask_api import status
import bcrypt
import connections, datatypes

user_key_prefix = 'hashes'
expire_time = 60 * 30 # 30 minutes

def is_logged_in(username, key, redis_conn):
    user_key = user_key_prefix + '-' + username
    if not redis_conn.exists(user_key):
        return False
    stored = redis_conn.get(user_key).decode()
    if stored == key:
        redis_conn.expire(user_key, expire_time)
        return True
    return False


def log_in(username, hpw, mongo_conn, redis_conn):
    user_doc = mongo_conn.users.find_one({'uname': username})
    if bcrypt.checkpw(hpw.encode(), user_doc['password'].encode()):
        # this should be set to a random key and returned to the user
        user_key = user_key_prefix + '-' + username
        token = str(uuid.uuid4())
        redis_conn.setex(user_key, token, expire_time)
        return token
    return False


def log_out(username, key, redis_conn):
    if is_logged_in(username, key, redis_conn):
        user_key = user_key_prefix + '-' + username
        redis_conn.delete(user_key)
        return True
    return False


def createUser(uname, name, description, password, arangoDB, mongoDB, redis_conn):
    if not(connections.mongo_up(mongoDB)):
        return jsonify({}), status.HTTP_503_SERVICE_UNAVAILABLE

    if mongoDB.users.find_one({'uname': uname}):
        return False

    mongoUser = mongoDB.users.insert_one({
        'uname': uname,
        'password': password,
        'name': name,
        'description': description,
        'recent_matches': [],
        'recent_answers': []
    })

    if not(connections.arango_up(arangoDB, redis_conn)):
        recovery_entry = json.dumps({
            'request_type': 'create_user',
            'uname': uname,
            'password': password,
            'name': name,
            'description': description,
        })
        print('recovery entry:', recovery_entry)
        redis_conn.rpush('recovery_queue', recovery_entry)
        mongoUser = mongoDB.users.find_one({'uname': uname})
        del mongoUser['_id']
        return mongoUser
    else:
        userGraph = arangoDB.graphs['UserGraph']
        try:
            newUser = userGraph.createVertex('Users',
                                         {'uname': uname})
            return newUser._store
        except CreationError:
            return False


def get_user(arango, mongo, uname, redis_conn):
    if not(connections.mongo_up(mongo)):
        return jsonify({}), status.HTTP_503_SERVICE_UNAVAILABLE

    user = mongo.users.find_one({'uname': uname}, projection={'_id': False})

    if connections.arango_up(arango, redis_conn):
        userGraph = arango.graphs['UserGraph']
        users = arango['Users']
        arango_user = users.fetchFirstExample({'uname': uname})[0]

        # Getting responses to questions
        val = userGraph.traverse(arango_user,
                                 maxDepth=1,
                                 direction='any')
        trav = val['visited']['vertices']
        only_responses = list(filter(lambda x: x['_id'].startswith('Response'), trav))
        only_responses = list(map(lambda x: {'code': x['code']}, only_responses))
        user['answers'] = only_responses
        print(only_responses)
        mongo.users.update_one({'uname': uname}, {'$set': {'recent_answers': only_responses}}, upsert=True)
    else:
        user['answers'] = user['recent_answers']

    no_good = [ 'password', 'recent_answers', 'recent_matches' ]
    for x in no_good:
        if x in user:
            del user[x]

    return user

def getMatches(arango, mongo, uname, redis_conn):
    if connections.arango_up(arango, redis_conn):
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

        mongo.users.update_one({'uname': uname}, {'$set': {'recent_matches': matches}}, upsert=True)
        return jsonify(matches), status.HTTP_200_OK
    elif connections.mongo_up(mongo):
        matches = mongo.users.find_one({'uname': uname})['recent_matches']
        return jsonify(matches), status.HTTP_200_OK
    else:
        return jsonify({}), status.HTTP_503_SERVICE_UNAVAILABLE


def getUsers(db):
    if not(connections.mongo_up(db)):
        return jsonify({}), status.HTTP_503_SERVICE_UNAVAILABLE

    users = db.users.find(projection={'_id': False})
    userArray = []
    for u in users:
        del u['password']
        del u['recent_matches']
        userArray.append(u)
    return jsonify(userArray), status.HTTP_200_OK


def updateUserAttributes(mongo, uname, data):
    if not(connections.mongo_up(mongo)):
        return jsonify({}), status.HTTP_503_SERVICE_UNAVAILABLE

    no_good = [ 'key', 'username', 'password', 'uname', 'recent_matches', 'recent_answers' ]
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
