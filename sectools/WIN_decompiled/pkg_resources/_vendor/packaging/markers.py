
import operator
import os
import platform
import sys
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from pkg_resources.extern.pyparsing import Forward, Group, Literal as L, ParseException, ParseResults, QuotedString, ZeroOrMore, stringEnd, stringStart
from specifiers import InvalidSpecifier, Specifier
__all__ = [
    'InvalidMarker',
    'UndefinedComparison',
    'UndefinedEnvironmentName',
    'Marker',
    'default_environment']
Operator = Callable[([
    str,
    str], bool)]

class InvalidMarker(ValueError):
    '''
    An invalid marker was found, users should refer to PEP 508.
    '''
    pass


class UndefinedComparison(ValueError):
    """
    An invalid operation was attempted on a value that doesn't support it.
    """
    pass


class UndefinedEnvironmentName(ValueError):
    '''
    A name was attempted to be used that does not exist inside of the
    environment.
    '''
    pass


class Node:
    
    def __init__(self = None, value = None):
        self.value = value

    
    def __str__(self = None):
        return str(self.value)

    
    def __repr__(self = None):
        return f'''<{self.__class__.__name__}(\'{self}\')>'''

    
    def serialize(self = None):
        raise NotImplementedError



class Variable(Node):
    
    def serialize(self = None):
        return str(self)



class Value(Node):
    
    def serialize(self = None):
        return f'''"{self}"'''



class Op(Node):
    
    def serialize(self = None):
        return str(self)


VARIABLE = L('implementation_version') | L('platform_python_implementation') | L('implementation_name') | L('python_full_version') | L('platform_release') | L('platform_version') | L('platform_machine') | L('platform_system') | L('python_version') | L('sys_platform') | L('os_name') | L('os.name') | L('sys.platform') | L('platform.version') | L('platform.machine') | L('platform.python_implementation') | L('python_implementation') | L('extra')
ALIASES = {
    'os.name': 'os_name',
    'sys.platform': 'sys_platform',
    'platform.version': 'platform_version',
    'platform.machine': 'platform_machine',
    'platform.python_implementation': 'platform_python_implementation',
    'python_implementation': 'platform_python_implementation' }
VARIABLE.setParseAction((lambda s, l, t: Variable(ALIASES.get(t[0], t[0]))))
VERSION_CMP = L('===') | L('==') | L('>=') | L('<=') | L('!=') | L('~=') | L('>') | L('<')
MARKER_OP = VERSION_CMP | L('not in') | L('in')
MARKER_OP.setParseAction((lambda s, l, t: Op(t[0])))
MARKER_VALUE = QuotedString("'") | QuotedString('"')
MARKER_VALUE.setParseAction((lambda s, l, t: Value(t[0])))
BOOLOP = L('and') | L('or')
MARKER_VAR = VARIABLE | MARKER_VALUE
MARKER_ITEM = Group(MARKER_VAR + MARKER_OP + MARKER_VAR)
MARKER_ITEM.setParseAction((lambda s, l, t: tuple(t[0])))
LPAREN = L('(').suppress()
RPAREN = L(')').suppress()
MARKER_EXPR = Forward()
MARKER_ATOM = MARKER_ITEM | Group(LPAREN + MARKER_EXPR + RPAREN)
MARKER_EXPR << MARKER_ATOM + ZeroOrMore(BOOLOP + MARKER_EXPR)
MARKER = stringStart + MARKER_EXPR + stringEnd

def _coerce_parse_result(results = None):
    if isinstance(results, ParseResults):
        return (lambda .0: [ _coerce_parse_result(i) for i in .0 ])(results)


def _format_marker(marker = None, first = None):
    pass
# WARNING: Decompyle incomplete

_operators: Dict[(str, Operator)] = {
    'in': (lambda lhs, rhs: lhs in rhs),
    'not in': (lambda lhs, rhs: lhs not in rhs),
    '<': operator.lt,
    '<=': operator.le,
    '==': operator.eq,
    '!=': operator.ne,
    '>=': operator.ge,
    '>': operator.gt }

def _eval_op(lhs = None, op = None, rhs = None):
    pass
# WARNING: Decompyle incomplete


class Undefined:
    pass

_undefined = Undefined()

def _get_env(environment = None, name = None):
    value = environment.get(name, _undefined)
    if isinstance(value, Undefined):
        raise UndefinedEnvironmentName(f'''{name!r} does not exist in evaluation environment.''')


def _evaluate_markers(markers = None, environment = None):
    groups = [
        []]
# WARNING: Decompyle incomplete


def format_full_version(info = None):
    version = '{0.major}.{0.minor}.{0.micro}'.format(info)
    kind = info.releaselevel
    if kind != 'final':
        version += kind[0] + str(info.serial)
    return version


def default_environment():
    iver = format_full_version(sys.implementation.version)
    implementation_name = sys.implementation.name
    return {
        'implementation_name': implementation_name,
        'implementation_version': iver,
        'os_name': os.name,
        'platform_machine': platform.machine(),
        'platform_release': platform.release(),
        'platform_system': platform.system(),
        'platform_version': platform.version(),
        'python_full_version': platform.python_version(),
        'platform_python_implementation': platform.python_implementation(),
        'python_version': '.'.join(platform.python_version_tuple()[:2]),
        'sys_platform': sys.platform }


class Marker:
    
    def __init__(self = None, marker = None):
        pass
    # WARNING: Decompyle incomplete

    
    def __str__(self = None):
        return _format_marker(self._markers)

    
    def __repr__(self = None):
        return f'''<Marker(\'{self}\')>'''

    
    def evaluate(self = None, environment = None):
        '''Evaluate a marker.

        Return the boolean from evaluating the given marker against the
        environment. environment is an optional argument to override all or
        part of the determined environment.

        The environment is determined from the current Python process.
        '''
        current_environment = default_environment()
        if environment is not None:
            current_environment.update(environment)
        return _evaluate_markers(self._markers, current_environment)


