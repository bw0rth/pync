# -*- coding: utf-8 -*-

import io


def makefile(obj):
    '''
    This creates a file-like object from the given argument.
    '''
    # TODO: Add socket support (non-blocking socket).
    return io.StringIO(obj)

