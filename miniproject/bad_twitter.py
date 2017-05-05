from pyArango.connection import *
from pyArango.graph import Graph, EdgeDefinition
from pyArango.collection import Collection, Field
from pyArango.collection import Edges

class Users(Collection):
    _fields = {'uname': Field(), 'status': Field(), 'likes': Field()}

class Follows(Edges):
    _fields = {}

class BadGraph(Graph):
    _edgeDefinitions = [EdgeDefinition('Follows',
                                       fromCollections = ['Users'],
                                       toCollections = ['Users'])]
    _orphanedCollections = []

arango_url = 'http://127.0.0.1:8529'

conn = Connection(arangoURL=arango_url,
            username='root',
            password='srirammohan')

db = conn['BadTwitter']
users = db['Users']
follows = db['Follows']
graph = db.graphs['BadGraph']

def print_user(user):
    badKeys = []
    for key in user:
        if key[0] == '_':
            badKeys.append(key)
    for key in badKeys:
        del user[key]

    print(user)


def create_user():
    uname = input('enter uname: ')
    try:
        graph.createVertex('Users', {'uname': uname, 'status': '', 'likes': 0})
        print('User created.')
    except CreationError:
        print('Error: Username taken.')


def list_users():
    query = users.fetchByExample({},
                                 batchSize=50,
                                 rawResults=True)

    for u in query:
        print_user(u)


def set_status():
    uname = input('enter uname: ')
    status = input('enter new status: ')

    user = users.fetchFirstExample({'uname': uname})

    if len(user) == 0:
        print('User not found.')
        return

    user = user[0]
    user['status'] = status
    user['likes'] = 0
    user.patch()


def follow():
    uname = input('enter your uname: ')
    other = input('enter uname to follow: ')

    user = users.fetchFirstExample({'uname': uname})
    target = users.fetchFirstExample({'uname': other})


    if len(user) == 0:
        print('User not found.')
        return

    if len(target) == 0:
        print('Other user not found.')
        return

    user = user[0]
    target = target[0]

    existing = follows.fetchFirstExample({'_from': user._id,
                                          '_to': target._id})

    if len(existing) != 0:
        print('You are already following', target['uname'])
        return

    graph.link('Follows', user, target, {})


def unfollow():
    uname = input('enter your uname: ')
    other = input('enter uname to unfollow: ')

    user = users.fetchFirstExample({'uname': uname})
    target = users.fetchFirstExample({'uname': other})


    if len(user) == 0:
        print('User not found.')
        return

    if len(target) == 0:
        print('Other user not found.')
        return

    user = user[0]
    target = target[0]

    existing = follows.fetchFirstExample({'_from': user._id,
                                          '_to': target._id})

    if len(existing) == 0:
        print('You are not following', target['uname'])
        return

    existing[0].delete()


def get_statuses():
    uname = input('enter uname: ')

    user = users.fetchFirstExample({'uname': uname})

    if len(user) == 0:
        print('User not found.')
        return

    user = user[0]

    aql = "FOR v IN 1..1 OUTBOUND @uid GRAPH 'BadGraph' RETURN v"
    vars = {'uid': user._id}
    query = db.AQLQuery(aql, rawResults=True, bindVars=vars)
    for u in query:
        print_user(u)
        print()


def like():
    uname = input('enter your uname: ')
    other = input('enter uname to like: ')

    user = users.fetchFirstExample({'uname': uname})
    target = users.fetchFirstExample({'uname': other})


    if len(user) == 0:
        print('User not found.')
        return

    if len(target) == 0:
        print('Other user not found.')
        return

    target = target[0]
    target['likes'] += 1
    target.patch()


def delete_user():
    uname = input('enter uname to delete: ')
    user = users.fetchFirstExample({'uname': uname})

    if len(user) == 0:
        print('User not found.')
        return

    graph.deleteVertex(user[0])


running = True
while running:
    print()
    response = input('-> ')

    if response == 'quit':
        running = False

    elif response == 'create_user':
        create_user()

    elif response == 'list_users':
        list_users()

    elif response == 'set_status':
        set_status()

    elif response == 'follow':
        follow()

    elif response == 'unfollow':
        unfollow()

    elif response == 'get_statuses':
        get_statuses()

    elif response == 'like':
        like()

    elif response == 'delete_user':
        delete_user()

    else:
        print('bad command')
