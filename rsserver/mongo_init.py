from pymongo import MongoClient

conn = MongoClient("mongodb://cdk433.csse.rose-hulman.edu:27017")

db = conn.relational_schema
users = db.users

users.insert_many([{'uname': 'coleman'}, {'uname': 'kieran'}])