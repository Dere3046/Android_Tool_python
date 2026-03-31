
import ctypes
import weakref
from  import heap
from  import get_context
from context import reduction, assert_spawning
_ForkingPickler = reduction.ForkingPickler
__all__ = [
    'RawValue',
    'RawArray',
    'Value',
    'Array',
    'copy',
    'synchronized']
typecode_to_type = {
    'c': ctypes.c_char,
    'u': ctypes.c_wchar,
    'b': ctypes.c_byte,
    'B': ctypes.c_ubyte,
    'h': ctypes.c_short,
    'H': ctypes.c_ushort,
    'i': ctypes.c_int,
    'I': ctypes.c_uint,
    'l': ctypes.c_long,
    'L': ctypes.c_ulong,
    'q': ctypes.c_longlong,
    'Q': ctypes.c_ulonglong,
    'f': ctypes.c_float,
    'd': ctypes.c_double }

def _new_value(type_):
    size = ctypes.sizeof(type_)
    wrapper = heap.BufferWrapper(size)
    return rebuild_ctype(type_, wrapper, None)


def RawValue(typecode_or_type, *args):
    '''
    Returns a ctypes object allocated from shared memory
    '''
    type_ = typecode_to_type.get(typecode_or_type, typecode_or_type)
    obj = _new_value(type_)
    ctypes.memset(ctypes.addressof(obj), 0, ctypes.sizeof(obj))
# WARNING: Decompyle incomplete


def RawArray(typecode_or_type, size_or_initializer):
    '''
    Returns a ctypes array allocated from shared memory
    '''
    type_ = typecode_to_type.get(typecode_or_type, typecode_or_type)
    if isinstance(size_or_initializer, int):
        type_ = type_ * size_or_initializer
        obj = _new_value(type_)
        ctypes.memset(ctypes.addressof(obj), 0, ctypes.sizeof(obj))
        return obj
    type_ = None * len(size_or_initializer)
    result = _new_value(type_)
# WARNING: Decompyle incomplete


def Value(typecode_or_type = None, *, lock, ctx, *args):
    '''
    Return a synchronization wrapper for a Value
    '''
    pass
# WARNING: Decompyle incomplete


def Array(typecode_or_type = None, size_or_initializer = {
    'lock': True,
    'ctx': None }, *, lock, ctx):
    '''
    Return a synchronization wrapper for a RawArray
    '''
    obj = RawArray(typecode_or_type, size_or_initializer)
    if lock is False:
        return obj
    if None in (True, None):
        if not ctx:
            pass
        ctx = get_context()
        lock = ctx.RLock()
    if not hasattr(lock, 'acquire'):
        raise AttributeError("%r has no method 'acquire'" % lock)
    return None(obj, lock, ctx, **('ctx',))


def copy(obj):
    new_obj = _new_value(type(obj))
    ctypes.pointer(new_obj)[0] = obj
    return new_obj


def synchronized(obj, lock, ctx = (None, None)):
    pass
# WARNING: Decompyle incomplete


def reduce_ctype(obj):
    assert_spawning(obj)
    if isinstance(obj, ctypes.Array):
        return (rebuild_ctype, (obj._type_, obj._wrapper, obj._length_))
    return (None, (type(obj), obj._wrapper, None))


def rebuild_ctype(type_, wrapper, length):
    if length is not None:
        type_ = type_ * length
    _ForkingPickler.register(type_, reduce_ctype)
    buf = wrapper.create_memoryview()
    obj = type_.from_buffer(buf)
    obj._wrapper = wrapper
    return obj


def make_property(name):
    pass
# WARNING: Decompyle incomplete

template = '\ndef get%s(self):\n    self.acquire()\n    try:\n        return self._obj.%s\n    finally:\n        self.release()\ndef set%s(self, value):\n    self.acquire()\n    try:\n        self._obj.%s = value\n    finally:\n        self.release()\n%s = property(get%s, set%s)\n'
prop_cache = { }
class_cache = weakref.WeakKeyDictionary()

class SynchronizedBase(object):
    
    def __init__(self, obj, lock, ctx = (None, None)):
        self._obj = obj
        if lock:
            self._lock = lock
        elif not ctx:
            pass
        ctx = get_context(True, **('force',))
        self._lock = ctx.RLock()
        self.acquire = self._lock.acquire
        self.release = self._lock.release

    
    def __enter__(self):
        return self._lock.__enter__()

    
    def __exit__(self, *args):
        pass
    # WARNING: Decompyle incomplete

    
    def __reduce__(self):
        assert_spawning(self)
        return (synchronized, (self._obj, self._lock))

    
    def get_obj(self):
        return self._obj

    
    def get_lock(self):
        return self._lock

    
    def __repr__(self):
        return '<%s wrapper for %s>' % (type(self).__name__, self._obj)



class Synchronized(SynchronizedBase):
    value = make_property('value')


class SynchronizedArray(SynchronizedBase):
    
    def __len__(self):
        return len(self._obj)

    
    def __getitem__(self, i):
        pass
    # WARNING: Decompyle incomplete

    
    def __setitem__(self, i, value):
        pass
    # WARNING: Decompyle incomplete

    
    def __getslice__(self, start, stop):
        pass
    # WARNING: Decompyle incomplete

    
    def __setslice__(self, start, stop, values):
        pass
    # WARNING: Decompyle incomplete



class SynchronizedString(SynchronizedArray):
    value = make_property('value')
    raw = make_property('raw')

