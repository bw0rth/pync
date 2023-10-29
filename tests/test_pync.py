# -*- coding: utf-8 -*-

import io
import time
import pytest
import pync

SERVER_PORT = 8000
HELLO_WORLD = b'Hello, World!\n'


@pytest.fixture
def echo_server():
    server = pync.Netcat('localhost', SERVER_PORT,
        d=True, l=True, k=True,
        y='import sys; sys.stdout.write(sys.stdin.read())',
    )
    server.start_thread(daemon=True)
    return server


def test_string_io(echo_server):
    ret = pync.run('localhost {}'.format(echo_server.port),
            input=HELLO_WORLD,
            capture_output=True,
    )
    assert ret.returncode == 0
    assert ret.stdout == HELLO_WORLD


def test_file_io(echo_server):
    assert True


def test_pipe_io(echo_server):
    assert True


def test_subprocess_io(echo_server):
    assert True
