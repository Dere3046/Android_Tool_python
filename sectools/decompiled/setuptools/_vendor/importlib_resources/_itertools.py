
from itertools import filterfalse
from typing import Callable, Iterable, Iterator, Optional, Set, TypeVar, Union
_T = TypeVar('_T')
_U = TypeVar('_U')

def unique_everseen(iterable = None, key = None):
    '''List unique elements, preserving order. Remember all elements ever seen.'''
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
        return None
    for element in None:
        k = key(element)
        if k not in seen:
            seen_add(k)
            yield element

