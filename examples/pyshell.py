# -*- coding: utf-8 -*-
'''
A simple reverse or bind python interpreter shell using pync.

example bind shell:
    pyshell.py -l localhost 8000

example reverse shell:
    pyshell.py localhost 8000
'''

import argparse
import platform

from pync import Netcat


try:
    # py2
    input = raw_input
except NameError:
    # py3
    pass


def main():
    parser = argparse.ArgumentParser('pyshell.py',
            formatter_class=argparse.RawTextHelpFormatter,
            description=__doc__,
    )
    parser.add_argument('dest',
            help='Hostname or IP to connect or bind to',
            metavar='dest',
            nargs='?',
            default='',
    )
    parser.add_argument('port',
            help='Port number to connect to',
            metavar='port',
            type=int,
    )
    parser.add_argument('-l',
            help='Listen mode, for bind shell',
            action='store_true',
    )
    args = parser.parse_args()

    def print_warning(lines, ask_continue=False):
        print('WARNING')
        for l in lines:
            print(l)
        if ask_continue:
            print()
            response = ''
            while response != 'Y':
                response = input('Are you sure you want to continue? (Y/n): ')
                if response == 'n':
                    raise SystemExit

    warning = ''
    local_addresses = ('localhost', '127.0.0.1')
    if args.l and args.dest not in local_addresses:
        warning = 'You are about to bind a python shell to a non-local interface.'
    elif args.dest and args.dest not in local_addresses:
        warning = 'You are about to connect a python shell to a remote machine.'

    if warning:
        lines = (
                warning,
                'This may expose your system to attackers or eavesdroppers.',
        )
        print_warning(lines, ask_continue=True)

    pycode = "import code; code.interact()"
    nc = Netcat(
            dest=args.dest,
            port=args.port,
            y=pycode,
            l=args.l,
            v=True,
    )

    try:
        nc.run()
    except KeyboardInterrupt:
        print()


if __name__ == '__main__':
    main()

