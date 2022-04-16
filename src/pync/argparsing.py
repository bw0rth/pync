# -*- coding: utf-8 -*-

import argparse
from collections import defaultdict
import sys


class GroupingArgumentParser(argparse.ArgumentParser):

    def __init__(self, *args, **kwargs):
        super(GroupingArgumentParser, self).__init__(*args, **kwargs)
        self._group_args = defaultdict(list)
        self._group_parsers = dict()

    def add_argument(self, name, group='general arguments', **kwargs):
        if group not in self._group_parsers:
            self._group_parsers[group] = super(GroupingArgumentParser, self).add_argument_group(group)
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

    def error(self, message):
        self.print_usage(sys.stderr)
        args = {'prog': self.prog, 'message': message}
        sys.stderr.write('%(prog)s: error: %(message)s\n' % args)
        sys.stderr.flush()
        raise SystemExit


if __name__ == '__main__':
    # For test purposes.
    import sys

    parser = GroupingArgumentParser()
    parser.add_argument('-a')
    parser.add_argument('-b', 'server arguments')
    parser.add_argument('-c', 'client arguments')

    args = parser.parse_args(sys.argv[1:])

