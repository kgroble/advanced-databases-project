from pyArango.connection import *
from pyArango.graph import Graph, EdgeDefinition
from pyArango.collection import Collection, Field
from pyArango.collection import Edges
from flask import jsonify
from flask_api import status
import bcrypt
import datetime


def sendMessage(mongo, sender, to, body):
    messages = mongo.messages
    result = messages.insert_one({
        'from': sender,
        'to': to,
        'body': body,
        'date': datetime.datetime.now(),
    })
    newMessage = messages.find_one(result.inserted_id, projection={'_id':False})
    return jsonify(newMessage), status.HTTP_201_CREATED

def getMessages(mongo, uname):
    messages = mongo.messages.find(
        {'to': uname},
        projection={'_id':False, 'to':False}
    )
    ret = []
    for m in messages:
        ret.append(m)

    return jsonify(ret), status.HTTP_200_OK
