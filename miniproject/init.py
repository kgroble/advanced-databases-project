from pyArango.connection import *
from pyArango.graph import Graph, EdgeDefinition
from pyArango.collection import Collection, Field
from pyArango.collection import Edges

arango_url = 'http://127.0.0.1:8529'

conn = Connection(arangoURL=arango_url,
            username='root',
            password='srirammohan')

try:
    db = conn['BadTwitter']
except KeyError:
    conn.createDatabase(name = 'BadTwitter')
    db = conn['BadTwitter']

class Users(Collection):
    _fields = {'uname': Field(), 'status': Field(), 'likes': Field()}

class Follows(Edges):
    _fields = {}

class BadGraph(Graph):
    _edgeDefinitions = [EdgeDefinition('Follows',
                                       fromCollections = ['Users'],
                                       toCollections = ['Users'])]
    _orphanedCollections = []


for graph in db.graphs:
    db.graphs[graph].delete()

for coll in db.collections:
    if not(coll[0] == '_'):
        db[coll].delete()


db.createCollection('Users')
db.createCollection('Follows')
db['Users'].ensureHashIndex(['uname'], unique = True)
db.createGraph('BadGraph')
