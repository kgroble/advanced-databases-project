
import requests as req
import bcrypt
import hashlib


"""
CONSTANTS
"""

headers = {'content-type': 'application/json'}

"""
EXCEPTIONS
"""

class UserDoesNotExist(Exception):
    pass

class UserAlreadyExists(Exception):
    pass


"""
CLASSES
"""

class User:
    def __init__(self, username):
        self.username = username
    def to_json(self):
        pass
    def __str__(self):
        s  = 'Username: ' + self.username
        return s


class Question:
    def __init__(self, name, text, possible_answers):
        self.name = name
        self.text = text
        self.answers = possible_answers
    def get_title(self):
        return '(%s) %s' % (self.name, self.text)
    def __str__(self):
        s = self.get_title()
        for x in self.answers:
            s += '\n - %s: %s' % (x['label'],x['code'])
        return s


"""
USER API
"""

def is_logged_in(username, key):
    return True


def log_in(username, unsafe_password, hosts):
    h = hashlib.sha256()
    h.update(unsafe_password.encode())
    pw = h.hexdigest()
    result = make_post({'username': username,
                        'key': pw},
                       '/login/',
                       hosts)
    try:
        result.raise_for_status()
        return username, pw
    except:
        return False


def logout(username, key):
    return True


def create_user(username, unsafe_password, hosts):
    h = hashlib.sha256()
    h.update(unsafe_password.encode())
    hashed_pw = h.hexdigest() # this should just
    pw = bcrypt.hashpw(hashed_pw.encode(), bcrypt.gensalt()).decode()
    result = make_post({'username': username,
                        'password': pw
                        },
                       '/user/',
                       hosts)
    if not result:
        raise UserAlreadyExists('User already exists.')
    return True


def get_user(username, hosts, auth_user, key):
    usr = make_get({'username': auth_user,
                    'key': key},
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

def answer_question(username, code, hosts, auth_user, key) -> 'A boolean value':
    resp = make_post({'username': username,
                      'key': key},
                     '/user/' + username + '/answer/' + code,
                     hosts)
    try:
        resp.raise_for_status()
        return True
    except:
        return False


def get_questions(hosts, auth_user, key) -> 'A list of question objects':
    data = make_get({'username': auth_user,
                     'key': key},
                    '/questions/',
                    hosts)
    qs = map(question_from_json, data.json())
    return list(filter(lambda x: x != None, qs))


"""
HELPERS
"""


def user_from_json(json):
    if not 'uname' in json:
        return None
    username = json['uname']
    return User(username)


def question_from_json(json):
    if not 'text' in json:
        return None
    if not 'options' in json:
        return None
    if not '_id' in json:
        return None
    q = Question(json['_id'],
                 json['text'],
                 json['options'])
    return q


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
