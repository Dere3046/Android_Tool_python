
__doc__ = 'Support for tasks, coroutines and the scheduler.'
__all__ = ('Task', 'create_task', 'FIRST_COMPLETED', 'FIRST_EXCEPTION', 'ALL_COMPLETED', 'wait', 'wait_for', 'as_completed', 'sleep', 'gather', 'shield', 'ensure_future', 'run_coroutine_threadsafe', 'current_task', 'all_tasks', '_register_task', '_unregister_task', '_enter_task', '_leave_task')
import concurrent.futures as concurrent
import contextvars
import functools
import inspect
import itertools
import types
import warnings
import weakref
from  import base_tasks
from  import coroutines
from  import events
from  import exceptions
from  import futures
from coroutines import _is_coroutine
_task_name_counter = itertools.count(1).__next__

def current_task(loop = (None,)):
    '''Return a currently executed task.'''
    if loop is None:
        loop = events.get_running_loop()
    return _current_tasks.get(loop)


def all_tasks(loop = (None,)):
    '''Return a set of all tasks for the loop.'''
    if loop is None:
        loop = events.get_running_loop()
    i = 0
# WARNING: Decompyle incomplete


def _set_task_name(task, name):
    pass
# WARNING: Decompyle incomplete


class Task(futures._PyFuture):
    '''A coroutine wrapped in a Future.'''
    _log_destroy_pending = True
    
    def __init__(self = None, coro = None, *, loop, name):
        super().__init__(loop, **('loop',))
        if self._source_traceback:
            del self._source_traceback[-1]
        if not coroutines.iscoroutine(coro):
            self._log_destroy_pending = False
            raise TypeError(f'''a coroutine was expected, got {coro!r}''')
        if None is None:
            self._name = f'''Task-{_task_name_counter()}'''
        else:
            self._name = str(name)
        self._must_cancel = False
        self._fut_waiter = None
        self._coro = coro
        self._context = contextvars.copy_context()
        self._loop.call_soon(self.__step, self._context, **('context',))
        _register_task(self)

    
    def __del__(self = None):
        if self._state == futures._PENDING and self._log_destroy_pending:
            context = {
                'task': self,
                'message': 'Task was destroyed but it is pending!' }
            if self._source_traceback:
                context['source_traceback'] = self._source_traceback
            self._loop.call_exception_handler(context)
        super().__del__()

    
    def __class_getitem__(cls, type):
        return cls

    
    def _repr_info(self):
        return base_tasks._task_repr_info(self)

    
    def get_coro(self):
        return self._coro

    
    def get_name(self):
        return self._name

    
    def set_name(self, value):
        self._name = str(value)

    
    def set_result(self, result):
        raise RuntimeError('Task does not support set_result operation')

    
    def set_exception(self, exception):
        raise RuntimeError('Task does not support set_exception operation')

    
    def get_stack(self = None, *, limit):
        """Return the list of stack frames for this task's coroutine.

        If the coroutine is not done, this returns the stack where it is
        suspended.  If the coroutine has completed successfully or was
        cancelled, this returns an empty list.  If the coroutine was
        terminated by an exception, this returns the list of traceback
        frames.

        The frames are always ordered from oldest to newest.

        The optional limit gives the maximum number of frames to
        return; by default all available frames are returned.  Its
        meaning differs depending on whether a stack or a traceback is
        returned: the newest frames of a stack are returned, but the
        oldest frames of a traceback are returned.  (This matches the
        behavior of the traceback module.)

        For reasons beyond our control, only one stack frame is
        returned for a suspended coroutine.
        """
        return base_tasks._task_get_stack(self, limit)

    
    def print_stack(self = None, *, limit, file):
        """Print the stack or traceback for this task's coroutine.

        This produces output similar to that of the traceback module,
        for the frames retrieved by get_stack().  The limit argument
        is passed to get_stack().  The file argument is an I/O stream
        to which the output is written; by default output is written
        to sys.stderr.
        """
        return base_tasks._task_print_stack(self, limit, file)

    
    def cancel(self, msg = (None,)):
        '''Request that this task cancel itself.

        This arranges for a CancelledError to be thrown into the
        wrapped coroutine on the next cycle through the event loop.
        The coroutine then has a chance to clean up or even deny
        the request using try/except/finally.

        Unlike Future.cancel, this does not guarantee that the
        task will be cancelled: the exception might be caught and
        acted upon, delaying cancellation of the task or preventing
        cancellation completely.  The task may also return a value or
        raise a different exception.

        Immediately after this method is called, Task.cancelled() will
        not return True (unless the task was already cancelled).  A
        task will be marked as cancelled when the wrapped coroutine
        terminates with a CancelledError exception (even if cancel()
        was not called).
        '''
        self._log_traceback = False
        if self.done():
            return False
        if None._fut_waiter is not None and self._fut_waiter.cancel(msg, **('msg',)):
            return True
        self._must_cancel = None
        self._cancel_message = msg
        return True

    
    def __step(self = None, exc = None):
        if self.done():
            raise exceptions.InvalidStateError(f'''_step(): already done: {self!r}, {exc!r}''')
        if None._must_cancel:
            if not isinstance(exc, exceptions.CancelledError):
                exc = self._make_cancelled_error()
            self._must_cancel = False
        coro = self._coro
        self._fut_waiter = None
        _enter_task(self._loop, self)
    # WARNING: Decompyle incomplete

    
    def __wakeup(self, future):
        pass
    # WARNING: Decompyle incomplete

    __classcell__ = None

_PyTask = Task
# WARNING: Decompyle incomplete
