# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import argparse
import select
import shlex
import socket
import subprocess
import sys

from .pipe import Pipe
from .process import Process, ProcessTerminated
from .conin import ConsoleInput


if sys.version_info.major == 2:
    from socket import error as ConnectionRefusedError


class Netcat:
    name = 'pync'
    parser = argparse.ArgumentParser(name,
            usage='''
       {name} HOST PORT
       {name} -l [HOST] PORT
'''.lstrip().format(name=name),
    )
    parser.add_argument('host',
            help='The host name or ip to connect or bind to.',
            nargs='?',
            default='',
            metavar='HOST',
    )
    parser.add_argument('port',
            help='The port number to connect or bind to.',
            type=int,
            metavar='PORT',
    )
    parser.add_argument('--listen', '-l',
            help='Listen for a connection on the given port.',
            action='store_true',
    )
    parser.add_argument('--non-interactive', '-I',
            help='Do not accept user input.',
            action='store_true',
    )
    parser.add_argument('--execute', '-e',
            help='Execute a command over the connection.',
            metavar='CMD',
    )

    def __init__(self, sock, cmd=None, stdin=sys.stdin, stdout=sys.stdout,
            stderr=sys.stderr):
        self.socket = sock
        self.command = cmd
        self.stdin, self.stdout, self.stderr = stdin, stdout, stderr

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.socket.close()

    @classmethod
    def from_args(cls, args):
        try:
            # Assume args is a string and try and split it.
            args = shlex.split(args)
        except AttributeError:
            # args is not a string, assume it's a list.
            pass
        args = cls.parser.parse_args(args)

        if args.listen:
            nc = cls.listen(args.host, args.port,
                    cmd=args.execute,
            )
        else:
            nc = cls.connect(args.host, args.port,
                    cmd=args.execute,
            )

        return nc

    @classmethod
    def connect(cls, host, port, *args, **kwargs):
        sock = socket.create_connection((host, port))
        return cls(sock, *args, **kwargs)

    @classmethod
    def listen(cls, host, port, *args, **kwargs):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(1)

        # ctrl-c interrupt doesn't seem to break out of server accept.
        # So using select for non-blocking server accept.
        while True:
            readables, _, _ = select.select([server], [], [], .002)
            if server in readables:
                sock, _ = server.accept()
                break

        server.close()
        return cls(sock, *args, **kwargs)

    def run(self, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
        if self.command:
            return self.execute(self.command)
        self.readwrite(stdin, stdout, stderr)

    def recv(self, n, blocking=True):
        if blocking:
            return self.socket.recv(n)
        readables, _, _ = select.select([self.socket], [], [], .002)

        if self.socket in readables:
            return self.socket.recv(1024)

    def send(self, data):
        try:
            self.socket.sendall(data)
        except TypeError:
            self.socket.sendall(data.encode())

    def readwrite(self, stdin=None, stdout=None, stderr=None, until_eof=False):
        stdin = stdin or self.stdin
        stdout = stdout or self.stdout
        stderr = stderr or self.stderr

        if stdin is sys.__stdin__ and stdin.isatty():
            stdin = ConsoleInput()

        # (     )
        #   O O
        while(1<2):
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

            try:
                stdin_data = stdin.read(1024)
            except ProcessTerminated:
                break

            if stdin_data:
                self.send(stdin_data)
            else:
                if stdin_data is not None and until_eof:
                    # All input data is read (EOF).
                    break

    def execute(self, cmd):
        proc = Process(cmd)
        self.readwrite(stdin=proc.stdout, stdout=proc.stdin)


pync = Netcat.from_args
connect = Netcat.connect
listen = Netcat.listen

