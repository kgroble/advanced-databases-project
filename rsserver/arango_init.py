from pyArango.connection import *
from pyArango.graph import Graph, EdgeDefinition
from pyArango.collection import Collection, Field
from pyArango.collection import Edges
import socket

if 'cdk' in socket.gethostname():
    arango_url = 'http://cdk433.csse.rose-hulman.edu:8529'
elif 'JCG' in socket.gethostname():
    arango_url = 'http://127.0.0.1:8530'
else:
    arango_url = 'http://127.0.0.1:8529'

conn = Connection(arangoURL=arango_url,
            username='root',
            password='srirammohan')

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
    _fields = {'code': Field()}

class Answer(Edges):
    _fields = {}

class Question(Collection):
    _fields = {'code': Field()}

class AnswerTo(Edges):
    _fields = {}

class UserGraph(Graph):
    _edgeDefinitions = [EdgeDefinition('Match',
                                       fromCollections = ['Users'],
                                       toCollections = ['Users']),
                        EdgeDefinition('Answer',
                                       fromCollections = ['Users'],
                                       toCollections = ['Response']),
                        EdgeDefinition('AnswerTo',
                                       fromCollections = ['Response'],
                                       toCollections = ['Question'])]
    _orphanedCollections = []


# Creating collections
for graph in db.graphs:
    db.graphs[graph].delete()

for coll in db.collections:
    if not(coll[0] == '_'):
        db[coll].delete()


db.createCollection('Users')
db.createCollection('Match')
db.createCollection('Response')
db.createCollection('Answer')
db.createCollection('Question')
db.createCollection('AnswerTo')

# Creating indexes
db['Users'].ensureHashIndex(['uname'], unique = True)


g = db.createGraph('UserGraph')
c = g.createVertex('Users', {'uname': 'coleman'})
k = g.createVertex('Users', {'uname': 'kieran'})

indentation = g.createVertex('Question', {'code': 'indentation'})
os = g.createVertex('Question', {'code': 'os'})
editor = g.createVertex('Question', {'code': 'editor'})

tabs = g.createVertex('Response', {'code': 'indentation-tabs'})
spaces = g.createVertex('Response', {'code': 'indentation-spaces'})
emacs = g.createVertex('Response', {'code': 'editor-emacs'})
vim = g.createVertex('Response', {'code': 'editor-vim'})
both = g.createVertex('Response', {'code': 'editor-both'})
neither = g.createVertex('Response', {'code': 'editor-neither'})
linux = g.createVertex('Response', {'code': 'os-linux'})
osx = g.createVertex('Response', {'code': 'os-osx'})
windows = g.createVertex('Response', {'code': 'os-windows'})
other = g.createVertex('Response', {'code': 'os-other'})

g.link('AnswerTo', tabs, indentation, {})
g.link('AnswerTo', spaces, indentation, {})
g.link('AnswerTo', vim, editor, {})
g.link('AnswerTo', emacs, editor, {})
g.link('AnswerTo', both, editor, {})
g.link('AnswerTo', neither, editor, {})
g.link('AnswerTo', osx, os, {})
g.link('AnswerTo', windows, os, {})
g.link('AnswerTo', linux, os, {})
g.link('AnswerTo', other, os, {})

g.link('Answer', c, spaces, {})
g.link('Answer', k, tabs, {})
g.link('Answer', c, both, {})
g.link('Answer', k, both, {})
g.link('Answer', c, linux, {})
g.link('Answer', k, linux, {})
