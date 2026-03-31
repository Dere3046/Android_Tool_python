
import os
import signal
import socket
import sys
import threading
from  import process
from context import reduction
from  import util
__all__ = [
    'stop']
if sys.platform == 'win32':
    __all__ += [
        'DupSocket']
    
    class DupSocket(object):
        '''Picklable wrapper for a socket.'''
        
        def __init__(self, sock):
            new_sock = sock.dup()
            
            def send(conn = None, pid = None):
                share = new_sock.share(pid)
                conn.send_bytes(share)

            self._id = _resource_sharer.register(send, new_sock.close)

        
        def detach(self):
            '''Get the socket.  This should only be called once.'''
            pass
        # WARNING: Decompyle incomplete


else:
    __all__ += [
        'DupFd']
    
    class DupFd(object):
        '''Wrapper for fd which can be used at any time.'''
        
        def __init__(self, fd):
            new_fd = os.dup(fd)
            
            def send(conn = None, pid = None):
                reduction.send_handle(conn, new_fd, pid)

            
            def close():
                os.close(new_fd)

            self._id = _resource_sharer.register(send, close)

        
        def detach(self):
            '''Get the fd.  This should only be called once.'''
            pass
        # WARNING: Decompyle incomplete



class _ResourceSharer(object):
    '''Manager for resources using background thread.'''
    
    def __init__(self):
        self._key = 0
        self._cache = { }
        self._lock = threading.Lock()
        self._listener = None
        self._address = None
        self._thread = None
        util.register_after_fork(self, _ResourceSharer._afterfork)

    
    def register(self, send, close):
        '''Register resource, returning an identifier.'''
        pass
    # WARNING: Decompyle incomplete

    
    def get_connection(ident):
        '''Return connection from which to receive identified resource.'''
        Client = Client
        import connection
        (address, key) = ident
        c = Client(address, process.current_process().authkey, **('authkey',))
        c.send((key, os.getpid()))
        return c

    get_connection = staticmethod(get_connection)
    
    def stop(self, timeout = (None,)):
        '''Stop the background thread and clear registered resources.'''
        Client = Client
        import connection
    # WARNING: Decompyle incomplete

    
    def _afterfork(self):
        for send, close in self._cache.items():
            close()
        self._cache.clear()
        self._lock._at_fork_reinit()
        if self._listener is not None:
            self._listener.close()
        self._listener = None
        self._address = None
        self._thread = None

    
    def _start(self):
        Listener = Listener
        import connection
    # WARNING: Decompyle incomplete

    
    def _serve(self):
        if hasattr(signal, 'pthread_sigmask'):
            signal.pthread_sigmask(signal.SIG_BLOCK, signal.valid_signals())
    # WARNING: Decompyle incomplete


_resource_sharer = _ResourceSharer()
stop = _resource_sharer.stop
