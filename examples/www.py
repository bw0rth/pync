# -*- coding: utf-8 -*-
'''
A stupid server that hands out HTTP 200 OK responses.
'''

import pync


def main():
    '''
    This script demonstrates the use of the "k" option to keep
    the server open after each connection.
    '''

    with pync.Netcat(8000, dest='localhost', l=True, k=True) as nc:
        for connection in nc:
            response = pync.makefile('HTTP/1.1 200 OK\r\n')
            connection.readwrite(stdin=response)


if __name__ == '__main__':
    main()

