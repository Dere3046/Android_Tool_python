
import os
import re
import abc
import csv
import sys
from  import zipp
import email
import pathlib
import operator
import textwrap
import warnings
import functools
import itertools
import posixpath
import collections
from  import _adapters, _meta
from _collections import FreezableDefaultDict, Pair
from _compat import NullFinder, install, pypy_partial
from _functools import method_cache, pass_none
from _itertools import always_iterable, unique_everseen
from _meta import PackageMetadata, SimplePath
from contextlib import suppress
from importlib import import_module
from importlib.abc import MetaPathFinder
from itertools import starmap
from typing import List, Mapping, Optional, Union
__all__ = [
    'Distribution',
    'DistributionFinder',
    'PackageMetadata',
    'PackageNotFoundError',
    'distribution',
    'distributions',
    'entry_points',
    'files',
    'metadata',
    'packages_distributions',
    'requires',
    'version']

class PackageNotFoundError(ModuleNotFoundError):
    '''The package was not found.'''
    
    def __str__(self):
        return f'''No package metadata was found for {self.name}'''

    
    def name(self):
        (name,) = self.args
        return name

    name = property(name)


class Sectioned:
    """
    A simple entry point config parser for performance

    >>> for item in Sectioned.read(Sectioned._sample):
    ...     print(item)
    Pair(name='sec1', value='# comments ignored')
    Pair(name='sec1', value='a = 1')
    Pair(name='sec1', value='b = 2')
    Pair(name='sec2', value='a = 2')

    >>> res = Sectioned.section_pairs(Sectioned._sample)
    >>> item = next(res)
    >>> item.name
    'sec1'
    >>> item.value
    Pair(name='a', value='1')
    >>> item = next(res)
    >>> item.value
    Pair(name='b', value='2')
    >>> item = next(res)
    >>> item.name
    'sec2'
    >>> item.value
    Pair(name='a', value='2')
    >>> list(res)
    []
    """
    _sample = textwrap.dedent('\n        [sec1]\n        # comments ignored\n        a = 1\n        b = 2\n\n        [sec2]\n        a = 2\n        ').lstrip()
    
    def section_pairs(cls, text):
        return (lambda .0: for section in .0:
if section.name is not None:
section._replace(Pair.parse(section.value), **('value',))continueNone)(cls.read(text, cls.valid, **('filter_',)))

    section_pairs = classmethod(section_pairs)
    
    def read(text, filter_ = (None,)):
        lines = filter(filter_, map(str.strip, text.splitlines()))
        name = None
        for value in lines:
            if value.startswith('['):
                pass
            section_match = value.endswith(']')
            if section_match:
                name = value.strip('[]')
                continue
            yield Pair(name, value)

    read = staticmethod(read)
    
    def valid(line):
        if line:
            pass
        return not line.startswith('#')

    valid = staticmethod(valid)


class DeprecatedTuple:
    """
    Provide subscript item access for backward compatibility.

    >>> recwarn = getfixture('recwarn')
    >>> ep = EntryPoint(name='name', value='value', group='group')
    >>> ep[:]
    ('name', 'value', 'group')
    >>> ep[0]
    'name'
    >>> len(recwarn)
    1
    """
    _warn = functools.partial(warnings.warn, 'EntryPoint tuple interface is deprecated. Access members by name.', DeprecationWarning, pypy_partial(2), **('stacklevel',))
    
    def __getitem__(self, item):
        self._warn()
        return self._key()[item]



class EntryPoint(DeprecatedTuple):
    '''An entry point as defined by Python packaging conventions.

    See `the packaging docs on entry points
    <https://packaging.python.org/specifications/entry-points/>`_
    for more information.
    '''
    pattern = re.compile('(?P<module>[\\w.]+)\\s*(:\\s*(?P<attr>[\\w.]+)\\s*)?((?P<extras>\\[.*\\])\\s*)?$')
    dist: Optional['Distribution'] = None
    
    def __init__(self, name, value, group):
        vars(self).update(name, value, group, **('name', 'value', 'group'))

    
    def load(self):
        '''Load the entry point from its definition. If only a module
        is indicated by the value, return that module. Otherwise,
        return the named object.
        '''
        match = self.pattern.match(self.value)
        module = import_module(match.group('module'))
        if not match.group('attr'):
            pass
        attrs = filter(None, ''.split('.'))
        return functools.reduce(getattr, attrs, module)

    
    def module(self):
        match = self.pattern.match(self.value)
        return match.group('module')

    module = property(module)
    
    def attr(self):
        match = self.pattern.match(self.value)
        return match.group('attr')

    attr = property(attr)
    
    def extras(self):
        match = self.pattern.match(self.value)
        if not match.group('extras'):
            pass
        return list(re.finditer('\\w+', ''))

    extras = property(extras)
    
    def _for(self, dist):
        vars(self).update(dist, **('dist',))
        return self

    
    def __iter__(self):
        '''
        Supply iter so one may construct dicts of EntryPoints by name.
        '''
        msg = 'Construction of dict of EntryPoints is deprecated in favor of EntryPoints.'
        warnings.warn(msg, DeprecationWarning)
        return iter((self.name, self))

    
    def matches(self, **params):
        attrs = (lambda .0 = None: for param in .0:
getattr(self, param))(params)
        return all(map(operator.eq, params.values(), attrs))

    
    def _key(self):
        return (self.name, self.value, self.group)

    
    def __lt__(self, other):
        return self._key() < other._key()

    
    def __eq__(self, other):
        return self._key() == other._key()

    
    def __setattr__(self, name, value):
        raise AttributeError('EntryPoint objects are immutable.')

    
    def __repr__(self):
        return f'''EntryPoint(name={self.name!r}, value={self.value!r}, group={self.group!r})'''

    
    def __hash__(self):
        return hash(self._key())



class DeprecatedList(list):
    """
    Allow an otherwise immutable object to implement mutability
    for compatibility.

    >>> recwarn = getfixture('recwarn')
    >>> dl = DeprecatedList(range(3))
    >>> dl[0] = 1
    >>> dl.append(3)
    >>> del dl[3]
    >>> dl.reverse()
    >>> dl.sort()
    >>> dl.extend([4])
    >>> dl.pop(-1)
    4
    >>> dl.remove(1)
    >>> dl += [5]
    >>> dl + [6]
    [1, 2, 5, 6]
    >>> dl + (6,)
    [1, 2, 5, 6]
    >>> dl.insert(0, 0)
    >>> dl
    [0, 1, 2, 5]
    >>> dl == [0, 1, 2, 5]
    True
    >>> dl == (0, 1, 2, 5)
    True
    >>> len(recwarn)
    1
    """
    __slots__ = ()
    _warn = functools.partial(warnings.warn, 'EntryPoints list interface is deprecated. Cast to list if needed.', DeprecationWarning, pypy_partial(2), **('stacklevel',))
    
    def _wrap_deprecated_method(method_name = None):
        
        def wrapped(self = None, *args, **kwargs):
            self._warn()
        # WARNING: Decompyle incomplete

        return (method_name, wrapped)

    locals().update(map(_wrap_deprecated_method, '__setitem__ __delitem__ append reverse extend pop remove __iadd__ insert sort'.split()))
    
    def __add__(self, other):
        if not isinstance(other, tuple):
            self._warn()
            other = tuple(other)
        return self.__class__(tuple(self) + other)

    
    def __eq__(self, other):
        if not isinstance(other, tuple):
            self._warn()
            other = tuple(other)
        return tuple(self).__eq__(other)

    __classcell__ = None


class EntryPoints(DeprecatedList):
    '''
    An immutable collection of selectable EntryPoint objects.
    '''
    __slots__ = ()
    
    def __getitem__(self = None, name = None):
        '''
        Get the EntryPoint in self matching name.
        '''
        if isinstance(name, int):
            warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
            return super().__getitem__(name)
        :
            if isinstance(name, int):
                warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                return super().__getitem__(name)
            :
                if isinstance(name, int):
                    warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                    return super().__getitem__(name)
                :
                    if isinstance(name, int):
                        warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                        return super().__getitem__(name)
                    :
                        if isinstance(name, int):
                            warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                            return super().__getitem__(name)
                        :
                            if isinstance(name, int):
                                warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                return super().__getitem__(name)
                            :
                                if isinstance(name, int):
                                    warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                    return super().__getitem__(name)
                                :
                                    if isinstance(name, int):
                                        warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                        return super().__getitem__(name)
                                    :
                                        if isinstance(name, int):
                                            warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                            return super().__getitem__(name)
                                        :
                                            if isinstance(name, int):
                                                warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                return super().__getitem__(name)
                                            :
                                                if isinstance(name, int):
                                                    warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                    return super().__getitem__(name)
                                                :
                                                    if isinstance(name, int):
                                                        warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                        return super().__getitem__(name)
                                                    :
                                                        if isinstance(name, int):
                                                            warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                            return super().__getitem__(name)
                                                        :
                                                            if isinstance(name, int):
                                                                warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                return super().__getitem__(name)
                                                            :
                                                                if isinstance(name, int):
                                                                    warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                    return super().__getitem__(name)
                                                                :
                                                                    if isinstance(name, int):
                                                                        warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                        return super().__getitem__(name)
                                                                    :
                                                                        if isinstance(name, int):
                                                                            warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                            return super().__getitem__(name)
                                                                        :
                                                                            if isinstance(name, int):
                                                                                warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                return super().__getitem__(name)
                                                                            :
                                                                                if isinstance(name, int):
                                                                                    warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                    return super().__getitem__(name)
                                                                                :
                                                                                    if isinstance(name, int):
                                                                                        warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                        return super().__getitem__(name)
                                                                                    :
                                                                                        if isinstance(name, int):
                                                                                            warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                            return super().__getitem__(name)
                                                                                        :
                                                                                            if isinstance(name, int):
                                                                                                warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                return super().__getitem__(name)
                                                                                            :
                                                                                                if isinstance(name, int):
                                                                                                    warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                    return super().__getitem__(name)
                                                                                                :
                                                                                                    if isinstance(name, int):
                                                                                                        warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                        return super().__getitem__(name)
                                                                                                    :
                                                                                                        if isinstance(name, int):
                                                                                                            warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                            return super().__getitem__(name)
                                                                                                        :
                                                                                                            if isinstance(name, int):
                                                                                                                warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                return super().__getitem__(name)
                                                                                                            :
                                                                                                                if isinstance(name, int):
                                                                                                                    warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                    return super().__getitem__(name)
                                                                                                                :
                                                                                                                    if isinstance(name, int):
                                                                                                                        warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                        return super().__getitem__(name)
                                                                                                                    :
                                                                                                                        if isinstance(name, int):
                                                                                                                            warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                            return super().__getitem__(name)
                                                                                                                        :
                                                                                                                            if isinstance(name, int):
                                                                                                                                warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                return super().__getitem__(name)
                                                                                                                            :
                                                                                                                                if isinstance(name, int):
                                                                                                                                    warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                    return super().__getitem__(name)
                                                                                                                                :
                                                                                                                                    if isinstance(name, int):
                                                                                                                                        warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                        return super().__getitem__(name)
                                                                                                                                    :
                                                                                                                                        if isinstance(name, int):
                                                                                                                                            warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                            return super().__getitem__(name)
                                                                                                                                        :
                                                                                                                                            if isinstance(name, int):
                                                                                                                                                warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                return super().__getitem__(name)
                                                                                                                                            :
                                                                                                                                                if isinstance(name, int):
                                                                                                                                                    warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                    return super().__getitem__(name)
                                                                                                                                                :
                                                                                                                                                    if isinstance(name, int):
                                                                                                                                                        warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                        return super().__getitem__(name)
                                                                                                                                                    :
                                                                                                                                                        if isinstance(name, int):
                                                                                                                                                            warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                            return super().__getitem__(name)
                                                                                                                                                        :
                                                                                                                                                            if isinstance(name, int):
                                                                                                                                                                warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                return super().__getitem__(name)
                                                                                                                                                            :
                                                                                                                                                                if isinstance(name, int):
                                                                                                                                                                    warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                    return super().__getitem__(name)
                                                                                                                                                                :
                                                                                                                                                                    if isinstance(name, int):
                                                                                                                                                                        warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                        return super().__getitem__(name)
                                                                                                                                                                    :
                                                                                                                                                                        if isinstance(name, int):
                                                                                                                                                                            warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                            return super().__getitem__(name)
                                                                                                                                                                        :
                                                                                                                                                                            if isinstance(name, int):
                                                                                                                                                                                warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                return super().__getitem__(name)
                                                                                                                                                                            :
                                                                                                                                                                                if isinstance(name, int):
                                                                                                                                                                                    warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                    return super().__getitem__(name)
                                                                                                                                                                                :
                                                                                                                                                                                    if isinstance(name, int):
                                                                                                                                                                                        warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                        return super().__getitem__(name)
                                                                                                                                                                                    :
                                                                                                                                                                                        if isinstance(name, int):
                                                                                                                                                                                            warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                            return super().__getitem__(name)
                                                                                                                                                                                        :
                                                                                                                                                                                            if isinstance(name, int):
                                                                                                                                                                                                warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                return super().__getitem__(name)
                                                                                                                                                                                            :
                                                                                                                                                                                                if isinstance(name, int):
                                                                                                                                                                                                    warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                    return super().__getitem__(name)
                                                                                                                                                                                                :
                                                                                                                                                                                                    if isinstance(name, int):
                                                                                                                                                                                                        warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                        return super().__getitem__(name)
                                                                                                                                                                                                    :
                                                                                                                                                                                                        if isinstance(name, int):
                                                                                                                                                                                                            warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                            return super().__getitem__(name)
                                                                                                                                                                                                        :
                                                                                                                                                                                                            if isinstance(name, int):
                                                                                                                                                                                                                warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                return super().__getitem__(name)
                                                                                                                                                                                                            :
                                                                                                                                                                                                                if isinstance(name, int):
                                                                                                                                                                                                                    warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                    return super().__getitem__(name)
                                                                                                                                                                                                                :
                                                                                                                                                                                                                    if isinstance(name, int):
                                                                                                                                                                                                                        warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                        return super().__getitem__(name)
                                                                                                                                                                                                                    :
                                                                                                                                                                                                                        if isinstance(name, int):
                                                                                                                                                                                                                            warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                            return super().__getitem__(name)
                                                                                                                                                                                                                        :
                                                                                                                                                                                                                            if isinstance(name, int):
                                                                                                                                                                                                                                warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                return super().__getitem__(name)
                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                if isinstance(name, int):
                                                                                                                                                                                                                                    warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                    return super().__getitem__(name)
                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                    if isinstance(name, int):
                                                                                                                                                                                                                                        warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                        return super().__getitem__(name)
                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                        if isinstance(name, int):
                                                                                                                                                                                                                                            warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                            return super().__getitem__(name)
                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                            if isinstance(name, int):
                                                                                                                                                                                                                                                warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                return super().__getitem__(name)
                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                if isinstance(name, int):
                                                                                                                                                                                                                                                    warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                    return super().__getitem__(name)
                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                    if isinstance(name, int):
                                                                                                                                                                                                                                                        warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                        return super().__getitem__(name)
                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                        if isinstance(name, int):
                                                                                                                                                                                                                                                            warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                            return super().__getitem__(name)
                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                            if isinstance(name, int):
                                                                                                                                                                                                                                                                warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                return super().__getitem__(name)
                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                if isinstance(name, int):
                                                                                                                                                                                                                                                                    warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                    return super().__getitem__(name)
                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                    if isinstance(name, int):
                                                                                                                                                                                                                                                                        warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                        return super().__getitem__(name)
                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                        if isinstance(name, int):
                                                                                                                                                                                                                                                                            warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                            return super().__getitem__(name)
                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                            if isinstance(name, int):
                                                                                                                                                                                                                                                                                warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                return super().__getitem__(name)
                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                if isinstance(name, int):
                                                                                                                                                                                                                                                                                    warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                    return super().__getitem__(name)
                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                    if isinstance(name, int):
                                                                                                                                                                                                                                                                                        warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                        return super().__getitem__(name)
                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                        if isinstance(name, int):
                                                                                                                                                                                                                                                                                            warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                            return super().__getitem__(name)
                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                            if isinstance(name, int):
                                                                                                                                                                                                                                                                                                warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                return super().__getitem__(name)
                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                if isinstance(name, int):
                                                                                                                                                                                                                                                                                                    warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                    return super().__getitem__(name)
                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                    if isinstance(name, int):
                                                                                                                                                                                                                                                                                                        warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                        return super().__getitem__(name)
                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                        if isinstance(name, int):
                                                                                                                                                                                                                                                                                                            warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                            return super().__getitem__(name)
                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                            if isinstance(name, int):
                                                                                                                                                                                                                                                                                                                warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                                return super().__getitem__(name)
                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                if isinstance(name, int):
                                                                                                                                                                                                                                                                                                                    warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                                    return super().__getitem__(name)
                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                    if isinstance(name, int):
                                                                                                                                                                                                                                                                                                                        warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                                        return super().__getitem__(name)
                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                        if isinstance(name, int):
                                                                                                                                                                                                                                                                                                                            warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                                            return super().__getitem__(name)
                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                            if isinstance(name, int):
                                                                                                                                                                                                                                                                                                                                warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                                                return super().__getitem__(name)
                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                if isinstance(name, int):
                                                                                                                                                                                                                                                                                                                                    warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                                                    return super().__getitem__(name)
                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                    if isinstance(name, int):
                                                                                                                                                                                                                                                                                                                                        warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                                                        return super().__getitem__(name)
                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                        if isinstance(name, int):
                                                                                                                                                                                                                                                                                                                                            warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                                                            return super().__getitem__(name)
                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                            if isinstance(name, int):
                                                                                                                                                                                                                                                                                                                                                warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                                                                return super().__getitem__(name)
                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                if isinstance(name, int):
                                                                                                                                                                                                                                                                                                                                                    warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                                                                    return super().__getitem__(name)
                                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                                    if isinstance(name, int):
                                                                                                                                                                                                                                                                                                                                                        warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                                                                        return super().__getitem__(name)
                                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                                        if isinstance(name, int):
                                                                                                                                                                                                                                                                                                                                                            warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                                                                            return super().__getitem__(name)
                                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                                            if isinstance(name, int):
                                                                                                                                                                                                                                                                                                                                                                warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                                                                                return super().__getitem__(name)
                                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                                if isinstance(name, int):
                                                                                                                                                                                                                                                                                                                                                                    warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                                                                                    return super().__getitem__(name)
                                                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                                                    if isinstance(name, int):
                                                                                                                                                                                                                                                                                                                                                                        warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                                                                                        return super().__getitem__(name)
                                                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                                                        if isinstance(name, int):
                                                                                                                                                                                                                                                                                                                                                                            warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                                                                                            return super().__getitem__(name)
                                                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                                                            if isinstance(name, int):
                                                                                                                                                                                                                                                                                                                                                                                warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                                                                                                return super().__getitem__(name)
                                                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                                                if isinstance(name, int):
                                                                                                                                                                                                                                                                                                                                                                                    warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                                                                                                    return super().__getitem__(name)
                                                                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                                                                    if isinstance(name, int):
                                                                                                                                                                                                                                                                                                                                                                                        warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                                                                                                        return super().__getitem__(name)
                                                                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                                                                        if isinstance(name, int):
                                                                                                                                                                                                                                                                                                                                                                                            warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                                                                                                            return super().__getitem__(name)
                                                                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                                                                            if isinstance(name, int):
                                                                                                                                                                                                                                                                                                                                                                                                warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                                                                                                                return super().__getitem__(name)
                                                                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                                                                if isinstance(name, int):
                                                                                                                                                                                                                                                                                                                                                                                                    warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                                                                                                                    return super().__getitem__(name)
                                                                                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                                                                                    if isinstance(name, int):
                                                                                                                                                                                                                                                                                                                                                                                                        warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                                                                                                                        return super().__getitem__(name)
                                                                                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                                                                                        if isinstance(name, int):
                                                                                                                                                                                                                                                                                                                                                                                                            warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                                                                                                                            return super().__getitem__(name)
                                                                                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                                                                                            if isinstance(name, int):
                                                                                                                                                                                                                                                                                                                                                                                                                warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                                                                                                                                return super().__getitem__(name)
                                                                                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                                                                                if isinstance(name, int):
                                                                                                                                                                                                                                                                                                                                                                                                                    warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                                                                                                                                    return super().__getitem__(name)
                                                                                                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                                                                                                    if isinstance(name, int):
                                                                                                                                                                                                                                                                                                                                                                                                                        warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                                                                                                                                        return super().__getitem__(name)
                                                                                                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                                                                                                        if isinstance(name, int):
                                                                                                                                                                                                                                                                                                                                                                                                                            warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                                                                                                                                            return super().__getitem__(name)
                                                                                                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                                                                                                            if isinstance(name, int):
                                                                                                                                                                                                                                                                                                                                                                                                                                warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                                                                                                                                                return super().__getitem__(name)
                                                                                                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                                                                                                if isinstance(name, int):
                                                                                                                                                                                                                                                                                                                                                                                                                                    warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                                                                                                                                                    return super().__getitem__(name)
                                                                                                                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                                                                                                                    if isinstance(name, int):
                                                                                                                                                                                                                                                                                                                                                                                                                                        warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                                                                                                                                                        return super().__getitem__(name)
                                                                                                                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                                                                                                                        if isinstance(name, int):
                                                                                                                                                                                                                                                                                                                                                                                                                                            warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                                                                                                                                                            return super().__getitem__(name)
                                                                                                                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                                                                                                                            if isinstance(name, int):
                                                                                                                                                                                                                                                                                                                                                                                                                                                warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                                                                                                                                                                return super().__getitem__(name)
                                                                                                                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                                                                                                                if isinstance(name, int):
                                                                                                                                                                                                                                                                                                                                                                                                                                                    warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                                                                                                                                                                    return super().__getitem__(name)
                                                                                                                                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                                                                                                                                    if isinstance(name, int):
                                                                                                                                                                                                                                                                                                                                                                                                                                                        warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                                                                                                                                                                        return super().__getitem__(name)
                                                                                                                                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                                                                                                                                        if isinstance(name, int):
                                                                                                                                                                                                                                                                                                                                                                                                                                                            warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.', DeprecationWarning, 2, **('stacklevel',))
                                                                                                                                                                                                                                                                                                                                                                                                                                                            return sup