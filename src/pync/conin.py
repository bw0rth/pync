# -*- coding: utf-8 -*-

''' conin.py

This module contains classes to get non-blocking input from
the console.

You shouldn't have to use them directly. The nc.py module
will use them when input is (stdin and stdin.isatty).
'''

try:
    import msvcrt
    _WINDOWS = True
except ImportError:
    _WINDOWS = False

import select
import sys


class BaseConsoleInput:

    def read(self, n):
        return self.readline()


class WinConsoleInput(BaseConsoleInput):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.line = b''
    
    def readline(self):
        # Non-blocking console input for Windows.
        # select doesn't work for files on Windows.
        # So using msvcrt console IO functions instead.
        if msvcrt.kbhit():
            ch = msvcrt.getche()
            self.line += ch
            if ch == b'\r':
                line = self.line+b'\n'
                self.line = b''
                print()
                return line


class UnixConsoleInput(BaseConsoleInput):

    def readline(self):
        # Non-blocking console input for *nix.
        readables, _, _ = select.select([sys.stdin], [], [], .002)
        if sys.stdin in readables:
            return sys.stdin.readline()


if _WINDOWS:
    ConsoleInput = WinConsoleInput
else:
    ConsoleInput = UnixConsoleInput

