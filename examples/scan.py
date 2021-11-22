# -*- coding: utf-8 -*-
'''
Example of a simple port scan using pync.
'''

import argparse

import pync


def main():
    parser = argparse.ArgumentParser('scan.py',
            formatter_class=argparse.RawTextHelpFormatter,
            description=__doc__,
    )
    parser.add_argument('dest',
            help='Destination hostname or ip to connect to',
            metavar='DEST',
    )
    parser.add_argument('port',
            help='Port list or range for scanning',
            metavar='PORT',
            nargs='+',
    )
    args = parser.parse_args()

    # The "v" option is to turn verbose on, and "z" for
    # Zero-I/O mode (connect then close).
    with pync.Netcat(args.port, dest=args.dest, v=True, z=True) as nc:
        nc.run()


if __name__ == '__main__':
    main()

