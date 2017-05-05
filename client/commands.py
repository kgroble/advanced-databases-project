
import api
from functools import reduce
import getpass


"""
EXCEPTIONS
"""

class WrongNumberArguments(Exception):
    pass

class WrongCredentials(Exception):
    pass

class StopApplication(Exception):
    pass

"""
COMMANDS
"""


class LogInCommand(object):
    """
    Note that this is not a command to log in, but the super class for commands
    which are presented at log in.
    """
    def __init__(self, hosts):
        self._hosts = hosts
    def run(self, args_list) -> 'An error string or a username, key pair':
        raise NotImplemented('"run" has not been implemented.')
    def get_usage(self) -> 'String indicating command usage':
        raise NotImplemented('"get_usage" has not been implemented')


class Command(object):
    def __init__(self, hosts):
        self._hosts = hosts
    def run(self, args_list, user, key) -> 'A string':
        raise NotImplemented('"run" has not been implemented.')
    def get_usage(self) -> 'String indicating command usage':
        raise NotImplemented('"get_usage" has not been implemented')


class CommandNotFound(Command):
    def __init__(self):
        super(CommandNotFound, self).__init__([])
        self.name = 'command-not-found'
    def run(self, *_):
        return 'Command not found. Try running "help"'


class GetUser(Command):
    def __init__(self, hosts):
        super(GetUser, self).__init__(hosts)
        self.name = 'get-user'
    def run(self, args_list, auth_user, key):
        if len(args_list) != 1:
            raise WrongNumberArguments('Should only give one argument.')
        username = args_list[0]
        try:
            user = api.get_user(username, self._hosts, auth_user, key)
        except api.UserDoesNotExist:
            return "User does not exist."
        except api.InvalidUser:
            return 'User data is not valid.'
        return str(user)
    def get_usage(self):
        return '<username>'


class GetAllUsers(Command):
    def __init__(self, hosts):
        super(GetAllUsers, self).__init__(hosts)
        self.name = 'get-all-users'
    def run(self, args_list, auth_user, key):
        if len(args_list) != 0:
            raise WrongNumberArguments('Command takes no arguments.')
        users = api.get_usernames(self._hosts, auth_user, key)
        s = reduce(lambda a, b: a + '\n' + b, users)
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
        if len(qs) == 0:
            return 'There are currently no questions to answer.'
        s = qs[0].get_title()
        for q in qs[1:]:
            s += '\n' + q.get_title()
        return s
    def get_usage(self):
        return ''


class GetQuestion(Command):
    def __init__(self, hosts):
        super(GetQuestion, self).__init__(hosts)
        self.name = 'get-question'
    def run(self, args_list, auth_user, key):
        if len(args_list) != 1:
            raise WrongNumberArguments('Command takes one argument.')
        name = args_list[0]
        qs = api.get_questions(self._hosts, auth_user, key)
        q = list(filter(lambda x: x.name == name,
                        qs))[0]
        return str(q)
    def get_usage(self):
        return '<question-id>'


class AnswerQuestion(Command):
    def __init__(self, hosts):
        super(AnswerQuestion, self).__init__(hosts)
        self.name = 'answer-question'
    def run(self, args_list, auth_user, key):
        if len(args_list) != 2:
            raise WrongNumberArguments('Should be given two arguments')
        code = args_list[1]
        resp = api.answer_question(auth_user, code, self._hosts, auth_user, key)
        if resp:
            return 'Success.'
        return 'Fail!'
    def get_usage(self):
        return '<question-name> <answer-code>'


class GetMatches(Command):
    def __init__(self, hosts):
        super(GetMatches, self).__init__(hosts)
        self.name = 'get-matches'
    def run(self, args_list, auth_user, key) -> 'Will only return the top 5':
        if len(args_list) != 0:
            raise WrongNumberArguments('Command takes no arguments')
        resp = api.get_matches(self._hosts, auth_user, key)
        matches = []
        for k in resp:
            matches.append((k, resp[k]))
        best_matches = list(map(lambda x: x[0],
                                sorted(matches,
                                       key=lambda x: -x[1])))[:5]
        s = '\n'
        for x in best_matches:
            s += '\n' + x
        return s
    def get_usage(self):
        return ''


class GetMessages(Command):
    def __init__(self, hosts):
        super(GetMessages, self).__init__(hosts)
        self.name = 'get-messages'
    def run(self, args_list, auth_user, key):
        if len(args_list) != 0:
            raise WrongNumberArguments('Command takes no arguments')
        ms = api.get_messages(self._hosts, auth_user, key)
        s = ''
        for m in ms:
            s += '\n' + str(m) + '\n'
        return s
    def get_usage(self):
        return ''


class SendMessage(Command):
    def __init__(self, hosts):
        super(SendMessage, self).__init__(hosts)
        self.name = 'send-message'
    def run(self, args_list, auth_user, key):
        if len(args_list) != 1:
            raise WrongNumberArguments('Need to provide a target username ' + \
                                       'and no more.')
        to = args_list[0]
        body = input('Message body: ')

        api.send_message(to, body, self._hosts, auth_user, key)
        return 'Message probably sent'
    def get_usage(self):
        return '<user>'


class PutAttribute(Command):
    def __init__(self, hosts):
        super(PutAttribute, self).__init__(hosts)
        self.name = 'put-attribute'
    def run(self, args_list, auth_user, key):
        if len(args_list) != 0:
            raise WrongNumberArguments('Command does not take arguments')
        attr_name = input('Attribute name: ')
        val = input('Attribute value: ')
        api.patch_attribute(attr_name,
                            val,
                            self._hosts,
                            auth_user,
                            key)
        return 'Willing to bet that it worked. Not a lot though.'
    def get_usage(self):
        return ''


class DeleteAttribute(Command):
    def __init__(self, hosts):
        super(DeleteAttribute, self).__init__(hosts)
        self.name = 'delete-attribute'
    def run(self, args_list, auth_user, key):
        if len(args_list) != 0:
            raise WrongNumberArguments('Command does not take arguments')
        attr_name = input('Attribute name: ')
        api.patch_attribute(attr_name,
                            'dummy',
                            self._hosts,
                            auth_user,
                            key,
                            remove=True)
        return 'Almost certain that this worked.'
    def get_usage(self):
        return ''


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


class ExitCommand(Command):
    def __init__(self):
        super(ExitCommand, self).__init__([])
        self.name = 'exit'
    def run(self, *_):
        raise StopApplication('Calmly exit.')
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
        if not success:
            raise WrongCredentials('Credentials were incorrect')
        return success
    def get_usage(self):
        return ''


class CreateUser(LogInCommand):
    def __init__(self, hosts):
        super(CreateUser, self).__init__(hosts)
        self.name = 'create-user'
    def run(self, args_list):
        uname = input('Username: ')
        while True:
            unsafe_pw = getpass.getpass()
            unsafe_pw1 = getpass.getpass('Enter it again: ')
            if unsafe_pw == unsafe_pw1:
                break
            else:
                print('Passwords do not match')
        name = input('Name: ')
        description = input('Description: ')
        try:
            res = api.create_user(
                uname,
                name,
                description,
                unsafe_pw,
                self._hosts,
            )
        except api.UserAlreadyExists:
            return 'User already exists.'
        except api.InvalidUsername:
            return 'Invalid username.'

        res = api.log_in(uname, unsafe_pw, self._hosts)
        return res
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
