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
        CompletedNetcat,
)


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

    :return: Error status code depending on success (0) or failure (>0).
    :rtype: int

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
    """
    result = CompletedNetcat()
    result.returncode = 1
    result.args = args
    result.stdout = None
    result.stderr = None

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
