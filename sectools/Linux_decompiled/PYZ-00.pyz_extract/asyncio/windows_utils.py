
'''Various Windows specific bits and pieces.'''
import sys
if sys.platform != 'win32':
    raise ImportError('win32 only')
import _winapi
import itertools
import msvcrt
import os
import subprocess
import tempfile
import warnings
__all__ = ('pipe', 'Popen', 'PIPE', 'PipeHandle')
BUFSIZE = 8192
PIPE = subprocess.PIPE
STDOUT = subprocess.STDOUT
_mmap_counter = itertools.count()

def pipe(*, duplex, overlapped, bufsize):
    '''Like os.pipe() but with overlapped support and using handles not fds.'''
    address = tempfile.mktemp('\\\\.\\pipe\\python-pipe-{:d}-{:d}-'.format(os.getpid(), next(_mmap_counter)), **('prefix',))
    if duplex:
        openmode = _winapi.PIPE_ACCESS_DUPLEX
        access = _winapi.GENERIC_READ | _winapi.GENERIC_WRITE
        obsize = bufsize
        ibsize = bufsize
    else:
        openmode = _winapi.PIPE_ACCESS_INBOUND
        access = _winapi.GENERIC_WRITE
        obsize = 0
        ibsize = bufsize
    openmode |= _winapi.FILE_FLAG_FIRST_PIPE_INSTANCE
    if overlapped[0]:
        openmode |= _winapi.FILE_FLAG_OVERLAPPED
    if overlapped[1]:
        flags_and_attribs = _winapi.FILE_FLAG_OVERLAPPED
    else:
        flags_and_attribs = 0
    h1 = None
    h2 = None
    
    try:
        h1 = _winapi.CreateNamedPipe(address, openmode, _winapi.PIPE_WAIT, 1, obsize, ibsize, _winapi.NMPWAIT_WAIT_FOREVER, _winapi.NULL)
        h2 = _winapi.CreateFile(address, access, 0, _winapi.NULL, _winapi.OPEN_EXISTING, flags_and_attribs, _winapi.NULL)
        ov = _winapi.ConnectNamedPipe(h1, True, **('overlapped',))
        ov.GetOverlappedResult(True)
    finally:
        return None
        if h1 is not None:
            _winapi.CloseHandle(h1)
        if h2 is not None:
            _winapi.CloseHandle(h2)
        raise 



class PipeHandle:
    '''Wrapper for an overlapped pipe handle which is vaguely file-object like.

    The IOCP event loop can use these instead of socket objects.
    '''
    
    def __init__(self, handle):
        self._handle = handle

    
    def __repr__(self):
        if self._handle is not None:
            handle = f'''handle={self._handle!r}'''
        else:
            handle = 'closed'
        return f'''<{self.__class__.__name__} {handle}>'''

    
    def handle(self):
        return self._handle

    handle = property(handle)
    
    def fileno(self):
        if self._handle is None:
            raise ValueError('I/O operation on closed pipe')
        return None._handle

    
    def close(self = None, *, CloseHandle):
        if self._handle is not None:
            CloseHandle(self._handle)
            self._handle = None
            return None

    
    def __del__(self, _warn = (warnings.warn,)):
        if self._handle is not None:
            _warn(f'''unclosed {self!r}''', ResourceWarning, self, **('source',))
            self.close()
            return None

    
    def __enter__(self):
        return self

    
    def __exit__(self, t, v, tb):
        self.close()



class Popen(subprocess.Popen):
    '''Replacement for subprocess.Popen using overlapped pipe handles.

    The stdin, stdout, stderr are None or instances of PipeHandle.
    '''
    
    def __init__(self = None, args = None, stdin = None, stdout = None, stderr = None, **kwds):
        pass
    # WARNING: Decompyle incomplete

    __classcell__ = None

