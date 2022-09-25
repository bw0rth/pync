# -*- coding: utf-8 -*-

import os
import select

try:
    import msvcrt
    _WINDOWS = True
except ImportError:
    _WINDOWS = False
else:
    from ctypes import windll, byref, GetLastError, WinError, POINTER
    from ctypes.wintypes import HANDLE, DWORD, BOOL
    LPDWORD = POINTER(DWORD)
    PIPE_NOWAIT = DWORD(0x00000001)
    ERROR_NO_DATA = 232


class NonBlockingPipe(object):

    def __init__(self):
        self.pin, self.pout = self._create_pipe()
        if not self.pin.set_nowait():
            raise RuntimeError('Unable to create non-blocking pipe')

    def _create_pipe(self):
        rfd, wfd = os.pipe()
        return _PipeInput(rfd), _PipeOutput(wfd)


class _PipeIO(object):

    def __init__(self, fd):
        self._fd = fd

    def fileno(self):
        return self._fd


class _WinPipeInput(_PipeIO):

    def read(self, n):
        # https://stackoverflow.com/a/34504971/11106801
        try:
            return os.read(self._fd, n)
        except OSError as error:
            err_code = GetLastError()
            if err_code == ERROR_NO_DATA:
                return b""
            else:
                website = "https://docs.microsoft.com/en-us/windows/win32/" +\
                          "debug/system-error-codes--0-499-"
                raise OSError("An exception occured. Error code: %i Look up" +\
                              " the error code here: %s" % (err_code, website))

    def set_nowait(self):
        # https://stackoverflow.com/a/34504971/11106801
        SetNamedPipeHandleState = windll.kernel32.SetNamedPipeHandleState
        SetNamedPipeHandleState.argtypes = [HANDLE, LPDWORD, LPDWORD, LPDWORD]
        SetNamedPipeHandleState.restype = BOOL

        handle = msvcrt.get_osfhandle(self._fd)
        res = windll.kernel32.SetNamedPipeHandleState(handle,
                byref(PIPE_NOWAIT),
                None,
                None,
        )

        return not (res == 0)


class _UnixPipeInput(_PipeIO):

    def read(self, n):
        can_read, _, _ = select.select([self._fd], [], [], 0)
        if self._fd in can_read:
            return os.read(self._fd, n)

    def set_nowait(self):
        return True


if _WINDOWS:
    _PipeInput = _WinPipeInput
else:
    _PipeInput = _UnixPipeInput


class _PipeOutput(_PipeIO):

    def write(self, data):
        return os.write(self._fd, data)

