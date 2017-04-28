
import requests as req


"""
CONSTANTS
"""

headers = {'content-type': 'application/json'}

"""
EXCEPTIONS
"""

class UserDoesNotExist(Exception):
    pass


"""
USER API
"""


class User:
    def __init__(self, username):
        self.username = username
    def to_json(self):
        pass
    def __str__(self):
        s  = 'Username: ' + self.username
        return s


def is_logged_in(username, key):
    return True


def login(username, password, key):
    return True


def logout(username, key):
    return True


def create_user(username, hosts):
    make_post({'username': username},
              '/users/',
              hosts)
    return True


def get_user(username, hosts, auth_user, key):
    usr = make_get({},
                   '/user/' + username,
                   hosts)
    if usr == None:
        raise UserDoesNotExist('User does not exist.')
    data = usr.json()
    if not 'uname' in data:
        raise UserDoesNotExist('User does not exist.')
    username = data['uname']
    return User(username)


def get_users(hosts, auth_user, key):
    users_data = make_get({'username': auth_user,
                           'key': key},
                          '/users/',
                          hosts)
    users = filter(lambda x: x != None, map(user_from_json, users_data.json()))
    return users



"""
QUESTION API
"""

def answer_question(username, code, hosts, auth_user, key):
    resp = make_post({'username': username,
                      'key': key},
                     '/user/' + username + '/answer/' + code,
                     hosts)
    try:
        resp.raise_for_status()
        return True
    except:
        return False


def get_questions(username, hosts, auth_user, key):
    data = make_get({'username': username,
                     'key': key},
                    '/questions/',
                    hosts)
    if not 'uname' in data.json():
        raise UserDoesNotExist('User does not exist.')
    return data.json()


"""
HELPERS
"""


def user_from_json(json):
    if not 'uname' in json:
        return None
    username = json['uname']
    return User(username)


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
