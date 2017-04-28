
import requests as req


headers = {'content-type': 'application/json'}


def make_post(data, path, hosts, headers=headers):
    for host in hosts:
        result = req.post(host + path, json=data, headers=headers)
        try:
            result.raise_for_status()
            return result
        except:
            pass
    return False


def make_get(params, path, hosts, headers=headers):
    for host in hosts:
        result = req.get(host + path, params=params, headers=headers)
        try:
            result.raise_for_status()
            return result
        except:
            pass


"""
USER API
"""


class User:
    def __init__(self):
        pass
    def to_json(self):
        pass


def is_logged_in(username, key):
    return True


def login(username, password, key):
    return True


def logout(username, key):
    return True


def create_user(user, headers=headers):
    pass


def creating_user(username, hosts):
    make_post({'username': username},
              '/users/',
              hosts)


def get_user(username, hosts):
    make_get({'username': username},
             '/users/',
             hosts)


"""
QUESTION API
"""

def answer_question():
    pass
