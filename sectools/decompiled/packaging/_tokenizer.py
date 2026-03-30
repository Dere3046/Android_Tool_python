
from __future__ import annotations
import contextlib
import re
from dataclasses import dataclass
from typing import Iterator, NoReturn
from specifiers import Specifier
Token = dataclass(<NODE:12>)

class ParserSyntaxError(Exception):
    '''The provided source text could not be parsed correctly.'''
    
    def __init__(self = None, message = None, *, source, span):
        self.span = span
        self.message = message
        self.source = source
        super().__init__()

    
    def __str__(self = None):
        marker = ' ' * self.span[0] + '~' * (self.span[1] - self.span[0]) + '^'
        return '\n    '.join([
            self.message,
            self.source,
            marker])

    __classcell__ = None

# WARNING: Decompyle incomplete
