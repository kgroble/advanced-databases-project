from pyArango.connection import *
from pyArango.graph import Graph, EdgeDefinition
from pyArango.collection import Collection, Field
from pyArango.collection import Edges

conn = Connection(arangoURL='http://127.0.0.1:8529', username='root', password='foobar')
db = conn['RelationalSchema']
users = db['Users']

selector = {}
query = users.fetchByExample(selector, batchSize = 50)

for u in query:
    print('id: ' + u._id)
    print('uname: ' + u['uname'])
    print()
