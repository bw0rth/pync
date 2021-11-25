# -*- coding: utf-8 -*-

import socket
import sys
from .nc import pync, Netcat


def main():
    argv = sys.argv[1:]

    try:
        nc = pync(argv)
    except socket.error as e:
        # The NetcatServer may raise a socket error if
        # an invalid port number is given.
        sys.stderr.write('{}: {}\n'.format(
            Netcat.name,
            str(e),
        ))
        return 1

    try:
        nc.run()
    except KeyboardInterrupt:
        sys.stderr.write('\n')
    finally:
        nc.close()


if __name__ == '__main__':
    status = main()
    sys.exit(status)

