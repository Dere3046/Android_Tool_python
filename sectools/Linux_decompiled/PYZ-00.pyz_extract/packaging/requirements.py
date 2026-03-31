
import re
import string
import urllib.parse as urllib
from typing import List, Optional as TOptional, Set
from pyparsing import Combine, Literal as L, Optional, ParseException, Regex, Word, ZeroOrMore, originalTextFor, stringEnd, stringStart
from markers import MARKER_EXPR, Marker
from specifiers import LegacySpecifier, Specifier, SpecifierSet

class InvalidRequirement(ValueError):
    '''
    An invalid requirement was found, users should refer to PEP 508.
    '''
    pass

ALPHANUM = Word(string.ascii_letters + string.digits)
LBRACKET = L('[').suppress()
RBRACKET = L(']').suppress()
LPAREN = L('(').suppress()
RPAREN = L(')').suppress()
COMMA = L(',').suppress()
SEMICOLON = L(';').suppress()
AT = L('@').suppress()
PUNCTUATION = Word('-_.')
IDENTIFIER_END = ALPHANUM | ZeroOrMore(PUNCTUATION) + ALPHANUM
IDENTIFIER = Combine(ALPHANUM + ZeroOrMore(IDENTIFIER_END))
NAME = IDENTIFIER('name')
EXTRA = IDENTIFIER
URI = Regex('[^ ]+')('url')
URL = AT + URI
EXTRAS_LIST = EXTRA + ZeroOrMore(COMMA + EXTRA)
EXTRAS = LBRACKET + Optional(EXTRAS_LIST) + RBRACKET('extras')
VERSION_PEP440 = Regex(Specifier._regex_str, re.VERBOSE | re.IGNORECASE)
VERSION_LEGACY = Regex(LegacySpecifier._regex_str, re.VERBOSE | re.IGNORECASE)
VERSION_ONE = VERSION_PEP440 ^ VERSION_LEGACY
VERSION_MANY = Combine(VERSION_ONE + ZeroOrMore(COMMA + VERSION_ONE), ',', False, **('joinString', 'adjacent'))('_raw_spec')
_VERSION_SPEC = Optional(LPAREN + VERSION_MANY + RPAREN | VERSION_MANY)
_VERSION_SPEC.setParseAction((lambda s, l, t: if not t._raw_spec:
pass''))
VERSION_SPEC = originalTextFor(_VERSION_SPEC)('specifier')
VERSION_SPEC.setParseAction((lambda s, l, t: t[1]))
MARKER_EXPR = originalTextFor(MARKER_EXPR())('marker')
MARKER_EXPR.setParseAction((lambda s, l, t: Marker(s[t._original_start:t._original_end])))
MARKER_SEPARATOR = SEMICOLON
MARKER = MARKER_SEPARATOR + MARKER_EXPR
VERSION_AND_MARKER = VERSION_SPEC + Optional(MARKER)
URL_AND_MARKER = URL + Optional(MARKER)
NAMED_REQUIREMENT = NAME + Optional(EXTRAS) + (URL_AND_MARKER | VERSION_AND_MARKER)
REQUIREMENT = stringStart + NAMED_REQUIREMENT + stringEnd
REQUIREMENT.parseString('x[]')

class Requirement:
    '''Parse a requirement.

    Parse a given requirement string into its parts, such as name, specifier,
    URL, and extras. Raises InvalidRequirement on a badly-formed requirement
    string.
    '''
    
    def __init__(self = None, requirement_string = None):
        pass
    # WARNING: Decompyle incomplete

    
    def __str__(self = None):
        parts = [
            self.name]
        if self.extras:
            formatted_extras = ','.join(sorted(self.extras))
            parts.append(f'''[{formatted_extras}]''')
        if self.specifier:
            parts.append(str(self.specifier))
        if self.url:
            parts.append(f'''@ {self.url}''')
            if self.marker:
                parts.append(' ')
        if self.marker:
            parts.append(f'''; {self.marker}''')
        return ''.join(parts)

    
    def __repr__(self = None):
        return f'''<Requirement(\'{self}\')>'''


