
'''Implements ThreadPoolExecutor.'''
__author__ = 'Brian Quinlan (brian@sweetapp.com)'
from concurrent.futures import _base
import itertools
import queue
import threading
import types
import weakref
import os
_threads_queues = weakref.WeakKeyDictionary()
_shutdown = False
_global_shutdown_lock = threading.Lock()

def _python_exit():
    global _shutdown
    with _global_shutdown_lock:
        _shutdown = True
        None(None, None, None)
# WARNING: Decompyle incomplete

threading._register_atexit(_python_exit)
if hasattr(os, 'register_at_fork'):
    os.register_at_fork(_global_shutdown_lock.acquire, _global_shutdown_lock._at_fork_reinit, _global_shutdown_lock.release, **('before', 'after_in_child', 'after_in_parent'))

class _WorkItem(object):
    
    def __init__(self, future, fn, args, kwargs):
        self.future = future
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    
    def run(self):
        if not self.future.set_running_or_notify_cancel():
            return None
    # WARNING: Decompyle incomplete

    __class_getitem__ = classmethod(types.GenericAlias)


def _worker(executor_reference, work_queue, initializer, initargs):
    pass
# WARNING: Decompyle incomplete


class BrokenThreadPool(_base.BrokenExecutor):
    '''
    Raised when a worker thread in a ThreadPoolExecutor failed initializing.
    '''
    pass


class ThreadPoolExecutor(_base.Executor):
    _counter = itertools.count().__next__
    
    def __init__(self, max_workers, thread_name_prefix, initializer, initargs = (None, '', None, ())):
        '''Initializes a new ThreadPoolExecutor instance.

        Args:
            max_workers: The maximum number of threads that can be used to
                execute the given calls.
            thread_name_prefix: An optional name prefix to give our threads.
            initializer: A callable used to initialize worker threads.
            initargs: A tuple of arguments to pass to the initializer.
        '''
        if max_workers is None:
            if not os.cpu_count():
                pass
            max_workers = min(32, 1 + 4)
        if max_workers <= 0:
            raise ValueError('max_workers must be greater than 0')
        if not None is not None and callable(initializer):
            raise TypeError('initializer must be a callable')
        self._max_workers = None
        self._work_queue = queue.SimpleQueue()
        self._idle_semaphore = threading.Semaphore(0)
        self._threads = set()
        self._broken = False
        self._shutdown = False
        self._shutdown_lock = threading.Lock()
        if not thread_name_prefix:
            pass
        self._thread_name_prefix = 'ThreadPoolExecutor-%d' % self._counter()
        self._initializer = initializer
        self._initargs = initargs

    
    def submit(self, fn, *args, **kwargs):
        pass
    # WARNING: Decompyle incomplete

    submit.__doc__ = _base.Executor.submit.__doc__
    
    def _adjust_thread_count(self):
        if self._idle_semaphore.acquire(0, **('timeout',)):
            return None
        
        def weakref_cb(_, q = (None._work_queue,)):
            q.put(None)

        num_threads = len(self._threads)
        if num_threads < self._max_workers:
            if not self._thread_name_prefix:
                pass
            thread_name = '%s_%d' % (self, num_threads)
            t = threading.Thread(thread_name, _worker, (weakref.ref(self, weakref_cb), self._work_queue, self._initializer, self._initargs), **('name', 'target', 'args'))
            t.start()
            self._threads.add(t)
            _threads_queues[t] = self._work_queue
            return None

    
    def _initializer_failed(self):
        pass
    # WARNING: Decompyle incomplete

    
    def shutdown(self = None, wait = (True,), *, cancel_futures):
        pass
    # WARNING: Decompyle incomplete

    shutdown.__doc__ = _base.Executor.shutdown.__doc__

