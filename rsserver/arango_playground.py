from pyArango.connection import *
from pyArango.graph import Graph, EdgeDefinition
from pyArango.collection import Collection, Field
from pyArango.collection import Edges
import socket

if 'cdk' in socket.gethostname():
    arango_url = 'http://cdk433.csse.rose-hulman.edu:8529'
else:
    arango_url = 'http://127.0.0.1:8529'

conn = Connection(arangoURL=arango_url,
            username='root',
            password='srirammohan')

db = conn['RelationalSchema']
users = db['Users']

kieran = users.fetchFirstExample({'uname': 'kieran'}, rawResults = True)
print(kieran)

qText = "FOR v IN 2..2 ANY @user GRAPH 'UserGraph' RETURN v"
vars = {'user': kieran[0]['_id']}

query = db.AQLQuery(qText, bindVars = vars)

for u in query:
    print('id: ' + u._id)
    print('uname: ' + u['uname'])
    print()
