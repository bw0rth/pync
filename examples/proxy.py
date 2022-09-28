# -*- coding: utf-8 -*-

'''
simple TCP proxy using pync.

usage:
    proxy.py 8000 host.example.com 80
'''

import threading
import pync


def main():
    server = pync.Netcat(8000,
            v=True,
            l=True,
            stdin=pync.PIPE,
            stdout=pync.PIPE,
    )

    client = pync.Netcat('host.example.com', 80,
            v=True,
            stdin=server.stdout,
            stdout=server.stdin,
    )


if __name__ == '__main__':
    main()

