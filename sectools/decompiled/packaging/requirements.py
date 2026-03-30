
from __future__ import annotations
from typing import Any, Iterator
from _parser import parse_requirement as _parse_requirement
from _tokenizer import ParserSyntaxError
from markers import Marker, _normalize_extra_values
from specifiers import SpecifierSet
from utils import canonicalize_name

class InvalidRequirement(ValueError):
    '''
    An invalid requirement was found, users should refer to PEP 508.
    '''
    pass


class Requirement:
    '''Parse a requirement.

    Parse a given requirement string into its parts, such as name, specifier,
    URL, and extras. Raises InvalidRequirement on a badly-formed requirement
    string.
    '''
    
    def __init__(self = None, requirement_string = None):
        pass
    # WARNING: Decompyle incomplete

    
    def _iter_parts(self = None, name = None):
        yield name
        if self.extras:
            formatted_extras = ','.join(sorted(self.extras))
            yield f'''[{formatted_extras}]'''
        if self.specifier:
            yield str(self.specifier)
        if self.url:
            yield f'''@ {self.url}'''
            if self.marker:
                yield ' '
        if self.marker:
            yield f'''; {self.marker}'''
            return None

    
    def __str__(self = None):
        return ''.join(self._iter_parts(self.name))

    
    def __repr__(self = None):
        return f'''<Requirement(\'{self}\')>'''

    
    def __hash__(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def __eq__(self = None, other = None):
        if not isinstance(other, Requirement):
            return NotImplemented
        if None(self.name) == canonicalize_name(other.name) and self.extras == other.extras and self.specifier == other.specifier and self.url == other.url:
            pass
        return self.marker == other.marker


