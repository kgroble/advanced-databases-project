
from commands import *
import socket


def log_in_repl(comms):
    while True:
        inp = input('--> ')
        words = inp.split()
        if len(words) == 0:
            continue

        first, *rest = words
        command = get_command(first, comms)

        try:
            res = command.run(rest)
        except WrongCredentials:
            print('Incorrect credentials.')
            continue

        try: # This is for sure not the best way to do this
            uname, key = res
            return uname, key
        except ValueError:
            print(res)
            continue


def repl(comms, uname, key):
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


def main():
    if 'cdk' in socket.gethostname():
        hosts = [ 'http://cdk433.csse.rose-hulman.edu',
                  'http://cdk434.csse.rose-hulman.edu',
                  'http://cdk435.csse.rose-hulman.edu' ]
    else:
        hosts = [ 'http://127.0.0.1' ]

    comms = [ GetUser(hosts),
              GetAllUsers(hosts),
              GetQuestions(hosts),
              AnswerQuestion(hosts) ]
    comms.append(HelpCommand(comms))

    log_in_comms = [ LogIn(hosts) ]
    log_in_comms.append(HelpCommand(log_in_comms))

    uname, key = log_in_repl(log_in_comms)
    repl(comms, uname, key)


if __name__ == '__main__':
    main()
