
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

        res = command.run(rest)
        if res == True:
            break
        if res == False:
            print('Operation not successful')
        else:
            print(res)


def repl(comms):
    while True:
        inp = input('--> ')
        words = inp.split()
        if len(words) == 0:
            continue

        first, *rest = words
        command = get_command(first, comms)
        try:
            out = command.run(rest, '', '')
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

    log_in_repl(log_in_comms)
    repl(comms)


if __name__ == '__main__':
    main()
