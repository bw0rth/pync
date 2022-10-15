# -*- coding: utf-8 -*-

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
        super(_WinConsoleInput, self).__init__(*args, **kwargs)
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
                self._stdout_write(b'\b \b')
            elif ch == b'\r':
                # User has pressed enter to send the line.
                self.line += ch
                line = self.line+b'\n'
                self.line = b''
                self._stdout_write(b'\n')
                return line
            else:
                self.line += ch
                self._stdout_write(ch)

    def _stdout_write(self, data):
        try:
            sys.stdout.buffer.write(data)
        except AttributeError:
            sys.stdout.write(data)
        sys.stdout.flush()


class _UnixConsoleInput(_BaseConsoleInput):

    def readline(self):
        # Non-blocking console input for *nix.
        readables, _, _ = select.select([sys.stdin], [], [], 0)
        if sys.stdin in readables:
            return self._stdin_readline()

    def _stdin_readline(self):
        try:
            return sys.stdin.buffer.readline()
        except AttributeError:
            return sys.stdin.readline()


if _WINDOWS:
    NonBlockingConsoleInput = _WinConsoleInput
else:
    NonBlockingConsoleInput = _UnixConsoleInput

