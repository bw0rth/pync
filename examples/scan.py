# -*- coding: utf-8 -*-

import pync


def main():
    with pync.Netcat(args.host, args.port) as nc:
        for connection in nc:
            pass


if __name__ == '__main__':
    main()

