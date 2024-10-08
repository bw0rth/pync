# -*- coding: utf-8 -*-

import io

from .netcat import (
        PIPE, STDOUT, QUEUE,
        Netcat, NetcatPopen as Popen,
        NetcatArgumentParser,
        NetcatConnection,
        NetcatClient, NetcatServer,
        NetcatTCPClient, NetcatTCPServer, NetcatTCPConnection,
        NetcatUDPClient, NetcatUDPServer, NetcatUDPConnection,
        NetcatStopReadWrite, ConnectionRefused,
        NetcatConsoleInput,
        NetcatPythonProcess,
        NetcatError,
        readwrite,
)

    
class CompletedNetcat(object):
    """
    A Netcat instance that has finished running.
    This is returned by the :func:`pync.run` function.

    :param args: The args string given to run the Netcat instance.
    :type args: str
    
    :param returncode: The exit code of the Netcat instance.
    :type returncode: int

    :param stdout: The standard output (None if not captured).
    :type stdout: file, optional
    
    :param stderr: The standard error (None if not captured).
    :type stderr: file, optional
    """
    
    def __init__(self, args, returncode, stdout=None, stderr=None):
        self.args = args
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def run(args, stdin=None, stdout=None, stderr=None,
         input=None, capture_output=False, Netcat=Netcat):
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

    :param input: A byte string to use instead of stdin.
    :type input: bytes, optional

    :param capture_output: If set to True, capture output and return it as a file-like object via the :attr:`pync.CompletedNetcat.stdout` attribute. Defaults to "False".
    :type capture_output: bool, optional

    :param Netcat: The class to use for the Netcat instance.
    :type Netcat: :class:`pync.Netcat`

    :return: A :class:`CompletedNetcat` instance.
    :rtype: :class:`pync.CompletedNetcat`

    :Examples:

    .. code-block:: python
       :caption: Create a local TCP server on port 8000.
       
       import pync
       pync.run('-l localhost 8000')

    .. code-block:: python
       :caption: Connect to a local TCP server on port 8000.

       import pync
       pync.run('localhost 8000')

    .. code-block:: python
       :caption: Create a local TCP server to host a file on port 8000.

       import pync
       with open('file.in', 'rb') as f:
           pync.run('-l localhost 8000', stdin=f)

    .. code-block:: python
       :caption: Connect to a local TCP server to download a file on
           port 8000.

       import pync
       with open('file.out', 'wb') as f:
           pync.run('localhost 8000', stdout=f)

    .. code-block:: python
       :caption: Create a local TCP server and send a byte string on port 8000.
       
       import pync
       pync.run('-l localhost 8000', input=b'Hello, World!')

    .. code-block:: python
       :caption: Connect to a local TCP server and capture output to a byte string.
       
       import pync
       result = pync.run('localhost 8000', capture_output=True)
       print(result.stdout.decode())
    """
    result = CompletedNetcat(args, returncode=1)

    stdin_io = stdin or Netcat.stdin
    stdout_io = stdout or Netcat.stdout
    stderr_io = stderr or Netcat.stderr

    if input is not None:
        stdin_io = PIPE

    if capture_output:
        stdout_io = stderr_io = PIPE

    capture_stdout = False
    if stdout_io in (PIPE, QUEUE):
        capture_stdout = True
        stdout_io = io.BytesIO()

    capture_stderr = False
    if stderr_io in (PIPE, QUEUE):
        capture_stderr = True
        stderr_io = io.StringIO()


    class PyncTCPClient(Netcat.TCPClient):
        v_conn_refused = 'pync: ' + Netcat.TCPClient.v_conn_refused

        def _conn_succeeded(self, port):
            super(PyncTCPClient, self)._conn_succeeded(port)
            result.returncode = 0


    class PyncTCPServer(Netcat.TCPServer):

        def _listening(self):
            super(PyncTCPServer, self)._listening()
            result.returncode = 0


    class PyncUDPClient(Netcat.UDPClient):
        v_conn_refused = 'pync: ' + Netcat.UDPClient.v_conn_refused
        
        def _conn_succeeded(self, port):
            super(PyncUDPClient, self)._conn_succeeded(port)
            result.returncode = 0


    class PyncUDPServer(Netcat.UDPServer):

        def _listening(self):
            super(PyncUDPServer, self)._listening()
            result.returncode = 0


    class PyncArgumentParser(Netcat.ArgumentParser):
        prog = 'pync'

        def print_help(self, *args, **kwargs):
            super(PyncArgumentParser, self).print_help(*args, **kwargs)
            result.returncode = 0


    class PyncNetcat(Netcat):
        ArgumentParser = PyncArgumentParser

        TCPClient = PyncTCPClient
        TCPServer = PyncTCPServer
        UDPClient = PyncUDPClient
        UDPServer = PyncUDPServer

        stdin = stdin_io
        stdout = stdout_io
        stderr = stderr_io


    nc = None
    try:
        nc = PyncNetcat.from_args(args)
    except SystemExit:
        pass
    
    if nc is not None:
        try:
            result.stdout, result.stderr = nc.communicate(input)
        except NetcatError as e:
            stderr_io.write('pync: {}\n'.format(e))
            result.returncode = 1
        except KeyboardInterrupt:
            stderr_io.write('\n')
            result.returncode = 130
        finally:
            nc.close()

    if capture_stdout:
        stdout_io.seek(0)
        result.stdout = stdout_io.read()
    if capture_stderr:
        stderr_io.seek(0)
        result.stderr = stderr_io.read()

    return result
