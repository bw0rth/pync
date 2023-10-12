# -*- coding: utf-8 -*-

import socket
import sys

import pync


def main():
    args = sys.argv[1:]
    return pync.run(args).returncode


if __name__ == '__main__':
    returncode = main()
    sys.exit(returncode)

