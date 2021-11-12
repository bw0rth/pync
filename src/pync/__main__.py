# -*- coding: utf-8 -*-

import sys
from .nc import nc


def main():
    argv = sys.argv[1:]
    exit_code = nc(argv)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()

