# -*- coding: utf-8 -*-
'''
Simple connect scan using pync.

example:
    scan.py localhost 7999 8000 8003
'''

import argparse

from pync import Netcat


def main():
    parser = argparse.ArgumentParser('scan.py',
            formatter_class=argparse.RawTextHelpFormatter,
            description=__doc__,
    )
    parser.add_argument('dest',
            help='Destination hostname or IP to connect to',
            metavar='DEST',
    )
    parser.add_argument('port',
            help='Port(s) to scan',
            metavar='PORT',
            nargs='+',
            type=int,
    )
    args = parser.parse_args()

    # The "v" option is to turn verbose on, and "z" for
    # Zero-I/O mode (connect then close).
    with Netcat(args.port, dest=args.dest, v=True, z=True) as nc:
        nc.readwrite()


if __name__ == '__main__':
    main()

