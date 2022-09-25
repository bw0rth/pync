# -*- coding: utf-8 -*-
'''
Download client or server data to a file using pync.

example client:
    download.py localhost 8000 file.out

example server:
    download.py -l localhost 8000 file.out
'''

import argparse
import contextlib
import os

from pync import Netcat


def main():
    parser = argparse.ArgumentParser('download.py',
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
            help='Filename to save the data to',
            metavar='FILENAME',
    )
    parser.add_argument('-l',
            help='Listen mode, for inbound connects',
            action='store_true',
    )
    args = parser.parse_args()

    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    filepath = os.path.join('downloads', args.filename)
    with open(filepath, 'wb') as f:
        nc = Netcat(
                dest=args.dest,
                port=args.port,
                v=True,          # Verbose
                l=args.l,        # Listen for connections (server mode).
                stdout=f,        # Write network data to stdout (f).
        )
        with contextlib.closing(nc):
            nc.readwrite()


if __name__ == '__main__':
    main()

