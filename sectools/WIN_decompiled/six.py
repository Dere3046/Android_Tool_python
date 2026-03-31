
__doc__ = 'Utilities for writing code that runs on Python 2 and 3'
from __future__ import absolute_import
import functools
import itertools
import operator
import sys
import types
__author__ = 'Benjamin Peterson <benjamin@python.org>'
__version__ = '1.16.0'
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
PY34 = sys.version_info[0:2] >= (3, 4)
if PY3:
    string_types = (str,)
    integer_types = (int,)
    class_types = (type,)
    text_type = str
    binary_type = bytes
    MAXSIZE = sys.maxsize
# WARNING: Decompyle incomplete
