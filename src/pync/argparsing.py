# -*- coding: utf-8 -*-

import argparse
from collections import defaultdict
import sys


class ArgumentParser(argparse.ArgumentParser):
    '''
    ArgumentParser that accepts custom stdout and
    stderr file-like objects.
    '''
    stdout = sys.stdout
    stderr = sys.stderr

    def __init__(self, name, stdout=None, stderr=None, **kwargs):
        super(ArgumentParser, self).__init__(name, **kwargs)
        if stdout is not None:
            self.stdout = stdout
        if stderr is not None:
            self.stderr = stderr

    def _print_message(self, message, file=None):
        if file is sys.stdout:
            file = self.stdout
        elif file is sys.stderr:
            file = self.stderr

        if message:
            if file is None:
                file = self.stderr
            try:
                file.write(message)
            except TypeError:
                file.write(message.encode())
            file.flush()


class GroupingArgumentParser(object):
    '''
    ArgumentParser that separates parsed arguments
    by custom group names.
    '''
    default_group = 'general arguments'

    def __init__(self, *args, **kwargs):
        self._parser = ArgumentParser(*args, **kwargs)
        self._group_args = defaultdict(list)
        self._group_parsers = dict()

    def __getattr__(self, name):
        return getattr(self._parser, name)

    def add_argument(self, name, group='', **kwargs):
        if not group:
            group = self.default_group
        if group not in self._group_parsers:
            self._group_parsers[group] = self._parser.add_argument_group(group)
        parser = self._group_parsers[group]
        parser.add_argument(name, **kwargs)
        self._group_args[group].append(name.lstrip('-'))

    def parse_args(self, argv):
        try:
            args = self._parser.parse_args(argv)
        except SystemExit:
            raise ArgumentError

        arg_groups = defaultdict(argparse.Namespace)
        for group_name, arg_names in self._group_args.items():
            for arg_name in arg_names:
                try:
                    arg_attr = getattr(args, arg_name)
                except AttributeError:
                    continue
                setattr(arg_groups[group_name], arg_name, arg_attr)
        return arg_groups


class ArgumentError(Exception):
    '''
    Raised by GroupingArgumentParser().parse_args()
    to indicate an error while parsing the arguments.
    '''
    pass

