
from commands import *
from exceptions import *
import socket


startmsg = \
"    - -      - - - - -\n" + \
"  /     \\  /         \ \n" + \
"/        \\/           \ \n" + \
"\\                     / \n" + \
" \\                   / \n" + \
"  \\       cs        / \n" + \
"   \\               / \n" + \
"    \\             / \n" + \
"     \\           / \n" + \
"      \\         / \n" + \
"       \\       / \n" + \
"        \\     / \n" + \
"         \\   / \n" + \
"          \\ / "

remote_mode = False
if remote_mode:
    hosts = [ 'http://cdk433.csse.rose-hulman.edu',
              'http://cdk434.csse.rose-hulman.edu',
              'http://cdk435.csse.rose-hulman.edu' ]
else:
    hosts = [ 'http://127.0.0.1' ]


comms = [ GetUser(hosts),
              GetAllUsers(hosts),
              GetQuestions(hosts),
              GetQuestion(hosts),
              SendMessage(hosts),
              PutAttribute(hosts),
              DeleteAttribute(hosts),
              GetMessages(hosts),
              AnswerQuestion(hosts),
              ExitCommand(),
              GetMatches(hosts) ]
comms.append(HelpCommand(comms))

log_in_comms = [ LogIn(hosts),
                 ExitCommand(),
                 CreateUser(hosts) ]
log_in_comms.append(HelpCommand(log_in_comms))


def log_in_repl():
    while True:
        inp = input('--> ')
        words = inp.split()
        if len(words) == 0:
            continue

        first, *rest = words
        command = get_command(first, log_in_comms)

        try:
            res = command.run(rest)
        except WrongCredentials:
            print('Incorrect credentials.')
            continue
        except StopApplication:
            print('Come back soon!')
            return False

        try: # This is for sure not the best way to do this
            uname, key = res
            repl(uname, key)
        except ValueError:
            print(res)
            continue


def repl(uname, key):
    while True:
        inp = input('--> ')
        words = inp.split()
        if len(words) == 0:
            continue

        first, *rest = words
        command = get_command(first, comms)
        try:
            out = command.run(rest, uname, key)
            print(out)
        except WrongNumberArguments:
            print('Wrong number of arguments.')
        except NotLoggedIn:
            print('Not logged in - Please log in first!')
            log_in_repl()
        except UnknownError:
            print('The server has encountered an error - Please try again later!')
        except StopApplication:
            print('Come back soon!')
            return False


def main():

    print(startmsg)
    print('Run "help" for a list of valid commands.')

    log_in_repl()


if __name__ == '__main__':
    main()
