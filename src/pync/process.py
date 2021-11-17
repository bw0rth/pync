# -*- coding: utf-8 -*-

import subprocess

from .pipe import Pipe


class Process:

    def __init__(self, cmd):
        pipe = Pipe()
        if not pipe.pin.set_nowait():
            raise RuntimeError('Unable to create non-blocking process pipe.')

        self._proc = subprocess.Popen(cmd, shell=True,
                stdin=subprocess.PIPE,
                stdout=pipe.pout,
                stderr=subprocess.STDOUT,
        )
        self.stdout = _ProcStdout(self._proc, pipe.pin)

    def __getattr__(self, name):
        return getattr(self._proc, name)


class _ProcStdout:

    def __init__(self, proc, stdout):
        self._proc = proc
        self._stdout = stdout

    def __getattr__(self, name):
        return getattr(self._stdout, name)

    def read(self, n):
        data = self._stdout.read(n)
        if data:
            return data
        if self._proc.poll() is not None:
            raise ProcessTerminated


class ProcessTerminated(Exception):
    pass

