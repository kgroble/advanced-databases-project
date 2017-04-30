
import api
from functools import reduce
import getpass
import bcrypt


"""
EXCEPTIONS
"""

class WrongNumberArguments(Exception):
    def __init__(self, msg):
        pass

"""
COMMANDS
"""


class LogInCommand(object):
    def __init__(self, hosts):
        self._hosts = hosts
    def run(self, args_list):
        raise NotImplemented('"run" has not been implemented.')
    def get_usage(self):
        raise NotImplemented('"get_usage" has not been implemented')


class Command(object):
    def __init__(self, hosts):
        self._hosts = hosts

    def run(self, args_list, user, key):
        raise NotImplemented('"run" has not been implemented.')

    def get_usage(self):
        raise NotImplemented('"get_usage" has not been implemented')


class CommandNotFound(Command):
    def __init__(self):
        super(CommandNotFound, self).__init__([])
        self.name = 'command-not-found'
    def run(self, args_list, auth_user, key):
        return "Command not found."


class GetUser(Command):
    def __init__(self, hosts):
        super(GetUser, self).__init__(hosts)
        self.name = 'get-user'
    def run(self, args_list, auth_user, key):
        if len(args_list) != 1:
            raise WrongNumberArguments("Should only give one argument.")
        username = args_list[0]
        try:
            user = api.get_user(username, self._hosts, auth_user, key)
        except api.UserDoesNotExist:
            return "User does not exist."
        return str(user)
    def get_usage(self):
        return '<username>'


class GetAllUsers(Command):
    def __init__(self, hosts):
        super(GetAllUsers, self).__init__(hosts)
        self.name = 'get-all-users'
    def run(self, args_list, auth_user, key):
        if len(args_list) != 0:
            raise WrongNumberArguments("Command takes no arguments.")
        users = api.get_users(self._hosts, auth_user, key)
        susers = map(lambda x: str(x), users)
        s = reduce(lambda a, b: a + '\n' + b, susers)
        return s
    def get_usage(self):
        return ''


class GetQuestions(Command):
    def __init__(self, hosts):
        super(GetQuestions, self).__init__(hosts)
        self.name = 'get-questions'
    def run(self, args_list, auth_user, key):
        if len(args_list) != 0:
            raise WrongNumberArguments('Command takes no arguments.')
        qs = api.get_questions(self._hosts, auth_user, key)
        return qs
    def get_usage(self):
        return ''


class GetQuestion(Command):
    def __init__(self, hosts):
        super(GetQuestions, self).__init__(hosts)
        self.name = 'get-question'
    def run(self, args_list, auth_user, key):
        if len(args_list) != 1:
            raise WrongNumberArguments('Command takes no arguments.')
        q = api.get_question(self._hosts, auth_user, key)
        return q
    def get_usage(self):
        return '<question-id>'


class AnswerQuestion(Command):
    def __init__(self, hosts):
        super(AnswerQuestion, self).__init__(hosts)
        self.name = 'answer-question'
    def run(self, args_list, auth_user, key):
        if len(args_list) != 2:
            raise WrongNumberArguments('Should be giving two arguments.')
        username = args_list[0]
        code = args_list[1]
        resp = api.answer_question(username, code, self._hosts, auth_user, key)
        if resp:
            return 'Success.'
        return 'Fail!'
    def get_usage(self):
        return '<username> <code>'


class HelpCommand(Command):
    def __init__(self, commands):
        super(HelpCommand, self).__init__([])
        self.name = 'help'
        self._commands = commands
    def run(self, *_):
        help_strs = map(lambda x: x.name + ' ' + x.get_usage(),
                        sorted(self._commands, key=lambda x: x.name))
        return reduce(lambda a, b: a + '\n' + b, help_strs)
    def get_usage(self):
        return ''


class LogIn(LogInCommand):
    def __init__(self, hosts):
        super(LogIn, self).__init__(hosts)
        self.name = 'log-in'
    def run(self, args_list):
        uname = input('Username: ')
        unsafe_password = getpass.getpass()
        success = api.log_in(uname, unsafe_password, self._hosts)
        return success
    def get_usage(self):
        return ''



"""
HELPERS
"""

def get_command(command_name, commands):
    for c in commands:
        if c.name == command_name:
            return c
    return CommandNotFound()
