# -*- coding: utf-8 -*-

import argparse
import sys
from pync import pync, ConsoleInput


try:
    # py2
    input = raw_input
except NameError:
    # py3
    pass


class ChatInput(ConsoleInput):

    def __init__(self, username, *args, **kwargs):
        super(ChatInput, self).__init__(*args, **kwargs)
        self.username = username
        self.prompt = 'You: '
        self._lines = [
                "Chat started with user [{}]".format(self.username).encode(),
        ]

    def readline(self):
        if self._lines:
            line = self._lines.pop(0)
            return line+b'\n'
        line = super(ChatInput, self).readline()
        if line:
            sys.stdout.write(self.prompt)
            sys.stdout.flush()
            if line.strip():
                return self.username.encode()+b': ' + line


class ChatOutput(object):

    def __init__(self):
        self.prompt = 'You: '
        self._newline = False

    def write(self, data):
        if not self._newline:
            data = data.decode()
            self._newline = True
        else:
            data = '\n'+data.decode()
        sys.__stdout__.write(data)
        sys.__stdout__.write(self.prompt)

    def _write(self, data):
        sys.__stdout__.write('\n\n'+data.decode())
        sys.__stdout__.write(self.prompt)

    def flush(self):
        sys.__stdout__.flush()


def main():
    parser = argparse.ArgumentParser('chat.py')
    parser.add_argument('-l',
            help='listen for a connection.',
            action='store_true',
    )
    parser.add_argument('dest',
            help='destination hostname or ip to connect or bind to.',
    )
    parser.add_argument('port',
            help='port number to connect or bind to.',
    )
    parser.add_argument('--username',
            help='username to use for the chat.',
    )
    args = parser.parse_args()
    pync_args = '-v {dest} {port}'.format(
            dest=args.dest,
            port=args.port,
    )
    if args.l:
        pync_args = '-l ' + pync_args

    username = args.username
    while not username:
        username = input('Enter username: ')

    chatin = ChatInput(username)
    chatout = ChatOutput()
    return pync(pync_args, stdin=chatin, stdout=chatout)


if __name__ == '__main__':
    main()

