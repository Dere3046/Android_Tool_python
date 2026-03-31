
__doc__ = 'Various utility functions.'
from collections import namedtuple, Counter
from os.path import commonprefix
__unittest = True
_MAX_LENGTH = 80
_PLACEHOLDER_LEN = 12
_MIN_BEGIN_LEN = 5
_MIN_END_LEN = 5
_MIN_COMMON_LEN = 5
_MIN_DIFF_LEN = _MAX_LENGTH - _MIN_BEGIN_LEN + _PLACEHOLDER_LEN + _MIN_COMMON_LEN + _PLACEHOLDER_LEN + _MIN_END_LEN
# WARNING: Decompyle incomplete
