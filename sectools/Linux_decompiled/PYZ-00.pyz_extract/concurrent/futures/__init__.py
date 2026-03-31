
'''Execute computations asynchronously using threads or processes.'''
__author__ = 'Brian Quinlan (brian@sweetapp.com)'
from concurrent.futures._base import FIRST_COMPLETED, FIRST_EXCEPTION, ALL_COMPLETED, CancelledError, TimeoutError, InvalidStateError, BrokenExecutor, Future, Executor, wait, as_completed
__all__ = ('FIRST_COMPLETED', 'FIRST_EXCEPTION', 'ALL_COMPLETED', 'CancelledError', 'TimeoutError', 'BrokenExecutor', 'Future', 'Executor', 'wait', 'as_completed', 'ProcessPoolExecutor', 'ThreadPoolExecutor')

def __dir__():
    return __all__ + ('__author__', '__doc__')


def __getattr__(name):
    global ProcessPoolExecutor, ThreadPoolExecutor
    if name == 'ProcessPoolExecutor':
        pe = ProcessPoolExecutor
        import process
        ProcessPoolExecutor = pe
        return pe
    if None == 'ThreadPoolExecutor':
        te = ThreadPoolExecutor
        import thread
        ThreadPoolExecutor = te
        return te
    raise None(f'''module {__name__} has no attribute {name}''')

