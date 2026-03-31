
import warnings
from collections import Counter, defaultdict, deque, abc
from collections.abc import Sequence
from functools import partial, reduce, wraps
from heapq import merge, heapify, heapreplace, heappop
from itertools import chain, compress, count, cycle, dropwhile, groupby, islice, repeat, starmap, takewhile, tee, zip_longest
from math import exp, factorial, floor, log
from queue import Empty, Queue
from random import random, randrange, uniform
from operator import itemgetter, mul, sub, gt, lt, ge, le
from sys import hexversion, maxsize
from time import monotonic
from recipes import consume, flatten, pairwise, powerset, take, unique_everseen
__all__ = [
    'AbortThread',
    'SequenceView',
    'UnequalIterablesError',
    'adjacent',
    'all_unique',
    'always_iterable',
    'always_reversible',
    'bucket',
    'callback_iter',
    'chunked',
    'chunked_even',
    'circular_shifts',
    'collapse',
    'collate',
    'combination_index',
    'consecutive_groups',
    'consumer',
    'count_cycle',
    'countable',
    'difference',
    'distinct_combinations',
    'distinct_permutations',
    'distribute',
    'divide',
    'duplicates_everseen',
    'duplicates_justseen',
    'exactly_n',
    'filter_except',
    'first',
    'groupby_transform',
    'ichunked',
    'ilen',
    'interleave',
    'interleave_evenly',
    'interleave_longest',
    'intersperse',
    'is_sorted',
    'islice_extended',
    'iterate',
    'last',
    'locate',
    'lstrip',
    'make_decorator',
    'map_except',
    'map_if',
    'map_reduce',
    'mark_ends',
    'minmax',
    'nth_or_last',
    'nth_permutation',
    'nth_product',
    'numeric_range',
    'one',
    'only',
    'padded',
    'partitions',
    'peekable',
    'permutation_index',
    'product_index',
    'raise_',
    'repeat_each',
    'repeat_last',
    'replace',
    'rlocate',
    'rstrip',
    'run_length',
    'sample',
    'seekable',
    'set_partitions',
    'side_effect',
    'sliced',
    'sort_together',
    'split_after',
    'split_at',
    'split_before',
    'split_into',
    'split_when',
    'spy',
    'stagger',
    'strip',
    'strictly_n',
    'substrings',
    'substrings_indexes',
    'time_limited',
    'unique_in_window',
    'unique_to_each',
    'unzip',
    'value_chain',
    'windowed',
    'windowed_complete',
    'with_iter',
    'zip_broadcast',
    'zip_equal',
    'zip_offset']
_marker = object()

def chunked(iterable, n, strict = (False,)):
    '''Break *iterable* into lists of length *n*:

        >>> list(chunked([1, 2, 3, 4, 5, 6], 3))
        [[1, 2, 3], [4, 5, 6]]

    By the default, the last yielded list will have fewer than *n* elements
    if the length of *iterable* is not divisible by *n*:

        >>> list(chunked([1, 2, 3, 4, 5, 6, 7, 8], 3))
        [[1, 2, 3], [4, 5, 6], [7, 8]]

    To use a fill-in value instead, see the :func:`grouper` recipe.

    If the length of *iterable* is not divisible by *n* and *strict* is
    ``True``, then ``ValueError`` will be raised before the last
    list is yielded.

    '''
    iterator = iter(partial(take, n, iter(iterable)), [])
    if strict:
        if n is None:
            raise ValueError('n must not be None when using strict mode.')
        
        def ret():
            for chunk in iterator:
                if len(chunk) != n:
                    raise ValueError('iterable is not divisible by n.')
                yield None

        return iter(ret())


def first(iterable, default = (_marker,)):
    """Return the first item of *iterable*, or *default* if *iterable* is
    empty.

        >>> first([0, 1, 2, 3])
        0
        >>> first([], 'some default')
        'some default'

    If *default* is not provided and there are no items in the iterable,
    raise ``ValueError``.

    :func:`first` is useful when you have a generator of expensive-to-retrieve
    values and want any arbitrary one. It is marginally shorter than
    ``next(iter(iterable), default)``.

    """
    pass
# WARNING: Decompyle incomplete


def last(iterable, default = (_marker,)):
    """Return the last item of *iterable*, or *default* if *iterable* is
    empty.

        >>> last([0, 1, 2, 3])
        3
        >>> last([], 'some default')
        'some default'

    If *default* is not provided and there are no items in the iterable,
    raise ``ValueError``.
    """
    pass
# WARNING: Decompyle incomplete


def nth_or_last(iterable, n, default = (_marker,)):
    """Return the nth or the last item of *iterable*,
    or *default* if *iterable* is empty.

        >>> nth_or_last([0, 1, 2, 3], 2)
        2
        >>> nth_or_last([0, 1], 2)
        1
        >>> nth_or_last([], 0, 'some default')
        'some default'

    If *default* is not provided and there are no items in the iterable,
    raise ``ValueError``.
    """
    return last(islice(iterable, n + 1), default, **('default',))


class peekable:
    '''Wrap an iterator to allow lookahead and prepending elements.

    Call :meth:`peek` on the result to get the value that will be returned
    by :func:`next`. This won\'t advance the iterator:

        >>> p = peekable([\'a\', \'b\'])
        >>> p.peek()
        \'a\'
        >>> next(p)
        \'a\'

    Pass :meth:`peek` a default value to return that instead of raising
    ``StopIteration`` when the iterator is exhausted.

        >>> p = peekable([])
        >>> p.peek(\'hi\')
        \'hi\'

    peekables also offer a :meth:`prepend` method, which "inserts" items
    at the head of the iterable:

        >>> p = peekable([1, 2, 3])
        >>> p.prepend(10, 11, 12)
        >>> next(p)
        10
        >>> p.peek()
        11
        >>> list(p)
        [11, 12, 1, 2, 3]

    peekables can be indexed. Index 0 is the item that will be returned by
    :func:`next`, index 1 is the item after that, and so on:
    The values up to the given index will be cached.

        >>> p = peekable([\'a\', \'b\', \'c\', \'d\'])
        >>> p[0]
        \'a\'
        >>> p[1]
        \'b\'
        >>> next(p)
        \'a\'

    Negative indexes are supported, but be aware that they will cache the
    remaining items in the source iterator, which may require significant
    storage.

    To check whether a peekable is exhausted, check its truth value:

        >>> p = peekable([\'a\', \'b\'])
        >>> if p:  # peekable has items
        ...     list(p)
        [\'a\', \'b\']
        >>> if not p:  # peekable is exhausted
        ...     list(p)
        []

    '''
    
    def __init__(self, iterable):
        self._it = iter(iterable)
        self._cache = deque()

    
    def __iter__(self):
        return self

    
    def __bool__(self):
        pass
    # WARNING: Decompyle incomplete

    
    def peek(self, default = (_marker,)):
        '''Return the item that will be next returned from ``next()``.

        Return ``default`` if there are no items left. If ``default`` is not
        provided, raise ``StopIteration``.

        '''
        pass
    # WARNING: Decompyle incomplete

    
    def prepend(self, *items):
        '''Stack up items to be the next ones returned from ``next()`` or
        ``self.peek()``. The items will be returned in
        first in, first out order::

            >>> p = peekable([1, 2, 3])
            >>> p.prepend(10, 11, 12)
            >>> next(p)
            10
            >>> list(p)
            [11, 12, 1, 2, 3]

        It is possible, by prepending items, to "resurrect" a peekable that
        previously raised ``StopIteration``.

            >>> p = peekable([])
            >>> next(p)
            Traceback (most recent call last):
              ...
            StopIteration
            >>> p.prepend(1)
            >>> next(p)
            1
            >>> next(p)
            Traceback (most recent call last):
              ...
            StopIteration

        '''
        self._cache.extendleft(reversed(items))

    
    def __next__(self):
        if self._cache:
            return self._cache.popleft()
        return None(self._it)

    
    def _get_slice(self, index):
        step = 1 if index.step is None else index.step
        if step > 0:
            start = 0 if index.start is None else index.start
            stop = maxsize if index.stop is None else index.stop
        elif step < 0:
            start = -1 if index.start is None else index.start
            stop = -maxsize - 1 if index.stop is None else index.stop
        else:
            raise ValueError('slice step cannot be zero')
        if None < 0 or stop < 0:
            self._cache.extend(self._it)
        else:
            n = min(max(start, stop) + 1, maxsize)
            cache_len = len(self._cache)
            if n >= cache_len:
                self._cache.extend(islice(self._it, n - cache_len))
        return list(self._cache)[index]

    
    def __getitem__(self, index):
        if isinstance(index, slice):
            return self._get_slice(index)
        cache_len = None(self._cache)
        if index < 0:
            self._cache.extend(self._it)
        elif index >= cache_len:
            self._cache.extend(islice(self._it, index + 1 - cache_len))
        return self._cache[index]



def collate(*iterables, **kwargs):
    """Return a sorted merge of the items from each of several already-sorted
    *iterables*.

        >>> list(collate('ACDZ', 'AZ', 'JKL'))
        ['A', 'A', 'C', 'D', 'J', 'K', 'L', 'Z', 'Z']

    Works lazily, keeping only the next value from each iterable in memory. Use
    :func:`collate` to, for example, perform a n-way mergesort of items that
    don't fit in memory.

    If a *key* function is specified, the iterables will be sorted according
    to its result:

        >>> key = lambda s: int(s)  # Sort by numeric value, not by string
        >>> list(collate(['1', '10'], ['2', '11'], key=key))
        ['1', '2', '10', '11']


    If the *iterables* are sorted in descending order, set *reverse* to
    ``True``:

        >>> list(collate([5, 3, 1], [4, 2, 0], reverse=True))
        [5, 4, 3, 2, 1, 0]

    If the elements of the passed-in iterables are out of order, you might get
    unexpected results.

    On Python 3.5+, this function is an alias for :func:`heapq.merge`.

    """
    warnings.warn('collate is no longer part of more_itertools, use heapq.merge', DeprecationWarning)
# WARNING: Decompyle incomplete


def consumer(func):
    '''Decorator that automatically advances a PEP-342-style "reverse iterator"
    to its first yield point so you don\'t have to call ``next()`` on it
    manually.

        >>> @consumer
        ... def tally():
        ...     i = 0
        ...     while True:
        ...         print(\'Thing number %s is %s.\' % (i, (yield)))
        ...         i += 1
        ...
        >>> t = tally()
        >>> t.send(\'red\')
        Thing number 0 is red.
        >>> t.send(\'fish\')
        Thing number 1 is fish.

    Without the decorator, you would have to call ``next(t)`` before
    ``t.send()`` could be used.

    '''
    
    def wrapper(*args, **kwargs):
        pass
    # WARNING: Decompyle incomplete

    wrapper = None(wrapper)
    return wrapper


def ilen(iterable):
    '''Return the number of items in *iterable*.

        >>> ilen(x for x in range(1000000) if x % 3 == 0)
        333334

    This consumes the iterable, so handle with care.

    '''
    counter = count()
    deque(zip(iterable, counter), 0, **('maxlen',))
    return next(counter)


def iterate(func, start):
    '''Return ``start``, ``func(start)``, ``func(func(start))``, ...

    >>> from itertools import islice
    >>> list(islice(iterate(lambda x: 2*x, 1), 10))
    [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]

    '''
    yield start
    start = func(start)
    continue


def with_iter(context_manager):
    """Wrap an iterable in a ``with`` statement, so it closes once exhausted.

    For example, this will close the file when the iterator is exhausted::

        upper_lines = (line.upper() for line in with_iter(open('foo')))

    Any context manager which returns an iterable is a candidate for
    ``with_iter``.

    """
    pass
# WARNING: Decompyle incomplete


def one(iterable, too_short, too_long = (None, None)):
    """Return the first item from *iterable*, which is expected to contain only
    that item. Raise an exception if *iterable* is empty or has more than one
    item.

    :func:`one` is useful for ensuring that an iterable contains only one item.
    For example, it can be used to retrieve the result of a database query
    that is expected to return a single row.

    If *iterable* is empty, ``ValueError`` will be raised. You may specify a
    different exception with the *too_short* keyword:

        >>> it = []
        >>> one(it)  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        ValueError: too many items in iterable (expected 1)'
        >>> too_short = IndexError('too few items')
        >>> one(it, too_short=too_short)  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        IndexError: too few items

    Similarly, if *iterable* contains more than one item, ``ValueError`` will
    be raised. You may specify a different exception with the *too_long*
    keyword:

        >>> it = ['too', 'many']
        >>> one(it)  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        ValueError: Expected exactly one item in iterable, but got 'too',
        'many', and perhaps more.
        >>> too_long = RuntimeError
        >>> one(it, too_long=too_long)  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        RuntimeError

    Note that :func:`one` attempts to advance *iterable* twice to ensure there
    is only one item. See :func:`spy` or :func:`peekable` to check iterable
    contents less destructively.

    """
    it = iter(iterable)
# WARNING: Decompyle incomplete


def raise_(exception, *args):
    pass
# WARNING: Decompyle incomplete


def strictly_n(iterable, n, too_short, too_long = (None, None)):
    """Validate that *iterable* has exactly *n* items and return them if
    it does. If it has fewer than *n* items, call function *too_short*
    with those items. If it has more than *n* items, call function
    *too_long* with the first ``n + 1`` items.

        >>> iterable = ['a', 'b', 'c', 'd']
        >>> n = 4
        >>> list(strictly_n(iterable, n))
        ['a', 'b', 'c', 'd']

    By default, *too_short* and *too_long* are functions that raise
    ``ValueError``.

        >>> list(strictly_n('ab', 3))  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        ValueError: too few items in iterable (got 2)

        >>> list(strictly_n('abc', 2))  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        ValueError: too many items in iterable (got at least 3)

    You can instead supply functions that do something else.
    *too_short* will be called with the number of items in *iterable*.
    *too_long* will be called with `n + 1`.

        >>> def too_short(item_count):
        ...     raise RuntimeError
        >>> it = strictly_n('abcd', 6, too_short=too_short)
        >>> list(it)  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        RuntimeError

        >>> def too_long(item_count):
        ...     print('The boss is going to hear about this')
        >>> it = strictly_n('abcdef', 4, too_long=too_long)
        >>> list(it)
        The boss is going to hear about this
        ['a', 'b', 'c', 'd']

    """
    if too_short is None:
        
        too_short = lambda item_count: raise_(ValueError, 'Too few items in iterable (got {})'.format(item_count))
    if too_long is None:
        
        too_long = lambda item_count: raise_(ValueError, 'Too many items in iterable (got at least {})'.format(item_count))
    it = iter(iterable)
# WARNING: Decompyle incomplete


def distinct_permutations(iterable, r = (None,)):
    '''Yield successive distinct permutations of the elements in *iterable*.

        >>> sorted(distinct_permutations([1, 0, 1]))
        [(0, 1, 1), (1, 0, 1), (1, 1, 0)]

    Equivalent to ``set(permutations(iterable))``, except duplicates are not
    generated and thrown away. For larger input sequences this is much more
    efficient.

    Duplicate permutations arise when there are duplicated elements in the
    input iterable. The number of items returned is
    `n! / (x_1! * x_2! * ... * x_n!)`, where `n` is the total number of
    items input, and each `x_i` is the count of a distinct item in the input
    sequence.

    If *r* is given, only the *r*-length permutations are yielded.

        >>> sorted(distinct_permutations([1, 0, 1], r=2))
        [(0, 1), (1, 0), (1, 1)]
        >>> sorted(distinct_permutations(range(3), r=2))
        [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]

    '''
    
    def _full(A = None):
        yield tuple(A)
        for i in range(size - 2, -1, -1):
            if A[i] < A[i + 1]:
                pass
            
            return None
            for j in range(size - 1, i, -1):
                if A[i] < A[j]:
                    pass
                
                A[i] = A[j]
                A[j] = A[i]
                A[i + 1:] = A[:i - size:-1]

    
    def _partial(A, r):
        head = A[:r]
        tail = A[r:]
        right_head_indexes = range(r - 1, -1, -1)
        left_tail_indexes = range(len(tail))
        yield tuple(head)
        pivot = tail[-1]
        for i in right_head_indexes:
            if head[i] < pivot:
                pass
            else:
                pivot = head[i]
            return None
            for j in left_tail_indexes:
                if tail[j] > head[i]:
                    head[i] = tail[j]
                    tail[j] = head[i]
                
                for j in right_head_indexes:
                    if head[j] > head[i]:
                        head[i] = head[j]
                        head[j] = head[i]
                    
                    tail += head[:i - r:-1]
                    i += 1
                    head[i:] = tail[:r - i]
                    tail[:] = tail[r - i:]

    items = sorted(iterable)
    size = len(items)
    if r is None:
        r = size
    if r < r or r <= size:
        pass
    else:
        0
    if r == size:
        return _full(items)
    return 0(items, r)
    if r:
        return iter(())
    return None(iter)


def intersperse(e, iterable, n = (1,)):
    """Intersperse filler element *e* among the items in *iterable*, leaving
    *n* items between each filler element.

        >>> list(intersperse('!', [1, 2, 3, 4, 5]))
        [1, '!', 2, '!', 3, '!', 4, '!', 5]

        >>> list(intersperse(None, [1, 2, 3, 4, 5], n=2))
        [1, 2, None, 3, 4, None, 5]

    """
    if n == 0:
        raise ValueError('n must be > 0')
    if None == 1:
        return islice(interleave(repeat(e), iterable), 1, None)
    filler = None([
        e])
    chunks = chunked(iterable, n)
    return flatten(islice(interleave(filler, chunks), 1, None))


def unique_to_each(*iterables):
    '''Return the elements from each of the input iterables that aren\'t in the
    other input iterables.

    For example, suppose you have a set of packages, each with a set of
    dependencies::

        {\'pkg_1\': {\'A\', \'B\'}, \'pkg_2\': {\'B\', \'C\'}, \'pkg_3\': {\'B\', \'D\'}}

    If you remove one package, which dependencies can also be removed?

    If ``pkg_1`` is removed, then ``A`` is no longer necessary - it is not
    associated with ``pkg_2`` or ``pkg_3``. Similarly, ``C`` is only needed for
    ``pkg_2``, and ``D`` is only needed for ``pkg_3``::

        >>> unique_to_each({\'A\', \'B\'}, {\'B\', \'C\'}, {\'B\', \'D\'})
        [[\'A\'], [\'C\'], [\'D\']]

    If there are duplicates in one input iterable that aren\'t in the others
    they will be duplicated in the output. Input order is preserved::

        >>> unique_to_each("mississippi", "missouri")
        [[\'p\', \'p\'], [\'o\', \'u\', \'r\']]

    It is assumed that the elements of each iterable are hashable.

    '''
    pool = (lambda .0: [ list(it) for it in .0 ])(iterables)
    counts = Counter(chain.from_iterable(map(set, pool)))
    uniques = (lambda .0 = None: pass# WARNING: Decompyle incomplete
)(counts)
    return (lambda .0 = None: [ list(filter(uniques.__contains__, it)) for it in .0 ])(pool)


def windowed(seq, n, fillvalue, step = (None, 1)):
    """Return a sliding window of width *n* over the given iterable.

        >>> all_windows = windowed([1, 2, 3, 4, 5], 3)
        >>> list(all_windows)
        [(1, 2, 3), (2, 3, 4), (3, 4, 5)]

    When the window is larger than the iterable, *fillvalue* is used in place
    of missing values:

        >>> list(windowed([1, 2, 3], 4))
        [(1, 2, 3, None)]

    Each window will advance in increments of *step*:

        >>> list(windowed([1, 2, 3, 4, 5, 6], 3, fillvalue='!', step=2))
        [(1, 2, 3), (3, 4, 5), (5, 6, '!')]

    To slide into the iterable's items, use :func:`chain` to add filler items
    to the left:

        >>> iterable = [1, 2, 3, 4]
        >>> n = 3
        >>> padding = [None] * (n - 1)
        >>> list(windowed(chain(padding, iterable), 3))
        [(None, None, 1), (None, 1, 2), (1, 2, 3), (2, 3, 4)]
    """
    if n < 0:
        raise ValueError('n must be >= 0')
    if None == 0:
        yield tuple()
        return None
    if None < 1:
        raise ValueError('step must be >= 1')
    window = None(n, **('maxlen',))
    i = n
    for _ in map(window.append, seq):
        i -= 1
        if not i:
            i = step
            yield tuple(window)
    size = len(window)
    if size < n:
        yield tuple(chain(window, repeat(fillvalue, n - size)))
        return None
    if i < i or i < min(step, n):
        pass
    else:
        return None
    None += (fillvalue,) * i
    yield tuple(window)
    return None


def substrings(iterable):
    """Yield all of the substrings of *iterable*.

        >>> [''.join(s) for s in substrings('more')]
        ['m', 'o', 'r', 'e', 'mo', 'or', 're', 'mor', 'ore', 'more']

    Note that non-string iterables can also be subdivided.

        >>> list(substrings([0, 1, 2]))
        [(0,), (1,), (2,), (0, 1), (1, 2), (0, 1, 2)]

    """
    seq = []
    for item in iter(iterable):
        seq.append(item)
        yield (item,)
    seq = tuple(seq)
    item_count = len(seq)
    for n in range(2, item_count + 1):
        for i in range((item_count - n) + 1):
            yield seq[i:i + n]


def substrings_indexes(seq, reverse = (False,)):
    """Yield all substrings and their positions in *seq*

    The items yielded will be a tuple of the form ``(substr, i, j)``, where
    ``substr == seq[i:j]``.

    This function only works for iterables that support slicing, such as
    ``str`` objects.

    >>> for item in substrings_indexes('more'):
    ...    print(item)
    ('m', 0, 1)
    ('o', 1, 2)
    ('r', 2, 3)
    ('e', 3, 4)
    ('mo', 0, 2)
    ('or', 1, 3)
    ('re', 2, 4)
    ('mor', 0, 3)
    ('ore', 1, 4)
    ('more', 0, 4)

    Set *reverse* to ``True`` to yield the same items in the opposite order.


    """
    r = range(1, len(seq) + 1)
    if reverse:
        r = reversed(r)
    return (lambda .0 = None: for L in .0:
for i in range((len(seq) - L) + 1):
(seq[i:i + L], i, i + L))(r)


class bucket:
    """Wrap *iterable* and return an object that buckets it iterable into
    child iterables based on a *key* function.

        >>> iterable = ['a1', 'b1', 'c1', 'a2', 'b2', 'c2', 'b3']
        >>> s = bucket(iterable, key=lambda x: x[0])  # Bucket by 1st character
        >>> sorted(list(s))  # Get the keys
        ['a', 'b', 'c']
        >>> a_iterable = s['a']
        >>> next(a_iterable)
        'a1'
        >>> next(a_iterable)
        'a2'
        >>> list(s['b'])
        ['b1', 'b2', 'b3']

    The original iterable will be advanced and its items will be cached until
    they are used by the child iterables. This may require significant storage.

    By default, attempting to select a bucket to which no items belong  will
    exhaust the iterable and cache all values.
    If you specify a *validator* function, selected buckets will instead be
    checked against it.

       