# -*- coding: utf-8 -*-

import multiprocessing
import shlex
import subprocess
import sys

try:
    # py2
    import Queue as queue
except ImportError:
    # py3
    import queue

from .pipe import NonBlockingPipe


class PythonStdoutReader(object):

    def __init__(self, proc, conn):
        self._proc = proc
        self._conn = conn

    def read(self, *args, **kwargs):
        if self._conn.poll():
            try:
                data = self._conn.recv_bytes()
            except EOFError:
                pass
            else:
                return data
        if not self._proc.is_alive():
            raise ProcessTerminated


class PythonStdoutWriter(object):

    def __init__(self, conn):
        self._conn = conn

    def seekable(self):
        return False

    def readable(self):
        return False

    def writable(self):
        return True

    def write(self, data):
        data = data.encode()
        self._conn.send_bytes(data)

    def flush(self):
        pass


class PythonStdinReader(object):
    
    def __init__(self, conn):
        self._conn = conn

    def seekable(self):
        return False

    def writable(self):
        return False

    def readable(self):
        return True

    def read(self, *args, **kwargs):
        data = self._conn.recv_bytes()
        data = data.decode()
        return data

    def read1(self, *args, **kwargs):
        return self.read(*args, **kwargs)

    def readline(self):
        return self.read()


class PythonStdinWriter(object):

    def __init__(self, proc, conn):
        self._proc = proc
        self._conn = conn

    def seekable(self):
        return False

    def writable(self):
        return True

    def readable(self):
        return False

    def write(self, data):
        self._conn.send_bytes(data)

    def flush(self):
        pass


class PythonProcess(object):
    StdinReader = PythonStdinReader
    StdinWriter = PythonStdinWriter
    StdoutReader = PythonStdoutReader
    StdoutWriter = PythonStdoutWriter

    def __init__(self, code):
        self._code = code

        stdin_conn_out, stdin_conn_in = multiprocessing.Pipe(False)
        stdout_conn_out, stdout_conn_in = multiprocessing.Pipe(False)

        self._proc = multiprocessing.Process(
                target=self.run,
        )

        self._stdin_writer = self.StdinWriter(self._proc, stdin_conn_in)
        self._stdin_reader = self.StdinReader(stdin_conn_out)
        self._stdout_reader = self.StdoutReader(self._proc, stdout_conn_out)
        self._stdout_writer = self.StdoutWriter(stdout_conn_in)

        self.stdin = self._stdin_writer
        self.stdout = self._stdout_reader
        self.stderr = self.stdout

        self._proc.daemon = True
        self._proc.start()

    @classmethod
    def from_file(cls, filename):
        with open(filename) as f:
            code = f.read()
        return cls(code)

    def run(self):
        import sys
        sys.stdin = self._stdin_reader
        sys.stdout = self._stdout_writer
        sys.stderr = self._stdout_writer
        namespace = dict()
        try:
            exec(self._code, namespace)
        except SystemExit:
            pass
        except:
            import traceback
            exc = traceback.format_exc()
            self._stdout_writer.write(exc)

    def terminate(self, *args, **kwargs):
        return self._proc.terminate(*args, **kwargs)

    def kill(self, *args, **kwargs):
        return self._proc.kill(*args, **kwargs)

    def close(self):
        try:
            # py3.7+
            self.kill()
        except AttributeError:
            # py2
            self.terminate()
        try:
            self._proc.close()
        except (AttributeError, ValueError):
            # AttributeError may raise on older versions of python.
            # ValueError may raise when trying to close on a running process.
            pass


class NonBlockingPopen(object):

    def __init__(self, args, stdout=None, **kwargs):
        pipe = None
        if stdout == subprocess.PIPE:
            pipe = NonBlockingPipe()
            stdout = pipe.pout

        self._proc = subprocess.Popen(args, stdout=stdout, **kwargs)

        if pipe is not None:
            self.stdout = ProcessReader(self._proc, pipe.pin)

    def __getattr__(self, name):
        return getattr(self._proc, name)

    def close(self):
        try:
            self.kill()
        except OSError:
            pass


class ProcessTerminated(Exception):
    pass


class ProcessReader(object):

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

