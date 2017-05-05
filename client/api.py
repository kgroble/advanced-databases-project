
import requests as req
import bcrypt
import hashlib
import json


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

class InvalidUser(Exception):
    pass

class InvalidUsername(Exception):
    pass


"""
CLASSES
"""

class User:
    def __init__(self, username, name, description, answers, attrs):
        self.username = username
        self.name = name
        self.description = description
        self.answers = answers
        self.attrs = attrs
    def to_json(self):
        pass
    def __str__(self):
        s = 'Username: ' + self.username
        s += '\nName: ' + self.name
        s += '\nDescription: ' + self.description
        s += '\nAnswers:'
        for a in self.answers:
            s += '\n - ' + str(a)
        for k in self.attrs:
            s += '\n' + k + ': ' + str(self.attrs[k])
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


class Answer:
    def __init__(self, code):
        self.code = code
    def __str__(self):
        return self.code


class Message:
    def __init__(self, content, from_uname, date):
        self.content = content
        self.from_username = from_uname
        self.date = date
    def __str__(self):
        s = ''
        s += 'From: %s' % self.from_username
        s += '\nDate: %s' % self.date
        s += '\n' + self.content
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


def create_user(username, name, description, unsafe_password, hosts):
    h = hashlib.sha256()
    h.update(unsafe_password.encode())
    hashed_pw = h.hexdigest() # this should just
    pw = bcrypt.hashpw(hashed_pw.encode(), bcrypt.gensalt()).decode()
    result = make_post({'username': username,
                        'password': pw,
                        'name': name,
                        'description': description
                        },
                       '/user/',
                       hosts)
    try:
        result.raise_for_status()
        return True
    except:
        data = result.json()
        if 'bad username' in data['error'].lower():
            raise InvalidUsername('Invalid username.')
        else:
            raise UserAlreadyExists('User already exists.')


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
    if not 'name' in data:
        raise InvalidUser('User does not have a name.')
    if not 'description' in data:
        raise InvalidUser('User does not have a description.')

    uname = data['uname']
    name = data['name']
    description = data['description']
    answers = list(map(answer_from_document, data['answers']))
    del data['uname']
    del data['name']
    del data['description']
    del data['answers']

    return User(uname,
                name,
                description,
                answers,
                data)


def get_usernames(hosts, auth_user, key):
    users_data = make_get({'username': auth_user,
                           'key': key},
                          '/users/',
                          hosts)
    users = map(lambda x: x['uname'], users_data.json())
    return users


def get_messages(hosts, auth_user, key):
    data = make_get({'username': auth_user,
                     'key': key},
                    '/user/%s/messages/' % auth_user,
                    hosts)
    messages = data.json()
    return list(map(message_from_json, messages))


def send_message(to, body, hosts, auth_user, key):
    data = make_post({'username': auth_user,
                      'key': key,
                      'body': body},
                     '/user/%s/message/%s/' % (auth_user, to),
                     hosts)
    return True


def patch_attribute(attr_key, attr_val, hosts, auth_user, key, remove=False):
    data = {'username': auth_user,
            'key': key,
            'remove': remove}
    data[attr_key] = attr_val
    resp = make_patch(data,
                      '/user/%s/' % auth_user,
                      hosts)
    return True



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
    return list(filter(lambda x: x, qs))

"""
MATCH API
"""

def get_matches(hosts, auth_user, key) -> 'A list of usernames ordered' + \
                                          ' by match strength':
    resp = make_get({'username': auth_user,
                     'key': key},
                    '/user/%s/matches/' % auth_user,
                    hosts)
    return resp.json()




"""
HELPERS
"""


def answer_from_document(json):
    if not 'code' in json:
        return None
    return Answer(json['code'])


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


def message_from_json(json):
    if not 'from' in json:
        return None
    if not 'body' in json:
        return None
    return Message(json['body'], json['from'], '')


def make_post(data, path, hosts, headers=headers):
    num = len(hosts)
    for host in hosts:
        result = req.post(host + path, json=data, headers=headers)
        try:
            result.raise_for_status()
            return result
        except:
            if num == len(hosts):
                return result
    return False


def make_patch(data, path, hosts, headers=headers):
    for host in hosts:
        result = req.patch(
            host + path,
            data=json.dumps(data),
            headers=headers
        )
        try:
            result.raise_for_status()
            return result
        except:
            pass



def make_get(params, path, hosts, headers=headers):
    for host in hosts:
        result = req.get(host + path, params=params, headers=headers)
        try:
            result.raise_for_status()
            return result
        except:
            pass
