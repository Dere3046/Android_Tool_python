
import os
import itertools
import sys
import weakref
import atexit
import threading
from subprocess import _args_from_interpreter_flags
from  import process
__all__ = [
    'sub_debug',
    'debug',
    'info',
    'sub_warning',
    'get_logger',
    'log_to_stderr',
    'get_temp_dir',
    'register_after_fork',
    'is_exiting',
    'Finalize',
    'ForkAwareThreadLock',
    'ForkAwareLocal',
    'close_all_fds_except',
    'SUBDEBUG',
    'SUBWARNING']
NOTSET = 0
SUBDEBUG = 5
DEBUG = 10
INFO = 20
SUBWARNING = 25
LOGGER_NAME = 'multiprocessing'
DEFAULT_LOGGING_FORMAT = '[%(levelname)s/%(processName)s] %(message)s'
_logger = None
_log_to_stderr = False

def sub_debug(msg, *args):
    pass
# WARNING: Decompyle incomplete


def debug(msg, *args):
    pass
# WARNING: Decompyle incomplete


def info(msg, *args):
    pass
# WARNING: Decompyle incomplete


def sub_warning(msg, *args):
    pass
# WARNING: Decompyle incomplete


def get_logger():
    '''
    Returns logger used by multiprocessing
    '''
    global _logger
    import logging
    logging._acquireLock()
# WARNING: Decompyle incomplete


def log_to_stderr(level = (None,)):
    '''
    Turn on logging and add a handler which prints to stderr
    '''
    global _log_to_stderr
    import logging
    logger = get_logger()
    formatter = logging.Formatter(DEFAULT_LOGGING_FORMAT)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    if level:
        logger.setLevel(level)
    _log_to_stderr = True
    return _logger


def _platform_supports_abstract_sockets():
    if sys.platform == 'linux':
        return True
    if None(sys, 'getandroidapilevel'):
        return True


def is_abstract_socket_namespace(address):
    if not address:
        return False
    if None(address, bytes):
        return address[0] == 0
    if None(address, str):
        return address[0] == '\x00'
    raise None('address type of {address!r} unrecognized')

abstract_sockets_supported = _platform_supports_abstract_sockets()

def _remove_temp_dir(rmtree, tempdir):
    rmtree(tempdir)
    current_process = process.current_process()
    if current_process is not None:
        current_process._config['tempdir'] = None
        return None


def get_temp_dir():
    tempdir = process.current_process()._config.get('tempdir')
    if tempdir is None:
        import shutil
        import tempfile
        tempdir = tempfile.mkdtemp('pymp-', **('prefix',))
        info('created temp directory %s', tempdir)
        Finalize(None, _remove_temp_dir, (shutil.rmtree, tempdir), -100, **('args', 'exitpriority'))
        process.current_process()._config['tempdir'] = tempdir
    return tempdir

_afterfork_registry = weakref.WeakValueDictionary()
_afterfork_counter = itertools.count()

def _run_after_forkers():
    items = list(_afterfork_registry.items())
    items.sort()
# WARNING: Decompyle incomplete


def register_after_fork(obj, func):
    _afterfork_registry[(next(_afterfork_counter), id(obj), func)] = obj

_finalizer_registry = { }
_finalizer_counter = itertools.count()

class Finalize(object):
    '''
    Class which supports object finalization using weakrefs
    '''
    
    def __init__(self, obj, callback, args, kwargs, exitpriority = ((), None, None)):
        if not exitpriority is not None and isinstance(exitpriority, int):
            raise TypeError('Exitpriority ({0!r}) must be None or int, not {1!s}'.format(exitpriority, type(exitpriority)))
        if None is not None:
            self._weakref = weakref.ref(obj, self)
        elif exitpriority is None:
            raise ValueError('Without object, exitpriority cannot be None')
        self._callback = callback
        self._args = args
        if not kwargs:
            pass
        self._kwargs = { }
        self._key = (exitpriority, next(_finalizer_counter))
        self._pid = os.getpid()
        _finalizer_registry[self._key] = self

    
    def __call__(self, wr, _finalizer_registry, sub_debug, getpid = (None, _finalizer_registry, sub_debug, os.getpid)):
        '''
        Run the callback unless it has already been called or cancelled
        '''
        pass
    # WARNING: Decompyle incomplete

    
    def cancel(self):
        '''
        Cancel finalization of the object
        '''
        pass
    # WARNING: Decompyle incomplete

    
    def still_active(self):
        '''
        Return whether this finalizer is still waiting to invoke callback
        '''
        return self._key in _finalizer_registry

    
    def __repr__(self):
        pass
    # WARNING: Decompyle incomplete



def _run_finalizers(minpriority = (None,)):
    '''
    Run all finalizers whose exit priority is not None and at least minpriority

    Finalizers with highest priority are called first; finalizers with
    the same priority will be called in reverse order of creation.
    '''
    if _finalizer_registry is None:
        return None
    if None is None:
        
        f = lambda p: p[0] is not None
    else:
        
        f = lambda p = None: if p[0] is not None:
passp[0] >= minpriority
    keys = (lambda .0 = None: [ key for key in .0 if f(key) ])(list(_finalizer_registry))
    keys.sort(True, **('reverse',))
# WARNING: Decompyle incomplete


def is_exiting():
    '''
    Returns true if the process is shutting down
    '''
    if not _exiting:
        pass
    return _exiting is None

_exiting = False

def _exit_function(info, debug, _run_finalizers, active_children, current_process = (info, debug, _run_finalizers, process.active_children, process.current_process)):
    global _exiting
    if not _exiting:
        _exiting = True
        info('process shutting down')
        debug('running all "atexit" finalizers with priority >= 0')
        _run_finalizers(0)
        if current_process() is not None:
            for p in active_children():
                if p.daemon:
                    info('calling terminate() for daemon %s', p.name)
                    p._popen.terminate()
            for p in active_children():
                info('calling join() for process %s', p.name)
                p.join()
        debug('running the remaining "atexit" finalizers')
        _run_finalizers()
        return None

atexit.register(_exit_function)

class ForkAwareThreadLock(object):
    
    def __init__(self):
        self._lock = threading.Lock()
        self.acquire = self._lock.acquire
        self.release = self._lock.release
        register_after_fork(self, ForkAwareThreadLock._at_fork_reinit)

    
    def _at_fork_reinit(self):
        self._lock._at_fork_reinit()

    
    def __enter__(self):
        return self._lock.__enter__()

    
    def __exit__(self, *args):
        pass
    # WARNING: Decompyle incomplete



class ForkAwareLocal(threading.local):
    
    def __init__(self):
        register_after_fork(self, (lambda obj: obj.__dict__.clear()))

    
    def __reduce__(self):
        return (type(self), ())


# WARNING: Decompyle incomplete
