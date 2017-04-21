from pyArango.connection import *
from pyArango.graph import Graph, EdgeDefinition
from pyArango.collection import Collection, Field
from pyArango.collection import Edges
from flask import jsonify
from flask_api import status

class UserGraph(Graph):
    _edgeDefinitions = [EdgeDefinition('Match', fromCollections = ['Users'], toCollections = ['Users'])]
    _orphanedCollections = []

def createUser(arangoDB, mongoDB, uname):
    if mongoDB.users.find_one({'uname': uname}) != None:
        return jsonify({'error': 'User already exists.'}), \
            status.HTTP_400_BAD_REQUEST
    userGraph = arangoDB.graphs['UserGraph']
    newUser = userGraph.createVertex('Users', {'uname': uname})
    mongoDB.users.insert_one({'uname': uname})
    return jsonify(newUser._store), status.HTTP_201_CREATED

def getUsers(db):
    users = db['Users'].fetchAll(rawResults=True)
    userArray = []
    for u in users:
        userArray.append(u)
    return jsonify(userArray), status.HTTP_200_OK
