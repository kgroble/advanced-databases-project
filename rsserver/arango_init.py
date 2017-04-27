from pyArango.connection import *
from pyArango.graph import Graph, EdgeDefinition
from pyArango.collection import Collection, Field
from pyArango.collection import Edges

conn = Connection(arangoURL='http://127.0.0.1:8529',
                  username='root',
                  password='foobar')

# Creating/getting the database
try:
    db = conn['RelationalSchema']
except KeyError:
    conn.createDatabase(name = 'RelationalSchema')
    db = conn['RelationalSchema']

# Weird arango driver stuff
class Users(Collection):
    _fields = {'uname': Field()}

class Match(Edges):
    _fields = {'strength': Field()}


class Response(Collection):
    _fields = {'label': Field()}

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

# Creating collections
db.createCollection('Users')
db.createCollection('Match')
db.createCollection('Response')
db.createCollection('Answer')

# Creating indexes
db['Users'].ensureHashIndex(['uname'], unique = True)


g = db.createGraph('UserGraph')
c = g.createVertex('Users', {'uname': 'coleman'})
k = g.createVertex('Users', {'uname': 'kieran'})
tabs = g.createVertex('Response', {'label': 'tabs'})
spaces = g.createVertex('Response', {'label': 'spaces'})
g.link('Answer', c, spaces, {})
g.link('Answer', k, tabs, {})
g.link('Match', c, k, {'strength': 9999})
