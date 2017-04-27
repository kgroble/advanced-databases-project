from pyArango.connection import *
from pyArango.graph import Graph, EdgeDefinition
from pyArango.collection import Collection, Field
from pyArango.collection import Edges
from flask import jsonify
from flask_api import status


class UserGraph(Graph):
    _edgeDefinitions = [EdgeDefinition('Match',
                                       fromCollections = ['Users'],
                                       toCollections = ['Users'])]
    _orphanedCollections = []


def createUser(arangoDB, mongoDB, uname):
    userGraph = arangoDB.graphs['UserGraph']
    try:
        newUser = userGraph.createVertex('Users', {'uname': uname})
        mongoUser = mongoDB.users.insert_one({'uname': uname})
        return newUser
    except CreationError:
        return False


def get_user(arango, mongo, uname):
    user = mongo.users.find_one({'uname': uname})
    return user


def getUsers(db):
    users = db['Users'].fetchAll(rawResults=True)
    userArray = []
    for u in users:
        userArray.append(u)
    return jsonify(userArray), status.HTTP_200_OK

def updateUserAttributes(mongo, data):
    username = data['uname']
    mongo.users.update_one({'uname' : username}, {'$set': data}, upsert=True)
    return jsonify(data)