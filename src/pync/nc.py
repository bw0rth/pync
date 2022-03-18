# -*- coding: utf-8 -*-

"""
pync - arbitrary TCP and UDP connections and listens (Netcat for Python).
"""

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
    D = False
    v = False
    stdin = sys.stdin
    stdout = sys.stdout
    stderr = sys.stderr

    def __init__(self,
            D=None,
            v=None,
            stdin=None, stdout=None, stderr=None, **kwargs):

        if D is not None:
            self.D = D
        if v is not None:
            self.v = v

        self.stdin = stdin or self.stdin
        self.stdout = stdout or self.stdout
        self.stderr = stderr or self.stderr

        self._init_kwargs(**kwargs)

    def _init_kwargs(self, **kwargs):
        if kwargs:
            raise ValueError(kwargs)

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    def close(self):
        pass

    def print_verbose(self, message):
        if self.v:
            self.stderr.write(message+'\n')
            self.stderr.flush()

    def print_debug(self, message):
        if self.D:
            self.stderr.write(message+'\n')
            self.stderr.flush()


class NetcatConnection(NetcatContext):
    """
    Wraps a socket object to provide Netcat-like functionality.

    :param e: A string containing a process command to run and attach to the
        Netcat i_o.
    :type e: str

    :param N: Set to True to shutdown socket writes after EOF on stdin.
        Some servers require this to perform properly.
    :type N: bool

    :param q: Quit the readwrite loop after EOF on stdin and delay of secs.
    :type q: int

    You can use sub-classes of this class as a context manager using the "with" statement:

    .. code-block:: python

       with NetcatConnection(...) as nc:
           nc.run()

    If you choose not to use the "with" statement, please make sure to use
    the close() method after use:

    .. code-block:: python

       nc = NetcatConnection(...)
       nc.run()
       nc.close()
    """

    e = None
    N = False
    q = -1

    def __init__(self, sock,
            e=None,
            N=None,
            q=None,
            **kwargs):
        super(NetcatConnection, self).__init__(**kwargs)

        self.sock = sock

        if e is not None:
            self.e = e
        if N is not None:
            self.N = N
        if q is not None:
            self.q = q

        self.dest, self.port = sock.getpeername()
        if self.dest == '127.0.0.1':
            self.dest = 'localhost'
        self.proto = '*'

    @classmethod
    def connect(cls, dest, port, **kwargs):
        """
        Factory method to connect to a server and return a NetcatConnection
        instance.
        This method should be implemented by a sub-class.

        :param dest: The destination hostname or IP address to connect to.
        :type dest: str

        :param port: The port number to connect to.
        :type port: int

        :param kwargs: Any other keyword arguments get passed to __init__.

        :returns: Returns a subclass of :class:`pync.NetcatConnection` once
            a connection has been established.
        :rtype: :class:`pync.NetcatConnection`

        :Example:

        .. code-block:: python

           with NetcatConnection.connect('localhost', 8000) as conn:
               conn.run()
        """
        raise NotImplementedError

    @classmethod
    def listen(cls, dest, port, **kwargs):
        """
        Factory method to listen for a connection and return a NetcatConnection
        instance.
        This method should be implemented by a sub-class.

        :param dest: The hostname or IP address to bind to.
        :type dest: str

        :param port: The port number to bind to.
        :type port: int

        :param kwargs: Any other keyword arguments get passed to __init__.

        :returns: Returns a subclass of :class:`pync.NetcatConnection` once a
            connection has been established.
        :rtype: :class:`pync.NetcatConnection`

        :Example:

        .. code-block:: python

           with NetcatConnection.listen('localhost', 8000) as conn:
               conn.run()
        """
        raise NotImplementedError

    def run(self, **kwargs):
        """
        This method runs Netcat respecting all arguments that have been passed.

        :param kwargs: Any keyword arguments are passed to readwrite.

        :Example:

        .. code-block:: python
           
           with NetcatConnection(sock) as nc:
               nc.run()
        """
        command = self.e
        if command:
            return self.execute(command)
        self.readwrite(**kwargs)

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
        """
        The main loop to read and write i_o.
        Read from stdin and send to network.
        Receive from network and write to stdout.
        Write verbose/debug/error messages to stderr.

        :param stdin: A file-like object to read outgoing network data from.
        :type stdin: file, optional
        
        :param stdout: A file-like object to write incoming network data to.
        :type stdout: file, optional

        :param stderr: A file-like object to write verbose/debug/error messages
            to.
        :type stderr: file, optional

        :param N: Set to True to shutdown socket writes after EOF is reached
            on stdin.
            This will inform the other end of the connection that no more
            data will be sent.
        :type N: bool

        :param q: If set to a positive <number>, quit the readwrite loop after EOF
            and <number> of seconds has elapsed.
            If set to a negative number, readwrite until connection closes.
        :type q: int

        :Example:

        .. code-block:: python

           # Set the "q" option to 0 to quit the readwrite loop after EOF
           # on stdin.
           with NetcatConnection(sock, q=0) as nc:
               nc.readwrite(stdin=file1)
               # Set the "N" option to inform the other end of the connection
               # that we have no more data to send after EOF on file2.
               nc.readwrite(stdin=file2, N=True)
        """
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
                        #       write method? raise StopReadWrite
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
            except StopReadWrite:
                # IO has requested to stop the readwrite loop.
                break

    def execute(self, cmd):
        """
        Execute a command and connect i_o to the Netcat connection.

        :param cmd: A string or list containing the command and any
            arguments to run.
        :type cmd: str, list

        :Example:

        .. code-block:: python

           with NetcatConnection(sock) as nc:
               nc.execute('echo "Hello, World!"')
        """
        proc = Process(cmd)
        self.readwrite(stdin=proc.stdout, stdout=proc.stdin)


class NetcatTCPConnection(NetcatConnection):
    """
    Wraps a TCP socket to provide Netcat-like functionality.
    """

    @classmethod
    def connect(cls, dest, port, **kwargs):
        """
        Factory method to connect to a TCP server and return a
        :class:`pync.NetcatTCPConnection` object.

        :param dest: The destination hostname or IP address to connect to.
        :type dest: str

        :param port: The port number to connect to.
        :type port: int

        :param kwargs: Any other keyword arguments get passed to __init__.

        :rtype: :class:`pync.NetcatTCPConnection`

        :Example:

        .. code-block:: python
           
           from pync import NetcatTCPConnection
           with NetcatTCPConnection.connect('localhost', 8000) as conn:
               conn.run()
        """
        sock = socket.create_connection((dest, port))
        return cls(sock, **kwargs)

    @classmethod
    def listen(cls, dest, port, **kwargs):
        """
        Factory method to listen for an incoming TCP connection and
        return a :class:`pync.NetcatTCPConnection` object.

        :param dest: The destination hostname or IP address to bind to.
        :type dest: str

        :param port: The port number to bind to.
        :type port: int

        :param kwargs: Any other keyword arguments get passed to __init__.

        :rtype: :class:`pync.NetcatTCPConnection`

        :Example:

        .. code-block:: python

           from pync import NetcatTCPConnection
           with NetcatTCPConnection.listen('localhost', 8000) as conn:
               conn.run()
        """
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((dest, port))
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
    """
    Wraps a UDP socket object to provide Netcat-like functionality.
    """
    
    @classmethod
    def connect(cls, dest, port, **kwargs):
        """
        :TODO:
        """
        # TODO
        raise NotImplementedError

    @classmethod
    def listen(cls, dest, port, **kwargs):
        """
        :TODO:
        """
        raise NotImplementedError

    def recv(self, *args, **kwargs):
        try:
            return super(NetcatUDPConnection, self).recv(*args, **kwargs)
        except ConnectionRefusedError:
            raise StopReadWrite


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
    """
    A Netcat client is iterable.
    You can pass one or more ports and iterate through
    each :class:`pync.NetcatConnection`.

    :param dest: The destination hostname or IP address to connect to.
    :type dest: str

    :param port: The port number(s) to connect to.
    :type port: int, list(int)

    :param z: Set to True to turn Zero i_o on (connect then close).
        Useful for simple port scanning.
    :type z: bool, optional

    You can use sub-classes of this class as a context manager using the "with" statement:

    .. code-block:: python

       with NetcatClient(...) as nc:
           nc.run()

    If you choose not to use the "with" statement, please make sure to use
    the close() method after use:

    .. code-block:: python

       nc = NetcatClient(...)
       nc.run()
       nc.close()

    :Example:

    .. code-block:: python
       :caption: We can connect to multiple ports one after another by passing
           a list of ports.

       with NetcatClient('localhost', [8000, 8001]) as nc:
           for connection in nc:
               connection.run()

    .. code-block:: python
       :caption: Using the "z" and "v" options, we can perform a simple port scan.

       with NetcatClient('localhost', [8000, 8002], z=True, v=True) as nc:
           nc.run()
    """

    conn_succeeded = 'Connection to {dest} {port} port [{proto}] succeeded!'
    conn_refused = 'connect to {dest} port {port} failed: Connection refused'
    z = False

    def __init__(self, dest, port, z=None, **kwargs):
        super(NetcatClient, self).__init__(**kwargs)

        self.dest, self.port = dest, port
        if z is not None:
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
        return self._create_connection((self.dest, port))

    def run(self):
        """
        Convenience method to run each :class:`pync.NetcatConnection` one after another.

        :Example:

        .. code-block:: python

           with NetcatClient('localhost', [8000, 8001]) as nc:
               nc.run()
        """
        for conn in self:
            conn.run()

    def _create_connection(self, addr):
        raise NotImplementedError


class NetcatTCPClient(NetcatClient):
    """
    A :class:`pync.NetcatClient` for the Transmission Control Protocol.
    """

    conn_succeeded = 'Connection to {dest} {port} port [tcp/{proto}] succeeded!'
    conn_refused = 'connect to {dest} port {port} (tcp) failed: Connection refused'

    def _create_connection(self, addr):
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
        )

        if self.z:
            # If zero io mode, close the connection.
            nc_conn.close()
        return nc_conn


class NetcatUDPClient(NetcatClient):
    """
    A :class:`pync.NetcatClient` for the User Datagram Protocol.
    """

    conn_succeeded = 'Connection to {dest} {port} port [udp/{proto}] succeeded!'
    conn_refused = 'connect to {dest} port {port} (udp) failed: Connection refused'

    def _create_connection(self, addr):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(addr)
        nc_conn = NetcatUDPConnection(sock, **self._conn_kwargs)
        if self.z:
            # If zero io mode, close the connection.
            nc_conn.close()
        return nc_conn


class NetcatServer(NetcatIterator):
    """
    A Netcat server is an iterable.
    You can iterate through each incoming connection.

    :param port: The port number to bind the server to.
    :type port: int

    :param dest: The hostname or IP address to bind the server to.
    :type dest: str

    :param k: Set to True to keep the server open between connections.
    :type k: bool

    :param kwargs: Any other keyword arguments get passed to each
        connection.

    You can use sub-classes of this class as a context manager using the "with" statement:

    .. code-block:: python

       with NetcatServer(...) as nc:
           nc.run()

    If you don't use the "with" statement, please make sure to use the
    close() method after use:

    .. code-block:: python
       
       nc = NetcatServer(...)
       nc.run()
       nc.close()

    :Example:

    .. code-block:: python
       :caption: Use the "k" option to keep the server open and iterate
           through each :class:`pync.NetcatConnection`.

       with NetcatServer(8000, dest='localhost', k=True) as nc:
           for connection in nc:
               connection.execute('echo "Hello, World!"')
    """

    k = False
    address_family = None
    socket_type = None
    Connection = None

    def __init__(self, port, dest='', k=None, **kwargs):
        super(NetcatServer, self).__init__(**kwargs)
        bind_and_activate = True

        self.dest = dest
        if dest == '':
            # getaddrinfo doesn't accept an empty string.
            # set to 0.0.0.0 to listen on all interfaces.
            self.dest = '0.0.0.0'

        self.port = port
        if not isinstance(port, int) and not isinstance(port, str):
            # port is not an int or a string.
            # getaddrinfo expects an int or string.
            # All objects have __repr__ so call repr to get string.
            self.port = repr(port)

        if k is not None:
            self.k = k

        self.sock = socket.socket(self.address_family, self.socket_type)

        if bind_and_activate:
            try:
                self._server_bind()
                self._server_activate()
            except:
                self._server_close()
                raise

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
                cli_sock, _ = self._get_request()
                nc_conn = self.Connection(cli_sock, **self._conn_kwargs)
                break
        if not self.k:
            # The "k" option keeps the server open.
            # In this case, "k" is set to False so close the server.
            self.close()
        return nc_conn

    def run(self):
        """
        Convenience method to run each :class:`pync.NetcatConnection` one
        after another.

        :Example:

        .. code-block:: python

           with NetcatServer(8000, dest='localhost', k=True) as nc:
               nc.run()
        """
        for conn in self:
            conn.run()

    def _server_bind(self):
        raise NotImplementedError

    def _server_activate(self):
        pass

    def _server_close(self):
        self.sock.close()

    def _get_request(self):
        raise NotImplementedError

    def close(self):
        """
        Close the server.
        """
        self._server_close()


class NetcatTCPServer(NetcatServer):
    """
    A :class:`pync.NetcatServer` for the Transmission Control Protocol.
    """

    listening_msg = 'Listening on [{dest}] (family {fam}, port {port})'
    conn_msg = 'Connection from [{dest}] port {port} [tcp/{proto}] accepted (family {fam}, sport {sport})'
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = 1
    Connection = NetcatTCPConnection

    def _server_bind(self):
        # This should raise any errors if problems with dest and port.
        socket.getaddrinfo(self.dest, self.port)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.dest, self.port))

    def _server_activate(self):
        self.sock.listen(self.request_queue_size)

    def _get_request(self):
        return self.sock.accept()


class NetcatUDPServer(NetcatServer):
    """
    A :class:`pync.NetcatServer` for the User Datagram Protocol.
    """

    address_family = socket.AF_INET
    socket_type = socket.SOCK_DGRAM
    max_packet_size = 8192
    Connection = NetcatUDPConnection

    def _server_close(self):
        pass

    def _get_request(self):
        data, addr = self.sock.recvfrom(self.max_packet_size)
        self.stdout.write(data.decode())
        self.sock.connect(addr)
        return self.sock, addr


class StopReadWrite(Exception):
    """
    """


class Process(NonBlockingProcess):
    """
    """

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
            raise StopReadWrite


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
    """
    Factory class that returns the correct Netcat object based
    on the arguments given.

    :param port: The port number to connect or bind to depending on the "l" parameter.
    :type port: int, list(int)

    :param dest: The IP address or hostname to connect or bind to depending
        on the "l" parameter.
    :type dest: str, optional

    :param l: Set to True to create a server and listen for incoming connections.
    :type l: bool, optional

    :param u: Set to True to use UDP for transport instead of the default TCP.
    :type u: bool, optional

    :param kwargs: All other keyword arguments get passed to the underlying
        Netcat class.

    You can use this class as a context manager using the "with" statement:

    .. code-block:: python

       with Netcat(...) as nc:
           nc.run()

    If you use it without the "with" statement, please make sure to use the
    close method after use:

    .. code-block:: python

       nc = Netcat(...)
       nc.run()
       nc.close()

    :Examples:

    .. code-block:: python
       :caption: Use the "l" option to create a :class:`pync.NetcatTCPServer`
           object.

       from pync import Netcat
       with Netcat(8000, dest='localhost', l=True) as nc:
           nc.run()

    .. code-block:: python
       :caption: By default, without the "l" option, Netcat will return a
           :class:`pync.NetcatTCPClient` object.

       from pync import Netcat
       with Netcat(8000, dest='localhost') as nc:
           nc.run()

    .. code-block:: python
       :caption: Create a :class:`pync.NetcatUDPServer` with the "u" and "l" options.

       from pync import Netcat
       with Netcat(8000, dest='localhost', l=True, u=True) as nc:
           nc.run()

    .. code-block:: python
       :caption: And a :class:`pync.NetcatUDPClient` using only the "u" option.

       from pync import Netcat
       with Netcat(8000, dest='localhost', u=True) as nc:
           nc.run()

    .. code-block:: python
       :caption: Any other keyword arguments get passed to the underlying Netcat class.

       from pync import Netcat
       # Use the "k" option to keep the server open between connections.
       with Netcat(8000, dest='localhost', l=True, k=True) as nc:
           for connection in nc:
               connection.execute('echo "Hello, World!"')

    .. code-block:: python
       :caption: Pass a list of ports to connect to one after the other.

       # Simple port scan example.
       from pync import Netcat
       # Use the "z" option to turn Zero i_o on (connect then close).
       # Use the "v" option to turn verbose output on to see connection success or failure.
       with Netcat([8000, 8003, 8002], dest='localhost', z=True, v=True) as nc:
           for connection in nc:
               connection.run()
    """

    name = 'pync'
    description = 'pync - arbitrary TCP and UDP connections and listens (Netcat for Python).'

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
    def from_args(cls, args,
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr):
        """
        Create a Netcat object from command-line arguments instead of keyword
        arguments.

        :param args: A string containing the command-line arguments to create
            the Netcat instance with.
        :type args: str

        :param stdin: A file-like object to read outgoing network data from.
        :type stdin: file, optional

        :param stdout: A file-like object to write incoming network data to.
        :type stdout: file, optional

        :param stderr: A file-like object to write verbose/debug/error messages to.
        :type stderr: file, optional

        :Example:

        .. code-block:: python

           from pync import Netcat
           with Netcat.from_args('-l localhost 8000') as nc:
               nc.run()
        """

        try:
            # Assume args is a string and try to split it.
            args = shlex.split(args)
        except AttributeError:
            # args is not a string, assume it's a list.
            pass

        parser = cls.makeparser()
        parsed_args = parser.parse_args(args)

        general_args = parsed_args['general arguments']
        client_args = parsed_args['client arguments']
        server_args = parsed_args['server arguments']

        kwargs = dict()
        kwargs.update(vars(general_args))
        if server_args.l:
            kwargs.update(vars(server_args))
        else:
            kwargs.update(vars(client_args))

        return cls(**kwargs)

    @classmethod
    def makeparser(cls):
        parser = GroupingArgumentParser(cls.name,
                description=cls.description,
                usage='''
       {name} [OPTIONS] DEST PORT
       {name} [OPTIONS] -l [DEST] PORT
    '''.strip().format(name=cls.name),
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
        parser.add_argument('-D',
                help='Enable debugging output to stderr',
                action='store_true',
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
    """
    Create and run a Netcat instance.
    This is similar to running **pync** from the command-line.

    :param args: A string containing command-line arguments.
    :type args: str

    :param stdin: A file-like object to read outgoing network data from.
    :type stdin: file, optional

    :param stdout: A file-like object to write incoming network data to.
    :type stdout: file, optional

    :param stderr: A file-like object to write error/verbose/debug messages to.
    :type stderr: file, optional

    :return: Error status code depending on success (0) or failure (>0).
    :rtype: int

    :Examples:

    .. code-block:: python
       :caption: Create a local TCP server on port 8000.
       
       from pync import pync
       pync('-l localhost 8000')

    .. code-block:: python
       :caption: Connect to a local TCP server on port 8000.

       from pync import pync
       pync('localhost 8000')

    .. code-block:: python
       :caption: Create a local TCP server to host a file on port 8000.

       from pync import pync
       with open('file.in', 'rb') as f:
           pync('-l localhost 8000', stdin=f)

    .. code-block:: python
       :caption: Connect to a local TCP server to download a file on
           port 8000.

       from pync import pync
       with open('file.out', 'wb') as f:
           pync('localhost 8000', stdout=f)
    """

    try:
        nc = Netcat.from_args(args,
                stdin=stdin,
                stdout=stdout,
                stderr=stderr,
        )
    except socket.error as e:
        # NetcatServer may raise a socket error on bad address.
        stderr.write('pync: {}\n'.format(e))
        return 1

    try:
        nc.run()
    except KeyboardInterrupt:
        nc.stderr.write('\n')
    finally:
        nc.close()

