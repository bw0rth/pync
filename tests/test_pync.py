# -*- coding: utf-8 -*-

import io

from pync import pync
from .server import Server

HELLO_WORLD = b'Hello, World!\n'


def test_tcp_upload():
    # Create test pync server.
    server = Server()
    server.start()

    # Wait until the server is ready to accept
    # a connection.
    server.ready_event.wait()

    # Connect to the server and send some data.
    client_inout = dict(
            stdin=io.BytesIO(HELLO_WORLD),
            stdout=io.BytesIO(),
            stderr=io.StringIO(),
    )
    ret = pync('localhost 8000', **client_inout)
    assert ret == 0

    server.stdout.seek(0)
    assert server.stdout.read() == HELLO_WORLD

