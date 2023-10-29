# -*- coding: utf-8 -*-

import io

import pytest

import pync
from .server import PyncServer

SERVER_PORT = 8000
HELLO_WORLD = b'Hello, World!\n'


@pytest.fixture
def server():
    server = PyncServer(port=SERVER_PORT)
    server.start()
    server.ready_event.wait()
    return server


@pytest.fixture
def hello_server():
    server = PyncServer(
            port=SERVER_PORT,
            stdin=io.BytesIO(HELLO_WORLD))
    server.start()
    server.ready_event.wait()
    return server


def test_tcp_upload(server):
    # Connect to the server and send some data.
    ret = pync.run('localhost {}'.format(SERVER_PORT),
            stdin=io.BytesIO(HELLO_WORLD),
            stdout=io.BytesIO(),
            stderr=io.StringIO())
    assert ret.returncode == 0

    server.stdout.seek(0)
    assert server.stdout.read() == HELLO_WORLD


def test_tcp_download(hello_server):
    # Connect to the server and download some data.
    # -d -- Detach from stdin to prevent closing on EOF.
    stdout = io.BytesIO()
    ret = pync.run('-d localhost {}'.format(SERVER_PORT),
            stdout=stdout,
            stderr=io.StringIO())
    assert ret.returncode == 0

    stdout.seek(0)
    assert stdout.read() == HELLO_WORLD

