
from __future__ import annotations
import enum
import sys
import types
import typing
import warnings

class CryptographyDeprecationWarning(UserWarning):
    pass

DeprecatedIn36 = CryptographyDeprecationWarning
DeprecatedIn37 = CryptographyDeprecationWarning
DeprecatedIn40 = CryptographyDeprecationWarning
DeprecatedIn41 = CryptographyDeprecationWarning
DeprecatedIn42 = CryptographyDeprecationWarning
DeprecatedIn43 = CryptographyDeprecationWarning

def _check_bytes(name = None, value = None):
    if not isinstance(value, bytes):
        raise TypeError(f'''{name} must be bytes''')


def _check_byteslike(name = None, value = None):
    pass
# WARNING: Decompyle incomplete


def int_to_bytes(integer = None, length = None):
    if length == 0:
        raise ValueError("length argument can't be 0")
    if not length and (integer.bit_length() + 7) // 8:
        pass
    return None.to_bytes(1, 'big')


class InterfaceNotImplemented(Exception):
    pass


class _DeprecatedValue:
    
    def __init__(self = None, value = None, message = None, warning_class = ('value', 'object', 'message', 'str')):
        self.value = value
        self.message = message
        self.warning_class = warning_class



class _ModuleWithDeprecations(types.ModuleType):
    
    def __init__(self = None, module = None):
        super().__init__(module.__name__)
        self.__dict__['_module'] = module

    
    def __getattr__(self = None, attr = None):
        obj = getattr(self._module, attr)
        if isinstance(obj, _DeprecatedValue):
            warnings.warn(obj.message, obj.warning_class, 2, **('stacklevel',))
            obj = obj.value
        return obj

    
    def __setattr__(self = None, attr = None, value = None):
        setattr(self._module, attr, value)

    
    def __delattr__(self = None, attr = None):
        obj = getattr(self._module, attr)
        if isinstance(obj, _DeprecatedValue):
            warnings.warn(obj.message, obj.warning_class, 2, **('stacklevel',))
        delattr(self._module, attr)

    
    def __dir__(self = None):
        pass

    __classcell__ = None


def deprecated(value = None, module_name = None, message = None, warning_class = (None,), name = ('value', 'object', 'module_name', 'str', 'message', 'str', 'warning_class', 'type[Warning]', 'name', 'str | None', 'return', '_DeprecatedValue')):
    module = sys.modules[module_name]
    if not isinstance(module, _ModuleWithDeprecations):
        sys.modules[module_name] = module = _ModuleWithDeprecations(module)
    dv = _DeprecatedValue(value, message, warning_class)
    if name is not None:
        setattr(module, name, dv)
    return dv


def cached_property(func = None):
    cached_name = f'''_cached_{func}'''
    sentinel = object()
    
    def inner(instance = None):
        cache = getattr(instance, cached_name, sentinel)
        if cache is not sentinel:
            return cache
        result = None(instance)
        setattr(instance, cached_name, result)
        return result

    return property(inner)


class Enum(enum.Enum):
    
    def __repr__(self = None):
        return f'''<{self.__class__.__name__}.{self._name_}: {self._value_!r}>'''

    
    def __str__(self = None):
        return f'''{self.__class__.__name__}.{self._name_}'''


