
__all__ = ()
import reprlib
from _thread import get_ident
from  import format_helpers
_PENDING = 'PENDING'
_CANCELLED = 'CANCELLED'
_FINISHED = 'FINISHED'

def isfuture(obj):
    '''Check for a Future.

    This returns True when obj is a Future instance or is advertising
    itself as duck-type compatible by setting _asyncio_future_blocking.
    See comment in Future for more details.
    '''
    if hasattr(obj.__class__, '_asyncio_future_blocking'):
        pass
    return obj._asyncio_future_blocking is not None


def _format_callbacks(cb):
    '''helper function for Future.__repr__'''
    size = len(cb)
    if not size:
        cb = ''
    
    def format_cb(callback):
        return format_helpers._format_callback_source(callback, ())

    if size == 1:
        cb = format_cb(cb[0][0])
    elif size == 2:
        cb = '{}, {}'.format(format_cb(cb[0][0]), format_cb(cb[1][0]))
    elif size > 2:
        cb = '{}, <{} more>, {}'.format(format_cb(cb[0][0]), size - 2, format_cb(cb[-1][0]))
    return f'''cb=[{cb}]'''

_repr_running = set()

def _future_repr_info(future):
    '''helper function for Future.__repr__'''
    info = [
        future._state.lower()]
# WARNING: Decompyle incomplete

