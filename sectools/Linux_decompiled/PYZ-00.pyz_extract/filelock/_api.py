
import logging
import os
import time
import warnings
from abc import ABC, abstractmethod
from threading import Lock
from types import TracebackType
from typing import Any, Optional, Type, Union
from _error import Timeout
_LOGGER = logging.getLogger('filelock')

class AcquireReturnProxy:
    '''A context aware object that will release the lock file when exiting.'''
    
    def __init__(self = None, lock = None):
        self.lock = lock

    
    def __enter__(self = None):
        return self.lock

    
    def __exit__(self = None, exc_type = None, exc_value = None, traceback = ('exc_type', Optional[Type[BaseException]], 'exc_value', Optional[BaseException], 'traceback', Optional[TracebackType], 'return', None)):
        self.lock.release()



class BaseFileLock(ABC):
    '''Abstract base class for a file lock object.'''
    
    def __init__(self = None, lock_file = None, timeout = None):
        '''
        Create a new lock object.

        :param lock_file: path to the file
        :param timeout: default timeout when acquiring the lock. It will be used as fallback value in the acquire
        method, if no timeout value (``None``) is given. If you want to disable the timeout, set it to a negative value.
         A timeout of 0 means, that there is exactly one attempt to acquire the file lock.
        '''
        self._lock_file = os.fspath(lock_file)
        self._lock_file_fd = None
        self.timeout = timeout
        self._thread_lock = Lock()
        self._lock_counter = 0

    
    def lock_file(self = None):
        ''':return: path to the lock file'''
        return self._lock_file

    lock_file = None(lock_file)
    
    def timeout(self = None):
        '''
        :return: the default timeout value

        .. versionadded:: 2.0.0
        '''
        return self._timeout

    timeout = None(timeout)
    
    def timeout(self = None, value = None):
        '''
        Change the default timeout value.

        :param value: the new value
        '''
        self._timeout = float(value)

    timeout = None(timeout)
    
    def _acquire(self = None):
        '''If the file lock could be acquired, self._lock_file_fd holds the file descriptor of the lock file.'''
        raise NotImplementedError

    _acquire = None(_acquire)
    
    def _release(self = None):
        '''Releases the lock and sets self._lock_file_fd to None.'''
        raise NotImplementedError

    _release = None(_release)
    
    def is_locked(self = None):
        '''

        :return: A boolean indicating if the lock file is holding the lock currently.

        .. versionchanged:: 2.0.0

            This was previously a method and is now a property.
        '''
        return self._lock_file_fd is not None

    is_locked = None(is_locked)
    
    def acquire(self = None, timeout = None, poll_interval = None, poll_intervall = (None, 0.05, None)):
        '''
        Try to acquire the file lock.

        :param timeout: maximum wait time for acquiring the lock, ``None`` means use the default :attr:`~timeout` is and
         if ``timeout < 0``, there is no timeout and this method will block until the lock could be acquired
        :param poll_interval: interval of trying to acquire the lock file
        :param poll_intervall: deprecated, kept for backwards compatibility, use ``poll_interval`` instead
        :raises Timeout: if fails to acquire lock within the timeout period
        :return: a context object that will unlock the file when the context is exited

        .. code-block:: python

            # You can use this method in the context manager (recommended)
            with lock.acquire():
                pass

            # Or use an equivalent try-finally construct:
            lock.acquire()
            try:
                pass
            finally:
                lock.release()

        .. versionchanged:: 2.0.0

            This method returns now a *proxy* object instead of *self*, so that it can be used in a with statement             without side effects.

        '''
        if timeout is None:
            timeout = self.timeout
        if poll_intervall is not None:
            msg = 'use poll_interval instead of poll_intervall'
            warnings.warn(msg, DeprecationWarning)
            poll_interval = poll_intervall
        with self._thread_lock:
            self._lock_counter += 1
            self(None, None, None)
    # WARNING: Decompyle incomplete

    
    def release(self = None, force = None):
        '''
        Releases the file lock. Please note, that the lock is only completely released, if the lock counter is 0. Also
        note, that the lock file itself is not automatically deleted.

        :param force: If true, the lock counter is ignored and the lock is released in every case/
        '''
        pass
    # WARNING: Decompyle incomplete

    
    def __enter__(self = None):
        '''
        Acquire the lock.

        :return: the lock object
        '''
        self.acquire()
        return self

    
    def __exit__(self = None, exc_type = None, exc_value = None, traceback = ('exc_type', Optional[Type[BaseException]], 'exc_value', Optional[BaseException], 'traceback', Optional[TracebackType], 'return', None)):
        '''
        Release the lock.

        :param exc_type: the exception type if raised
        :param exc_value: the exception value if raised
        :param traceback: the exception traceback if raised
        '''
        self.release()

    
    def __del__(self = None):
        '''Called when the lock object is deleted.'''
        self.release(True, **('force',))


__all__ = [
    'BaseFileLock',
    'AcquireReturnProxy']
