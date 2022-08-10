# -*- coding: utf-8 -*-

import multiprocessing
import shlex
import subprocess

from .pipe import NonBlockingPipe


class PythonPipeInput(object):

    def __init__(self, q):
        self._q = q

    def write(self, data):
        self._q.put(data)


class PythonPipeOutput(object):

    def __init__(self, q):
        self._q = q

    def read(self):
        return self._q.get()


class PythonProcessInput(object):

    def __init__(self, q):
        self._q = q

    def read(self):
        return self._q.get()


class PythonProcessOutput(object):

    def __init__(self, q):
        self._q = q

    def write(self, data):
        self._q.put(data)


class PythonProcess(object):

    def __init__(self, code):
        self._code = code
        self._qin = multiprocessing.Queue()
        self._qout = multiprocessing.Queue()
        self._proc = multiprocessing.Process(
                target=self.run,
        )

        self.stdin = PythonPipeInput(self._qin)
        self.stdout = PythonPipeOutput(self._qout)
        self.stderr = self.stdout

        self._proc_stdin = PythonProcessInput(self._qin)
        self._proc_stdout = PythonProcessOutput(self._qout)
        self._proc_stderr = self._proc_stdout

    @classmethod
    def from_file(cls, filename):
        with open(filename) as f:
            code = f.read()
        return cls(code)

    def __getattr__(self, name):
        return getattr(self._proc, name)

    def run(self):
        import sys
        sys.stdin = self._proc_stdin
        sys.stdout = self._proc_stdout
        sys.stderr = self._proc_stderr
        exec(self._code, locals())


class NonBlockingProcess(object):

    def __init__(self, cmd, shell=False):
        pipe = NonBlockingPipe()

        if not shell:
            cmd = shlex.split(cmd)

        self._proc = subprocess.Popen(cmd, shell=shell,
                stdin=subprocess.PIPE,
                stdout=pipe.pout,
                stderr=subprocess.STDOUT,
        )
        self.stdout = _ProcStdout(self._proc, pipe.pin)

    def __getattr__(self, name):
        return getattr(self._proc, name)


class ProcessTerminated(Exception):
    pass


class _ProcStdout(object):

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

