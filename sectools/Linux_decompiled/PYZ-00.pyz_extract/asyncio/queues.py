
__all__ = ('Queue', 'PriorityQueue', 'LifoQueue', 'QueueFull', 'QueueEmpty')
import collections
import heapq
from  import locks
from  import mixins

class QueueEmpty(Exception):
    '''Raised when Queue.get_nowait() is called on an empty Queue.'''
    pass


class QueueFull(Exception):
    '''Raised when the Queue.put_nowait() method is called on a full Queue.'''
    pass


class Queue(mixins._LoopBoundMixin):
    '''A queue, useful for coordinating producer and consumer coroutines.

    If maxsize is less than or equal to zero, the queue size is infinite. If it
    is an integer greater than 0, then "await put()" will block when the
    queue reaches maxsize, until an item is removed by get().

    Unlike the standard library Queue, you can reliably know this Queue\'s size
    with qsize(), since your single-threaded asyncio application won\'t be
    interrupted between calling qsize() and doing an operation on the Queue.
    '''
    
    def __init__(self = None, maxsize = None, *, loop):
        super().__init__(loop, **('loop',))
        self._maxsize = maxsize
        self._getters = collections.deque()
        self._putters = collections.deque()
        self._unfinished_tasks = 0
        self._finished = locks.Event()
        self._finished.set()
        self._init(maxsize)

    
    def _init(self, maxsize):
        self._queue = collections.deque()

    
    def _get(self):
        return self._queue.popleft()

    
    def _put(self, item):
        self._queue.append(item)

    
    def _wakeup_next(self, waiters):
        if waiters:
            waiter = waiters.popleft()
            if not waiter.done():
                waiter.set_result(None)
                return None
            if not None:
                return None
            return None

    
    def __repr__(self):
        return f'''<{type(self).__name__} at {id(self):#x} {self._format()}>'''

    
    def __str__(self):
        return f'''<{type(self).__name__} {self._format()}>'''

    
    def __class_getitem__(cls, type):
        return cls

    
    def _format(self):
        result = f'''maxsize={self._maxsize!r}'''
        if getattr(self, '_queue', None):
            result += f''' _queue={list(self._queue)!r}'''
        if self._getters:
            result += f''' _getters[{len(self._getters)}]'''
        if self._putters:
            result += f''' _putters[{len(self._putters)}]'''
        if self._unfinished_tasks:
            result += f''' tasks={self._unfinished_tasks}'''
        return result

    
    def qsize(self):
        '''Number of items in the queue.'''
        return len(self._queue)

    
    def maxsize(self):
        '''Number of items allowed in the queue.'''
        return self._maxsize

    maxsize = property(maxsize)
    
    def empty(self):
        '''Return True if the queue is empty, False otherwise.'''
        return not (self._queue)

    
    def full(self):
        '''Return True if there are maxsize items in the queue.

        Note: if the Queue was initialized with maxsize=0 (the default),
        then full() is never True.
        '''
        if self._maxsize <= 0:
            return False
        return None.qsize() >= self._maxsize

    
    async def put(self, item):
        '''Put an item into the queue.

        Put an item into the queue. If the queue is full, wait until a free
        slot is available before adding item.
        '''
        pass
    # WARNING: Decompyle incomplete

    
    def put_nowait(self, item):
        '''Put an item into the queue without blocking.

        If no free slot is immediately available, raise QueueFull.
        '''
        if self.full():
            raise QueueFull
        None._put(item)
        self._unfinished_tasks += 1
        self._finished.clear()
        self._wakeup_next(self._getters)

    
    async def get(self):
        '''Remove and return an item from the queue.

        If queue is empty, wait until an item is available.
        '''
        pass
    # WARNING: Decompyle incomplete

    
    def get_nowait(self):
        '''Remove and return an item from the queue.

        Return an item if one is immediately available, else raise QueueEmpty.
        '''
        if self.empty():
            raise QueueEmpty
        item = None._get()
        self._wakeup_next(self._putters)
        return item

    
    def task_done(self):
        '''Indicate that a formerly enqueued task is complete.

        Used by queue consumers. For each get() used to fetch a task,
        a subsequent call to task_done() tells the queue that the processing
        on the task is complete.

        If a join() is currently blocking, it will resume when all items have
        been processed (meaning that a task_done() call was received for every
        item that had been put() into the queue).

        Raises ValueError if called more times than there were items placed in
        the queue.
        '''
        if self._unfinished_tasks <= 0:
            raise ValueError('task_done() called too many times')
        None._unfinished_tasks -= 1
        if self._unfinished_tasks == 0:
            self._finished.set()
            return None

    
    async def join(self):
        '''Block until all items in the queue have been gotten and processed.

        The count of unfinished tasks goes up whenever an item is added to the
        queue. The count goes down whenever a consumer calls task_done() to
        indicate that the item was retrieved and all work on it is complete.
        When the count of unfinished tasks drops to zero, join() unblocks.
        '''
        if self._unfinished_tasks > 0:
            await self._finished.wait()
            return None

    __classcell__ = None


class PriorityQueue(Queue):
    '''A subclass of Queue; retrieves entries in priority order (lowest first).

    Entries are typically tuples of the form: (priority number, data).
    '''
    
    def _init(self, maxsize):
        self._queue = []

    
    def _put(self, item, heappush = (heapq.heappush,)):
        heappush(self._queue, item)

    
    def _get(self, heappop = (heapq.heappop,)):
        return heappop(self._queue)



class LifoQueue(Queue):
    '''A subclass of Queue that retrieves most recently added entries first.'''
    
    def _init(self, maxsize):
        self._queue = []

    
    def _put(self, item):
        self._queue.append(item)

    
    def _get(self):
        return self._queue.pop()


