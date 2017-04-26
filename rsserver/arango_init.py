from pyArango.connection import *
from pyArango.graph import Graph, EdgeDefinition
from pyArango.collection import Collection, Field
from pyArango.collection import Edges

conn = Connection(arangoURL='http://127.0.0.1:8530',
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

class UserGraph(Graph):
    _edgeDefinitions = [EdgeDefinition('Match',
                                       fromCollections = ['Users'],
                                       toCollections = ['Users'])]
    _orphanedCollections = []

# Creating collections
db.createCollection('Users')
db.createCollection('Match')

# Creating indexes
db['Users'].ensureHashIndex(['uname'], unique = True)


g = db.createGraph('UserGraph')
c = g.createVertex('Users', {'uname': 'coleman'})
k = g.createVertex('Users', {'uname': 'kieran'})
g.link('Match', c, k, {'strength': 9999})
