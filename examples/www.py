# -*- coding: utf-8 -*-
'''
A stupid server that hands out 200 OK responses.
'''

import pync


def main():
    with pync.listen(args.host, args.port, k=True) as server:
        for nc in server:
            response = pync.makefile('HTTP/1.1 200 OK\r\n')
            nc.readwrite(stdin=response)


if __name__ == '__main__':
    main()

