
__doc__ = 'Event loop and event loop policy.'
__all__ = ('AbstractEventLoopPolicy', 'AbstractEventLoop', 'AbstractServer', 'Handle', 'TimerHandle', 'get_event_loop_policy', 'set_event_loop_policy', 'get_event_loop', 'set_event_loop', 'new_event_loop', 'get_child_watcher', 'set_child_watcher', '_set_running_loop', 'get_running_loop', '_get_running_loop')
import contextvars
import os
import socket
import subprocess
import sys
import threading
from  import format_helpers

class Handle:
    '''Object returned by callback registration methods.'''
    __slots__ = ('_callback', '_args', '_cancelled', '_loop', '_source_traceback', '_repr', '__weakref__', '_context')
    
    def __init__(self, callback, args, loop, context = (None,)):
        if context is None:
            context = contextvars.copy_context()
        self._context = context
        self._loop = loop
        self._callback = callback
        self._args = args
        self._cancelled = False
        self._repr = None
        if self._loop.get_debug():
            self._source_traceback = format_helpers.extract_stack(sys._getframe(1))
            return None
        self._source_traceback = None

    
    def _repr_info(self):
        info = [
            self.__class__.__name__]
        if self._cancelled:
            info.append('cancelled')
        if self._callback is not None:
            info.append(format_helpers._format_callback_source(self._callback, self._args))
        if self._source_traceback:
            frame = self._source_traceback[-1]
            info.append(f'''created at {frame[0]}:{frame[1]}''')
        return info

    
    def __repr__(self):
        if self._repr is not None:
            return self._repr
        info = None._repr_info()
        return '<{}>'.format(' '.join(info))

    
    def cancel(self):
        if not self._cancelled:
            self._cancelled = True
            if self._loop.get_debug():
                self._repr = repr(self)
            self._callback = None
            self._args = None
            return None

    
    def cancelled(self):
        return self._cancelled

    
    def _run(self):
        pass
    # WARNING: Decompyle incomplete



class TimerHandle(Handle):
    '''Object returned by timed callback registration methods.'''
    __slots__ = [
        '_scheduled',
        '_when']
    
    def __init__(self = None, when = None, callback = None, args = None, loop = None, context = None):
        pass
    # WARNING: Decompyle incomplete

    
    def _repr_info(self = None):
        info = super()._repr_info()
        pos = 2 if self._cancelled else 1
        info.insert(pos, f'''when={self._when}''')
        return info

    
    def __hash__(self):
        return hash(self._when)

    
    def __lt__(self, other):
        if isinstance(other, TimerHandle):
            return self._when < other._when

    
    def __le__(self, other):
        if isinstance(other, TimerHandle):
            if not self._when < other._when:
                pass
            return self.__eq__(other)

    
    def __gt__(self, other):
        if isinstance(other, TimerHandle):
            return self._when > other._when

    
    def __ge__(self, other):
        if isinstance(other, TimerHandle):
            if not self._when > other._when:
                pass
            return self.__eq__(other)

    
    def __eq__(self, other):
        if isinstance(other, TimerHandle):
            if self._when == other._when and self._callback == other._callback and self._args == other._args:
                pass
            return self._cancelled == other._cancelled

    
    def cancel(self = None):
        if not self._cancelled:
            self._loop._timer_handle_cancelled(self)
        super().cancel()

    
    def when(self):
        '''Return a scheduled callback time.

        The time is an absolute timestamp, using the same time
        reference as loop.time().
        '''
        return self._when

    __classcell__ = None


class AbstractServer:
    '''Abstract server returned by create_server().'''
    
    def close(self):
        '''Stop serving.  This leaves existing connections open.'''
        raise NotImplementedError

    
    def get_loop(self):
        '''Get the event loop the Server object is attached to.'''
        raise NotImplementedError

    
    def is_serving(self):
        '''Return True if the server is accepting connections.'''
        raise NotImplementedError

    
    async def start_serving(self):
        '''Start accepting connections.

        This method is idempotent, so it can be called when
        the server is already being serving.
        '''
        raise NotImplementedError

    
    async def serve_forever(self):
        '''Start accepting connections until the coroutine is cancelled.

        The server is closed when the coroutine is cancelled.
        '''
        raise NotImplementedError

    
    async def wait_closed(self):
        '''Coroutine to wait until service is closed.'''
        raise NotImplementedError

    
    async def __aenter__(self):
        return self

    
    async def __aexit__(self, *exc):
        self.close()
        await self.wait_closed()



class AbstractEventLoop:
    '''Abstract event loop.'''
    
    def run_forever(self):
        '''Run the event loop until stop() is called.'''
        raise NotImplementedError

    
    def run_until_complete(self, future):
        """Run the event loop until a Future is done.

        Return the Future's result, or raise its exception.
        """
        raise NotImplementedError

    
    def stop(self):
        '''Stop the event loop as soon as reasonable.

        Exactly how soon that is may depend on the implementation, but
        no more I/O callbacks should be scheduled.
        '''
        raise NotImplementedError

    
    def is_running(self):
        '''Return whether the event loop is currently running.'''
        raise NotImplementedError

    
    def is_closed(self):
        '''Returns True if the event loop was closed.'''
        raise NotImplementedError

    
    def close(self):
        '''Close the loop.

        The loop should not be running.

        This is idempotent and irreversible.

        No other methods should be called after this one.
        '''
        raise NotImplementedError

    
    async def shutdown_asyncgens(self):
        '''Shutdown all active asynchronous generators.'''
        raise NotImplementedError

    
    async def shutdown_default_executor(self):
        '''Schedule the shutdown of the default executor.'''
        raise NotImplementedError

    
    def _timer_handle_cancelled(self, handle):
        '''Notification that a TimerHandle has been cancelled.'''
        raise NotImplementedError

    
    def call_soon(self = None, callback = {
        'context': None }, *, context, *args):
        pass
    # WARNING: Decompyle incomplete

    
    def call_later(self, delay = None, callback = {
        'context': None }, *, context, *args):
        raise NotImplementedError

    
    def call_at(self, when = None, callback = {
        'context': None }, *, context, *args):
        raise NotImplementedError

    
    def time(self):
        raise NotImplementedError

    
    def create_future(self):
        raise NotImplementedError

    
    def create_task(self = None, coro = {
        'name': None }, *, name):
        raise NotImplementedError

    
    def call_soon_threadsafe(self = None, callback = {
        'context': None }, *, context, *args):
        raise NotImplementedError

    
    def run_in_executor(self, executor, func, *args):
        raise NotImplementedError

    
    def set_default_executor(self, executor):
        raise NotImplementedError

    
    async def getaddrinfo(self, host = None, port = {
        'family': 0,
        'type': 0,
        'proto': 0,
        'flags': 0 }, *, family, type, proto, flags):
        raise NotImplementedError

    
    async def getnameinfo(self, sockaddr, flags = (0,)):
        raise NotImplementedError

    
    async def create_connection(self, protocol_factory = None, host = (None, None), port = {
        'ssl': None,
        'family': 0,
        'proto': 0,
        'flags': 0,
        'sock': None,
        'local_addr': None,
        'server_hostname': None,
        'ssl_handshake_timeout': None,
        'happy_eyeballs_delay': None,
        'interleave': None }, *, ssl, family, proto, flags, sock, local_addr, server_hostname, ssl_handshake_timeout, happy_eyeballs_delay, interleave):
        raise NotImplementedError

    
    async def create_server(self, protocol_factory = None, host = (None, None), port = {
        'family': socket.AF_UNSPEC,
        'flags': socket.AI_PASSIVE,
        'sock': None,
        'backlog': 100,
        'ssl': None,
        'reuse_address': None,
        'reuse_port': None,
        'ssl_handshake_timeout': None,
        'start_serving': True }, *, family, flags, sock, backlog, ssl, reuse_address, reuse_port, ssl_handshake_timeout, start_serving):
        '''A coroutine which creates a TCP server bound to host and port.

        The return value is a Server object which can be used to stop
        the service.

        If host is an empty string or None all interfaces are assumed
        and a list of multiple sockets will be returned (most likely
        one for IPv4 and another one for IPv6). The host parameter can also be
        a sequence (e.g. list) of hosts to bind to.

        family can be set to either AF_INET or AF_INET6 to force the
        socket to use IPv4 or IPv6. If not set it will be determined
        from host (defaults to AF_UNSPEC).

        flags is a bitmask for getaddrinfo().

        sock can optionally be specified in order to use a preexisting
        socket object.

        backlog is the maximum number of queued connections passed to
        listen() (defaults to 100).

        ssl can be set to an SSLContext to enable SSL over the
        accepted connections.

        reuse_address tells the kernel to reuse a local socket in
        TIME_WAIT state, without waiting for its natural timeout to
        expire. If not specified will automatically be set to True on
        UNIX.

        reuse_port tells the kernel to allow this endpoint to be bound to
        the same port as other existing endpoints are bound to, so long as
        they all set this flag when being created. This option is not
        supported on Windows.

        ssl_handshake_timeout is the time in seconds that an SSL server
        will wait for completion of the SSL handshake before aborting the
        connection. Default is 60s.

        start_serving set to True (default) causes the created server
        to start accepting connections immediately.  When set to False,
        the user should await Server.start_serving() or Server.serve_forever()
        to make the server to start accepting connections.
        '''
        raise NotImplementedError

    
    async def sendfile(self, transport, file = None, offset = (0, None), count = {
        'fallback': True }, *, fallback):
        '''Send a file through a transport.

        Return an amount of sent bytes.
        '''
        raise NotImplementedError

    
    async def start_tls(self, transport, protocol = None, sslcontext = {
        'server_side': False,
        'server_hostname': None,
        'ssl_handshake_timeout': None }, *, server_side, server_hostname, ssl_handshake_timeout):
        '''Upgrade a transport to TLS.

        Return a new transport that *protocol* should start using
        immediately.
        '''
        raise NotImplementedError

    
    async def create_unix_connection(self = None, protocol_factory = (None,), path = {
        'ssl': None,
        'sock': None,
        'server_hostname': None,
        'ssl_handshake_timeout': None }, *, ssl, sock, server_hostname, ssl_handshake_timeout):
        raise NotImplementedError

    
    async def create_unix_server(self = None, protocol_factory = (None,), path = {
        'sock': None,
        'backlog': 100,
        'ssl': None,
        'ssl_handshake_timeout': None,
        'start_serving': True }, *, sock, backlog, ssl, ssl_handshake_timeout, start_serving):
        '''A coroutine which creates a UNIX Domain Socket server.

        The return value is a Server object, which can be used to stop
        the service.

        path is a str, representing a file system path to bind the
        server socket to.

        sock can optionally be specified in order to use a preexisting
        socket object.

        backlog is the maximum number of queued connections passed to
        listen() (defaults to 100).

        ssl can be set to an SSLContext to enable SSL over the
        accepted connections.

        ssl_handshake_timeout is the time in seconds that an SSL server
        will wait for the SSL handshake to complete (defaults to 60s).

        start_serving set to True (default) causes the created server
        to start accepting connections immediately.  When set to False,
        the user should await Server.start_serving() or Server.serve_forever()
        to make the server to start accepting connections.
        '''
        raise NotImplementedError

    
    async def connect_accepted_socket(self, protocol_factory = None, sock = {
        'ssl': None,
        'ssl_handshake_timeout': None }, *, ssl, ssl_handshake_timeout):
        '''Handle an accepted connection.

        This is used by servers that accept connections outside of
        asyncio, but use asyncio to handle connections.

        This method is a coroutine.  When completed, the coroutine
        returns a (transport, protocol) pair.
        '''
        raise NotImplementedError

    
    async def create_datagram_endpoint(self, protocol_factory = None, local_addr = (None, None), remote_addr = {
        'family': 0,
        'proto': 0,
        'flags': 0,
        'reuse_address': None,
        'reuse_port': None,
        'allow_broadcast': None,
        'sock': None }, *, family, proto, flags, reuse_address, reuse_port, allow_broadcast, sock):
        """A coroutine which creates a datagram endpoint.

        This method will try to establish the endpoint in the background.
        When successful, the coroutine returns a (transport, protocol) pair.

        protocol_factory must be a callable returning a protocol instance.

        socket family AF_INET, socket.AF_INET6 or socket.AF_UNIX depending on
        host (or family if specified), socket type SOCK_DGRAM.

        reuse_address tells the kernel to reuse a local socket in
        TIME_WAIT state, without waiting for its natural timeout to
        expire. If not specified it will automatically be set to True on
        UNIX.

        reuse_port tells the kernel to allow this endpoint to be bound to
        the same port as other existing endpoints are bound to, so long as
        they all set this flag when being created. This option is not
        supported on Windows and some UNIX's. If the
        :py:data:`~socket.SO_REUSEPORT` constant is not defined then this
        capability is unsupported.

        allow_broadcast tells the kernel to allow this endpoint to send
        messages to the broadcast address.

        sock can optionally be specified in order to use a preexisting
        socket object.
        """
        raise NotImplementedError

    
    async def connect_read_pipe(self, protocol_factory, pipe):
        '''Register read pipe in event loop. Set the pipe to non-blocking mode.

        protocol_factory should instantiate object with Protocol interface.
        pipe is a file-like object.
        Return pair (transport, protocol), where transport supports the
        ReadTransport interface.'''
        raise NotImplementedError

    
    async def connect_write_pipe(self, protocol_factory, pipe):
        '''Register write pipe in event loop.

        protocol_factory should instantiate object with BaseProtocol interface.
        Pipe is file-like object already switched to nonblocking.
        Return pair (transport, protocol), where transport support
        WriteTransport interface.'''
        raise NotImplementedError

    
    async def subprocess_shell(self, protocol_factory = None, cmd = {
        'stdin': subprocess.PIPE,
        'stdout': subprocess.PIPE,
        'stderr': subprocess.PIPE }, *, stdin, stdout, stderr, **kwargs):
        raise NotImplementedError

    
    async def subprocess_exec(self = None, protocol_factory = {
        'stdin': subprocess.PIPE,
        'stdout': subprocess.PIPE,
        'stderr': subprocess.PIPE }, *, stdin, stdout, stderr, *args, **kwargs):
        raise NotImplementedError

    
    def add_reader(self, fd, callback, *args):
        raise NotImplementedError

    
    def remove_reader(self, fd):
        raise NotImplementedError

    
    def add_writer(self, fd, callback, *args):
        raise NotImplementedError

    
    def remove_writer(self, fd):
        raise NotImplementedError

    
    async def sock_recv(self, sock, nbytes):
        raise NotImplementedError

    
    async def sock_recv_into(self, sock, buf):
        raise NotImplementedError

    
    async def sock_sendall(self, sock, data):
        raise NotImplementedError

    
    async def sock_connect(self, sock, address):
        raise NotImplementedError

    
    async def sock_accept(self, sock):
        raise NotImplementedError

    
    async def sock_sendfile(self, sock, file = None, offset = (0, None), count = {
        'fallback': None }, *, fallback):
        raise NotImplementedError

    
    def add_signal_handler(self, sig, callback, *args):
        raise NotImplementedError

    
    def remove_signal_handler(self, sig):
        raise NotImplementedError

    
    def set_task_factory(self, factory):
        raise NotImplementedError

    
    def get_task_factory(self):
        raise NotImplementedError

    
    def get_exception_handler(self):
        raise NotImplementedError

    
    def set_exception_handler(self, handler):
        raise NotImplementedError

    
    def default_exception_handler(self, context):
        raise NotImplementedError

    
    def call_exception_handler(self, context):
        raise NotImplementedError

    
    def get_debug(self):
        raise NotImplementedError

    
    def set_debug(self, enabled):
        raise NotImplementedError



class AbstractEventLoopPolicy:
    '''Abstract policy for accessing the event loop.'''
    
    def get_event_loop(self):
        '''Get the event loop for the current context.

        Returns an event loop object implementing the BaseEventLoop interface,
        or raises an exception in case no event loop has been set for the
        current context and the current policy does not specify to create one.

        It should never return None.'''
        raise NotImplementedError

    
    def set_event_loop(self, loop):
        '''Set the event loop for the current context to loop.'''
        raise NotImplementedError

    
    def new_event_loop(self):
        """Create and return a new event loop object according to this
        policy's rules. If there's need to set this loop as the event loop for
        the current context, set_event_loop must be called explicitly."""
        raise NotImplementedError

    
    def get_child_watcher(self):
        '''Get the watcher for child processes.'''
        raise NotImplementedError

    
    def set_child_watcher(self, watcher):
        '''Set the watcher for child processes.'''
        raise NotImplementedError



class BaseDefaultEventLoopPolicy(AbstractEventLoopPolicy):
    '''Default policy implementation for accessing the event loop.

    In this policy, each thread has its own event loop.  However, we
    only automatically create an event loop by default for the main
    thread; other threads by default have no event loop.

    Other policies may have different rules (e.g. a single global
    event loop, or automatically creating an event loop per thread, or
    using some other notion of context to which an event loop is
    associated).
    '''
    _loop_factory = None
    
    class _Local(threading.local):
        __qualname__ = 'BaseDefaultEventLoopPolicy._Local'
        _loop = None
        _set_called = False

    
    def __init__(self):
        self._local = self._Local()

    
    def get_event_loop(self):
        '''Get the event loop for the current context.

        Returns an instance of EventLoop or raises an exception.
        '''
        if self._local._loop is None and self._local._set_called and threading.current_thread() is threading.main_thread():
            self.set_event_loop(self.new_event_loop())
        if self._local._loop is None:
            raise RuntimeError('There is no current event loop in thread %r.' % threading.current_thread().name)
        return None._local._loop

    
    def set_event_loop(self, loop):
        '''Set the event loop.'''
        self._local._set_called = True
    # WARNING: Decompyle incomplete

    
    def new_event_loop(self):
        '''Create a new event loop.

        You must call set_event_loop() to make this the current event
        loop.
        '''
        return self._loop_factory()


_event_loop_policy = None
_lock = threading.Lock()

class _RunningLoop(threading.local):
    loop_pid = (None, None)

_running_loop = _RunningLoop()

def get_running_loop():
    '''Return the running event loop.  Raise a RuntimeError if there is none.

    This function is thread-specific.
    '''
    loop = _get_running_loop()
    if loop is None:
        raise RuntimeError('no running event loop')


def _get_running_loop():
    '''Return the running event loop or None.

    This is a low-level function intended to be used by event loops.
    This function is thread-specific.
    '''
    (running_loop, pid) = _running_loop.loop_pid
    if running_loop is not None or pid == os.getpid():
        return running_loop
    return None


def _set_running_loop(loop):
    '''Set the running event loop.

    This is a low-level function intended to be used by event loops.
    This function is thread-specific.
    '''
    _running_loop.loop_pid = (loop, os.getpid())


def _init_event_loop_policy():
    global _event_loop_policy
    pass
# WARNING: Decompyle incomplete


def get_event_loop_policy():
    '''Get the current event loop policy.'''
    if _event_loop_policy is None:
        _init_event_loop_policy()
    return _event_loop_policy


def set_event_loop_policy(policy):
    '''Set the current event loop policy.

    If policy is None, the default policy is restored.'''
    pass
# WARNING: Decompyle incomplete


def get_event_loop():
    '''Return an asyncio event loop.

    When called from a coroutine or a callback (e.g. scheduled with call_soon
    or similar API), this function will always return the running event loop.

    If there is no running event loop set, the function will return
    the result of `get_event_loop_policy().get_event_loop()` call.
    '''
    return _py__get_event_loop()


def _get_event_loop(stacklevel = (3,)):
    current_loop = _get_running_loop()
    if current_loop is not None:
        return current_loop
    import warnings
    warnings.warn('There is no current event loop', DeprecationWarning, stacklevel, **('stacklevel',))
    return get_event_loop_policy().get_event_loop()


def set_event_loop(loop):
    '''Equivalent to calling get_event_loop_policy().set_event_loop(loop).'''
    get_event_loop_policy().set_event_loop(loop)


def new_event_loop():
    '''Equivalent to calling get_event_loop_policy().new_event_loop().'''
    return get_event_loop_policy().new_event_loop()


def get_child_watcher():
    '''Equivalent to calling get_event_loop_policy().get_child_watcher().'''
    return get_event_loop_policy().get_child_watcher()


def set_child_watcher(watcher):
    '''Equivalent to calling
    get_event_loop_policy().set_child_watcher(watcher).'''
    return get_event_loop_policy().set_child_watcher(watcher)

_py__get_running_loop = _get_running_loop
_py__set_running_loop = _set_running_loop
_py_get_running_loop = get_running_loop
_py_get_event_loop = get_event_loop
_py__get_event_loop = _get_event_loop
# WARNING: Decompyle incomplete
