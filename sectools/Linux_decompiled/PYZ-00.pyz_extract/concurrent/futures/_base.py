
__author__ = 'Brian Quinlan (brian@sweetapp.com)'
import collections
import logging
import threading
import time
import types
FIRST_COMPLETED = 'FIRST_COMPLETED'
FIRST_EXCEPTION = 'FIRST_EXCEPTION'
ALL_COMPLETED = 'ALL_COMPLETED'
_AS_COMPLETED = '_AS_COMPLETED'
PENDING = 'PENDING'
RUNNING = 'RUNNING'
CANCELLED = 'CANCELLED'
CANCELLED_AND_NOTIFIED = 'CANCELLED_AND_NOTIFIED'
FINISHED = 'FINISHED'
_FUTURE_STATES = [
    PENDING,
    RUNNING,
    CANCELLED,
    CANCELLED_AND_NOTIFIED,
    FINISHED]
_STATE_TO_DESCRIPTION_MAP = {
    FINISHED: 'finished',
    CANCELLED_AND_NOTIFIED: 'cancelled',
    CANCELLED: 'cancelled',
    RUNNING: 'running',
    PENDING: 'pending' }
LOGGER = logging.getLogger('concurrent.futures')

class Error(Exception):
    '''Base class for all future-related exceptions.'''
    pass


class CancelledError(Error):
    '''The Future was cancelled.'''
    pass


class TimeoutError(Error):
    '''The operation exceeded the given deadline.'''
    pass


class InvalidStateError(Error):
    '''The operation is not allowed in this state.'''
    pass


class _Waiter(object):
    '''Provides the event that wait() and as_completed() block on.'''
    
    def __init__(self):
        self.event = threading.Event()
        self.finished_futures = []

    
    def add_result(self, future):
        self.finished_futures.append(future)

    
    def add_exception(self, future):
        self.finished_futures.append(future)

    
    def add_cancelled(self, future):
        self.finished_futures.append(future)



class _AsCompletedWaiter(_Waiter):
    '''Used by as_completed().'''
    
    def __init__(self = None):
        super(_AsCompletedWaiter, self).__init__()
        self.lock = threading.Lock()

    
    def add_result(self = None, future = None):
        pass
    # WARNING: Decompyle incomplete

    
    def add_exception(self = None, future = None):
        pass
    # WARNING: Decompyle incomplete

    
    def add_cancelled(self = None, future = None):
        pass
    # WARNING: Decompyle incomplete

    __classcell__ = None


class _FirstCompletedWaiter(_Waiter):
    '''Used by wait(return_when=FIRST_COMPLETED).'''
    
    def add_result(self = None, future = None):
        super().add_result(future)
        self.event.set()

    
    def add_exception(self = None, future = None):
        super().add_exception(future)
        self.event.set()

    
    def add_cancelled(self = None, future = None):
        super().add_cancelled(future)
        self.event.set()

    __classcell__ = None


class _AllCompletedWaiter(_Waiter):
    '''Used by wait(return_when=FIRST_EXCEPTION and ALL_COMPLETED).'''
    
    def __init__(self = None, num_pending_calls = None, stop_on_exception = None):
        self.num_pending_calls = num_pending_calls
        self.stop_on_exception = stop_on_exception
        self.lock = threading.Lock()
        super().__init__()

    
    def _decrement_pending_calls(self):
        pass
    # WARNING: Decompyle incomplete

    
    def add_result(self = None, future = None):
        super().add_result(future)
        self._decrement_pending_calls()

    
    def add_exception(self = None, future = None):
        super().add_exception(future)
        if self.stop_on_exception:
            self.event.set()
            return None
        None._decrement_pending_calls()

    
    def add_cancelled(self = None, future = None):
        super().add_cancelled(future)
        self._decrement_pending_calls()

    __classcell__ = None


class _AcquireFutures(object):
    '''A context manager that does an ordered acquire of Future conditions.'''
    
    def __init__(self, futures):
        self.futures = sorted(futures, id, **('key',))

    
    def __enter__(self):
        for future in self.futures:
            future._condition.acquire()

    
    def __exit__(self, *args):
        for future in self.futures:
            future._condition.release()



def _create_and_install_waiters(fs, return_when):
    if return_when == _AS_COMPLETED:
        waiter = _AsCompletedWaiter()
    elif return_when == FIRST_COMPLETED:
        waiter = _FirstCompletedWaiter()
    else:
        pending_count = sum((lambda .0: for f in .0:
f._state not in (CANCELLED_AND_NOTIFIED, FINISHED))(fs))
        if return_when == FIRST_EXCEPTION:
            waiter = _AllCompletedWaiter(pending_count, True, **('stop_on_exception',))
        elif return_when == ALL_COMPLETED:
            waiter = _AllCompletedWaiter(pending_count, False, **('stop_on_exception',))
        else:
            raise ValueError('Invalid return condition: %r' % return_when)
        for f in None:
            f._waiters.append(waiter)
        return waiter


def _yield_finished_futures(fs, waiter, ref_collect):
    '''
    Iterate on the list *fs*, yielding finished futures one by one in
    reverse order.
    Before yielding a future, *waiter* is removed from its waiters
    and the future is removed from each set in the collection of sets
    *ref_collect*.

    The aim of this function is to avoid keeping stale references after
    the future is yielded and before the iterator resumes.
    '''
    pass
# WARNING: Decompyle incomplete


def as_completed(fs, timeout = (None,)):
    '''An iterator over the given futures that yields each as it completes.

    Args:
        fs: The sequence of Futures (possibly created by different Executors) to
            iterate over.
        timeout: The maximum number of seconds to wait. If None, then there
            is no limit on the wait time.

    Returns:
        An iterator that yields the given Futures as they complete (finished or
        cancelled). If any given Futures are duplicated, they will be returned
        once.

    Raises:
        TimeoutError: If the entire result iterator could not be generated
            before the given timeout.
    '''
    if timeout is not None:
        end_time = timeout + time.monotonic()
    fs = set(fs)
    total_futures = len(fs)
    with _AcquireFutures(fs):
        finished = set((lambda .0: for f in .0:
if f._state in (CANCELLED_AND_NOTIFIED, FINISHED):
fcontinueNone)(fs))
        pending = fs - finished
        waiter = _create_and_install_waiters(fs, _AS_COMPLETED)
        None(None, None, None)
# WARNING: Decompyle incomplete

DoneAndNotDoneFutures = collections.namedtuple('DoneAndNotDoneFutures', 'done not_done')

def wait(fs, timeout, return_when = (None, ALL_COMPLETED)):
    """Wait for the futures in the given sequence to complete.

    Args:
        fs: The sequence of Futures (possibly created by different Executors) to
            wait upon.
        timeout: The maximum number of seconds to wait. If None, then there
            is no limit on the wait time.
        return_when: Indicates when this function should return. The options
            are:

            FIRST_COMPLETED - Return when any future finishes or is
                              cancelled.
            FIRST_EXCEPTION - Return when any future finishes by raising an
                              exception. If no future raises an exception
                              then it is equivalent to ALL_COMPLETED.
            ALL_COMPLETED -   Return when all futures finish or are cancelled.

    Returns:
        A named 2-tuple of sets. The first set, named 'done', contains the
        futures that completed (is finished or cancelled) before the wait
        completed. The second set, named 'not_done', contains uncompleted
        futures. Duplicate futures given to *fs* are removed and will be 
        returned only once.
    """
    fs = set(fs)
    with _AcquireFutures(fs):
        done = (lambda .0: pass# WARNING: Decompyle incomplete
)(fs)
        not_done = fs - done
        if return_when == FIRST_COMPLETED and done:
            pass
        None(None, None, None)
        return None
        if return_when == FIRST_EXCEPTION and done and any((lambda .0: for f in .0:
if f.cancelled() and f.exception() is not None:
fcontinueNone)(done)):
            pass
        None(None, None, None)
        return None
        if len(done) == len(fs):
            pass
        None(None, None, None)
        return None
        waiter = _create_and_install_waiters(fs, return_when)
        None(None, None, None)
# WARNING: Decompyle incomplete


class Future(object):
    '''Represents the result of an asynchronous computation.'''
    
    def __init__(self):
        '''Initializes the future. Should not be called by clients.'''
        self._condition = threading.Condition()
        self._state = PENDING
        self._result = None
        self._exception = None
        self._waiters = []
        self._done_callbacks = []

    
    def _invoke_callbacks(self):
        pass
    # WARNING: Decompyle incomplete

    
    def __repr__(self):
        pass
    # WARNING: Decompyle incomplete

    
    def cancel(self):
        '''Cancel the future if possible.

        Returns True if the future was cancelled, False otherwise. A future
        cannot be cancelled if it is running or has already completed.
        '''
        with self._condition:
            if self._state in (RUNNING, FINISHED):
                pass
            None(None, None, None)
            return False
            if self._state in (CANCELLED, CANCELLED_AND_NOTIFIED):
                pass
            None(None, None, None)
            return True
            self._state = CANCELLED
            self._condition.notify_all()
            None(None, None, None)
    # WARNING: Decompyle incomplete

    
    def cancelled(self):
        '''Return True if the future was cancelled.'''
        pass
    # WARNING: Decompyle incomplete

    
    def running(self):
        '''Return True if the future is currently executing.'''
        pass
    # WARNING: Decompyle incomplete

    
    def done(self):
        '''Return True of the future was cancelled or finished executing.'''
        pass
    # WARNING: Decompyle incomplete

    
    def __get_result(self):
        pass
    # WARNING: Decompyle incomplete

    
    def add_done_callback(self, fn):
        '''Attaches a callable that will be called when the future finishes.

        Args:
            fn: A callable that will be called with this future as its only
                argument when the future completes or is cancelled. The callable
                will always be called by a thread in the same process in which
                it was added. If the future has already completed or been
                cancelled then the callable will be called immediately. These
                callables are called in the order that they were added.
        '''
        with self._condition:
            if self._state not in (CANCELLED, CANCELLED_AND_NOTIFIED, FINISHED):
                self._done_callbacks.append(fn)
            None(None, None, None)
            return None
            None(None, None, None)
    # WARNING: Decompyle incomplete

    
    def result(self, timeout = (None,)):
        """Return the result of the call that the future represents.

        Args:
            timeout: The number of seconds to wait for the result if the future
                isn't done. If None, then there is no limit on the wait time.

        Returns:
            The result of the call that the future represents.

        Raises:
            CancelledError: If the future was cancelled.
            TimeoutError: If the future didn't finish executing before the given
                timeout.
            Exception: If the call raised then that exception will be raised.
        """
        pass
    # WARNING: Decompyle incomplete

    
    def exception(self, timeout = (None,)):
        """Return the exception raised by the call that the future represents.

        Args:
            timeout: The number of seconds to wait for the exception if the
                future isn't done. If None, then there is no limit on the wait
                time.

        Returns:
            The exception raised by the call that the future represents or None
            if the call completed without raising.

        Raises:
            CancelledError: If the future was cancelled.
            TimeoutError: If the future didn't finish executing before the given
                timeout.
        """
        pass
    # WARNING: Decompyle incomplete

    
    def set_running_or_notify_cancel(self):
        '''Mark the future as running or process any cancel notifications.

        Should only be used by Executor implementations and unit tests.

        If the future has been cancelled (cancel() was called and returned
        True) then any threads waiting on the future completing (though calls
        to as_completed() or wait()) are notified and False is returned.

        If the future was not cancelled then it is put in the running state
        (future calls to running() will return True) and True is returned.

        This method should be called by Executor implementations before
        executing the work associated with this future. If this method returns
        False then the work should not be executed.

        Returns:
            False if the Future was cancelled, True otherwise.

        Raises:
            RuntimeError: if this method was already called or if set_result()
                or set_exception() was called.
        '''
        pass
    # WARNING: Decompyle incomplete

    
    def set_result(self, result):
        '''Sets the return value of work associated with the future.

        Should only be used by Executor implementations and unit tests.
        '''
        with self._condition:
            if self._state in {
                CANCELLED,
                CANCELLED_AND_NOTIFIED,
                FINISHED}:
                raise InvalidStateError('{}: {!r}'.format(self._state, self))
            self._result = None
            self._state = FINISHED
            for waiter in self._waiters:
                waiter.add_result(self)
            self._condition.notify_all()
            None(None, None, None)
    # WARNING: Decompyle incomplete

    
    def set_exception(self, exception):
        '''Sets the result of the future as being the given exception.

        Should only be used by Executor implementations and unit tests.
        '''
        with self._condition:
            if self._state in {
                CANCELLED,
                CANCELLED_AND_NOTIFIED,
                FINISHED}:
                raise InvalidStateError('{}: {!r}'.format(self._state, self))
            self._exception = None
            self._state = FINISHED
            for waiter in self._waiters:
                waiter.add_exception(self)
            self._condition.notify_all()
            None(None, None, None)
    # WARNING: Decompyle incomplete

    __class_getitem__ = classmethod(types.GenericAlias)


class Executor(object):
    '''This is an abstract base class for concrete asynchronous executors.'''
    
    def submit(self, fn, *args, **kwargs):
        '''Submits a callable to be executed with the given arguments.

        Schedules the callable to be executed as fn(*args, **kwargs) and returns
        a Future instance representing the execution of the callable.

        Returns:
            A Future representing the given call.
        '''
        raise NotImplementedError()

    
    def map(self = None, fn = {
        'timeout': None,
        'chunksize': 1 }, *, timeout, chunksize, *iterables):
        '''Returns an iterator equivalent to map(fn, iter).

        Args:
            fn: A callable that will take as many arguments as there are
                passed iterables.
            timeout: The maximum number of seconds to wait. If None, then there
                is no limit on the wait time.
            chunksize: The size of the chunks the iterable will be broken into
                before being passed to a child process. This argument is only
                used by ProcessPoolExecutor; it is ignored by
                ThreadPoolExecutor.

        Returns:
            An iterator equivalent to: map(func, *iterables) but the calls may
            be evaluated out-of-order.

        Raises:
            TimeoutError: If the entire result iterator could not be generated
                before the given timeout.
            Exception: If fn(*args) raises for any values.
        '''
        if timeout is not None:
            end_time = timeout + time.monotonic()
    # WARNING: Decompyle incomplete

    
    def shutdown(self = None, wait = (True,), *, cancel_futures):
        '''Clean-up the resources associated with the Executor.

        It is safe to call this method several times. Otherwise, no other
        methods can be called after this one.

        Args:
            wait: If True then shutdown will not return until all running
                futures have finished executing and the resources used by the
                executor have been reclaimed.
            cancel_futures: If True then shutdown will cancel all pending
                futures. Futures that are completed or running will not be
                cancelled.
        '''
        pass

    
    def __enter__(self):
        return self

    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown(True, **('wait',))
        return False



class BrokenExecutor(RuntimeError):
    '''
    Raised when a executor has become non-functional after a severe failure.
    '''
    pass

