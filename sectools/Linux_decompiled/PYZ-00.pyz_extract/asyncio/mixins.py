
'''Event loop mixins.'''
import threading
from  import events
_global_lock = threading.Lock()
_marker = object()

class _LoopBoundMixin:
    _loop = None
    
    def __init__(self = None, *, loop):
        if loop is not _marker:
            raise TypeError(f'''As of 3.10, the *loop* parameter was removed from {type(self).__name__}() since it is no longer necessary''')

    
    def _get_loop(self):
        loop = events._get_running_loop()
    # WARNING: Decompyle incomplete


