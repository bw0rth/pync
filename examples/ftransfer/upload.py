# -*- coding: utf-8 -*-
'''
Upload a file to a client or server using pync.

example client:
    upload.py localhost 8000 file.in

example server:
    upload.py -l localhost 8000 file.in
'''

import argparse
import contextlib

from pync import Netcat


def main():
    parser = argparse.ArgumentParser('upload.py',
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
    parser.add_argument('filename',
            help='Filename to upload',
            metavar='FILENAME',
    )
    parser.add_argument('-l',
            help='Listen mode, for inbound connects',
            action='store_true',
    )
    args = parser.parse_args()

    with open(args.filename, 'rb') as f:
        nc = Netcat(
                dest=args.dest,
                port=args.port,
                v=True,          # Verbose
                l=args.l,        # Listen for connections (server mode).
                stdin=f,         # Write stdin data (f) to the network.
        )
        with contextlib.closing(nc):
            nc.readwrite()


if __name__ == '__main__':
    main()

