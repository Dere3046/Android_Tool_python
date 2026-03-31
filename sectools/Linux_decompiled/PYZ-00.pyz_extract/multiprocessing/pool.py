
__all__ = [
    'Pool',
    'ThreadPool']
import collections
import itertools
import os
import queue
import threading
import time
import traceback
import types
import warnings
from  import util
from  import get_context, TimeoutError
from connection import wait
INIT = 'INIT'
RUN = 'RUN'
CLOSE = 'CLOSE'
TERMINATE = 'TERMINATE'
job_counter = itertools.count()

def mapstar(args):
    pass
# WARNING: Decompyle incomplete


def starmapstar(args):
    return list(itertools.starmap(args[0], args[1]))


class RemoteTraceback(Exception):
    
    def __init__(self, tb):
        self.tb = tb

    
    def __str__(self):
        return self.tb



class ExceptionWithTraceback:
    
    def __init__(self, exc, tb):
        tb = traceback.format_exception(type(exc), exc, tb)
        tb = ''.join(tb)
        self.exc = exc
        self.tb = '\n"""\n%s"""' % tb

    
    def __reduce__(self):
        return (rebuild_exc, (self.exc, self.tb))



def rebuild_exc(exc, tb):
    exc.__cause__ = RemoteTraceback(tb)
    return exc


class MaybeEncodingError(Exception):
    '''Wraps possible unpickleable errors, so they can be
    safely sent through the socket.'''
    
    def __init__(self = None, exc = None, value = None):
        self.exc = repr(exc)
        self.value = repr(value)
        super(MaybeEncodingError, self).__init__(self.exc, self.value)

    
    def __str__(self):
        return "Error sending result: '%s'. Reason: '%s'" % (self.value, self.exc)

    
    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self)

    __classcell__ = None


def worker(inqueue, outqueue, initializer, initargs, maxtasks, wrap_exception = (None, (), None, False)):
    if maxtasks is not None:
        if not isinstance(maxtasks, int) or maxtasks >= 1:
            raise AssertionError('Maxtasks {!r} is not valid'.format(maxtasks))
        put = None.put
        get = inqueue.get
        if hasattr(inqueue, '_writer'):
            inqueue._writer.close()
            outqueue._reader.close()
# WARNING: Decompyle incomplete


def _helper_reraises_exception(ex):
    '''Pickle-able helper function for use by _guarded_task_generation.'''
    raise ex


class _PoolCache(dict):
    '''
    Class that implements a cache for the Pool class that will notify
    the pool management threads every time the cache is emptied. The
    notification is done by the use of a queue that is provided when
    instantiating the cache.
    '''
    
    def __init__(self = None, *, notifier, *args, **kwds):
        self.notifier = notifier
    # WARNING: Decompyle incomplete

    
    def __delitem__(self = None, item = None):
        super().__delitem__(item)
        if not self:
            self.notifier.put(None)
            return None

    __classcell__ = None


class Pool(object):
    '''
    Class which supports an async version of applying functions to arguments.
    '''
    _wrap_exception = True
    
    def Process(ctx, *args, **kwds):
        pass
    # WARNING: Decompyle incomplete

    Process = staticmethod(Process)
    
    def __init__(self, processes, initializer, initargs, maxtasksperchild, context = (None, None, (), None, None)):
        self._pool = []
        self._state = INIT
        if not context:
            pass
        self._ctx = get_context()
        self._setup_queues()
        self._taskqueue = queue.SimpleQueue()
        self._change_notifier = self._ctx.SimpleQueue()
        self._cache = _PoolCache(self._change_notifier, **('notifier',))
        self._maxtasksperchild = maxtasksperchild
        self._initializer = initializer
        self._initargs = initargs
        if processes is None:
            if not os.cpu_count():
                pass
            processes = 1
        if processes < 1:
            raise ValueError('Number of processes must be at least 1')
        if not None is not None and callable(initializer):
            raise TypeError('initializer must be a callable')
        self._processes = None
    # WARNING: Decompyle incomplete

    
    def __del__(self, _warn, RUN = (warnings.warn, RUN)):
        if self._state == RUN:
            _warn(f'''unclosed running multiprocessing pool {self!r}''', ResourceWarning, self, **('source',))
            if getattr(self, '_change_notifier', None) is not None:
                self._change_notifier.put(None)
                return None
            return None

    
    def __repr__(self):
        cls = self.__class__
        return f'''<{cls.__module__}.{cls.__qualname__} state={self._state} pool_size={len(self._pool)}>'''

    
    def _get_sentinels(self):
