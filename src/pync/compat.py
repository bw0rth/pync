# -*- coding: utf-8 -*-

import sys


if sys.version_info.major == 2:
    class ConnectionError(OSError):
        pass

    class ConnectionRefusedError(ConnectionError):
        pass

    class range(object):

        def __init__(self, *args):
            self.start = 0
            self.stop = None
            self.step = 1

            try:
                self.start, self.stop, self.step = args
            except ValueError:
                try:
                    self.start, self.stop = args
                except ValueError:
                    self.stop = args[0]

            self._rng = xrange(self.start, self.stop, self.step)  # noqa: F821

        def __getattr__(self, name):
            return getattr(self._rng, name)

        def __iter__(self):
            return iter(self._rng)
else:
    ConnectionError = ConnectionError
    ConnectionRefusedError = ConnectionRefusedError
    range = range

