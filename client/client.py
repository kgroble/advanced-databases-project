
from commands import *


def repl(hosts, comms):
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
    # hosts = [ 'http://cdk433.csse.rose-hulman.edu',
    #           'http://cdk434.csse.rose-hulman.edu',
    #           'http://cdk435.csse.rose-hulman.edu' ]
    hosts = [ 'http://127.0.0.1' ]

    comms = [ GetUser(hosts),
              GetAllUsers(hosts),
              GetQuestions(hosts),
              AnswerQuestion(hosts) ]
    comms.append(HelpCommand(comms))

    repl(hosts, comms)


if __name__ == '__main__':
    main()
