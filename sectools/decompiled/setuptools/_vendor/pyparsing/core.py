
import os
import typing
from typing import NamedTuple, Union, Callable, Any, Generator, Tuple, List, TextIO, Set, Sequence
from abc import ABC, abstractmethod
from enum import Enum
import string
import copy
import warnings
import re
import sys
from collections.abc import Iterable
import traceback
import types
from operator import itemgetter
from functools import wraps
from threading import RLock
from pathlib import Path
from util import _FifoCache, _UnboundedCache, __config_flags, _collapse_string_to_ranges, _escape_regex_range_chars, _bslash, _flatten, LRUMemo as _LRUMemo, UnboundedMemo as _UnboundedMemo
from exceptions import *
from actions import *
from results import ParseResults, _ParseResultsWithOffset
from unicode import pyparsing_unicode
_MAX_INT = sys.maxsize
str_type: Tuple[(type, ...)] = (str, bytes)
if sys.version_info >= (3, 8):
    from functools import cached_property
else:
    
    class cached_property:
        
        def __init__(self, func):
            self._func = func

        
        def __get__(self, instance, owner = (None,)):
            ret = instance.__dict__[self._func.__name__] = self._func(instance)
            return ret



class __compat__(__config_flags):
    '''
    A cross-version compatibility configuration for pyparsing features that will be
    released in a future version. By setting values in this configuration to True,
    those features can be enabled in prior versions for compatibility development
    and testing.

    - ``collect_all_And_tokens`` - flag to enable fix for Issue #63 that fixes erroneous grouping
      of results names when an :class:`And` expression is nested within an :class:`Or` or :class:`MatchFirst`;
      maintained for compatibility, but setting to ``False`` no longer restores pre-2.3.1
      behavior
    '''
    _type_desc = 'compatibility'
    collect_all_And_tokens = True
    _all_names = (lambda .0: [ __ for __ in .0 if __.startswith('_') ])(locals())
    _fixed_names = '\n        collect_all_And_tokens\n        '.split()


class __diag__(__config_flags):
    _type_desc = 'diagnostic'
    warn_multiple_tokens_in_named_alternation = False
    warn_ungrouped_named_tokens_in_collection = False
    warn_name_set_on_empty_Forward = False
    warn_on_parse_using_empty_Forward = False
    warn_on_assignment_to_Forward = False
    warn_on_multiple_string_args_to_oneof = False
    warn_on_match_first_with_lshift_operator = False
    enable_debug_on_named_expressions = False
    _all_names = (lambda .0: [ __ for __ in .0 if __.startswith('_') ])(locals())
    _warning_names = (lambda .0: [ name for name in .0 if name.startswith('warn') ])(_all_names)
    _debug_names = (lambda .0: [ name for name in .0 if name.startswith('enable_debug') ])(_all_names)
    
    def enable_all_warnings(cls = None):
        for name in cls._warning_names:
            cls.enable(name)

    enable_all_warnings = None(enable_all_warnings)


class Diagnostics(Enum):
    """
    Diagnostic configuration (all default to disabled)
    - ``warn_multiple_tokens_in_named_alternation`` - flag to enable warnings when a results
      name is defined on a :class:`MatchFirst` or :class:`Or` expression with one or more :class:`And` subexpressions
    - ``warn_ungrouped_named_tokens_in_collection`` - flag to enable warnings when a results
      name is defined on a containing expression with ungrouped subexpressions that also
      have results names
    - ``warn_name_set_on_empty_Forward`` - flag to enable warnings when a :class:`Forward` is defined
      with a results name, but has no contents defined
    - ``warn_on_parse_using_empty_Forward`` - flag to enable warnings when a :class:`Forward` is
      defined in a grammar but has never had an expression attached to it
    - ``warn_on_assignment_to_Forward`` - flag to enable warnings when a :class:`Forward` is defined
      but is overwritten by assigning using ``'='`` instead of ``'<<='`` or ``'<<'``
    - ``warn_on_multiple_string_args_to_oneof`` - flag to enable warnings when :class:`one_of` is
      incorrectly called with multiple str arguments
    - ``enable_debug_on_named_expressions`` - flag to auto-enable debug on all subsequent
      calls to :class:`ParserElement.set_name`

    Diagnostics are enabled/disabled by calling :class:`enable_diag` and :class:`disable_diag`.
    All warnings can be enabled by calling :class:`enable_all_warnings`.
    """
    warn_multiple_tokens_in_named_alternation = 0
    warn_ungrouped_named_tokens_in_collection = 1
    warn_name_set_on_empty_Forward = 2
    warn_on_parse_using_empty_Forward = 3
    warn_on_assignment_to_Forward = 4
    warn_on_multiple_string_args_to_oneof = 5
    warn_on_match_first_with_lshift_operator = 6
    enable_debug_on_named_expressions = 7


def enable_diag(diag_enum = None):
    '''
    Enable a global pyparsing diagnostic flag (see :class:`Diagnostics`).
    '''
    __diag__.enable(diag_enum.name)


def disable_diag(diag_enum = None):
    '''
    Disable a global pyparsing diagnostic flag (see :class:`Diagnostics`).
    '''
    __diag__.disable(diag_enum.name)


def enable_all_warnings():
    '''
    Enable all global pyparsing diagnostic warnings (see :class:`Diagnostics`).
    '''
    __diag__.enable_all_warnings()

del __config_flags

def _should_enable_warnings(cmd_line_warn_options = None, warn_env_var = None):
    enable = bool(warn_env_var)
    for warn_opt in cmd_line_warn_options:
        (w_action, w_message, w_category, w_module, w_line) = (warn_opt + '::::').split(':')[:5]
        if not w_action.lower().startswith('i'):
            if w_message and w_category or w_module or w_module == 'pyparsing':
                enable = True
                continue
        if w_action.lower().startswith('i') and w_module in ('pyparsing', ''):
            enable = False
    return enable

if _should_enable_warnings(sys.warnoptions, os.environ.get('PYPARSINGENABLEALLWARNINGS')):
    enable_all_warnings()
_single_arg_builtins = {
    sum,
    len,
    sorted,
    reversed,
    list,
    tuple,
    set,
    any,
    all,
    min,
    max}
_generatorType = types.GeneratorType
ParseAction = Union[(Callable[([], Any)], Callable[([
    ParseResults], Any)], Callable[([
    int,
    ParseResults], Any)], Callable[([
    str,
    int,
    ParseResults], Any)])]
ParseCondition = Union[(Callable[([], bool)], Callable[([
    ParseResults], bool)], Callable[([
    int,
    ParseResults], bool)], Callable[([
    str,
    int,
    ParseResults], bool)])]
ParseFailAction = Callable[([
    str,
    int,
    'ParserElement',
    Exception], None)]
DebugStartAction = Callable[([
    str,
    int,
    'ParserElement',
    bool], None)]
DebugSuccessAction = Callable[([
    str,
    int,
    int,
    'ParserElement',
    ParseResults,
    bool], None)]
DebugExceptionAction = Callable[([
    str,
    int,
    'ParserElement',
    Exception,
    bool], None)]
alphas = string.ascii_uppercase + string.ascii_lowercase
identchars = pyparsing_unicode.Latin1.identchars
identbodychars = pyparsing_unicode.Latin1.identbodychars
nums = '0123456789'
hexnums = nums + 'ABCDEFabcdef'
alphanums = alphas + nums
printables = ''.join((lambda .0: [ c for c in .0 if c not in string.whitespace ])(string.printable))
_trim_arity_call_line: traceback.StackSummary = None

def _trim_arity(func, max_limit = (3,)):
    '''decorator to trim function calls to match the arity of the target'''
    global _trim_arity_call_line
    if func in _single_arg_builtins:
        return (lambda s = None, l = None, t = None: func(t))
    limit = None
    found_arity = False
    
    def extract_tb(tb, limit = (0,)):
        frames = traceback.extract_tb(tb, limit, **('limit',))
        frame_summary = frames[-1]
        return [
            frame_summary[:2]]

    LINE_DIFF = 7
    if not _trim_arity_call_line:
        pass
    _trim_arity_call_line = traceback.extract_stack(2, **('limit',))[-1]
    pa_call_line_synth = (_trim_arity_call_line[0], _trim_arity_call_line[1] + LINE_DIFF)
    
    def wrapper(*args):
        pass
    # WARNING: Decompyle incomplete

    func_name = getattr(func, '__name__', getattr(func, '__class__').__name__)
    wrapper.__name__ = func_name
    wrapper.__doc__ = func.__doc__
    return wrapper


def condition_as_parse_action(fn = None, message = None, fatal = None):
    '''
    Function to convert a simple predicate function that returns ``True`` or ``False``
    into a parse action. Can be used in places when a parse action is required
    and :class:`ParserElement.add_condition` cannot be used (such as when adding a condition
    to an operator level in :class:`infix_notation`).

    Optional keyword arguments:

    - ``message`` - define a custom message to be used in the raised exception
    - ``fatal`` - if True, will raise :class:`ParseFatalException` to stop parsing immediately;
      otherwise will raise :class:`ParseException`

    '''
    msg = message if message is not None else 'failed user-defined condition'
    exc_type = ParseFatalException if fatal else ParseException
    fn = _trim_arity(fn)
    
    def pa(s = None, l = None, t = None):
        if not bool(fn(s, l, t)):
            raise exc_type(s, l, msg)

    pa = None(pa)
    return pa


def _default_start_debug_action(instring = None, loc = None, expr = None, cache_hit = (False,)):
    cache_hit_str = '*' if cache_hit else ''
    print('{}Match {} at loc {}({},{})\n  {}\n  {}^'.format(cache_hit_str, expr, loc, lineno(loc, instring), col(loc, instring), line(loc, instring), ' ' * (col(loc, instring) - 1)))


def _default_success_debug_action(instring, startloc = None, endloc = None, expr = None, toks = (False,), cache_hit = ('instring', str, 'startloc', int, 'endloc', int, 'expr', 'ParserElement', 'toks', ParseResults, 'cache_hit', bool)):
    cache_hit_str = '*' if cache_hit else ''
    print('{}Matched {} -> {}'.format(cache_hit_str, expr, toks.as_list()))


def _default_exception_debug_action(instring = None, loc = None, expr = None, exc = (False,), cache_hit = ('instring', str, 'loc', int, 'expr', 'ParserElement', 'exc', Exception, 'cache_hit', bool)):
    cache_hit_str = '*' if cache_hit else ''
    print('{}Match {} failed, {} raised: {}'.format(cache_hit_str, expr, type(exc).__name__, exc))


def null_debug_action(*args):
    """'Do-nothing' debug action, to suppress debugging output during parsing."""
    pass


class ParserElement(ABC):
    '''Abstract base level parser element class.'''
    DEFAULT_WHITE_CHARS: str = ' \n\t\r'
    verbose_stacktrace: bool = False
    _literalStringClass: typing.Optional[type] = None
    
    def set_default_whitespace_chars(chars = None):
        '''
        Overrides the default whitespace chars

        Example::

            # default whitespace chars are space, <TAB> and newline
            Word(alphas)[1, ...].parse_string("abc def\\nghi jkl")  # -> [\'abc\', \'def\', \'ghi\', \'jkl\']

            # change to just treat newline as significant
            ParserElement.set_default_whitespace_chars(" \\t")
            Word(alphas)[1, ...].parse_string("abc def\\nghi jkl")  # -> [\'abc\', \'def\']
        '''
        ParserElement.DEFAULT_WHITE_CHARS = chars
        for expr in _builtin_exprs:
            if expr.copyDefaultWhiteChars:
                expr.whiteChars = set(chars)

    set_default_whitespace_chars = None(set_default_whitespace_chars)
    
    def inline_literals_using(cls = None):
        '''
        Set class to be used for inclusion of string literals into a parser.

        Example::

            # default literal class used is Literal
            integer = Word(nums)
            date_str = integer("year") + \'/\' + integer("month") + \'/\' + integer("day")

            date_str.parse_string("1999/12/31")  # -> [\'1999\', \'/\', \'12\', \'/\', \'31\']


            # change to Suppress
            ParserElement.inline_literals_using(Suppress)
            date_str = integer("year") + \'/\' + integer("month") + \'/\' + integer("day")

            date_str.parse_string("1999/12/31")  # -> [\'1999\', \'12\', \'31\']
        '''
        ParserElement._literalStringClass = cls

    inline_literals_using = None(inline_literals_using)
    
    class DebugActions(NamedTuple):
        debug_fail: typing.Optional[DebugExceptionAction] = 'ParserElement.DebugActions'

    
    def __init__(self = None, savelist = None):
        self.parseAction = list()
        self.failAction = None
        self.customName = None
        self._defaultName = None
        self.resultsName = None
        self.saveAsList = savelist
        self.skipWhitespace = True
        self.whiteChars = set(ParserElement.DEFAULT_WHITE_CHARS)
        self.copyDefaultWhiteChars = True
        self.mayReturnEmpty = False
        self.keepTabs = False
        self.ignoreExprs = list()
        self.debug = False
        self.streamlined = False
        self.mayIndexError = True
        self.errmsg = ''
        self.modalResults = True
        self.debugActions = self.DebugActions(None, None, None)
        self.callPreparse = True
        self.callDuringTry = False
        self.suppress_warnings_ = []

    
    def suppress_warning(self = None, warning_type = None):
        '''
        Suppress warnings emitted for a particular diagnostic on this expression.

        Example::

            base = pp.Forward()
            base.suppress_warning(Diagnostics.warn_on_parse_using_empty_Forward)

            # statement would normally raise a warning, but is now suppressed
            print(base.parseString("x"))

        '''
        self.suppress_warnings_.append(warning_type)
        return self

    
    def copy(self = None):
        '''
        Make a copy of this :class:`ParserElement`.  Useful for defining
        different parse actions for the same parsing pattern, using copies of
        the original parse element.

        Example::

            integer = Word(nums).set_parse_action(lambda toks: int(toks[0]))
            integerK = integer.copy().add_parse_action(lambda toks: toks[0] * 1024) + Suppress("K")
            integerM = integer.copy().add_parse_action(lambda toks: toks[0] * 1024 * 1024) + Suppress("M")

            print((integerK | integerM | integer)[1, ...].parse_string("5K 100 640K 256M"))

        prints::

            [5120, 100, 655360, 268435456]

        Equivalent form of ``expr.copy()`` is just ``expr()``::

            integerM = integer().add_parse_action(lambda toks: toks[0] * 1024 * 1024) + Suppress("M")
        '''
        cpy = copy.copy(self)
        cpy.parseAction = self.parseAction[:]
        cpy.ignoreExprs = self.ignoreExprs[:]
        if self.copyDefaultWhiteChars:
            cpy.whiteChars = set(ParserElement.DEFAULT_WHITE_CHARS)
        return cpy

    
    def set_results_name(self = None, name = None, list_all_matches = None, *, listAllMatches):
        '''
        Define name for referencing matching tokens as a nested attribute
        of the returned parse results.

        Normally, results names are assigned as you would assign keys in a dict:
        any existing value is overwritten by later values. If it is necessary to
        keep all values captured for a particular results name, call ``set_results_name``
        with ``list_all_matches`` = True.

        NOTE: ``set_results_name`` returns a *copy* of the original :class:`ParserElement` object;
        this is so that the client can define a basic element, such as an
        integer, and reference it in multiple places with different names.

        You can also set results names using the abbreviated syntax,
        ``expr("name")`` in place of ``expr.set_results_name("name")``
        - see :class:`__call__`. If ``list_all_matches`` is required, use
        ``expr("name*")``.

        Example::

            date_str = (integer.set_results_name("year") + \'/\'
                        + integer.set_results_name("month") + \'/\'
                        + integer.set_results_name("day"))

            # equivalent form:
            date_str = integer("year") + \'/\' + integer("month") + \'/\' + integer("day")
        '''
        if not listAllMatches:
            pass
        listAllMatches = list_all_matches
        return self._setResultsName(name, listAllMatches)

    
    def _setResultsName(self, name, listAllMatches = (False,)):
        if name is None:
            return self
        newself = None.copy()
        if name.endswith('*'):
            name = name[:-1]
            listAllMatches = True
        newself.resultsName = name
        newself.modalResults = not listAllMatches
        return newself

    
    def set_break(self = None, break_flag = None):
        '''
        Method to invoke the Python pdb debugger when this element is
        about to be parsed. Set ``break_flag`` to ``True`` to enable, ``False`` to
        disable.
        '''
        if break_flag:
            _parseMethod = self._parse
            
            def breaker(instring = None, loc = None, doActions = None, callPreParse = None):
                import pdb
                pdb.set_trace()
                return _parseMethod(instring, loc, doActions, callPreParse)

            breaker._originalParseMethod = _parseMethod
            self._parse = breaker
            return self
        if None(self._parse, '_originalParseMethod'):
            self._parse = self._parse._originalParseMethod
        return self

    
    def set_parse_action(self = None, *fns, **kwargs):
        '''
        Define one or more actions to perform when successfully matching parse element definition.

        Parse actions can be called to perform data conversions, do extra validation,
        update external data structures, or enhance or replace the parsed tokens.
        Each parse action ``fn`` is a callable method with 0-3 arguments, called as
        ``fn(s, loc, toks)`` , ``fn(loc, toks)`` , ``fn(toks)`` , or just ``fn()`` , where:

        - s   = the original string being parsed (see note below)
        - loc = the location of the matching substring
        - toks = a list of the matched tokens, packaged as a :class:`ParseResults` object

        The parsed tokens are passed to the parse action as ParseResults. They can be
        modified in place using list-style append, extend, and pop operations to update
        the parsed list elements; and with dictionary-style item set and del operations
        to add, update, or remove any named results. If the tokens are modified in place,
        it is not necessary to return them with a return statement.

        Parse actions can also completely replace the given tokens, with another ``ParseResults``
        object, or with some entirely different object (common for parse actions that perform data
        conversions). A convenient way to build a new parse result is to define the values
        using a dict, and then create the return value using :class:`ParseResults.from_dict`.

        If None is passed as the ``fn`` parse action, all previously added parse actions for this
        expression are cleared.

        Optional keyword arguments:

        - call_during_try = (default= ``False``) indicate if parse action should be run during
          lookaheads and alternate testing. For parse actions that have side effects, it is
          important to only call the parse action once it is determined that it is being
          called as part of a successful parse. For parse actions that perform additional
          validation, then call_during_try should be passed as True, so that the validation
          code is included in the preliminary "try" parses.

        Note: the default parsing behavior is to expand tabs in the input string
        before starting the parsing process.  See :class:`parse_string` for more
        information on parsing strings containing ``<TAB>`` s, and suggested
        methods to maintain a consistent view of the parsed string, the parse
        location, and line and column positions within the parsed string.

        Example::

            # parse dates in the form YYYY/MM/DD

            # use parse action to convert toks from str to int at parse time
            def convert_to_int(toks):
                return int(toks[0])

            # use a parse action to verify that the date is a valid date
            def is_valid_date(instring, loc, toks):
                from datetime import date
                year, month, day = toks[::2]
                try:
                    date(year, month, day)
                except ValueError:
                    raise ParseException(instring, loc, "invalid date given")

            integer = Word(nums)
            date_str = integer + \'/\' + integer + \'/\' + integer

            # add parse actions
            integer.set_parse_action(convert_to_int)
            date_str.set_parse_action(is_valid_date)

            # note that integer fields are now ints, not strings
            date_str.run_tests(\'\'\'
                # successful parse - note that integer fields were converted to ints
                1999/12/31

                # fail - invalid date
                1999/13/31
                \'\'\')
        '''
        if list(fns) == [
            None]:
            self.parseAction = []
            return self
        if not None((lambda .0: for fn in .0:
callable(fn))(fns)):
            raise TypeError('parse actions must be callable')
        self.parseAction = (lambda 