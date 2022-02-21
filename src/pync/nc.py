# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import argparse
import contextlib
import itertools
import logging
import select
import shlex
import socket
import subprocess
import sys
import time

from .argparsing import GroupingArgumentParser
from .process import NonBlockingProcess, ProcessTerminated
from .conin import NonBlockingConsoleInput

if sys.version_info.major == 2:
    from socket import error as ConnectionRefusedError
    
    class range(object):

        def __init__(self, start, stop, *args, **kwargs):
            self.start = start
            self.stop = stop
            self._rng = xrange(start, stop, *args, **kwargs)

        def __getattr__(self, name):
            return getattr(self._rng, name)

        def __iter__(self):
            return iter(self._rng)


class NetcatContext(object):

    def __init__(self,
            D=False,
            v=False,
            stdin=None, stdout=None, stderr=None, **kwargs):
        self.stdin = stdin or sys.stdin
        self.stdout = stdout or sys.stdout
        self.stderr = stderr or sys.stderr

        self.D = D
        self.v = v

        self._init_kwargs(**kwargs)

    def _init_kwargs(self, **kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    def close(self):
        pass

    def print_verbose(self, message):
        if self.v:
            self.stderr.write(message)

    def print_debug(self, message):
        if self.D:
            self.stderr.write(message)


class NetcatConnection(NetcatContext):

    def __init__(self, sock,
            e=None,
            N=False,
            q=-1,
            **kwargs):
        super(NetcatConnection, self).__init__(**kwargs)

        self.sock = sock
        self.e = e
        self.N = N
        self.q = q
        self.dest, self.port = sock.getpeername()

        if self.dest == '127.0.0.1':
            self.dest = 'localhost'
        self.proto = '*'

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
        command = self.e
        if command:
            return self.execute(command)
        self.readwrite(stdin, stdout, stderr)

    def recv(self, n, blocking=True):
        if blocking:
            return self.sock.recv(n)
        can_read, _, _ = select.select([self.sock], [], [], .002)

        if self.sock in can_read:
            return self.sock.recv(1024)

    def send(self, data):
        self.sock.sendall(data)

    def close(self):
        self.sock.close()

    def shutdown(self, how):
        return self.sock.shutdown(how)

    def readwrite(self, stdin=None, stdout=None, stderr=None, N=None, q=None):
        stdin = stdin or self.stdin
        stdout = stdout or self.stdout
        stderr = stderr or self.stderr

        if stdin is sys.__stdin__ and stdin.isatty():
            stdin = NonBlockingConsoleInput()

        # flag to shutdown socket writes on stdin EOF.
        if N is None:
            N = self.N

        # flag to quit after EOF on stdin.
        if q is None:
            q = self.q

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
                            stdout.buffer.write(net_data)
                        except AttributeError:
                            stdout.write(net_data)
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
                    try:
                        stdin_data = stdin.buffer.read(1024)
                    except AttributeError:
                        stdin_data = stdin.read(1024)
                    if stdin_data:
                        self.send(stdin_data)
                    elif stdin_data is not None:
                        # EOF reached on stdin.
                        # Store the time to calculate time elapsed.
                        eof_reached = time.time()
                        if N:
                            # shutdown socket writes.
                            # Some servers require this to finish their work.
                            try:
                                self.shutdown(socket.SHUT_WR)
                            except OSError:
                                pass
                elif q >= 0:
                    # exit on connection close or q seconds elapsed.
                    eof_elapsed = time.time() - eof_reached
                    if eof_elapsed >= q:
                        # quit after elapsed eof time.
                        break
                # q is a negative number, run loop until end of
                # connection.
            except StopNetcat:
                # IO has requested to stop the readwrite loop.
                break

    def execute(self, cmd):
        proc = Process(cmd)
        self.readwrite(stdin=proc.stdout, stdout=proc.stdin)


class NetcatTCPConnection(NetcatConnection):

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


class NetcatUDPConnection(NetcatConnection):
    
    @classmethod
    def connect(cls):
        pass

    @classmethod
    def listen(cls):
        pass

    def recv(self, *args, **kwargs):
        try:
            return super(NetcatUDPConnection, self).recv(*args, **kwargs)
        except ConnectionRefusedError:
            raise StopNetcat


class ConnectionRefused(ConnectionRefusedError):
    '''
    Same as ConnectionRefusedError but passes back the
    dest and port of the refused connection.
    '''

    def __init__(self, dest, port):
        self.dest = dest
        self.port = port


class NetcatIterator(NetcatContext):

    def _init_kwargs(self, **kwargs):
        self._conn_kwargs = kwargs

    def __iter__(self):
        raise NotImplementedError

    def __next__(self):
        raise NotImplementedError


class NetcatClient(NetcatIterator):
    conn_succeeded = 'Connection to {dest} {port} port [{proto}] succeeded!'
    conn_refused = 'connect to {dest} port {port} failed: Connection refused'

    def __init__(self, dest, port, z=False, **kwargs):
        super(NetcatClient, self).__init__(**kwargs)

        self.dest, self.port = dest, port
        self.z = z
        
        if isinstance(self.port, int):
            # Only one port passed, wrap it in a list
            # for the __iter__ function.
            self.port = [self.port]

        self._iterports = iter(self.port)

    def __iter__(self):
        while True:
            try:
                nc_conn = next(self)
            except StopIteration:
                # No more ports to connect to.
                # Exit loop
                return
            except (ConnectionRefused, socket.error):
                # Move onto next connection if any errors.
                continue

            try:
                if not self.z:
                    yield nc_conn
            finally:
                nc_conn.close()

    def __next__(self):
        # This will raise StopIteration when no more ports.
        port = next(self._iterports)
        return self.create_connection((self.dest, port))

    def run(self):
        for conn in self:
            conn.run()

    def create_connection(self, addr):
        raise NotImplementedError


class NetcatTCPClient(NetcatClient):
    conn_succeeded = 'Connection to {dest} {port} port [tcp/{proto}] succeeded!'
    conn_refused = 'connect to {dest} port {port} (tcp) failed: Connection refused'

    def create_connection(self, addr):
        dest, port = addr
        try:
            sock = socket.create_connection(addr)
        except ConnectionRefusedError:
            self.print_verbose(
                    self.conn_refused.format(
                        dest=dest, port=port,
                    ),
            )
            raise ConnectionRefused(dest, port)
        except socket.error as e:
            self.print_verbose(str(e))
            raise

        nc_conn = NetcatTCPConnection(sock, **self._conn_kwargs)
        self.print_verbose(
                self.conn_succeeded.format(
                    dest=nc_conn.dest,
                    port=nc_conn.port,
                    proto=nc_conn.proto,
                ),
                prefix='',
        )

        if self.z:
            # If zero io mode, close the connection.
            nc_conn.close()
        return nc_conn


class NetcatUDPClient(NetcatClient):
    conn_succeeded = 'Connection to {dest} {port} port [udp/{proto}] succeeded!'
    conn_refused = 'connect to {dest} port {port} (udp) failed: Connection refused'

    def create_connection(self, addr):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(addr)
        nc_conn = NetcatUDPConnection(sock, **self._conn_kwargs)
        if self.z:
            # If zero io mode, close the connection.
            nc_conn.close()
        return nc_conn


class NetcatServer(NetcatIterator):
    
    def __iter__(self):
        while True:
            try:
                nc_conn = next(self)
            except StopIteration:
                return

            try:
                yield nc_conn
            finally:
                nc_conn.close()

    def __next__(self):
        while True:
            try:
                can_read, _, _ = select.select([self.sock], [], [], .002)
            except (ValueError, socket.error):
                # Bad / closed socket.
                # This can occur when the server is closed.
                raise StopIteration
            if self.sock in can_read:
                cli_sock, _ = self.sock.accept()
                nc_conn = self.NetcatConnection(cli_sock, **self._conn_kwargs)
                break
        if not self.k:
            # The "k" option keeps the server open.
            # In this case, "k" is set to False so close the server.
            self.close()
        return nc_conn


class NetcatTCPServer(NetcatIterator):
    listening_msg = 'Listening on [{dest}] (family {fam}, port {port})'
    conn_msg = 'Connection from [{dest}] port {port} [tcp/{proto}] accepted (family {fam}, sport {sport})'

    def __init__(self, port, dest='', k=False, v=False, **kwargs):
        super(NetcatTCPServer, self).__init__(**kwargs)

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

    def __iter__(self):
        while True:
            nc_conn = self.next_connection()
            try:
                yield nc_conn
            finally:
                nc_conn.close()

    def run(self):
        while True:
            try:
                conn = self.next_connection()
            except StopIteration:
                # Server can't accept any more connections.
                break
            try:
                conn.run()
            finally:
                conn.close()

    def next_connection(self):
        while True:
            try:
                can_read, _, _ = select.select([self.sock], [], [], .002)
            except (ValueError, socket.error):
                # Bad / closed socket.
                # This can occur when the server is closed.
                raise StopIteration
            if self.sock in can_read:
                cli_sock, _ = self.sock.accept()
                nc_conn = NetcatTCPConnection(cli_sock, **self._conn_kwargs)
                break
        if not self.k:
            # The "k" option keeps the server open.
            # In this case, "k" is set to False so close the server.
            self.close()
        return nc_conn

    def close(self):
        self.sock.close()


class NetcatUDPServer(NetcatIterator):

    def __init__(self, port, dest='', k=False, v=False, **kwargs):
        super(NetcatUDPServer, self).__init__(**kwargs)
        self.k = k
        self.v = v
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((dest, port))

    def __iter__(self):
        while True:
            nc_conn = self.next_connection()
            try:
                yield nc_conn
            finally:
                nc_conn.close()

    def run(self):
        while True:
            try:
                conn = self.next_connection()
            except StopIteration:
                # Server can't accept any more connections.
                break
            try:
                conn.run()
            finally:
                conn.close()

    def next_connection(self):
        while True:
            try:
                can_read, _, _ = select.select([self.sock], [], [], .002)
            except (ValueError, TypeError):
                # Bad / closed socket.
                # This can occur when the server is closed.
                raise StopIteration
            if self.sock in can_read:
                data, addr = self.sock.recvfrom(1024)
                self.stdout.write(data.decode())
                self.sock.connect(addr)
                nc_conn = NetcatUDPConnection(self.sock, **self._conn_kwargs)
                break
        if not self.k:
            self.sock = None
        return nc_conn

    def close(self):
        pass


class StopNetcat(Exception):
    pass


class Process(NonBlockingProcess):

    def __init__(self, *args, **kwargs):
        super(Process, self).__init__(*args, **kwargs)
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


connect = NetcatTCPConnection.connect
listen = NetcatTCPConnection.listen


def PORT(value):
    # This should always return a range of ports.
    # Even if only one port is given.
    #
    # The port action then turns it into a single port
    # if one port is given or a chain of sorted port
    # ranges if more than one port is given.

    invalid_msg = 'Given value is not a valid port number'
    def valid_port(p):
        # check if port is actually a valid port number.
        return 1 <= p <= 65535

    try:
        # assume port value is a range.
        # e.g 8000-8005
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
        # If more that one is given, sort and chain as one iterator.

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


class Netcat(object):
    ''' Factory class that returns the correct Netcat object based
    on the arguments given. '''
    name = 'pync'

    TCPServer = NetcatTCPServer
    TCPClient = NetcatTCPClient
    TCPConnection = NetcatTCPConnection

    UDPServer = NetcatUDPServer
    UDPClient = NetcatUDPClient
    UDPConnection = NetcatUDPConnection

    def __new__(cls, port, dest='', l=False, u=False, **kwargs):
        if l:
            if u:
                return cls.UDPServer(port, dest=dest, **kwargs)
            else:
                return cls.TCPServer(port, dest=dest, **kwargs)
        else:
            if u:
                return cls.UDPClient(dest, port, **kwargs)
            else:
                return cls.TCPClient(dest, port, **kwargs)

    @classmethod
    def from_args(cls, argv, **kwargs):
        try:
            # Assume args is a string and try to split it.
            argv = shlex.split(argv)
        except AttributeError:
            # args is not a string, assume it's a list.
            pass

        parser = cls.makeparser()
        args = parser.parse_args(argv)
        kwargs.update(vars(args['general arguments']))

        server_args = args['server arguments']
        if server_args.l:
            kwargs.update(vars(server_args))

        return cls(**kwargs)

    @classmethod
    def makeparser(cls):
        parser = GroupingArgumentParser(cls.name,
                usage='''
       {name} [OPTIONS] DEST PORT
       {name} [OPTIONS] -l [DEST] PORT
    '''.lstrip().format(name=cls.name),
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
        parser.add_argument('-k',
                group='server arguments',
                help='Keep inbound sockets open for multiple connects',
                action='store_true',
        )
        parser.add_argument('-l',
                group='server arguments',
                help='Listen mode, for inbound connects',
                action='store_true',
        )
        parser.add_argument('-N',
                help='Shutdown socket on EOF',
                action='store_true',
        )
        parser.add_argument('-e',
                help='Execute a command over the connection',
                metavar='CMD',
        )
        parser.add_argument('-q',
                help='quit after EOF on stdin and delay of SECS',
                metavar='SECS',
                default=-1,
                type=int,
        )
        parser.add_argument('-v',
                help='Verbose',
                action='store_true',
        )
        parser.add_argument('-z',
                group='client arguments',
                help='Zero-I/O mode (useful for scanning)',
                action='store_true',
        )
        parser.add_argument('-u',
                help='UDP mode. [default: TCP]',
                action='store_true',
        )
        return parser


def pync(args, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    nc = Netcat.from_args(args,
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
    )

    try:
        nc.run()
    except KeyboardInterrupt:
        sys.stderr.write('\n')
    finally:
        nc.close()

