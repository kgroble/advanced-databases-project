
from flask import Flask, abort, redirect, url_for, render_template, \
        send_from_directory

app = Flask(__name__, static_url_path='/static', static_folder='../client/dist/')

@app.route('/')
def hello_world():
    return send_from_directory('../client/src/', 'index.html')

# @app.route('/login/', methods=['GET', 'POST'])
# def another_page():
#     return 'Another page!'
