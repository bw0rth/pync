# -*- coding: utf-8 -*-

try:
    import msvcrt
    _WINDOWS = True
except ImportError:
    _WINDOWS = False
import sys


class BaseConsoleInput:

    def __init__(self, buf=None, blocking=True):
        # blocking - wait for user input after buffer data exhausted.
        self.blocking = blocking
        self.buffer = buf
        # If no buffer data given and stdin is piped data.
        if buf is None and not sys.stdin.isatty():
            # set buffer to the stdin pipe.
            self.buffer = sys.stdin


class WinConsoleInput(BaseConsoleInput):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.line = b''
    
    def readline(self):
        if self.buffer is not None:
            line = self.buffer.readline()
            if line:
                return line
            # END OF PIPE DATA
            if self.blocking:
                #sys.stdin = os.fdopen(1)
                pass
            self.buffer = None

        # select doesn't work for files on Windows.
        # So using msvcrt console IO functions instead.
        if msvcrt.kbhit():
            ch = msvcrt.getche()
            self.line += ch
            if ch == b'\r':
                line = self.line+b'\n'
                self.line = b''
                print()
                if self.blocking:
                    return line


class UnixConsoleInput(BaseConsoleInput):

    def readline(self):
        if self.buffer is not None:
            line = self.buffer.readline()
            if line:
                return line
            # END OF BUFFER DATA
            if self.blocking:
                # Reopen stdin for user input when buffer is EOF.
                sys.stdin = os.fdopen(1)
            self.buffer = None

        if self.blocking:
            readables, _, _ = select.select([sys.stdin], [], [], .002)
            if sys.stdin in readables:
                return sys.stdin.readline()


if _WINDOWS:
    ConsoleInput = WinConsoleInput
else:
    ConsoleInput = UnixConsoleInput

