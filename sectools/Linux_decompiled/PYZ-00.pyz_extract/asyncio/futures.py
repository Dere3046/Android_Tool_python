
__doc__ = 'A Future class similar to the one in PEP 3148.'
__all__ = ('Future', 'wrap_future', 'isfuture')
import concurrent.futures as concurrent
import contextvars
import logging
import sys
from  import base_futures
from  import events
from  import exceptions
from  import format_helpers
isfuture = base_futures.isfuture
_PENDING = base_futures._PENDING
_CANCELLED = base_futures._CANCELLED
_FINISHED = base_futures._FINISHED
STACK_DEBUG = logging.DEBUG - 1

class Future:
    """This class is *almost* compatible with concurrent.futures.Future.

    Differences:

    - This class is not thread-safe.

    - result() and exception() do not take a timeout argument and
      raise an exception when the future isn't done yet.

    - Callbacks registered with add_done_callback() are always called
      via the event loop's call_soon().

    - This class is not compatible with the wait() and as_completed()
      methods in the concurrent.futures package.

    (In Python 3.4 or later we may be able to unify the implementations.)
    """
    _state = _PENDING
    _result = None
    _exception = None
    _loop = None
    _source_traceback = None
    _cancel_message = None
    _cancelled_exc = None
    _asyncio_future_blocking = False
    __log_traceback = False
    
    def __init__(self = None, *, loop):
        """Initialize the future.

        The optional event_loop argument allows explicitly setting the event
        loop object used by the future. If it's not provided, the future uses
        the default event loop.
        """
        if loop is None:
            self._loop = events._get_event_loop()
        else:
            self._loop = loop
        self._callbacks = []
        if self._loop.get_debug():
            self._source_traceback = format_helpers.extract_stack(sys._getframe(1))
            return None

    _repr_info = base_futures._future_repr_info
    
    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, ' '.join(self._repr_info()))

    
    def __del__(self):
        if not self.__log_traceback:
            return None
        exc = None._exception
        context = {
            'message': f'''{self.__class__.__name__} exception was never retrieved''',
            'exception': exc,
            'future': self }
        if self._source_traceback:
            context['source_traceback'] = self._source_traceback
        self._loop.call_exception_handler(context)

    
    def __class_getitem__(cls, type):
        return cls

    
    def _log_traceback(self):
        return self.__log_traceback

    _log_traceback = property(_log_traceback)
    
    def _log_traceback(self, val):
        if val:
            raise ValueError('_log_traceback can only be set to False')
        self.__log_traceback = None

    _log_traceback = _log_traceback.setter(_log_traceback)
    
    def get_loop(self):
        '''Return the event loop the Future is bound to.'''
        loop = self._loop
        if loop is None:
            raise RuntimeError('Future object is not initialized.')

    
    def _make_cancelled_error(self):
        '''Create the CancelledError to raise if the Future is cancelled.

        This should only be called once when handling a cancellation since
        it erases the saved context exception value.
        '''
        if self._cancel_message is None:
            exc = exceptions.CancelledError()
        else:
            exc = exceptions.CancelledError(self._cancel_message)
        exc.__context__ = self._cancelled_exc
        self._cancelled_exc = None
        return exc

    
    def cancel(self, msg = (None,)):
        """Cancel the future and schedule callbacks.

        If the future is already done or cancelled, return False.  Otherwise,
        change the future's state to cancelled, schedule the callbacks and
        return True.
        """
        self.__log_traceback = False
        if self._state != _PENDING:
            return False
        self._state = None
        self._cancel_message = msg
        self.__schedule_callbacks()
        return True

    
    def __schedule_callbacks(self):
        '''Internal: Ask the event loop to call all callbacks.

        The callbacks are scheduled to be called as soon as possible. Also
        clears the callback list.
        '''
        callbacks = self._callbacks[:]
        if not callbacks:
            return None
        self._callbacks[:] = None
        for callback, ctx in callbacks:
            self._loop.call_soon(callback, self, ctx, **('context',))

    
    def cancelled(self):
        '''Return True if the future was cancelled.'''
        return self._state == _CANCELLED

    
    def done(self):
        '''Return True if the future is done.

        Done means either that a result / exception are available, or that the
        future was cancelled.
        '''
        return self._state != _PENDING

    
    def result(self):
        """Return the result this future represents.

        If the future has been cancelled, raises CancelledError.  If the
        future's result isn't yet available, raises InvalidStateError.  If
        the future is done and has an exception set, this exception is raised.
        """
        if self._state == _CANCELLED:
            exc = self._make_cancelled_error()
            raise exc
        if None._state != _FINISHED:
            raise exceptions.InvalidStateError('Result is not ready.')
        self.__log_traceback = None
        if self._exception is not None:
            raise self._exception
        return None._result

    
    def exception(self):
        """Return the exception that was set on this future.

        The exception (or None if no exception was set) is returned only if
        the future is done.  If the future has been cancelled, raises
        CancelledError.  If the future isn't done yet, raises
        InvalidStateError.
        """
        if self._state == _CANCELLED:
            exc = self._make_cancelled_error()
            raise exc
        if None._state != _FINISHED:
            raise exceptions.InvalidStateError('Exception is not set.')
        self.__log_traceback = None
        return self._exception

    
    def add_done_callback(self = None, fn = {
        'context': None }, *, context):
        '''Add a callback to be run when the future becomes done.

        The callback is called with a single argument - the future object. If
        the future is already done when this is called, the callback is
        scheduled with call_soon.
        '''
        if self._state != _PENDING:
            self._loop.call_soon(fn, self, context, **('context',))
            return None
        if None is None:
            context = contextvars.copy_context()
        self._callbacks.append((fn, context))

    
    def remove_done_callback(self, fn):
        '''Remove all instances of a callback from the "call when done" list.

        Returns the number of callbacks removed.
        '''
        filtered_callbacks = (lambda .0 = None: [ (f, ctx) for f, ctx in .0 if f != fn ])(self._callbacks)
        removed_count = len(self._callbacks) - len(filtered_callbacks)
        if removed_count:
            self._callbacks[:] = filtered_callbacks
        return removed_count

    
    def set_result(self, result):
        '''Mark the future done and set its result.

        If the future is already done when this method is called, raises
        InvalidStateError.
        '''
        if self._state != _PENDING:
            raise exceptions.InvalidStateError(f'''{self._state}: {self!r}''')
        self._result = None
        self._state = _FINISHED
        self.__schedule_callbacks()

    
    def set_exception(self, exception):
        '''Mark the future done and set an exception.

        If the future is already done when this method is called, raises
        InvalidStateError.
        '''
        if self._state != _PENDING:
            raise exceptions.InvalidStateError(f'''{self._state}: {self!r}''')
        if None(exception, type):
            exception = exception()
        if type(exception) is StopIteration:
            raise TypeError('StopIteration interacts badly with generators and cannot be raised into a Future')
        self._exception = None
        self._state = _FINISHED
        self.__schedule_callbacks()
        self.__log_traceback = True

    
    def __await__(self):
        if not self.done():
            self._asyncio_future_blocking = True
            yield self
        if not self.done():
            raise RuntimeError("await wasn't used with future")
        return None.result()

    __iter__ = __await__

_PyFuture = Future

def _get_loop(fut):
    pass
# WARNING: Decompyle incomplete


def _set_result_unless_cancelled(fut, result):
    '''Helper setting the result only if the future was not cancelled.'''
    if fut.cancelled():
        return None
    None.set_result(result)


def _convert_future_exc(exc):
    exc_class = type(exc)
# WARNING: Decompyle incomplete


def _set_concurrent_future_state(concurrent, source):
    '''Copy state from a future to a concurrent.futures.Future.'''
    pass
# WARNING: Decompyle incomplete


def _copy_future_state(source, dest):
    '''Internal helper to copy state from another Future.

    The other Future may be a concurrent.futures.Future.
    '''
    pass
# WARNING: Decompyle incomplete


def _chain_future(source, destination):
    '''Chain two futures so that when one completes, so does the other.

    The result (or exception) of source will be copied to destination.
    If destination is cancelled, source gets cancelled too.
    Compatible with both asyncio.Future and concurrent.futures.Future.
    '''
    if not isfuture(source) and isinstance(source, concurrent.futures.Future):
        raise TypeError('A future is required for source argument')
    if not None(destination) and isinstance(destination, concurrent.futures.Future):
        raise TypeError('A future is required for destination argument')
    source_loop = _get_loop(source) if None(source) else None
    dest_loop = _get_loop(destination) if isfuture(destination) else None
    
    def _set_state(future, other):
        if isfuture(future):
            _copy_future_state(other, future)
            return None
        None(future, other)

    
    def _call_check_cancel(destination = None):
        if destination.cancelled():
            if source_loop is None or source_loop is dest_loop:
                source.cancel()
                return None
            None.call_soon_threadsafe(source.cancel)
            return None

    
    def _call_set_state(source = None):
        if destination.cancelled() and dest_loop is not None and dest_loop.is_closed():
            return None
        if None is None or dest_loop is source_loop:
            _set_state(destination, source)
            return None
        None.call_soon_threadsafe(_set_state, destination, source)

    destination.add_done_callback(_call_check_cancel)
    source.add_done_callback(_call_set_state)


def wrap_future(future = None, *, loop):
    '''Wrap concurrent.futures.Future object.'''
    if isfuture(future):
        return future
# WARNING: Decompyle incomplete

# WARNING: Decompyle incomplete
