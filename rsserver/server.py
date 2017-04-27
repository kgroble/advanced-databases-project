from flask import Flask
import socket
import routes

if (__name__ == '__main__'):
    if 'cdk' in socket.gethostname():
        dbg = False
    else:
        dbg = True
    routes.app.run(debug=dbg)
