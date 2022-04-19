# -*- coding: utf-8 -*-

import io
import threading

import pync


class MockStdin(object):
    '''
    A stdin that never returns EOF.
    This is to prevent the server from
    shutting down prematurely.
    '''

    def read(self, n):
        return None


class Server(threading.Thread):

    def __init__(self):
        super(Server, self).__init__()
        self.daemon = True

        self.stdin = MockStdin()
        self.stdout = io.BytesIO()
        self.stderr = io.StringIO()

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
            
            def next_connection(self):
                ready_event.set()
                return super(NetcatTCPServer, self).next_connection()


        class Netcat(pync.Netcat):
            TCPServer = NetcatTCPServer

        return Netcat

    def run(self):
        pync.pync('-l localhost 8000',
                stdin=self.stdin,
                stdout=self.stdout,
                stderr=self.stderr,
                Netcat=self.Netcat,
        )

