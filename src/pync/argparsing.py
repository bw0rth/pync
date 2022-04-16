# -*- coding: utf-8 -*-

import argparse
from collections import defaultdict


class GroupingArgumentParser(object):

    def __init__(self, *args, **kwargs):
        self._parser = argparse.ArgumentParser(
                *args,
                **kwargs,
        )
        self._group_args = defaultdict(list)
        self._group_parsers = dict()

    def __getattr__(self, name):
        return getattr(self._parser, name)

    def add_argument(self, name, group='general arguments', **kwargs):
        if group not in self._group_parsers:
            self._group_parsers[group] = self._parser.add_argument_group(group)
        parser = self._group_parsers[group]
        parser.add_argument(name, **kwargs)
        self._group_args[group].append(name.lstrip('-'))

    def parse_args(self, argv):
        args = self._parser.parse_args(argv)
        arg_groups = defaultdict(argparse.Namespace)
        for group_name, arg_names in self._group_args.items():
            for arg_name in arg_names:
                try:
                    arg_attr = getattr(args, arg_name)
                except AttributeError:
                    continue
                setattr(arg_groups[group_name], arg_name, arg_attr)
        return arg_groups


if __name__ == '__main__':
    # For test purposes.
    import sys

    parser = GroupingArgumentParser()
    parser.add_argument('-a')
    parser.add_argument('-b', 'server arguments')
    parser.add_argument('-c', 'client arguments')

    args = parser.parse_args(sys.argv[1:])

