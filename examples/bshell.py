# -*- coding: utf-8 -*-

import argparse
import platform

from pync import pync


DESCRIPTION = '''
A simple bind shell using pync.
Run this, then connect to it with Netcat.'''


def main():
    parser = argparse.ArgumentParser('rshell',
            formatter_class=argparse.RawTextHelpFormatter,
            description=DESCRIPTION,
    )
    parser.add_argument('host',
            help='Hostname or IP to bind to.',
            metavar='HOST',
            nargs='?',
            default='',
    )
    parser.add_argument('port',
            help='Port number to bind to.',
            metavar='PORT',
    )
    args = parser.parse_args()
    host, port = args.host, args.port

    if platform.system() == 'Windows':
        command = 'cmd /q'
    else:
        command = "PS1='$ ' sh -i"

    args = '-l {host} {port} -e "{command}"'.format(
            host=host,
            port=port,
            command=command,
    )

    with pync(args) as nc:
        nc.run()


if __name__ == '__main__':
    main()

