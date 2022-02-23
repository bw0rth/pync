# -*- coding: utf-8 -*-
'''
Upload a file to a client or server using pync.
'''

import argparse

import pync


def main():
    parser = argparse.ArgumentParser('upload.py',
            description=__doc__,
    )
    parser.add_argument('host',
            help='Hostname or ip to connect or bind to',
            nargs='?',
            default='',
            metavar='HOST',
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
    parser.add_argument('--listen', '-l',
            help='Listen mode, for inbound connects',
            action='store_true',
    )
    args = parser.parse_args()

    mode = pync.connect
    if args.listen:
        mode = pync.listen

    with mode(args.host, args.port) as conn:
        with open(args.filename, 'rb') as f:
            # pass the open file to stdin.
            # Shut down socket writes after EOF with the N option.
            conn.readwrite(stdin=f, N=True)


if __name__ == '__main__':
    main()

