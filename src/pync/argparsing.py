# -*- coding: utf-8 -*-

import argparse
from collections import defaultdict
import sys


class GroupingArgumentParser(argparse.ArgumentParser):
    '''
    ArgumentParser that separates parsed arguments
    by custom group names.
    '''
    stdout = sys.stdout
    stderr = sys.stderr

    default_group = 'general arguments'

    def __init__(self, name, stdout=None, stderr=None, **kwargs):
        super(GroupingArgumentParser, self).__init__(name, **kwargs)

        if stdout is not None:
            self.stdout = stdout
        if stderr is not None:
            self.stderr = stderr

        self._group_args = defaultdict(list)
        self._group_parsers = dict()

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

    def add_argument(self, name, group='', **kwargs):
        if not group:
            group = self.default_group
        if group not in self._group_parsers:
            self._group_parsers[group] = self.add_argument_group(group)
        parser = self._group_parsers[group]
        parser.add_argument(name, **kwargs)
        self._group_args[group].append(name.lstrip('-'))

    def parse_args(self, argv):
        args = super(GroupingArgumentParser, self).parse_args(argv)
        arg_groups = defaultdict(argparse.Namespace)
        for group_name, arg_names in self._group_args.items():
            for arg_name in arg_names:
                try:
                    arg_attr = getattr(args, arg_name)
                except AttributeError:
                    continue
                setattr(arg_groups[group_name], arg_name, arg_attr)
        return arg_groups

