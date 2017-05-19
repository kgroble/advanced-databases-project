
import time
import redis
import json
from pyArango.connection import *
from question_controller import *
import time


def arango_up(arango_db):
    try:
        arango_db.reload()
        return True
    except:
        return False

"""
{
    "request_type": "answer_question",
    "uname": "kieran",
    "code": "os-linux"
}
{
    "request_type": "create_user",
    "uname": "navin",
    "name": "navin",
    "password": "hashedxxx123",
    "description": "I am awesome!"
}
"""


open_requests_dict = 'recovery_queue'


def handle_user_insert(user_dict, arango_conn):
    user_graph = arango_conn.graphs['UserGraph']
    uname = user_dict['uname']
    user_graph.createVertex('Users',
                            {'uname': uname})


def handle_question_insert(question_dict, arango_db):
    uname = question_dict['uname']
    code = question_dict['code']
    graph = arango_db.graphs['UserGraph']
    users = arango_db['Users']
    responses = arango_db['Response']
    answers = arango_db['Answer']
    answerTo = arango_db['AnswerTo']
    no_check_insert_answer(arango_db, uname, code)


def handle_command(command, arango_conn):
    if type(command) != type({'foo': 'bar'}) or not 'request_type' in command:
        print('Invalid format:', command)
        return

    command_type = command['request_type']
    if command_type == 'create_user':
        handle_user_insert(command, arango_conn)
    elif command_type == 'answer_question':
        handle_question_insert(command, arango_conn)
    else:
        print('Command not recognized')


def poll(redis_conn, arango_conn):
    while True:
        str_result = redis_conn.blpop(open_requests_dict)
        print('Recieved', str_result)
        result = json.loads(str_result[1].decode())
        if not arango_up(arango_conn):
            redis_conn.lpush(open_requests_dict, json.dumps(result))
            time.sleep(1)
            continue
        handle_command(result, arango_conn)


def main():
    redis_conn = redis.Redis()
    arango_username = 'root'
    arango_password = 'srirammohan'
    arango_url = 'http://127.0.0.1:8529'
    arangoConn = Connection(arangoURL=arango_url,
                            username=arango_username,
                            password=arango_password)
    print('Starting recovery process.')
    poll(redis_conn, arangoConn['RelationalSchema'])


if __name__ == '__main__':
    main()
