# -*- coding: utf-8 -*-
'''
A simple echo client/server

example client:
    echo.py localhost 8000

example server:
    echo.py -l localhost 8000
'''

import argparse
import pync


def main():
    parser = argparse.ArgumentParser('echo.py',
            formatter_class=argparse.RawTextHelpFormatter,
            description=__doc__,
    )
    parser.add_argument('dest',
            help='Destination hostname or ip to connect or bind to',
            nargs='?',
            default='',
            metavar='DEST',
    )
    parser.add_argument('port',
            help='Port to connect or bind to',
            metavar='PORT',
            type=int,
    )
    parser.add_argument('-l',
            help='Listen mode, for inbound connects',
            action='store_true',
    )
    args = parser.parse_args()
    
    nc = pync.Netcat(
        dest=args.dest,
        port=args.port,
        l=args.l,
        y='import sys; sys.stdout.write(sys.stdin.read())',
        v=True,
    )
    nc.run()


if __name__ == '__main__':
    main()
