# -*- coding: utf-8 -*-

import argparse
import sys
from pync import pync, NetcatConsoleInput


try:
    # py2
    input = raw_input
except NameError:
    # py3
    pass


class ChatInput(NetcatConsoleInput):

    def __init__(self, username, *args, **kwargs):
        super(ChatInput, self).__init__(*args, **kwargs)
        self.username = username
        self.prompt = 'You: '
        self._lines = [
                self.username.encode(),
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
    intro = 'Chat started with username [{user}] speaking with [{ruser}]\n'

    def __init__(self, username):
        self.prompt = 'You: '
        self.username = username
        self._intro = True

    def write(self, data):
        if self._intro:
            ruser = data.decode().strip()
            sys.__stdout__.write(self.intro.format(
                user=self.username,
                ruser=ruser,
            ))
            sys.__stdout__.write(self.prompt)
            self._intro = False
            return
        data = '\n'+data.decode()
        sys.__stdout__.write(data)
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
    chatout = ChatOutput(username)
    return pync(pync_args, stdin=chatin, stdout=chatout)


if __name__ == '__main__':
    main()

