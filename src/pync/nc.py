# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import argparse
import select
import socket
import subprocess
import sys

from .pipe import Pipe
from .conin import ConsoleInput


class NetCat:

    def __init__(self, sock):
        self.socket = sock

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.socket.close()

    @classmethod
    def connect(cls, host, port):
        sock = socket.create_connection((host, port))
        return cls(sock)

    @classmethod
    def listen(cls, host, port):
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
        return cls(sock)

    def sendline(self):
        raise NotImplementedError

    def readlines(self):
        raise NotImplementedError

    def run(self, fin, fout=sys.stdout):
        while True:
            readables, _, _ = select.select([self.socket], [], [], .002)

            if self.socket in readables:
                data = self.socket.recv(1024)
                if not data:
                    break
                data = data.decode()
                fout.write(data)

            data = fin.readline()
            if data:
                try:
                    self.socket.sendall(data)
                except TypeError:
                    self.socket.sendall(data.encode())

    def run_until_eof(self):
        raise NotImplementedError

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
            readables, _, _ = select.select([self.socket], [], [], .002)

            if self.socket in readables:
                # incoming socket data is available.
                data = self.socket.recv(1024)
                if not data:
                    # connection closed.
                    break
                try:
                    # write the data to the commands input.
                    try:
                        proc.stdin.write(data)
                    except TypeError:
                        proc.stdin.write(data.encode())
                    proc.stdin.flush()
                except OSError:
                    # process terminated.
                    break

            # Check if the command has written data to our pipe.
            data = pipe.pin.read(1024)
            if data:
                # Got data from the pipe.
                # Send it over the network.
                try:
                    self.socket.sendall(data)
                except TypeError:
                    self.socket.sendall(data.encode())
            else:
                # No data in the pipe.
                # Check process is still alive.
                if proc.poll() is not None:
                    # process has terminated and we have read all the data.
                    break


connect = NetCat.connect
listen = NetCat.listen


try:
    # py3
    class _ConnRefusedError(ConnectionRefusedError):
        pass
except NameError:
    # py2
    class _ConnRefusedError(Exception):
        pass


def nc(argv):
    prog_name = 'pync'
    parser = argparse.ArgumentParser(prog_name,
            usage='''
       {name} HOST PORT
       {name} -l [HOST] PORT
'''.lstrip().format(name=prog_name),
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

    args = parser.parse_args(argv)
    conin = ConsoleInput(blocking=not args.non_interactive)

    if args.listen:
        # listen for connection.
        # nc.py -l [HOST] PORT
        try:
            with listen(args.host, args.port) as nc:
                nc.run(conin)
        except socket.error:
            pass
        except KeyboardInterrupt:
            pass
    else:
        # connect to server.
        # nc.py HOST PORT
        if not args.host:
            parser.print_help(sys.stderr)
            return 1

        try:
            with connect(args.host, args.port) as nc:
                cmd = args.execute
                if cmd:
                    nc.execute(cmd)
                else:
                    nc.run(conin)
        except ConnectionRefusedError:
            parser.error('connection refused')
            return 1
        except KeyboardInterrupt:
            pass

