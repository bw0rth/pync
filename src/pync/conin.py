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


class _BaseConsoleInput(object):

    def read(self, n):
        return self.readline()


class _WinConsoleInput(_BaseConsoleInput):

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


class _UnixConsoleInput(_BaseConsoleInput):

    def readline(self):
        stdin = sys.__stdin__
        def py2_readline():
            return stdin.readline()
        def py3_readline():
            return stdin.buffer.readline()
        # Non-blocking console input for *nix.
        readables, _, _ = select.select([stdin], [], [], .002)
        if stdin in readables:
            try:
                return py3_readline()
            except AttributeError:
                return py2_readline()


if _WINDOWS:
    NonBlockingConsoleInput = _WinConsoleInput
else:
    NonBlockingConsoleInput = _UnixConsoleInput

