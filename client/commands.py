
import api

"""
EXCEPTIONS
"""

class WrongNumberArguments(Exception):
    def __init__(self, msg):
        pass

"""
COMMANDS
"""


class Command(object):
    def __init__(self, hosts):
        self._hosts = hosts

    def run(self, args_list):
        raise NotImplemented('"run" has not been implemented.')

    def get_usage(self):
        raise NotImplemented('"get_usage" has not been implemented')


class CommandNotFound(Command):
    def __init__(self):
        super(CommandNotFound, self).__init__([])
        self.name = 'command-not-found'
    def run(self, args_list):
        return "Command not found."


class GetUser(Command):
    def __init__(self, hosts):
        super(GetUser, self).__init__(hosts)
        self.name = 'get-user'
    def run(self, args_list):
        if len(args_list) != 1:
            raise WrongNumberArguments("Should only give one argument")
        username = args_list[0]
        user = api.get_user(username, self._hosts)
        print(user)
        return "Success!"


class LogIn(Command):
    pass


"""
HELPERS
"""

def get_command(command_name, commands):
    for c in commands:
        if c.name == command_name:
            return c
    return CommandNotFound()
