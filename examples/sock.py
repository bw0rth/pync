'''
Simple script to demonstrate using a socket with pync.
'''

import argparse
import socket

import pync


def listen(addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)
    print(f'Listening for a connection... {addr}')
    connection, cli_addr = s.accept()
    print(f'Connection successful! {cli_addr}')
    return connection


def connect(addr):
    connection = socket.create_connection(addr)
    print(f'Connection successful! {addr}')
    return connection


def main():
    parser = argparse.ArgumentParser('sock.py',
        formatter_class=argparse.RawTextHelpFormatter,
        description=__doc__,
    )
    parser.add_argument('dest',
        help='Hostname or IP connect or bind to',
        metavar='dest',
        nargs='?',
        default='',
    )
    parser.add_argument('port',
        help='Port number to connect to',
        metavar='port',
        type=int,
    )
    parser.add_argument('-l',
        help='Listen mode, for bind shell',
        action='store_true',
    )
    args = parser.parse_args()
    addr = args.dest, args.port

    make_connection = connect
    if args.l:
        make_connection = listen

    with make_connection(addr) as conn:
        pync.readwrite(conn)


if __name__ == '__main__':
    main()
