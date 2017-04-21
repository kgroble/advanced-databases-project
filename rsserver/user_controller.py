from pyArango.connection import *
from pyArango.graph import Graph, EdgeDefinition
from pyArango.collection import Collection, Field
from pyArango.collection import Edges
from flask import jsonify
from flask_api import status

class UserGraph(Graph):
    _edgeDefinitions = [EdgeDefinition('Match', fromCollections = ['Users'], toCollections = ['Users'])]
    _orphanedCollections = []

def createUser(db, uname):
    userGraph = db.graphs['UserGraph']
    newUser = userGraph.createVertex('Users', {'uname': uname})
    return jsonify(newUser._store), status.HTTP_201_CREATED

def getUsers(db):
    users = db['Users'].fetchAll(rawResults=True)
    userArray = []
    for u in users:
        userArray += [u]
    return jsonify(userArray), status.HTTP_200_OK
