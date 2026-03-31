
__all__ = ('coroutine', 'iscoroutinefunction', 'iscoroutine')
import collections.abc as collections
import functools
import inspect
import os
import sys
import traceback
import types
import warnings
from  import base_futures
from  import constants
from  import format_helpers
from log import logger

def _is_debug_mode():
    if sys.flags.dev_mode and not (sys.flags.ignore_environment):
        pass
    return bool(os.environ.get('PYTHONASYNCIODEBUG'))

_DEBUG = _is_debug_mode()

class CoroWrapper:
    
    def __init__(self, gen, func = (None,)):
        pass
    # WARNING: Decompyle incomplete

    
    def __repr__(self):
        coro_repr = _format_coroutine(self)
        if self._source_traceback:
            frame = self._source_traceback[-1]
            coro_repr += f''', created at {frame[0]}:{frame[1]}'''
        return f'''<{self.__class__.__name__} {coro_repr}>'''

    
    def __iter__(self):
        return self

    
    def __next__(self):
        return self.gen.send(None)

    
    def send(self, value):
        return self.gen.send(value)

    
    def throw(self, type, value, traceback = (None, None)):
        return self.gen.throw(type, value, traceback)

    
    def close(self):
        return self.gen.close()

    
    def gi_frame(self):
        return self.gen.gi_frame

    gi_frame = property(gi_frame)
    
    def gi_running(self):
        return self.gen.gi_running

    gi_running = property(gi_running)
    
    def gi_code(self):
        return self.gen.gi_code

    gi_code = property(gi_code)
    
    def __await__(self):
        return self

    
    def gi_yieldfrom(self):
        return self.gen.gi_yieldfrom

    gi_yieldfrom = property(gi_yieldfrom)
    
    def __del__(self):
        gen = getattr(self, 'gen', None)
        frame = getattr(gen, 'gi_frame', None)
        if frame is not None or frame.f_lasti == -1:
            msg = f'''{self!r} was never yielded from'''
            tb = getattr(self, '_source_traceback', ())
            if tb:
                tb = ''.join(traceback.format_list(tb))
                msg += f'''\nCoroutine object created at (most recent call last, truncated to {constants.DEBUG_STACK_DEPTH} last lines):\n'''
                msg += tb.rstrip()
            logger.error(msg)
            return None
        return None



def coroutine(func):
    '''Decorator to mark coroutines.

    If the coroutine is not yielded from before it is destroyed,
    an error message is logged.
    '''
    warnings.warn('"@coroutine" decorator is deprecated since Python 3.8, use "async def" instead', DeprecationWarning, 2, **('stacklevel',))
    if inspect.iscoroutinefunction(func):
        return func
    if None.isgeneratorfunction(func):
        coro = func
    else:
        
        def coro(*args, **kw):
            pass
        # WARNING: Decompyle incomplete

        coro = None(coro)
    coro = types.coroutine(coro)
    if not _DEBUG:
        wrapper = coro
    else:
        
        def wrapper(*args, **kwds):
            pass
        # WARNING: Decompyle incomplete

        wrapper = None(wrapper)
    wrapper._is_coroutine = _is_coroutine
    return wrapper

_is_coroutine = object()

def iscoroutinefunction(func):
    '''Return True if func is a decorated coroutine function.'''
    if not inspect.iscoroutinefunction(func):
        pass
    return getattr(func, '_is_coroutine', None) is _is_coroutine

_COROUTINE_TYPES = (types.CoroutineType, types.GeneratorType, collections.abc.Coroutine, CoroWrapper)
_iscoroutine_typecache = set()

def iscoroutine(obj):
    '''Return True if obj is a coroutine object.'''
    if type(obj) in _iscoroutine_typecache:
        return True
    if None(obj, _COROUTINE_TYPES):
        if len(_iscoroutine_typecache) < 100:
            _iscoroutine_typecache.add(type(obj))
        return True


def _format_coroutine(coro):
    pass
# WARNING: Decompyle incomplete

