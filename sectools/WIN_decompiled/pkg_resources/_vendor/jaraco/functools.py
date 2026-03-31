
import functools
import time
import inspect
import collections
import types
import itertools
import pkg_resources.extern.more_itertools as pkg_resources
from typing import Callable, TypeVar
CallableT = TypeVar('CallableT', Callable[(..., object)], **('bound',))

def compose(*funcs):
    '''
    Compose any number of unary functions into a single unary function.

    >>> import textwrap
    >>> expected = str.strip(textwrap.dedent(compose.__doc__))
    >>> strip_and_dedent = compose(str.strip, textwrap.dedent)
    >>> strip_and_dedent(compose.__doc__) == expected
    True

    Compose also allows the innermost function to take arbitrary arguments.

    >>> round_three = lambda x: round(x, ndigits=3)
    >>> f = compose(round_three, int.__truediv__)
    >>> [f(3*x, x+1) for x in range(1,10)]
    [1.5, 2.0, 2.25, 2.4, 2.5, 2.571, 2.625, 2.667, 2.7]
    '''
    
    def compose_two(f1, f2):
        return (lambda : pass# WARNING: Decompyle incomplete
)

    return functools.reduce(compose_two, funcs)


def method_caller(method_name, *args, **kwargs):
    """
    Return a function that will call a named method on the
    target object with optional positional and keyword
    arguments.

    >>> lower = method_caller('lower')
    >>> lower('MyString')
    'mystring'
    """
    
    def call_method(target = None):
        func = getattr(target, method_name)
    # WARNING: Decompyle incomplete

    return call_method


def once(func):
    """
    Decorate func so it's only ever called the first time.

    This decorator can ensure that an expensive or non-idempotent function
    will not be expensive on subsequent calls and is idempotent.

    >>> add_three = once(lambda a: a+3)
    >>> add_three(3)
    6
    >>> add_three(9)
    6
    >>> add_three('12')
    6

    To reset the stored value, simply clear the property ``saved_result``.

    >>> del add_three.saved_result
    >>> add_three(9)
    12
    >>> add_three(8)
    12

    Or invoke 'reset()' on it.

    >>> add_three.reset()
    >>> add_three(-3)
    0
    >>> add_three(0)
    0
    """
    
    def wrapper(*args, **kwargs):
        pass
    # WARNING: Decompyle incomplete

    wrapper = None(wrapper)
    
    wrapper.reset = lambda : vars(wrapper).__delitem__('saved_result')
    return wrapper


def method_cache(method = None, cache_wrapper = None):
    """
    Wrap lru_cache to support storing the cache data in the object instances.

    Abstracts the common paradigm where the method explicitly saves an
    underscore-prefixed protected property on first call and returns that
    subsequently.

    >>> class MyClass:
    ...     calls = 0
    ...
    ...     @method_cache
    ...     def method(self, value):
    ...         self.calls += 1
    ...         return value

    >>> a = MyClass()
    >>> a.method(3)
    3
    >>> for x in range(75):
    ...     res = a.method(x)
    >>> a.calls
    75

    Note that the apparent behavior will be exactly like that of lru_cache
    except that the cache is stored on each instance, so values in one
    instance will not flush values from another, and when an instance is
    deleted, so are the cached values for that instance.

    >>> b = MyClass()
    >>> for x in range(35):
    ...     res = b.method(x)
    >>> b.calls
    35
    >>> a.method(0)
    0
    >>> a.calls
    75

    Note that if method had been decorated with ``functools.lru_cache()``,
    a.calls would have been 76 (due to the cached value of 0 having been
    flushed by the 'b' instance).

    Clear the cache with ``.cache_clear()``

    >>> a.method.cache_clear()

    Same for a method that hasn't yet been called.

    >>> c = MyClass()
    >>> c.method.cache_clear()

    Another cache wrapper may be supplied:

    >>> cache = functools.lru_cache(maxsize=2)
    >>> MyClass.method2 = method_cache(lambda self: 3, cache_wrapper=cache)
    >>> a = MyClass()
    >>> a.method2()
    3

    Caution - do not subsequently wrap the method with another decorator, such
    as ``@property``, which changes the semantics of the function.

    See also
    http://code.activestate.com/recipes/577452-a-memoize-decorator-for-instance-methods/
    for another implementation and additional justification.
    """
    
    def wrapper(self = None, *args, **kwargs):
        bound_method = types.MethodType(method, self)
        cached_method = cache_wrapper(bound_method)
        setattr(self, method.__name__, cached_method)
    # WARNING: Decompyle incomplete

    
    wrapper.cache_clear = lambda : pass
    if not _special_method_cache(method, cache_wrapper):
        pass
    return wrapper


def _special_method_cache(method, cache_wrapper):
    """
    Because Python treats special methods differently, it's not
    possible to use instance attributes to implement the cached
    methods.

    Instead, install the wrapper method under a different name
    and return a simple proxy to that wrapper.

    https://github.com/jaraco/jaraco.functools/issues/5
    """
    name = method.__name__
    special_names = ('__getattr__', '__getitem__')
    if name not in special_names:
        return None
    wrapper_name = None + name
    
    def proxy(self = None, *args, **kwargs):
        if wrapper_name not in vars(self):
            bound = types.MethodType(method, self)
            cache = cache_wrapper(bound)
            setattr(self, wrapper_name, cache)
        else:
            cache = getattr(self, wrapper_name)
    # WARNING: Decompyle incomplete

    return proxy


def apply(transform):
    '''
    Decorate a function with a transform function that is
    invoked on results returned from the decorated function.

    >>> @apply(reversed)
    ... def get_numbers(start):
    ...     "doc for get_numbers"
    ...     return range(start, start+3)
    >>> list(get_numbers(4))
    [6, 5, 4]
    >>> get_numbers.__doc__
    \'doc for get_numbers\'
    '''
    
    def wrap(func = None):
        return functools.wraps(func)(compose(transform, func))

    return wrap


def result_invoke(action):
    '''
    Decorate a function with an action function that is
    invoked on the results returned from the decorated
    function (for its side-effect), then return the original
    result.

    >>> @result_invoke(print)
    ... def add_two(a, b):
    ...     return a + b
    >>> x = add_two(2, 3)
    5
    >>> x
    5
    '''
    
    def wrap(func = None):
        
        def wrapper(*args, **kwargs):
            pass
        # WARNING: Decompyle incomplete

        wrapper = None(wrapper)
        return wrapper

    return wrap


def call_aside(f, *args, **kwargs):
    '''
    Call a function for its side effect after initialization.

    >>> @call_aside
    ... def func(): print("called")
    called
    >>> func()
    called

    Use functools.partial to pass parameters to the initial call

    >>> @functools.partial(call_aside, name=\'bingo\')
    ... def func(name): print("called with", name)
    called with bingo
    '''
    pass
# WARNING: Decompyle incomplete


class Throttler:
    '''
    Rate-limit a function (or other callable)
    '''
    
    def __init__(self, func, max_rate = (float('Inf'),)):
        if isinstance(func, Throttler):
            func = func.func
        self.func = func
        self.max_rate = max_rate
        self.reset()

    
    def reset(self):
        self.last_called = 0

    
    def __call__(self, *args, **kwargs):
        self._wait()
    # WARNING: Decompyle incomplete

    
    def _wait(self):
        '''ensure at least 1/max_rate seconds from last call'''
        elapsed = time.time() - self.last_called
        must_wait = 1 / self.max_rate - elapsed
        time.sleep(max(0, must_wait))
        self.last_called = time.time()

    
    def __get__(self, obj, type = (None,)):
        return first_invoke(self._wait, functools.partial(self.func, obj))



def first_invoke(func1, func2):
    '''
    Return a function that when invoked will invoke func1 without
    any parameters (for its side-effect) and then invoke func2
    with whatever parameters were passed, returning its result.
    '''
    
    def wrapper(*args, **kwargs):
        func1()
    # WARNING: Decompyle incomplete

    return wrapper


def retry_call(func, cleanup, retries, trap = ((lambda : pass), 0, ())):
    """
    Given a callable func, trap the indicated exceptions
    for up to 'retries' times, invoking cleanup on the
    exception. On the final attempt, allow any exceptions
    to propagate.
    """
    attempts = itertools.count() if retries == float('inf') else range(retries)
# WARNING: Decompyle incomplete


def retry(*r_args, **r_kwargs):
    '''
    Decorator wrapper for retry_call. Accepts arguments to retry_call
    except func and then returns a decorator for the decorated function.

    Ex:

    >>> @retry(retries=3)
    ... def my_func(a, b):
    ...     "this is my funk"
    ...     print(a, b)
    >>> my_func.__doc__
    \'this is my funk\'
    '''
    
    def decorate(func = None):
        
        def wrapper(*f_args, **f_kwargs):
            pass
        # WARNING: Decompyle incomplete

        wrapper = None(wrapper)
        return wrapper

    return decorate


def print_yielded(func):
    '''
    Convert a generator into a function that prints all yielded elements

    >>> @print_yielded
    ... def x():
    ...     yield 3; yield None
    >>> x()
    3
    None
    '''
    print_all = functools.partial(map, print)
    print_results = compose(more_itertools.consume, print_all, func)
    return functools.wraps(func)(print_results)


def pass_none(func):
    """
    Wrap func so it's not called if its first param is None

    >>> print_text = pass_none(print)
    >>> print_text('text')
    text
    >>> print_text(None)
    """
    
    def wrapper(param = None, *args, **kwargs):
        pass
    # WARNING: Decompyle incomplete

    wrapper = None(wrapper)
    return wrapper


def assign_params(func, namespace):
    """
    Assign parameters from namespace where func solicits.

    >>> def func(x, y=3):
    ...     print(x, y)
    >>> assigned = assign_params(func, dict(x=2, z=4))
    >>> assigned()
    2 3

    The usual errors are raised if a function doesn't receive
    its required parameters:

    >>> assigned = assign_params(func, dict(y=3, z=4))
    >>> assigned()
    Traceback (most recent call last):
    TypeError: func() ...argument...

    It even works on methods:

    >>> class Handler:
    ...     def meth(self, arg):
    ...         print(arg)
    >>> assign_params(Handler().meth, dict(arg='crystal', foo='clear'))()
    crystal
    """
    sig = inspect.signature(func)
    params = sig.parameters.keys()
    call_ns = (lambda .0 = None: pass# WARNING: Decompyle incomplete
)(params)
# WARNING: Decompyle incomplete


def save_method_args(method):
    """
    Wrap a method such that when it is called, the args and kwargs are
    saved on the method.

    >>> class MyClass:
    ...     @save_method_args
    ...     def method(self, a, b):
    ...         print(a, b)
    >>> my_ob = MyClass()
    >>> my_ob.method(1, 2)
    1 2
    >>> my_ob._saved_method.args
    (1, 2)
    >>> my_ob._saved_method.kwargs
    {}
    >>> my_ob.method(a=3, b='foo')
    3 foo
    >>> my_ob._saved_method.args
    ()
    >>> my_ob._saved_method.kwargs == dict(a=3, b='foo')
    True

    The arguments are stored on the instance, allowing for
    different instance to save different args.

    >>> your_ob = MyClass()
    >>> your_ob.method({str('x'): 3}, b=[4])
    {'x': 3} [4]
    >>> your_ob._saved_method.args
    ({'x': 3},)
    >>> my_ob._saved_method.args
    ()
    """
    args_and_kwargs = collections.namedtuple('args_and_kwargs', 'args kwargs')
    
    def wrapper(self = None, *args, **kwargs):
        attr_name = '_saved_' + method.__name__
        attr = args_and_kwargs(args, kwargs)
        setattr(self, attr_name, attr)
    # WARNING: Decompyle incomplete

    wrapper = None(wrapper)
    return wrapper


def except_(*, replace, use, *exceptions):
    """
    Replace the indicated exceptions, if raised, with the indicated
    literal replacement or evaluated expression (if present).

    >>> safe_int = except_(ValueError)(int)
    >>> safe_int('five')
    >>> safe_int('5')
    5

    Specify a literal replacement with ``replace``.

    >>> safe_int_r = except_(ValueError, replace=0)(int)
    >>> safe_int_r('five')
    0

    Provide an expression to ``use`` to pass through particular parameters.

    >>> safe_int_pt = except_(ValueError, use='args[0]')(int)
    >>> safe_int_pt('five')
    'five'

    """
    
    def decorate(func = None):
        
        def wrapper(*args, **kwargs):
            pass
        # WARNING: Decompyle incomplete

        wrapper = None(wrapper)
        return wrapper

    return decorate

