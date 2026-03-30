
__doc__ = 'Imported from the recipes section of the itertools documentation.\n\nAll functions taken from the recipes section of the itertools library docs\n[1]_.\nSome backward-compatible usability improvements have been made.\n\n.. [1] http://docs.python.org/library/itertools.html#recipes\n\n'
import warnings
from collections import deque
from itertools import chain, combinations, count, cycle, groupby, islice, repeat, starmap, tee, zip_longest
import operator
from random import randrange, sample, choice
__all__ = [
    'all_equal',
    'before_and_after',
    'consume',
    'convolve',
    'dotproduct',
    'first_true',
    'flatten',
    'grouper',
    'iter_except',
    'ncycles',
    'nth',
    'nth_combination',
    'padnone',
    'pad_none',
    'pairwise',
    'partition',
    'powerset',
    'prepend',
    'quantify',
    'random_combination_with_replacement',
    'random_combination',
    'random_permutation',
    'random_product',
    'repeatfunc',
    'roundrobin',
    'sliding_window',
    'tabulate',
    'tail',
    'take',
    'triplewise',
    'unique_everseen',
    'unique_justseen']

def take(n, iterable):
    '''Return first *n* items of the iterable as a list.

        >>> take(3, range(10))
        [0, 1, 2]

    If there are fewer than *n* items in the iterable, all of them are
    returned.

        >>> take(10, range(3))
        [0, 1, 2]

    '''
    return list(islice(iterable, n))


def tabulate(function, start = (0,)):
    '''Return an iterator over the results of ``func(start)``,
    ``func(start + 1)``, ``func(start + 2)``...

    *func* should be a function that accepts one integer argument.

    If *start* is not specified it defaults to 0. It will be incremented each
    time the iterator is advanced.

        >>> square = lambda x: x ** 2
        >>> iterator = tabulate(square, -3)
        >>> take(4, iterator)
        [9, 4, 1, 0]

    '''
    return map(function, count(start))


def tail(n, iterable):
    """Return an iterator over the last *n* items of *iterable*.

    >>> t = tail(3, 'ABCDEFG')
    >>> list(t)
    ['E', 'F', 'G']

    """
    return iter(deque(iterable, n, **('maxlen',)))


def consume(iterator, n = (None,)):
    '''Advance *iterable* by *n* steps. If *n* is ``None``, consume it
    entirely.

    Efficiently exhausts an iterator without returning values. Defaults to
    consuming the whole iterator, but an optional second argument may be
    provided to limit consumption.

        >>> i = (x for x in range(10))
        >>> next(i)
        0
        >>> consume(i, 3)
        >>> next(i)
        4
        >>> consume(i)
        >>> next(i)
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
        StopIteration

    If the iterator has fewer items remaining than the provided limit, the
    whole iterator will be consumed.

        >>> i = (x for x in range(3))
        >>> consume(i, 5)
        >>> next(i)
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
        StopIteration

    '''
    if n is None:
        deque(iterator, 0, **('maxlen',))
        return None
    None(islice(iterator, n, n), None)


def nth(iterable, n, default = (None,)):
    '''Returns the nth item or a default value.

    >>> l = range(10)
    >>> nth(l, 3)
    3
    >>> nth(l, 20, "zebra")
    \'zebra\'

    '''
    return next(islice(iterable, n, None), default)


def all_equal(iterable):
    """
    Returns ``True`` if all the elements are equal to each other.

        >>> all_equal('aaaa')
        True
        >>> all_equal('aaab')
        False

    """
    g = groupby(iterable)
    if next(g, True):
        pass
    return not next(g, False)


def quantify(iterable, pred = (bool,)):
    '''Return the how many times the predicate is true.

    >>> quantify([True, False, True])
    2

    '''
    return sum(map(pred, iterable))


def pad_none(iterable):
    '''Returns the sequence of elements and then returns ``None`` indefinitely.

        >>> take(5, pad_none(range(3)))
        [0, 1, 2, None, None]

    Useful for emulating the behavior of the built-in :func:`map` function.

    See also :func:`padded`.

    '''
    return chain(iterable, repeat(None))

padnone = pad_none

def ncycles(iterable, n):
    '''Returns the sequence elements *n* times

    >>> list(ncycles(["a", "b"], 3))
    [\'a\', \'b\', \'a\', \'b\', \'a\', \'b\']

    '''
    return chain.from_iterable(repeat(tuple(iterable), n))


def dotproduct(vec1, vec2):
    '''Returns the dot product of the two iterables.

    >>> dotproduct([10, 10], [20, 20])
    400

    '''
    return sum(map(operator.mul, vec1, vec2))


def flatten(listOfLists):
    '''Return an iterator flattening one level of nesting in a list of lists.

        >>> list(flatten([[0, 1], [2, 3]]))
        [0, 1, 2, 3]

    See also :func:`collapse`, which can flatten multiple levels of nesting.

    '''
    return chain.from_iterable(listOfLists)


def repeatfunc(func, times = (None,), *args):
    '''Call *func* with *args* repeatedly, returning an iterable over the
    results.

    If *times* is specified, the iterable will terminate after that many
    repetitions:

        >>> from operator import add
        >>> times = 4
        >>> args = 3, 5
        >>> list(repeatfunc(add, times, *args))
        [8, 8, 8, 8]

    If *times* is ``None`` the iterable will not terminate:

        >>> from random import randrange
        >>> times = None
        >>> args = 1, 11
        >>> take(6, repeatfunc(randrange, times, *args))  # doctest:+SKIP
        [2, 4, 8, 1, 8, 4]

    '''
    if times is None:
        return starmap(func, repeat(args))
    return None(func, repeat(args, times))


def _pairwise(iterable):
    '''Returns an iterator of paired items, overlapping, from the original

    >>> take(4, pairwise(count()))
    [(0, 1), (1, 2), (2, 3), (3, 4)]

    On Python 3.10 and above, this is an alias for :func:`itertools.pairwise`.

    '''
    (a, b) = tee(iterable)
    next(b, None)
    yield from zip(a, b)

# WARNING: Decompyle incomplete
