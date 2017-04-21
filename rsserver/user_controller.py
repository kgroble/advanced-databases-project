from pyArango.connection import *
from pyArango.graph import Graph, EdgeDefinition
from pyArango.collection import Collection, Field
from pyArango.collection import Edges
from flask import jsonify

class UserGraph(Graph):
    _edgeDefinitions = [EdgeDefinition('Match', fromCollections = ['Users'], toCollections = ['Users'])]
    _orphanedCollections = []

def createUser(db, uname):
    userGraph = db.graphs['UserGraph']
    newUser = userGraph.createVertex('Users', {'uname': uname})
    return jsonify(newUser._store), status.HTTP_201_CREATED

def getUsers(db):
    users = db['Users'].fetchAll()
    print(users)
    users = db['Users'].fetchAll(rawResults=True)
    print(users)
