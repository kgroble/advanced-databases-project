from pymongo import MongoClient

conn = MongoClient()

db = conn.relational_schema
users = db.users

users.insert_many([{'uname': 'coleman'}, {'uname': 'kieran'}])
