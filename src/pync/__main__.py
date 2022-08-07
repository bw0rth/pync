# -*- coding: utf-8 -*-

import socket
import sys

from . import pync


def main():
    args = sys.argv[1:]
    return pync(args)


if __name__ == '__main__':
    status = main()
    sys.exit(status)

