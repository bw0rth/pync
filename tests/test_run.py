# -*- coding: utf-8 -*-

import io
import time
import subprocess

import pytest
import pync


SERVER_PORT = 8000
HELLO_FILE = 'tests/hello.txt'
with open(HELLO_FILE, 'rb') as f:
    HELLO_WORLD = f.read()


@pytest.fixture(scope="session")
def echo_server():
    p = subprocess.Popen(["python", "tests/echo_server.py"])
    time.sleep(1)
    yield p
    p.terminate()


def test_io(echo_server):
    ret = pync.run('-vq -1 localhost {}'.format(SERVER_PORT),
            input=HELLO_WORLD,
            capture_output=True,
    )
    assert ret.returncode == 0
    assert ret.stdout == HELLO_WORLD


def test_bytes_io(echo_server):
    hello = io.BytesIO(HELLO_WORLD)
    ret = pync.run('-vq -1 localhost {}'.format(SERVER_PORT),
            stdin=hello,
            capture_output=True,
    )
    assert ret.returncode == 0
    assert ret.stdout == HELLO_WORLD


def test_file_io(echo_server):
    with open(HELLO_FILE, 'rb') as f:
        ret = pync.run('-vq -1 localhost {}'.format(SERVER_PORT),
               stdin=f,
               capture_output=True, 
        )
    assert ret.returncode == 0
    assert ret.stdout == HELLO_WORLD


def test_pipe_io():
    assert True


def test_subprocess_io():
    assert True
