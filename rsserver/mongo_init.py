from pymongo import MongoClient
import pymongo
import socket
import hashlib
import bcrypt

if 'cdk' in socket.gethostname():
    mongo_url = 'mongodb://cdk433.csse.rose-hulman.edu'
else:
    mongo_url = 'mongodb://127.0.0.1'

conn = MongoClient(mongo_url, 27017, replicaset='cdk')

db = conn.relational_schema
users = db.users
questions = db.questions

try:
    users.create_index('uname', unique = True)
except pymongo.errors.DuplicateKeyError:
    pass

users.delete_many({})
questions.delete_many({})

h = hashlib.sha256()
h.update(b'abc')
hashed_pw = h.hexdigest()
pw = bcrypt.hashpw(hashed_pw.encode(), bcrypt.gensalt()).decode()


users.insert_many([{'uname': 'coleman',
                    'password': pw},
                   {'uname': 'kieran',
                    'password': pw},
                   {'uname': 'derek',
                    'password': pw}])


indentation = {'_id': 'indentation',
               'text': 'What kind of indentation do you prefer?',
               'options': [{'code': 'indentation-tabs', 'label': 'Tabs'},
                           {'code': 'indentation-spaces', 'label': 'Spaces'}]}

editor = {'_id': 'editor',
          'text': 'What editor do you use?',
          'options': [{'code': 'editor-emacs', 'label': 'Emacs'},
                      {'code': 'editor-vim', 'label': 'Vim'},
                      {'code': 'editor-both', 'label': 'Both'},
                      {'code': 'editor-neither',
                       'label': 'Neither (Hint: This is the wrong answer. ' +
                       'If you select this, your account will be deleted.)'}]}

os = {'_id': 'os',
      'text': 'What operating system do you use?',
      'options': [{'code': 'os-linux', 'label': 'Linux'},
                  {'code': 'os-osx', 'label': 'OS X'},
                  {'code': 'os-windows', 'label': 'Windows'},
                  {'code': 'os-other', 'label': 'Other'}]}

questions.insert_many([indentation, editor, os])
