from pymongo import MongoClient

conn = MongoClient("mongodb://cdk433.csse.rose-hulman.edu", 27017, replicaset='cdk')

db = conn.relational_schema
users = db.users
questions = db.questions

users.create_index('uname', unique = True)

users.delete_many({})
users.insert_many([{'uname': 'coleman'}, {'uname': 'kieran'}])

questions.delete_many({})

indentation = {'_id': 'indentation',
               'text': 'What kind of indentation do you prefer?',
               'options': [{'code': 'indentation-tabs', 'label': 'Tabs'},
                           {'code': 'indentation-spaces', 'label': 'Spaces'}]}

editor = {'_id': 'editor',
          'text': 'What editor do you use?',
          'options': [{'code': 'editor-emacs', 'label': 'Emacs'},
                      {'code': 'editor-vim', 'label': 'Vim'},
                      {'code': 'editor-both', 'label': 'Both'},
                      {'code': 'editor-neither', 'label': 'Neither (Hint: This is the wrong answer. If you select this, your account will be deleted.)'}]}

os = {'_id': 'os',
      'text': 'What operating system do you use?',
      'options': [{'code': 'os-linux', 'label': 'Linux'},
                  {'code': 'os-osx', 'label': 'OS X'},
                  {'code': 'os-windows', 'label': 'Windows'},
                  {'code': 'os-other', 'label': 'Other'}]}

questions.insert_many([indentation, editor, os])
