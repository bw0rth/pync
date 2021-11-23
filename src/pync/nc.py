# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import argparse
import itertools
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


def PORT(value):
    # This should always return a range of ports.
    # Even if only one port is given.

    invalid_msg = 'Given value is not a valid port number'
    def valid_port(p):
        return 1 <= p <= 65535

    try:
        # assume port value is a range.
        start_port, end_port = [int(x) for x in value.split('-')]
    except ValueError:
        # port value is not a range.
        value = int(value)
        if not valid_port(value):
            raise ValueError(invalid_msg)
        return range(value, value+1)

    if start_port > end_port:
        start_port, end_port = end_port, start_port

    for p in [start_port, end_port]:
        if not valid_port(p):
            raise ValueError(invalid_msg)

    return range(start_port, end_port+1)


class PortAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        # If one port is given on the command line, set that as value.
        # If more that one is given, set as port iterator.

        if len(values) == 1 and values[0].start == (values[0].stop - 1):
            # Only one port given.
            setattr(namespace, self.dest, values[0].start)
            return

        # sort the list of port ranges.
        sorted_values = sorted(values, key=lambda r: r.start)
        # chain the port ranges into one iter.
        chained_values = itertools.chain(*sorted_values)
        setattr(namespace, self.dest, chained_values)
        return


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
            type=PORT,
            metavar='PORT',
            nargs='+',
            action=PortAction,
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
    parser.add_argument('-v',
            help='Verbose',
            action='store_true',
    )
    parser.add_argument('-z',
            help='Zero-I/O mode [used for scanning]',
            action='store_true',
    )

    def __init__(self, port,    # Port number or range.
            dest='',            # Destination hostname or ip.
            e=None,             # Command to execute through connection.
            k=False,            # Keep the server sock open in listen mode.
            l=False,            # Listen mode.
            q=0,                # Quit after EOF with delay.
            v=False,            # Verbose
            z=False,            # Zero IO mode.
            stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):

        if l:
            # The NetcatTCPServer allows only one port to be given.
            self._connection_iter = NetcatTCPServer(port,
                    dest=dest,
                    k=k,
                    e=e,
                    q=q,
                    v=v,
                    stdin=stdin, stdout=stdout, stderr=stderr,
            )
        else:
            # The NetcatClient allows one port or a range of ports
            # to be passed.
            self._connection_iter = NetcatTCPClient(dest, port,
                    e=e,
                    q=q,
                    v=v,
                    z=z,
                    stdin=stdin, stdout=stdout, stderr=stderr,
            )

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self._connection_iter.close()

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
        kwargs = vars(args)

        return cls(**kwargs)

    def run(self):
        for conn in self:
            conn.run()

    def next_connection(self):
        raise NotImplementedError


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
                        # TODO: Could I move this into the custom Process
                        #       write method? raise StopNetcat
                        #
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

    def __init__(self, dest, port, v=False, z=False,
            stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr,
            **kwargs):
        self.dest, self.port = dest, port
        
        if isinstance(self.port, int):
            # Only one port passed, wrap it in a list
            # for the __iter__ function.
            self.port = [self.port]

        self._iterports = iter(self.port)

        self.v = v
        self.z = z
        self._kwargs = kwargs
        self.stdin, self.stdout, self.stderr = stdin, stdout, stderr

    def __iter__(self):
        while True:
            nc_conn = self.next_connection()
            try:
                if not self.z:
                    yield nc_conn
            finally:
                nc_conn.close()

    def next_connection(self):
        port = next(self._iterports)
        sock = socket.create_connection((self.dest, port))
        return NetcatTCPConnection(sock, **self._kwargs)

    def close(self):
        pass


class NetcatTCPServer:

    def __init__(self, port, dest='', k=False, v=False, **kwargs):
        # First, use "getaddrinfo" to raise a socket error if
        # there are any problems with the given dest and port.
        if dest == '':
            # getaddrinfo doesn't accept an empty string.
            # set to 0.0.0.0 to listen on all interfaces.
            dest = '0.0.0.0'
        if not isinstance(port, int) and not isinstance(port, str):
            # port is not an int or a string.
            # getaddrinfo expects an int or string.
            # All objects have __repr__ so call repr to get string.
            port = repr(port)
        socket.getaddrinfo(dest, port)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((dest, port))
        self.sock.listen(1)
        self.k = k
        self.v = v
        self._kwargs = kwargs

    def __iter__(self):
        while True:
            nc_conn = self.next_connection()
            try:
                yield nc_conn
            finally:
                nc_conn.close()

    def next_connection(self):
        while True:
            try:
                can_read, _, _ = select.select([self.sock], [], [], .002)
            except ValueError:
                # Bad socket.
                raise StopIteration
            if self.sock in can_read:
                cli_sock, _ = self.sock.accept()
                nc_conn = NetcatTCPConnection(cli_sock, **self._kwargs)
                break
        if not self.k:
            # The "k" option keeps the server open.
            # In this case, "k" is set to False so close the server.
            self.close()
        return nc_conn

    def close(self):
        self.sock.close()


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

