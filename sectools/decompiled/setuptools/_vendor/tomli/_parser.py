
from __future__ import annotations
from collections.abc import Iterable
import string
from types import MappingProxyType
from typing import Any, BinaryIO, NamedTuple
from _re import RE_DATETIME, RE_LOCALTIME, RE_NUMBER, match_to_datetime, match_to_localtime, match_to_number
from _types import Key, ParseFloat, Pos
ASCII_CTRL = frozenset((lambda .0: for i in .0:
chr(i))(range(32))) | frozenset(chr(127))
ILLEGAL_BASIC_STR_CHARS = ASCII_CTRL - frozenset('\t')
ILLEGAL_MULTILINE_BASIC_STR_CHARS = ASCII_CTRL - frozenset('\t\n')
ILLEGAL_LITERAL_STR_CHARS = ILLEGAL_BASIC_STR_CHARS
ILLEGAL_MULTILINE_LITERAL_STR_CHARS = ILLEGAL_MULTILINE_BASIC_STR_CHARS
ILLEGAL_COMMENT_CHARS = ILLEGAL_BASIC_STR_CHARS
TOML_WS = frozenset(' \t')
TOML_WS_AND_NEWLINE = TOML_WS | frozenset('\n')
BARE_KEY_CHARS = frozenset(string.ascii_letters + string.digits + '-_')
KEY_INITIAL_CHARS = BARE_KEY_CHARS | frozenset('"\'')
HEXDIGIT_CHARS = frozenset(string.hexdigits)
BASIC_STR_ESCAPE_REPLACEMENTS = MappingProxyType({
    '\\b': '\x08',
    '\\t': '\t',
    '\\n': '\n',
    '\\f': '\x0c',
    '\\r': '\r',
    '\\"': '"',
    '\\\\': '\\' })

class TOMLDecodeError(ValueError):
    '''An error raised if a document is not valid TOML.'''
    pass


def load(__fp = None, *, parse_float):
    '''Parse TOML from a binary file object.'''
    b = __fp.read()
# WARNING: Decompyle incomplete


def loads(__s = None, *, parse_float):
    '''Parse TOML from a string.'''
    src = __s.replace('\r\n', '\n')
    pos = 0
    out = Output(NestedDict(), Flags())
    header = ()
    parse_float = make_safe_parse_float(parse_float)
    pos = skip_chars(src, pos, TOML_WS)
# WARNING: Decompyle incomplete


class Flags:
    '''Flags that map to parsed keys/namespaces.'''
    FROZEN = 0
    EXPLICIT_NEST = 1
    
    def __init__(self = None):
        self._flags = { }
        self._pending_flags = set()

    
    def add_pending(self = None, key = None, flag = None):
        self._pending_flags.add((key, flag))

    
    def finalize_pending(self = None):
        for key, flag in self._pending_flags:
            self.set(key, flag, False, **('recursive',))
        self._pending_flags.clear()

    
    def unset_all(self = None, key = None):
        cont = self._flags
        for k in key[:-1]:
            if k not in cont:
                return None
            cont = None[k]['nested']
        cont.pop(key[-1], None)

    
    def set(self = None, key = None, flag = None, *, recursive):
        cont = self._flags
        key_parent = key[:-1]
        key_stem = key[-1]
        for k in key_parent:
            if k not in cont:
                cont[k] = {
                    'flags': set(),
                    'recursive_flags': set(),
                    'nested': { } }
            cont = cont[k]['nested']
        if key_stem not in cont:
            cont[key_stem] = {
                'flags': set(),
                'recursive_flags': set(),
                'nested': { } }
        cont[key_stem]['recursive_flags' if recursive else 'flags'].add(flag)

    
    def is_(self = None, key = None, flag = None):
        if not key:
            return False
        cont = None._flags
        for k in key[:-1]:
            if k not in cont:
                return False
            inner_cont = None[k]
            if flag in inner_cont['recursive_flags']:
                return True
            cont = None['nested']
        key_stem = key[-1]
        if key_stem in cont:
            cont = cont[key_stem]
            if not flag in cont['flags']:
                pass
            return flag in cont['recursive_flags']



class NestedDict:
    
    def __init__(self = None):
        self.dict = { }

    
    def get_or_create_nest(self = None, key = None, *, access_lists):
        cont = self.dict
        for k in key:
            if k not in cont:
                cont[k] = { }
            cont = cont[k]
            if access_lists and isinstance(cont, list):
                cont = cont[-1]
            if not is