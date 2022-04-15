# -*- coding: utf-8 -*-

import argparse
import sys
from pync import pync, ConsoleInput


class ChatInput(ConsoleInput):

    def __init__(self, username, *args, **kwargs):
        super(ChatInput, self).__init__(*args, **kwargs)
        self.username = username

    def readline(self):
        line = super(ChatInput, self).readline()
        if line:
            sys.stdout.buffer.write(self.username + b': ')
            sys.stdout.flush()
            return self.username + b': ' + line


def main():
    parser = argparse.ArgumentParser('chat.py')

    chatin = ChatInput(b'bren')
    pync('localhost 8000', stdin=chatin)


if __name__ == '__main__':
    main()

