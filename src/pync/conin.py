# -*- coding: utf-8 -*-

''' conin.py

This module contains classes to get non-blocking input from
the console.

You shouldn't have to use them directly. The nc.py module
will use them when input is (stdin and stdin.isatty).
'''

from __future__ import print_function

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
            ch = msvcrt.getch()
            if ch == b'\x08':
                # User has pressed backspace.
                # Remove last character from line.
                self.line = self.line[:-1]
                # The only way I could find to remove
                # the last character from the console
                # was to move the cursor back with '\b'
                # then overwrite the character with a
                # space before moving the cursor back
                # again with '\b'.
                try:
                    sys.stdout.buffer.write(b'\b \b')
                except AttributeError:
                    sys.stdout.write(b'\b \b')
                sys.stdout.flush()
            elif ch == b'\r':
                # User has pressed enter to send the line.
                self.line += ch
                line = self.line+b'\n'
                self.line = b''
                print()
                return line
            else:
                self.line += ch
                try:
                    sys.stdout.buffer.write(ch)
                except AttributeError:
                    sys.stdout.write(ch)
                sys.stdout.flush()


class _UnixConsoleInput(_BaseConsoleInput):

    def readline(self):
        stdin = sys.__stdin__
        # Non-blocking console input for *nix.
        readables, _, _ = select.select([stdin], [], [], .002)
        if stdin in readables:
            try:
                return stdin.buffer.readline()
            except AttributeError:
                return stdin.readline()


if _WINDOWS:
    NonBlockingConsoleInput = _WinConsoleInput
else:
    NonBlockingConsoleInput = _UnixConsoleInput

