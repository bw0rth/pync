# -*- coding: utf-8 -*-
'''
A stupid server that stays open and prints a message
to each client that connects.
'''

import argparse

import pync


def main():
    parser = argparse.ArgumentParser('msg.py',
            formatter_class=argparse.RawTextHelpFormatter,
            description=__doc__,
    )
    parser.add_argument('dest',
            help='Interface to bind the server to',
            nargs='?',
            metavar='DEST',
            default='',
    )
    parser.add_argument('port',
            help='Port number to bind the server to',
            type=int,
            metavar='PORT',
    )
    parser.add_argument('-m',
            help='The message to send to clients',
            metavar='MSG',
            default='HTTP/1.1 200 OK',
    )
    args = parser.parse_args()

    # The l option is for listen mode and k for keeping the server open
    # between each client connection.
    #
    # We use the "pync.makefile" helper function to turn a string into
    # a file-like object ready for the "conn.readwrite" method.
    with pync.Netcat(args.port, dest=args.dest, l=True, k=True) as nc:
        for conn in nc:
            response = pync.makefile("{}\r\n".format(args.m))
            conn.readwrite(stdin=response)


if __name__ == '__main__':
    main()

