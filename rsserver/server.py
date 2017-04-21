from flask import Flask
import routes

def getUsernames():
    return "GET succeeded"

def addUser(uname):
    pass

if (__name__ == '__main__'):
    routes.app.run(debug=True)