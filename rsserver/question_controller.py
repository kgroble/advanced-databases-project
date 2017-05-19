import json
from flask import jsonify
from flask_api import status
from pyArango.connection import *
from pyArango.graph import Graph, EdgeDefinition
from pyArango.collection import Collection, Field
from pyArango.collection import Edges
import connections, datatypes


def getQuestions(mongo):
    if not(connections.mongo_up(mongo)):
        return jsonify({}), status.HTTP_503_SERVICE_UNAVAILABLE

    questions = mongo.questions.find()
    questionArray = []
    for q in questions:
        questionArray.append(q)
    return jsonify(questionArray), status.HTTP_200_OK


def no_check_insert_answer(arango, uname, code):
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


def setAnswer(arango, uname, code, redis_conn):
    if not(connections.arango_up(arango, redis_conn)):
        recovery_entry = json.dumps({
            'request_type': 'answer_question',
            'uname': uname,
            'code': code
        })
        redis_conn.rpush('recovery_queue', recovery_entry)

        return jsonify({}), status.HTTP_204_NO_CONTENT

    no_check_insert_answer(arango, uname, code)
    return jsonify({}), status.HTTP_204_NO_CONTENT
