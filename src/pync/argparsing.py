# -*- coding: utf-8 -*-

import argparse
from collections import defaultdict
import sys


class ArgumentParser(argparse.ArgumentParser):
    '''
    An ArgumentParser that can take custom stdout
    and stderr file-like objects.
    '''
    prog = ''
    usage = None
    description = None
    add_help = True

    stdout = sys.stdout
    stderr = sys.stderr

    def __init__(self, prog=None, usage=None, description=None,
            add_help=None, stdout=None, stderr=None, **kwargs):
        if prog is not None:
            self.prog = prog
        if usage is not None:
            self.usage = usage
        if description is not None:
            self.description = description
        if add_help is not None:
            self.add_help = add_help

        if stdout is not None:
            self.stdout = stdout
        if stderr is not None:
            self.stderr = stderr

        super(ArgumentParser, self).__init__(self.prog,
                usage=self.usage,
                description=self.description,
                add_help=self.add_help,
                **kwargs)

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


class GroupingArgumentParser(ArgumentParser):
    '''
    ArgumentParser that separates parsed arguments
    by custom group names.
    '''
    default_group = 'general arguments'

    def __init__(self, *args, **kwargs):
        self._group_args = defaultdict(list)
        self._group_parsers = dict()
        super(GroupingArgumentParser, self).__init__(*args, **kwargs)

    def add_argument(self, *args, **kwargs):
        name = args[-1]
        group = ''
        if 'group' in kwargs:
            group = kwargs['group']
            del kwargs['group']
        if not group:
            group = self.default_group
        if group not in self._group_parsers:
            self._group_parsers[group] = self.add_argument_group(group)
        parser = self._group_parsers[group]
        parser.add_argument(*args, **kwargs)
        dest = name.lstrip('-')
        if 'dest' in kwargs:
            dest = kwargs['dest']
        self._group_args[group].append(dest)

    def group_parse_args(self, argv):
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

