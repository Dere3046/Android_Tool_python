
import abc
import builtins
import collections
import collections.abc as collections
import contextlib
import enum
import functools
import inspect
import io
import keyword
import operator
import sys
import types as _types
import typing
import warnings
if sys.version_info >= (3, 14):
    import annotationlib
__all__ = [
    'Any',
    'ClassVar',
    'Concatenate',
    'Final',
    'LiteralString',
    'ParamSpec',
    'ParamSpecArgs',
    'ParamSpecKwargs',
    'Self',
    'Type',
    'TypeVar',
    'TypeVarTuple',
    'Unpack',
    'Awaitable',
    'AsyncIterator',
    'AsyncIterable',
    'Coroutine',
    'AsyncGenerator',
    'AsyncContextManager',
    'Buffer',
    'ChainMap',
    'ContextManager',
    'Counter',
    'Deque',
    'DefaultDict',
    'NamedTuple',
    'OrderedDict',
    'TypedDict',
    'SupportsAbs',
    'SupportsBytes',
    'SupportsComplex',
    'SupportsFloat',
    'SupportsIndex',
    'SupportsInt',
    'SupportsRound',
    'Reader',
    'Writer',
    'Annotated',
    'assert_never',
    'assert_type',
    'clear_overloads',
    'dataclass_transform',
    'deprecated',
    'Doc',
    'evaluate_forward_ref',
    'get_overloads',
    'final',
    'Format',
    'get_annotations',
    'get_args',
    'get_origin',
    'get_original_bases',
    'get_protocol_members',
    'get_type_hints',
    'IntVar',
    'is_protocol',
    'is_typeddict',
    'Literal',
    'NewType',
    'overload',
    'override',
    'Protocol',
    'Sentinel',
    'reveal_type',
    'runtime',
    'runtime_checkable',
    'Text',
    'TypeAlias',
    'TypeAliasType',
    'TypeForm',
    'TypeGuard',
    'TypeIs',
    'TYPE_CHECKING',
    'Never',
    'NoReturn',
    'ReadOnly',
    'Required',
    'NotRequired',
    'NoDefault',
    'NoExtraItems',
    'AbstractSet',
    'AnyStr',
    'BinaryIO',
    'Callable',
    'Collection',
    'Container',
    'Dict',
    'ForwardRef',
    'FrozenSet',
    'Generator',
    'Generic',
    'Hashable',
    'IO',
    'ItemsView',
    'Iterable',
    'Iterator',
    'KeysView',
    'List',
    'Mapping',
    'MappingView',
    'Match',
    'MutableMapping',
    'MutableSequence',
    'MutableSet',
    'Optional',
    'Pattern',
    'Reversible',
    'Sequence',
    'Set',
    'Sized',
    'TextIO',
    'Tuple',
    'Union',
    'ValuesView',
    'cast',
    'no_type_check',
    'no_type_check_decorator']
PEP_560 = True
GenericMeta = type
_PEP_696_IMPLEMENTED = sys.version_info >= (3, 13, 0, 'beta')
_FORWARD_REF_HAS_CLASS = '__forward_is_class__' in typing.ForwardRef.__slots__

class _Sentinel:
    
    def __repr__(self):
        return '<sentinel>'


_marker = _Sentinel()
if sys.version_info >= (3, 10):
    
    def _should_collect_from_parameters(t):
        return isinstance(t, (typing._GenericAlias, _types.GenericAlias, _types.UnionType))

else:
    
    def _should_collect_from_parameters(t):
        return isinstance(t, (typing._GenericAlias, _types.GenericAlias))

NoReturn = typing.NoReturn
T = typing.TypeVar('T')
KT = typing.TypeVar('KT')
VT = typing.TypeVar('VT')
T_co = typing.TypeVar('T_co', True, **('covariant',))
T_contra = typing.TypeVar('T_contra', True, **('contravariant',))
if sys.version_info >= (3, 11):
    from typing import Any
else:
    
    class _AnyMeta(type):
        
        def __instancecheck__(self = None, obj = None):
            if self is Any:
                raise TypeError('typing_extensions.Any cannot be used with isinstance()')
            return None().__instancecheck__(obj)

        
        def __repr__(self = None):
            if self is Any:
                return 'typing_extensions.Any'
            return None().__repr__()

        __classcell__ = None

    Any = <NODE:27>((lambda : __doc__ = 'Special type indicating an unconstrained type.\n        - Any is compatible with every type.\n        - Any assumed to have all methods.\n        - All values assumed to be instances of Any.\n        Note that all the above statements are true from the point of view of\n        static type checkers. At runtime, Any should not be used with instance\n        checks.\n        '
def __new__(cls = None, *args, **kwargs):
if cls is Any:
raise TypeError('Any cannot be instantiated')# WARNING: Decompyle incomplete
__classcell__ = None), 'Any', _AnyMeta, **('metaclass',))
ClassVar = typing.ClassVar
_ExtensionsSpecialForm = <NODE:27>((lambda : 
def __repr__(self):
'typing_extensions.' + self._name), '_ExtensionsSpecialForm', typing._SpecialForm, True, **('_root',))
Final = typing.Final
if sys.version_info >= (3, 11):
    final = typing.final
else:
    
    def final(f):
        '''This decorator can be used to indicate to type checkers that
        the decorated method cannot be overridden, and decorated class
        cannot be subclassed. For example:

            class Base:
                @final
                def done(self) -> None:
                    ...
            class Sub(Base):
                def done(self) -> None:  # Error reported by type checker
                    ...
            @final
            class Leaf:
                ...
            class Other(Leaf):  # Error reported by type checker
                ...

        There is no runtime checking of these properties. The decorator
        sets the ``__final__`` attribute to ``True`` on the decorated object
        to allow runtime introspection.
        '''
        pass
    # WARNING: Decompyle incomplete


def IntVar(name):
    return typing.TypeVar(name)

if sys.version_info >= (3, 10, 1):
    Literal = typing.Literal
else:
    
    def _flatten_literal_params(parameters):
        '''An internal helper for Literal creation: flatten Literals among parameters'''
        params = []
        for p in parameters:
            if isinstance(p, _LiteralGenericAlias):
                params.extend(p.__args__)
                continue
            params.append(p)
        return tuple(params)

    
    def _value_and_type_iter(params):
        for p in params:
            yield (p, type(p))

    _LiteralGenericAlias = <NODE:27>((lambda : 
def __eq__(self, other):
if not isinstance(other, _LiteralGenericAlias):
NotImplementedthese_args_deduped = None(_value_and_type_iter(self.__args__))other_args_deduped = set(_value_and_type_iter(other.__args__))these_args_deduped == other_args_deduped
def __hash__(self):
hash(frozenset(_value_and_type_iter(self.__args__)))), '_LiteralGenericAlias', typing._GenericAlias, True, **('_root',))
    _LiteralForm = <NODE:27>((lambda : 
def __init__(self = None, doc = None):
self._name = 'Literal'self._doc = self.__doc__ = doc
def __getitem__(self, parameters):
if not isinstance(parameters, tuple):
parameters = (parameters,)parameters = _flatten_literal_params(parameters)val_type_pairs = list(_value_and_type_iter(parameters))# WARNING: Decompyle incomplete
), '_LiteralForm', _ExtensionsSpecialForm, True, **('_root',))
    Literal = _LiteralForm("                           A type that can be used to indicate to type checkers\n                           that the corresponding value has a value literally equivalent\n                           to the provided parameter. For example:\n\n                               var: Literal[4] = 4\n\n                           The type checker understands that 'var' is literally equal to\n                           the value 4 and no other value.\n\n                           Literal[...] cannot be subclassed. There is no runtime\n                           checking verifying that the parameter is actually a value\n                           instead of a type.", **('doc',))
_overload_dummy = typing._overload_dummy
if hasattr(typing, 'get_overloads'):
    overload = typing.overload
    get_overloads = typing.get_overloads
    clear_overloads = typing.clear_overloads
else:
    _overload_registry = collections.defaultdict(functools.partial(collections.defaultdict, dict))
    
    def overload(func):
        '''Decorator for overloaded functions/methods.

        In a stub file, place two or more stub definitions for the same
        function in a row, each decorated with @overload.  For example:

        @overload
        def utf8(value: None) -> None: ...
        @overload
        def utf8(value: bytes) -> bytes: ...
        @overload
        def utf8(value: str) -> bytes: ...

        In a non-stub file (i.e. a regular .py file), do the same but
        follow it with an implementation.  The implementation should *not*
        be decorated with @overload.  For example:

        @overload
        def utf8(value: None) -> None: ...
        @overload
        def utf8(value: bytes) -> bytes: ...
        @overload
        def utf8(value: str) -> bytes: ...
        def utf8(value):
            # implementation goes here

        The overloads for a function can be retrieved at runtime using the
        get_overloads() function.
        '''
        f = getattr(func, '__func__', func)
    # WARNING: Decompyle incomplete

    
    def get_overloads(func):
        '''Return all defined overloads for *func* as a sequence.'''
        f = getattr(func, '__func__', func)
        if f.__module__ not in _overload_registry:
            return []
        mod_dict = None[f.__module__]
        if f.__qualname__ not in mod_dict:
            return []
        return None(mod_dict[f.__qualname__].values())

    
    def clear_overloads():
        '''Clear all overloads in the registry.'''
        _overload_registry.clear()

Type = typing.Type
Awaitable = typing.Awaitable
Coroutine = typing.Coroutine
AsyncIterable = typing.AsyncIterable
AsyncIterator = typing.AsyncIterator
Deque = typing.Deque
DefaultDict = typing.DefaultDict
OrderedDict = typing.OrderedDict
Counter = typing.Counter
ChainMap = typing.ChainMap
Text = typing.Text
TYPE_CHECKING = typing.TYPE_CHECKING
if sys.version_info >= (3, 13, 0, 'beta'):
    from typing import AsyncContextManager, AsyncGenerator, ContextManager, Generator
else:
    
    def _is_dunder(attr):
        if attr.startswith('__'):
            pass
        return attr.endswith('__')

    _SpecialGenericAlias = <NODE:27>((lambda : 
def __init__(self = None, origin = None, nparams = None, *, inst, name, defaults):
super().__init__(origin, nparams, inst, name, **('inst', 'name'))self._defaults = defaults
def __setattr__(self, attr, val):
allowed_attrs = {
'_name',
'_inst',
'_nparams',
'_defaults'}if _is_dunder(attr) or attr in allowed_attrs:
object.__setattr__(self, attr, val)NoneNone(self.__origin__, attr, val)
def __getitem__(self, params):
