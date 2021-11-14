# -*- coding: utf-8 -*-

import sys
from .nc import pync


def main():
    argv = sys.argv[1:]
    with pync(argv) as nc:
        nc.run()


if __name__ == '__main__':
    status = main()
    sys.exit(status)

