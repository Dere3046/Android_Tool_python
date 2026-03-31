
from __future__ import annotations
import operator
import os
import platform
import sys
from typing import AbstractSet, Any, Callable, Literal, TypedDict, Union, cast
from _parser import MarkerAtom, MarkerList, Op, Value, Variable
from _parser import parse_marker as _parse_marker
from _tokenizer import ParserSyntaxError
from specifiers import InvalidSpecifier, Specifier
from utils import canonicalize_name
__all__ = [
    'EvaluateContext',
    'InvalidMarker',
    'Marker',
    'UndefinedComparison',
    'UndefinedEnvironmentName',
    'default_environment']
Operator = Callable[([
    str,
    Union[(str, AbstractSet[str])]], bool)]
EvaluateContext = Literal[('metadata', 'lock_file', 'requirement')]
MARKERS_ALLOWING_SET = {
    'extras',
    'dependency_groups'}

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


class Environment(TypedDict):
    sys_platform: 'str' = 'Environment'


def _normalize_extra_values(results = None):
    '''
    Normalize extra values.
    '''
    if isinstance(results[0], tuple):
        (lhs, op, rhs) = results[0]
        if isinstance(lhs, Variable) and lhs.value == 'extra':
            normalized_extra = canonicalize_name(rhs.value)
            rhs = Value(normalized_extra)
        elif isinstance(rhs, Variable) and rhs.value == 'extra':
            normalized_extra = canonicalize_name(lhs.value)
            lhs = Value(normalized_extra)
        results[0] = (lhs, op, rhs)
    return results


def _format_marker(marker = None, first = None):
    pass
# WARNING: Decompyle incomplete

_operators: 'dict[str, Operator]' = {
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


def _normalize(lhs = None, rhs = None, key = None):
    pass
# WARNING: Decompyle incomplete


def _evaluate_markers(markers = None, environment = None):
    groups = [
        []]
# WARNING: Decompyle incomplete


def format_full_version(info = None):
    version = f'''{info.major}.{info.minor}.{info.micro}'''
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

    
    def __hash__(self = None):
        return hash((self.__class__.__name__, str(self)))

    
    def __eq__(self = None, other = None):
        if not isinstance(other, Marker):
            return NotImplemented
        return None(self) == str(other)

    
    def evaluate(self = None, environment = None, context = None):
        '''Evaluate a marker.

        Return the boolean from evaluating the given marker against the
        environment. environment is an optional argument to override all or
        part of the determined environment. The *context* parameter specifies what
        context the markers are being evaluated for, which influences what markers
        are considered valid. Acceptable values are "metadata" (for core metadata;
        default), "lock_file", and "requirement" (i.e. all other situations).

        The environment is determined from the current Python process.
        '''
        current_environment = cast('dict[str, str | AbstractSet[str]]', default_environment())
        if context == 'lock_file':
            current_environment.update(frozenset(), frozenset(), **('extras', 'dependency_groups'))
        elif context == 'metadata':
            current_environment['extra'] = ''
        if environment is not None:
            current_environment.update(environment)
            if 'extra' in current_environment and current_environment['extra'] is None:
                current_environment['extra'] = ''
        return _evaluate_markers(self._markers, _repair_python_full_version(current_environment))



def _repair_python_full_version(env = None):
    '''
    Work around platform.python_version() returning something that is not PEP 440
    compliant for non-tagged Python builds.
    '''
    python_full_version = cast(str, env['python_full_version'])
    if python_full_version.endswith('+'):
        env['python_full_version'] = f'''{python_full_version}local'''
    return env

