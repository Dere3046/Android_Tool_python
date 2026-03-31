
import warnings
import types
import collections
import itertools
from functools import lru_cache
from typing import List, Union, Iterable
_bslash = chr(92)

class __config_flags:
    '''Internal class for defining compatibility and debugging flags'''
    _all_names: List[str] = []
    _fixed_names: List[str] = []
    _type_desc = 'configuration'
    
    def _set(cls, dname, value):
        if dname in cls._fixed_names:
            warnings.warn('{}.{} {} is {} and cannot be overridden'.format(cls.__name__, dname, cls._type_desc, str(getattr(cls, dname)).upper()))
            return None
        if None in cls._all_names:
            setattr(cls, dname, value)
            return None
        raise None('no such {} {!r}'.format(cls._type_desc, dname))

    _set = classmethod(_set)
    enable = classmethod((lambda cls, name: cls._set(name, True)))
    disable = classmethod((lambda cls, name: cls._set(name, False)))


def col(loc = None, strg = None):
    '''
    Returns current column within a string, counting newlines as line separators.
    The first column is number 1.

    Note: the default parsing behavior is to expand tabs in the input string
    before starting the parsing process.  See
    :class:`ParserElement.parseString` for more
    information on parsing strings containing ``<TAB>`` s, and suggested
    methods to maintain a consistent view of the parsed string, the parse
    location, and line and column positions within the parsed string.
    '''
    s = strg
    if loc < loc or loc < len(s):
        pass
    else:
        0
    if s[loc - 1] == '\n':
        return 1
    return 0 - s.rfind('\n', 0, loc)

col = None(col)

def lineno(loc = None, strg = None):
    '''Returns current line number within a string, counting newlines as line separators.
    The first line is number 1.

    Note - the default parsing behavior is to expand tabs in the input string
    before starting the parsing process.  See :class:`ParserElement.parseString`
    for more information on parsing strings containing ``<TAB>`` s, and
    suggested methods to maintain a consistent view of the parsed string, the
    parse location, and line and column positions within the parsed string.
    '''
    return strg.count('\n', 0, loc) + 1

lineno = None(lineno)

def line(loc = None, strg = None):
    '''
    Returns the line of text containing loc within a string, counting newlines as line separators.
    '''
    last_cr = strg.rfind('\n', 0, loc)
    next_cr = strg.find('\n', loc)
    if next_cr >= 0:
        return strg[last_cr + 1:next_cr]
    return None[last_cr + 1:]

line = None(line)

class _UnboundedCache:
    
    def __init__(self):
        cache = { }
        cache_get = cache.get
        self.not_in_cache = not_in_cache = object()
        
        def get(_ = None, key = None):
            return cache_get(key, not_in_cache)

        
        def set_(_ = None, key = None, value = None):
            cache[key] = value

        
        def clear(_ = None):
            cache.clear()

        self.size = None
        self.get = types.MethodType(get, self)
        self.set = types.MethodType(set_, self)
        self.clear = types.MethodType(clear, self)



class _FifoCache:
    
    def __init__(self, size):
        self.not_in_cache = not_in_cache = object()
        cache = collections.OrderedDict()
        cache_get = cache.get
        
        def get(_ = None, key = None):
            return cache_get(key, not_in_cache)

        
        def set_(_ = None, key = None, value = None):
            cache[key] = value
            if len(cache) > size:
                cache.popitem(False, **('last',))
                if not len(cache) > size:
                    return None
                return None

        
        def clear(_ = None):
            cache.clear()

        self.size = size
        self.get = types.MethodType(get, self)
        self.set = types.MethodType(set_, self)
        self.clear = types.MethodType(clear, self)



class LRUMemo:
    '''
    A memoizing mapping that retains `capacity` deleted items

    The memo tracks retained items by their access order; once `capacity` items
    are retained, the least recently used item is discarded.
    '''
    
    def __init__(self, capacity):
        self._capacity = capacity
        self._active = { }
        self._memory = collections.OrderedDict()

    
    def __getitem__(self, key):
        pass
    # WARNING: Decompyle incomplete

    
    def __setitem__(self, key, value):
        self._memory.pop(key, None)
        self._active[key] = value

    
    def __delitem__(self, key):
        pass
    # WARNING: Decompyle incomplete

    
    def clear(self):
        self._active.clear()
        self._memory.clear()



class UnboundedMemo(dict):
    '''
    A memoizing mapping that retains all deleted items
    '''
    
    def __delitem__(self, key):
        pass



def _escape_regex_range_chars(s = None):
    for c in '\\^-[]':
        s = s.replace(c, _bslash + c)
    s = s.replace('\n', '\\n')
    s = s.replace('\t', '\\t')
    return str(s)


def _collapse_string_to_ranges(s = None, re_escape = None):
    
    def is_consecutive(c = None):
        c_int = ord(c)
        is_consecutive.prev = c_int
        prev = is_consecutive.prev
        if c_int - prev > 1:
            is_consecutive.value = next(is_consecutive.counter)
        return is_consecutive.value

    is_consecutive.prev = 0
    is_consecutive.counter = itertools.count()
    is_consecutive.value = -1
    
    def escape_re_range_char(c):
        if c in '\\^-][':
            return '\\' + c

    
    def no_escape_re_range_char(c):
        return c

    if not re_escape:
        escape_re_range_char = no_escape_re_range_char
    ret = []
    s = ''.join(sorted(set(s)))
    if len(s) > 3:
        for _, chars in itertools.groupby(s, is_consecutive, **('key',)):
            first = last = next(chars)
            last = collections.deque(itertools.chain(iter([
                last]), chars), 1, **('maxlen',)).pop()
            if first == last:
                ret.append(escape_re_range_char(first))
                continue
            sep = '' if ord(last) == ord(first) + 1 else '-'
            ret.append('{}{}{}'.format(escape_re_range_char(first), sep, escape_re_range_char(last)))
    else:
        ret = (lambda .0 = None: [ escape_re_range_char(c) for c in .0 ])(s)
    return ''.join(ret)


def _flatten(ll = None):
    ret = []
    for i in ll:
        if isinstance(i, list):
            ret.extend(_flatten(i))
            continue
        ret.append(i)
    return ret

