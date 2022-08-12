# -*- coding: utf-8 -*-

import multiprocessing
import shlex
import subprocess

try:
    # py2
    import Queue as queue
except ImportError:
    # py3
    import queue

from .pipe import NonBlockingPipe


class PythonPipeInput(object):

    def __init__(self, proc, conn):
        self._proc = proc
        self._conn = conn

    def write(self, data):
        self._conn.send(data)

    def flush(self):
        pass


class PythonPipeOutput(object):

    def __init__(self, proc, conn):
        self._proc = proc
        self._conn = conn

    def read(self, n):
        if self._conn.poll():
            try:
                data = self._conn.recv()
            except EOFError:
                pass
            else:
                data = data.encode('utf-8')
                return data
        if not self._proc.is_alive():
            raise ProcessTerminated


class PythonProcessInput(object):

    def __init__(self, conn):
        self._conn = conn

    def read(self):
        data = self._conn.recv()
        data = data.decode()
        return data

    def readline(self):
        return self.read()


class PythonProcessOutput(object):

    def __init__(self, conn):
        self._conn = conn

    def write(self, data):
        self._conn.send(data)

    def flush(self):
        pass


class PythonProcess(object):

    def __init__(self, code):
        self._code = code
        stdin_conn_out, stdin_conn_in = multiprocessing.Pipe()
        stdout_conn_out, stdout_conn_in = multiprocessing.Pipe()
        self._proc = multiprocessing.Process(
                target=self.run,
        )

        self.stdin = PythonPipeInput(self._proc, stdin_conn_in)
        self.stdout = PythonPipeOutput(self._proc, stdout_conn_out)
        self.stderr = self.stdout

        self._proc_stdin = PythonProcessInput(stdin_conn_out)
        self._proc_stdout = PythonProcessOutput(stdout_conn_in)
        self._proc_stderr = self._proc_stdout

        self._proc.start()

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

