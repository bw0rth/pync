# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import argparse
import select
import shlex
import socket
import subprocess
import sys

from .pipe import Pipe
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

    def __init__(self, sock, cmd=None, fin=sys.stdin, fout=sys.stdout,
            ferr=sys.stderr):
        self.socket = sock
        self.command = cmd
        self.fin, self.fout, self.ferr = fin, fout, ferr

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

    def run(self, fin=sys.stdin, fout=sys.stdout, ferr=sys.stderr):
        if self.command:
            return self.execute(self.command)
        self.readwrite(fin, fout, ferr)

    def readwrite(self, fin=None, fout=None, ferr=None, until_eof=False):
        fin = fin or self.fin
        fout = fout or self.fout
        ferr = ferr or self.ferr

        if fin is sys.__stdin__ and fin.isatty():
            fin = ConsoleInput()

        while True:
            net_data = self.recv(1024, blocking=False)
            if net_data:
                fout.write(net_data.decode())
            else:
                if net_data is not None:
                    # connection lost.
                    break

            fin_data = fin.read(1024)
            if fin_data:
                self.send(fin_data)
            else:
                if fin_data is not None and until_eof:
                    # All input data is read (EOF).
                    break

    def execute(self, cmd):
        # setup the non-blocking pipe.
        # We don't want it to wait when there's nothing to read.
        pipe = Pipe()
        if not pipe.pin.set_nowait():
            raise RuntimeError('Unable to create non-blocking pipe.')

        proc = subprocess.Popen(cmd, shell=True,
                stdin=subprocess.PIPE,
                stdout=pipe.pout.fileno(),
                stderr=subprocess.STDOUT,
        )

        # Any incoming socket data goes to the commands standard input.
        # socket -> proc.stdin

        # The command writes all its output to our pipe's output.
        # (proc.stderr | proc.stdout) -> pipe.pout

        # Any data that the command has written to our pipe's output
        # will be read from our pipe's input and sent over the socket.
        # pipe.pin -> socket

        # (     )
        #   O O
        while(1<2):
            net_data = self.recv(1024, blocking=False)
            if net_data:
                try:
                    # write the data to the commands input.
                    try:
                        proc.stdin.write(net_data)
                    except TypeError:
                        proc.stdin.write(net_data.encode())
                    proc.stdin.flush()
                except OSError:
                    # process terminated.
                    break

            # Check if the command has written data to our pipe.
            proc_data = pipe.pin.read(1024)
            if proc_data:
                # Got data from the pipe.
                # Send it over the network.
                self.send(proc_data)
            else:
                # No data in the pipe.
                # Check process is still alive.
                if proc.poll() is not None:
                    # process has terminated and we have read all the data.
                    break

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


pync = Netcat.from_args
connect = Netcat.connect
listen = Netcat.listen

