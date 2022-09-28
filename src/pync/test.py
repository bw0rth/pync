# -*- coding: utf-8 -*-

import pync


def main():
    nc = pync.Netcat('localhost', 8000,
            v=True,
            stdin=pync.PIPE,
            stdout=pync.PIPE,
    )

    nc.stdin.write(b'hello, world.\n')
    nc.readwrite()


if __name__ == '__main__':
    main()

