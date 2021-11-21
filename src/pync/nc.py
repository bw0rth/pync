# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import argparse
import select
import shlex
import socket
import subprocess
import sys
import time

from .process import NonBlockingProcess, ProcessTerminated
from .conin import NonBlockingConsoleInput


if sys.version_info.major == 2:
    from socket import error as ConnectionRefusedError


class Netcat:
    name = 'pync'
    parser = argparse.ArgumentParser(name,
            usage='''
       {name} [OPTIONS] DEST PORT
       {name} [OPTIONS] -l [DEST] PORT
'''.lstrip().format(name=name),
    )
    parser.add_argument('dest',
            help='The host name or ip to connect or bind to',
            nargs='?',
            default='',
            metavar='DEST',
    )
    parser.add_argument('port',
            help='The port number to connect or bind to',
            type=int,
            metavar='PORT',
    )
    parser.add_argument('-l',
            help='Listen mode, for inbound connects',
            action='store_true',
    )
    parser.add_argument('-e',
            help='Execute a command over the connection',
            metavar='CMD',
    )
    parser.add_argument('-q',
            help='quit after EOF on stdin and delay of SECS',
            metavar='SECS',
    )

    def __init__(self, port,    # Port number or range.
            dest='',            # Destination hostname or ip.
            e=None,             # Command to execute through connection.
            q=0,                # Quit after EOF with delay.
            l=False,            # Listen mode.
            k=False,            # Keep the server sock open in listen mode.
            stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):

        if l:
            self._connection_iter = NetcatTCPServer(port,
                    dest=dest,
                    k=k,
                    e=e,
                    q=q,
                    stdin=stdin, stdout=stdout, stderr=stderr,
            )
        else:
            self._connection_iter = NetcatTCPClient(dest, port,
                    e=e,
                    q=q,
                    stdin=stdin, stdout=stdout, stderr=stderr,
            )

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def __iter__(self):
        '''Yield NetcatConnection objects'''
        return iter(self._connection_iter)

    @classmethod
    def from_args(cls, args):
        try:
            # Assume args is a string and try and split it.
            args = shlex.split(args)
        except AttributeError:
            # args is not a string, assume it's a list.
            pass
        args = cls.parser.parse_args(args)

        return cls(**vars(args))

    def run(self):
        for conn in self:
            conn.run()


class NetcatTCPConnection:

    def __init__(self, sock,
            e=None,
            q=0,
            stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
        self.sock = sock
        self.command = e
        self.q = q
        self.stdin, self.stdout, self.stderr = stdin, stdout, stderr

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    @classmethod
    def connect(cls, host, port, **kwargs):
        sock = socket.create_connection((host, port))
        return cls(sock, **kwargs)

    @classmethod
    def listen(cls, host, port, **kwargs):
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((host, port))
        server_sock.listen(1)

        # ctrl-c interrupt doesn't seem to break out of server accept.
        # So using select for non-blocking server accept.
        while True:
            readables, _, _ = select.select([server_sock], [], [], .002)
            if server_sock in readables:
                sock, _ = server_sock.accept()
                break

        server_sock.close()
        return cls(sock, **kwargs)

    def run(self, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
        if self.command:
            return self.execute(self.command)
        self.readwrite(stdin, stdout, stderr)

    def recv(self, n, blocking=True):
        if blocking:
            return self.sock.recv(n)
        can_read, _, _ = select.select([self.sock], [], [], .002)

        if self.sock in can_read:
            return self.sock.recv(1024)

    def send(self, data):
        try:
            self.sock.sendall(data)
        except TypeError:
            self.sock.sendall(data.encode())

    def close(self):
        self.sock.close()

    def readwrite(self, stdin=None, stdout=None, stderr=None, q=None):
        q = self.q if q is None else q
        stdin = stdin or self.stdin
        stdout = stdout or self.stdout
        stderr = stderr or self.stderr

        if stdin is sys.__stdin__ and stdin.isatty():
            stdin = NonBlockingConsoleInput()

        eof_reached = None
        eof_elapsed = None

        # (     )
        #   O O
        while(1<2):
            try:
                net_data = self.recv(1024, blocking=False)
                if net_data:
                    try:
                        try:
                            stdout.write(net_data)
                        except TypeError:
                            try:
                                stdout.write(net_data.encode())
                            except AttributeError:
                                stdout.write(net_data.decode())
                        stdout.flush()
                    except OSError:
                        # process terminated.
                        break
                else:
                    if net_data is not None:
                        # connection lost.
                        break

                if not eof_reached:
                    stdin_data = stdin.read(1024)
                    if stdin_data:
                        self.send(stdin_data)
                    else:
                        if stdin_data is not None:
                            # EOF reached on stdin.
                            # Store the time to calculate time elapsed.
                            eof_reached = time.time()
                # if q is a negative value, ignore EOF.
                elif q >= 0:
                    eof_elapsed = time.time() - eof_reached
                    if eof_elapsed >= q:
                        # quit after elapsed eof time.
                        break
            except StopNetcat:
                # IO has requested to stop the readwrite loop.
                break

    def execute(self, cmd):
        proc = Process(cmd)
        self.readwrite(stdin=proc.stdout, stdout=proc.stdin)


class NetcatTCPClient:

    def __init__(self, dest, port, **kwargs):
        self.dest, self.port = dest, port
        self._kwargs = kwargs

    def __iter__(self):
        '''
        Multiple client connects may occur when port range
        is given.
        '''
        for p in self.port:
            nc_conn = self.next_connection()
            try:
                yield nc_conn
            finally:
                nc_conn.close()

    def next_connection(self):
        sock = socket.create_connection((self.dest, self.port))
        return NetcatTCPConnection(sock, **self._kwargs)


class NetcatTCPServer:

    def __init__(self, port, dest='', k=False, **kwargs):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((dest, port))
        self.sock.listen(1)
        self.k = k
        self._kwargs = kwargs

    def __iter__(self):
        '''
        Multiple client connects may occur when the "k" option
        is given.
        '''
        nc_conn = self.next_connection()
        try:
            yield nc_conn
        finally:
            nc_conn.close()

        if not self.k:
            self.sock.close()
            return

        while True:
            nc_conn = self.next_connection()
            try:
                yield nc_conn
            finally:
                nc_conn.close()

    def next_connection(self):
        while True:
            can_read, _, _ = select.select([self.sock], [], [], .002)
            if self.sock in can_read:
                cli_sock, _ = self.sock.accept()
                return NetcatTCPConnection(cli_sock, **self._kwargs)


class StopNetcat(Exception):
    pass


class Process(NonBlockingProcess):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stdout = _ProcStdout(self.stdout)


class _ProcStdout:

    def __init__(self, stdout):
        self._stdout = stdout

    def __getattr__(self, name):
        return getattr(self._stdout, name)

    def read(self, n):
        try:
            return self._stdout.read(n)
        except ProcessTerminated:
            raise StopNetcat


pync = Netcat.from_args
connect = NetcatTCPConnection.connect
listen = NetcatTCPConnection.listen

