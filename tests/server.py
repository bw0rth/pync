# -*- coding: utf-8 -*-

import io
import threading

import pync


class PyncServer(threading.Thread):
    port = 8000

    def __init__(self, port=None, stdin=None, stdout=None, stderr=None):
        super(PyncServer, self).__init__()
        self.daemon = True

        if port is not None:
            self.port = port

        self.stdin = None
        self.stdout = io.BytesIO()
        self.stderr = io.StringIO()

        if stdin is not None:
            self.stdin = stdin
        if stdout is not None:
            self.stdout = stdout
        if stderr is not None:
            self.stderr = stderr

        self.d = False
        if self.stdin is None:
            self.d = True

        self.ready_event = threading.Event()
        self.Netcat = self._create_netcat(self.ready_event)

    def _create_netcat(self, ready_event):
        '''
        Create a Netcat class that sets an event
        before waiting for a connection.
        This is to make sure the server is ready
        before connecting to it with the client.
        '''

        class NetcatTCPServer(pync.NetcatTCPServer):

            def _listening(self):
                super(NetcatTCPServer, self)._listening()
                ready_event.set()


        class Netcat(pync.Netcat):
            TCPServer = NetcatTCPServer

        return Netcat

    def run(self):
        # -d -- Detach from stdin to prevent server from closing on EOF.
        # -l -- Server mode.
        args = '-l localhost {}'.format(self.port)
        if self.d:
            args = '-d ' + args
        pync.run(args,
                stdin=self.stdin,
                stdout=self.stdout,
                stderr=self.stderr,
                Netcat=self.Netcat,
        )

