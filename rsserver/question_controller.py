from flask import jsonify
from flask_api import status
from pyArango.connection import *
from pyArango.graph import Graph, EdgeDefinition
from pyArango.collection import Collection, Field
from pyArango.collection import Edges

class Users(Collection):
    _fields = {'uname': Field()}

class Match(Edges):
    _fields = {'strength': Field()}


class Response(Collection):
    _fields = {'code': Field()}

class Answer(Edges):
    _fields = {}

class UserGraph(Graph):
    _edgeDefinitions = [EdgeDefinition('Match',
                                       fromCollections = ['Users'],
                                       toCollections = ['Users']),
                        EdgeDefinition('Answer',
                                       fromCollections = ['Users'],
                                       toCollections = ['Response'])]
    _orphanedCollections = []

def getQuestions(mongo):
    questions = mongo.questions.find()
    questionArray = []
    for q in questions:
        questionArray.append(q)
    return jsonify(questionArray), status.HTTP_200_OK

def setAnswer(arango, uname, code):
    graph = arango.graphs['UserGraph']
    users = arango['Users']
    responses = arango['Response']
    answers = arango['Answer']
    answerTo = arango['AnswerTo']

    user = users.fetchFirstExample({'uname': uname})
    response = responses.fetchFirstExample({'code': code})
    questionID = answerTo.fetchFirstExample({'_from': response[0]._id})[0]['_to']
    aql = "FOR v IN 1..1 INBOUND @QID GRAPH 'UserGraph' RETURN v"
    vars = {'QID': questionID}
    query = arango.AQLQuery(aql, bindVars=vars)
    for r in query:
        toDelete = answers.fetchByExample({'_from': user[0]._id, '_to': r._id}, 50)
        for ans in toDelete:
            ans.delete()

    graph.link('Answer', user[0], response[0], {})
    return jsonify({}), status.HTTP_204_NO_CONTENT
