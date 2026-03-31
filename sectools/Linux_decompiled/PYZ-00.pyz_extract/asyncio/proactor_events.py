
'''Event loop using a proactor and related classes.

A proactor is a "notify-on-completion" multiplexer.  Currently a
proactor is only implemented on Windows with IOCP.
'''
__all__ = ('BaseProactorEventLoop',)
import io
import os
import socket
import warnings
import signal
import threading
import collections
from  import base_events
from  import constants
from  import futures
from  import exceptions
from  import protocols
from  import sslproto
from  import transports
from  import trsock
from log import logger

def _set_socket_extra(transport, sock):
    transport._extra['socket'] = trsock.TransportSocket(sock)
# WARNING: Decompyle incomplete


class _ProactorBasePipeTransport(transports.BaseTransport, transports._FlowControlMixin):
    '''Base class for pipe and socket transports.'''
    
    def __init__(self = None, loop = None, sock = None, protocol = None, waiter = None, extra = None, server = None):
        super().__init__(extra, loop)
        self._set_extra(sock)
        self._sock = sock
        self.set_protocol(protocol)
        self._server = server
        self._buffer = None
        self._read_fut = None
        self._write_fut = None
        self._pending_write = 0
        self._conn_lost = 0
        self._closing = False
        self._eof_written = False
        if self._server is not None:
            self._server._attach()
        self._loop.call_soon(self._protocol.connection_made, self)
        if waiter is not None:
            self._loop.call_soon(futures._set_result_unless_cancelled, waiter, None)
            return None

    
    def __repr__(self):
        info = [
            self.__class__.__name__]
        if self._sock is None:
            info.append('closed')
        elif self._closing:
            info.append('closing')
        if self._sock is not None:
            info.append(f'''fd={self._sock.fileno()}''')
        if self._read_fut is not None:
            info.append(f'''read={self._read_fut!r}''')
        if self._write_fut is not None:
            info.append(f'''write={self._write_fut!r}''')
        if self._buffer:
            info.append(f'''write_bufsize={len(self._buffer)}''')
        if self._eof_written:
            info.append('EOF written')
        return '<{}>'.format(' '.join(info))

    
    def _set_extra(self, sock):
        self._extra['pipe'] = sock

    
    def set_protocol(self, protocol):
        self._protocol = protocol

    
    def get_protocol(self):
        return self._protocol

    
    def is_closing(self):
        return self._closing

    
    def close(self):
        if self._closing:
            return None
        self._closing = None
        self._conn_lost += 1
        if self._buffer and self._write_fut is None:
            self._loop.call_soon(self._call_connection_lost, None)
        if self._read_fut is not None:
            self._read_fut.cancel()
            self._read_fut = None
            return None
        return self

    
    def __del__(self, _warn = (warnings.warn,)):
        if self._sock is not None:
            _warn(f'''unclosed transport {self!r}''', ResourceWarning, self, **('source',))
            self.close()
            return None

    
    def _fatal_error(self, exc, message = ('Fatal error on pipe transport',)):
        pass
    # WARNING: Decompyle incomplete

    
    def _force_close(self, exc):
        if not self._empty_waiter is not None and self._empty_waiter.done():
            if exc is None:
                self._empty_waiter.set_result(None)
            else:
                self._empty_waiter.set_exception(exc)
        if self._closing:
            return None
        self._closing = None
        self._conn_lost += 1
        if self._write_fut:
            self._write_fut.cancel()
            self._write_fut = None
        if self._read_fut:
            self._read_fut.cancel()
            self._read_fut = None
        self._pending_write = 0
        self._buffer = None
        self._loop.call_soon(self._call_connection_lost, exc)

    
    def _call_connection_lost(self, exc):
        pass
    # WARNING: Decompyle incomplete

    
    def get_write_buffer_size(self):
        size = self._pending_write
        if self._buffer is not None:
            size += len(self._buffer)
        return size

    __classcell__ = None


class _ProactorReadPipeTransport(transports.ReadTransport, _ProactorBasePipeTransport):
    '''Transport for read pipes.'''
    
    def __init__(self = None, loop = None, sock = None, protocol = None, waiter = None, extra = None, server = None, buffer_size = None):
        self._pending_data_length = -1
        self._paused = True
        super().__init__(loop, sock, protocol, waiter, extra, server)
        self._data = bytearray(buffer_size)
        self._loop.call_soon(self._loop_reading)
        self._paused = False

    
    def is_reading(self):
        if not (self._paused):
            pass
        return not (self._closing)

    
    def pause_reading(self):
        if self._closing or self._paused:
            return None
        self._paused = None
        if self._loop.get_debug():
            logger.debug('%r pauses reading', self)
            return None

    
    def resume_reading(self):
        if not self._closing or self._paused:
            return None
        self._paused = None
        if self._read_fut is None:
            self._loop.call_soon(self._loop_reading, None)
        length = self._pending_data_length
        self._pending_data_length = -1
        if length > -1:
            self._loop.call_soon(self._data_received, self._data[:length], length)
        if self._loop.get_debug():
            logger.debug('%r resumes reading', self)
            return None

    
    def _eof_received(self):
        if self._loop.get_debug():
            logger.debug('%r received EOF', self)
    # WARNING: Decompyle incomplete

    
    def _data_received(self, data, length):
        pass
    # WARNING: Decompyle incomplete

    
    def _loop_reading(self, fut = (None,)):
        length = -1
        data = None
    # WARNING: Decompyle incomplete

    __classcell__ = None


class _ProactorBaseWritePipeTransport(transports.WriteTransport, _ProactorBasePipeTransport):
    '''Transport for write pipes.'''
    _start_tls_compatible = True
    
    def __init__(self = None, *args, **kw):
        pass
    # WARNING: Decompyle incomplete

    
    def write(self, data):
        if not isinstance(data, (bytes, bytearray, memoryview)):
            raise TypeError(f'''data argument must be a bytes-like object, not {type(data).__name__}''')
        if None._eof_written:
            raise RuntimeError('write_eof() already called')
        if None._empty_waiter is not None:
            raise RuntimeError('unable to write; sendfile is in progress')
        if not None:
            return None
        if None._conn_lost:
            if self._conn_lost >= constants.LOG_THRESHOLD_FOR_CONNLOST_WRITES:
                logger.warning('socket.send() raised exception.')
            self._conn_lost += 1
            return None
    # WARNING: Decompyle incomplete

    
    def _loop_writing(self, f, data = (None, None)):
        pass
    # WARNING: Decompyle incomplete

    
    def can_write_eof(self):
        return True

    
    def write_eof(self):
        self.close()

    
    def abort(self):
        self._force_close(None)

    
    def _make_empty_waiter(self):
        if self._empty_waiter is not None:
            raise RuntimeError('Empty waiter is already set')
        self._empty_waiter = None._loop.create_future()
        if self._write_fut is None:
            self._empty_waiter.set_result(None)
        return self._empty_waiter

    
    def _reset_empty_waiter(self):
        self._empty_waiter = None

    __classcell__ = None


class _ProactorWritePipeTransport(_ProactorBaseWritePipeTransport):
    
    def __init__(self = None, *args, **kw):
        pass
    # WARNING: Decompyle incomplete

    
    def _pipe_closed(self, fut):
        if fut.cancelled():
            return None
    # WARNING: Decompyle incomplete

    __classcell__ = None


class _ProactorDatagramTransport(_ProactorBasePipeTransport):
    max_size = 262144
    
    def __init__(self = None, loop = None, sock = None, protocol = None, address = None, waiter = None, extra = None):
        self._address = address
        self._empty_waiter = None
        super().__init__(loop, sock, protocol, waiter, extra, **('waiter', 'extra'))
        self._buffer = collections.deque()
        self._loop.call_soon(self._loop_reading)

    
    def _set_extra(self, sock):
        _set_socket_extra(self, sock)

    
    def get_write_buffer_size(self):
        return sum((lambda .0: for data, _ in .0:
len(data))(self._buffer))

    
    def abort(self):
        self._force_close(None)

    
    def sendto(self, data, addr = (None,)):
        if not isinstance(data, (bytes, bytearray, memoryview)):
            raise TypeError('data argument must be bytes-like object (%r)', type(data))
        if not None:
            return None
        if None._address is not None and addr not in (None, self._address):
            raise ValueError(f'''Invalid address: must be None or {self._address}''')
        if None._conn_lost and self._address:
            if self._conn_lost >= constants.LOG_THRESHOLD_FOR_CONNLOST_WRITES:
                logger.warning('socket.sendto() raised exception.')
            self._conn_lost += 1
            return None
        None._buffer.append((bytes(data), addr))
        if self._write_fut is None:
            self._loop_writing()
        self._maybe_pause_protocol()

    
    def _loop_writing(self, fut = (None,)):
        pass
    # WARNING: Decompyle incomplete

    
    def _loop_reading(self, fut = (None,)):
        data = None
    # WARNING: Decompyle incomplete

    __classcell__ = None


class _ProactorDuplexPipeTransport(transports.Transport, _ProactorBaseWritePipeTransport, _ProactorReadPipeTransport):
    '''Transport for duplex pipes.'''
    
    def can_write_eof(self):
        return False

    
    def write_eof(self):
        raise NotImplementedError



class _ProactorSocketTransport(transports.Transport, _ProactorBaseWritePipeTransport, _ProactorReadPipeTransport):
    '''Transport for connected sockets.'''
    _sendfile_compatible = constants._SendfileMode.TRY_NATIVE
    
    def __init__(self = None, loop = None, sock = None, protocol = None, waiter = None, extra = None, server = None):
        super().__init__(loop, sock, protocol, waiter, extra, server)
        base_events._set_nodelay(sock)

    
    def _set_extra(self, sock):
        _set_socket_extra(self, sock)

    
    def can_write_eof(self):
        return True

    
    def write_eof(self):
        if self._closing or self._eof_written:
            return None
        self._eof_written = None
        if self._write_fut is None:
            self._sock.shutdown(socket.SHUT_WR)
            return None

    __classcell__ = None


class BaseProactorEventLoop(base_events.BaseEventLoop):
    
    def __init__(self = None, proactor = None):
        super().__init__()
        logger.debug('Using proactor: %s', proactor.__class__.__name__)
        self._proactor = proactor
        self._selector = proactor
        self._self_reading_future = None
        self._accept_futures = { }
        proactor.set_loop(self)
        self._make_self_pipe()
        if threading.current_thread() is threading.main_thread():
            signal.set_wakeup_fd(self._csock.fileno())
            return None

    
    def _make_socket_transport(self, sock, protocol, waiter, extra, server = (None, None, None)):
        return _ProactorSocketTransport(self, sock, protocol, waiter, extra, server)

    
    def _make_ssl_transport(self, rawsock, protocol = None, sslcontext = (None,), waiter = {
        'server_side': False,
        'server_hostname': None,
        'extra': None,
        'server': None,
        'ssl_handshake_timeout': None }, *, server_side, server_hostname, extra, server, ssl_handshake_timeout):
        ssl_protocol = sslproto.SSLProtocol(self, protocol, sslcontext, waiter, server_side, server_hostname, ssl_handshake_timeout, **('ssl_handshake_timeout',))
        _ProactorSocketTransport(self, rawsock, ssl_protocol, extra, server, **('extra', 'server'))
        return ssl_protocol._app_transport

    
    def _make_datagram_transport(self, sock, protocol, address, waiter, extra = (None, None, None)):
        return _ProactorDatagramTransport(self, sock, protocol, address, waiter, extra)

    
    def _make_duplex_pipe_transport(self, sock, protocol, waiter, extra = (None, None)):
        return _ProactorDuplexPipeTransport(self, sock, protocol, waiter, extra)

    
    def _make_read_pipe_transport(self, sock, protocol, waiter, extra = (None, None)):
        return _ProactorReadPipeTransport(self, sock, protocol, waiter, extra)

    
    def _make_write_pipe_transport(self, sock, protocol, waiter, extra = (None, None)):
        return _ProactorWritePipeTransport(self, sock, protocol, waiter, extra)

    
    def close(self = None):
        if self.is_running():
            raise RuntimeError('Cannot close a running event loop')
        if None.is_closed():
            return None
        if None.current_thread() is threading.main_thread():
            signal.set_wakeup_fd(-1)
        self._stop_accept_futures()
        self._close_self_pipe()
        self._proactor.close()
        self._proactor = None
        self._selector = None
        super().close()

    
    async def sock_recv(self, sock, n):
        await self._proactor.recv(sock, n)
        return <NODE:28>

    
    async def sock_recv_into(self, sock, buf):
        await self._proactor.recv_into(sock, buf)
        return <NODE:28>

    
    async def sock_sendall(self, sock, data):
        await self._proactor.send(sock, data)
        return <NODE:28>

    
    async def sock_connect(self, sock, address):
        await self._proactor.connect(sock, address)
        return <NODE:28>

    
    async def sock_accept(self, sock):
        await self._proactor.accept(sock)
        return <NODE:28>

    
    async def _sock_sendfile_native(self, sock, file, offset, count):
        pass
    # WARNING: Decompyle incomplete

    
    async def _sendfile_native(self, transp, file, offset, count):
        resume_reading = transp.is_reading()
        transp.pause_reading()
        await transp._make_empty_waiter()
    # WARNING: Decompyle incomplete

    
    def _close_self_pipe(self):
        if self._self_reading_future is not None:
            self._self_reading_future.cancel()
            self._self_reading_future = None
        self._ssock.close()
        self._ssock = None
        self._csock.close()
        self._csock = None
        self._internal_fds -= 1

    
    def _make_self_pipe(self):
        (self._ssock, self._csock) = socket.socketpair()
        self._ssock.setblocking(False)
        self._csock.setblocking(False)
        self._internal_fds += 1

    
    def _loop_self_reading(self, f = (None,)):
        pass
    # WARNING: Decompyle incomplete

    
    def _write_to_self(self):
        csock = self._csock
        if csock is None:
            return None
        csock.send(b'\x00')
        :
            csock = self._csock
            if csock is None:
                return None
            csock.send(b'\x00')
            :
                csock = self._csock
                if csock is None:
                    return None
                csock.send(b'\x00')
                :
                    csock = self._csock
                    if csock is None:
                        return None
                    csock.send(b'\x00')
                    :
                        csock = self._csock
                        if csock is None:
                            return None
                        csock.send(b'\x00')
                        :
                            csock = self._csock
                            if csock is None:
                                return None
                            csock.send(b'\x00')
                            :
                                csock = self._csock
                                if csock is None:
                                    return None
                                csock.send(b'\x00')
                                :
                                    csock = self._csock
                                    if csock is None:
                                        return None
                                    csock.send(b'\x00')
                                    :
                                        csock = self._csock
                                        if csock is None:
                                            return None
                                        csock.send(b'\x00')
                                        :
                                            csock = self._csock
                                            if csock is None:
                                                return None
                                            csock.send(b'\x00')
                                            :
                                                csock = self._csock
                                                if csock is None:
                                                    return None
                                                csock.send(b'\x00')
                                                :
                                                    csock = self._csock
                                                    if csock is None:
                                                        return None
                                                    csock.send(b'\x00')
                                                    :
                                                        csock = self._csock
                                                        if csock is None:
                                                            return None
                                                        csock.send(b'\x00')
                                                        :
                                                            csock = self._csock
                                                            if csock is None:
                                                                return None
                                                            csock.send(b'\x00')
                                                            :
                                                                csock = self._csock
                                                                if csock is None:
                                                                    return None
                                                                csock.send(b'\x00')
                                                                :
                                                                    csock = self._csock
                                                                    if csock is None:
                                                                        return None
                                                                    csock.send(b'\x00')
                                                                    :
                                                                        csock = self._csock
                                                                        if csock is None:
                                                                            return None
                                                                        csock.send(b'\x00')
                                                                        :
                                                                            csock = self._csock
                                                                            if csock is None:
                                                                                return None
                                                                            csock.send(b'\x00')
                                                                            :
                                                                                csock = self._csock
                                                                                if csock is None:
                                                                                    return None
                                                                                csock.send(b'\x00')
                                                                                :
                                                                                    csock = self._csock
                                                                                    if csock is None:
                                                                                        return None
                                                                                    csock.send(b'\x00')
                                                                                    :
                                                                                        csock = self._csock
                                                                                        if csock is None:
                                                                                            return None
                                                                                        csock.send(b'\x00')
                                                                                        :
                                                                                            csock = self._csock
                                                                                            if csock is None:
                                                                                                return None
                                                                                            csock.send(b'\x00')
                                                                                            :
                                                                                                csock = self._csock
                                                                                                if csock is None:
                                                                                                    return None
                                                                                                csock.send(b'\x00')
                                                                                                :
                                                                                                    csock = self._csock
                                                                                                    if csock is None:
                                                                                                        return None
                                                                                                    csock.send(b'\x00')
                                                                                                    :
                                                                                                        csock = self._csock
                                                                                                        if csock is None:
                                                                                                            return None
                                                                                                        csock.send(b'\x00')
                                                                                                        :
                                                                                                            csock = self._csock
                                                                                                            if csock is None:
                                                                                                                return None
                                                                                                            csock.send(b'\x00')
                                                                                                            :
                                                                                                                csock = self._csock
                                                                                                                if csock is None:
                                                                                                                    return None
                                                                                                                csock.send(b'\x00')
                                                                                                                :
                                                                                                                    csock = self._csock
                                                                                                                    if csock is None:
                                                                                                                        return None
                                                                                                                    csock.send(b'\x00')
                                                                                                                    :
                                                                                                                        csock = self._csock
                                                                                                                        if csock is None:
                                                                                                                            return None
                                                                                                                        csock.send(b'\x00')
                                                                                                                        :
                                                                                                                            csock = self._csock
                                                                                                                            if csock is None:
                                                                                                                                return None
                                                                                                                            csock.send(b'\x00')
                                                                                                                            :
                                                                                                                                csock = self._csock
                                                                                                                                if csock is None:
                                                                                                                                    return None
                                                                                                                                csock.send(b'\x00')
                                                                                                                                :
                                                                                                                                    csock = self._csock
                                                                                                                                    if csock is None:
                                                                                                                                        return None
                                                                                                                                    csock.send(b'\x00')
                                                                                                                                    :
                                                                                                                                        csock = self._csock
                                                                                                                                        if csock is None:
                                                                                                                                            return None
                                                                                                                                        csock.send(b'\x00')
                                                                                                                                        :
                                                                                                                                            csock = self._csock
                                                                                                                                            if csock is None:
                                                                                                                                                return None
                                                                                                                                            csock.send(b'\x00')
                                                                                                                                            :
                                                                                                                                                csock = self._csock
                                                                                                                                                if csock is None:
                                                                                                                                                    return None
                                                                                                                                                csock.send(b'\x00')
                                                                                                                                                :
                                                                                                                                                    csock = self._csock
                                                                                                                                                    if csock is None:
                                                                                                                                                        return None
                                                                                                                                                    csock.send(b'\x00')
                                                                                                                                                    :
                                                                                                                                                        csock = self._csock
                                                                                                                                                        if csock is None:
                                                                                                                                                            return None
                                                                                                                                                        csock.send(b'\x00')
                                                                                                                                                        :
                                                                                                                                                            csock = self._csock
                                                                                                                                                            if csock is None:
                                                                                                                                                                return None
                                                                                                                                                            csock.send(b'\x00')
                                                                                                                                                            :
                                                                                                                                                                csock = self._csock
                                                                                                                                                                if csock is None:
                                                                                                                                                                    return None
                                                                                                                                                                csock.send(b'\x00')
                                                                                                                                                                :
                                                                                                                                                                    csock = self._csock
                                                                                                                                                                    if csock is None:
                                                                                                                                                                        return None
                                                                                                                                                                    csock.send(b'\x00')
                                                                                                                                                                    :
                                                                                                                                                                        csock = self._csock
                                                                                                                                                                        if csock is None:
                                                                                                                                                                            return None
                                                                                                                                                                        csock.send(b'\x00')
                                                                                                                                                                        :
                                                                                                                                                                            csock = self._csock
                                                                                                                                                                            if csock is None:
                                                                                                                                                                                return None
                                                                                                                                                                            csock.send(b'\x00')
                                                                                                                                                                            :
                                                                                                                                                                                csock = self._csock
                                                                                                                                                                                if csock is None:
                                                                                                                                                                                    return None
                                                                                                                                                                                csock.send(b'\x00')
                                                                                                                                                                                :
                                                                                                                                                                                    csock = self._csock
                                                                                                                                                                                    if csock is None:
                                                                                                                                                                                        return None
                                                                                                                                                                                    csock.send(b'\x00')
                                                                                                                                                                                    :
                                                                                                                                                                                        csock = self._csock
                                                                                                                                                                                        if csock is None:
                                                                                                                                                                                            return None
                                                                                                                                                                                        csock.send(b'\x00')
                                                                                                                                                                                        :
                                                                                                                                                                                            csock = self._csock
                                                                                                                                                                                            if csock is None:
                                                                                                                                                                                                return None
                                                                                                                                                                                            csock.send(b'\x00')
                                                                                                                                                                                            :
                                                                                                                                                                                                csock = self._csock
                                                                                                                                                                                                if csock is None:
                                                                                                                                                                                                    return None
                                                                                                                                                                                                csock.send(b'\x00')
                                                                                                                                                                                                :
                                                                                                                                                                                                    csock = self._csock
                                                                                                                                                                                                    if csock is None:
                                                                                                                                                                                                        return None
                                                                                                                                                                                                    csock.send(b'\x00')
                                                                                                                                                                                                    :
                                                                                                                                                                                                        csock = self._csock
                                                                                                                                                                                                        if csock is None:
                                                                                                                                                                                                            return None
                                                                                                                                                                                                        csock.send(b'\x00')
                                                                                                                                                                                                        :
                                                                                                                                                                                                            csock = self._csock
                                                                                                                                                                                                            if csock is None:
                                                                                                                                                                                                                return None
                                                                                                                                                                                                            csock.send(b'\x00')
                                                                                                                                                                                                            :
                                                                                                                                                                                                                csock = self._csock
                                                                                                                                                                                                                if csock is None:
                                                                                                                                                                                                                    return None
                                                                                                                                                                                                                csock.send(b'\x00')
                                                                                                                                                                                                                :
                                                                                                                                                                                                                    csock = self._csock
                                                                                                                                                                                                                    if csock is None:
                                                                                                                                                                                                                        return None
                                                                                                                                                                                                                    csock.send(b'\x00')
                                                                                                                                                                                                                    :
                                                                                                                                                                                                                        csock = self._csock
                                                                                                                                                                                                                        if csock is None:
                                                                                                                                                                                                                            return None
                                                                                                                                                                                                                        csock.send(b'\x00')
                                                                                                                                                                                                                        :
                                                                                                                                                                                                                            csock = self._csock
                                                                                                                                                                                                                            if csock is None:
                                                                                                                                                                                                                                return None
                                                                                                                                                                                                                            csock.send(b'\x00')
                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                csock = self._csock
                                                                                                                                                                                                                                if csock is None:
                                                                                                                                                                                                                                    return None
                                                                                                                                                                                                                                csock.send(b'\x00')
                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                    csock = self._csock
                                                                                                                                                                                                                                    if csock is None:
                                                                                                                                                                                                                                        return None
                                                                                                                                                                                                                                    csock.send(b'\x00')
                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                        csock = self._csock
                                                                                                                                                                                                                                        if csock is None:
                                                                                                                                                                                                                                            return None
                                                                                                                                                                                                                                        csock.send(b'\x00')
                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                            csock = self._csock
                                                                                                                                                                                                                                            if csock is None:
                                                                                                                                                                                                                                                return None
                                                                                                                                                                                                                                            csock.send(b'\x00')
                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                csock = self._csock
                                                                                                                                                                                                                                                if csock is None:
                                                                                                                                                                                                                                                    return None
                                                                                                                                                                                                                                                csock.send(b'\x00')
                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                    csock = self._csock
                                                                                                                                                                                                                                                    if csock is None:
                                                                                                                                                                                                                                                        return None
                                                                                                                                                                                                                                                    csock.send(b'\x00')
                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                        csock = self._csock
                                                                                                                                                                                                                                                        if csock is None:
                                                                                                                                                                                                                                                            return None
                                                                                                                                                                                                                                                        csock.send(b'\x00')
                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                            csock = self._csock
                                                                                                                                                                                                                                                            if csock is None:
                                                                                                                                                                                                                                                                return None
                                                                                                                                                                                                                                                            csock.send(b'\x00')
                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                csock = self._csock
                                                                                                                                                                                                                                                                if csock is None:
                                                                                                                                                                                                                                                                    return None
                                                                                                                                                                                                                                                                csock.send(b'\x00')
                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                    csock = self._csock
                                                                                                                                                                                                                                                                    if csock is None:
                                                                                                                                                                                                                                                                        return None
                                                                                                                                                                                                                                                                    csock.send(b'\x00')
                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                        csock = self._csock
                                                                                                                                                                                                                                                                        if csock is None:
                                                                                                                                                                                                                                                                            return None
                                                                                                                                                                                                                                                                        csock.send(b'\x00')
                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                            csock = self._csock
                                                                                                                                                                                                                                                                            if csock is None:
                                                                                                                                                                                                                                                                                return None
                                                                                                                                                                                                                                                                            csock.send(b'\x00')
                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                csock = self._csock
                                                                                                                                                                                                                                                                                if csock is None:
                                                                                                                                                                                                                                                                                    return None
                                                                                                                                                                                                                                                                                csock.send(b'\x00')
                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                    csock = self._csock
                                                                                                                                                                                                                                                                                    if csock is None:
                                                                                                                                                                                                                                                                                        return None
                                                                                                                                                                                                                                                                                    csock.send(b'\x00')
                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                        csock = self._csock
                                                                                                                                                                                                                                                                                        if csock is None:
                                                                                                                                                                                                                                                                                            return None
                                                                                                                                                                                                                                                                                        csock.send(b'\x00')
                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                            csock = self._csock
                                                                                                                                                                                                                                                                                            if csock is None:
                                                                                                                                                                                                                                                                                                return None
                                                                                                                                                                                                                                                                                            csock.send(b'\x00')
                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                csock = self._csock
                                                                                                                                                                                                                                                                                                if csock is None:
                                                                                                                                                                                                                                                                                                    return None
                                                                                                                                                                                                                                                                                                csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                    csock = self._csock
                                                                                                                                                                                                                                                                                                    if csock is None:
                                                                                                                                                                                                                                                                                                        return None
                                                                                                                                                                                                                                                                                                    csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                        csock = self._csock
                                                                                                                                                                                                                                                                                                        if csock is None:
                                                                                                                                                                                                                                                                                                            return None
                                                                                                                                                                                                                                                                                                        csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                            csock = self._csock
                                                                                                                                                                                                                                                                                                            if csock is None:
                                                                                                                                                                                                                                                                                                                return None
                                                                                                                                                                                                                                                                                                            csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                csock = self._csock
                                                                                                                                                                                                                                                                                                                if csock is None:
                                                                                                                                                                                                                                                                                                                    return None
                                                                                                                                                                                                                                                                                                                csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                    csock = self._csock
                                                                                                                                                                                                                                                                                                                    if csock is None:
                                                                                                                                                                                                                                                                                                                        return None
                                                                                                                                                                                                                                                                                                                    csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                        csock = self._csock
                                                                                                                                                                                                                                                                                                                        if csock is None:
                                                                                                                                                                                                                                                                                                                            return None
                                                                                                                                                                                                                                                                                                                        csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                            csock = self._csock
                                                                                                                                                                                                                                                                                                                            if csock is None:
                                                                                                                                                                                                                                                                                                                                return None
                                                                                                                                                                                                                                                                                                                            csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                csock = self._csock
                                                                                                                                                                                                                                                                                                                                if csock is None:
                                                                                                                                                                                                                                                                                                                                    return None
                                                                                                                                                                                                                                                                                                                                csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                    csock = self._csock
                                                                                                                                                                                                                                                                                                                                    if csock is None:
                                                                                                                                                                                                                                                                                                                                        return None
                                                                                                                                                                                                                                                                                                                                    csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                        csock = self._csock
                                                                                                                                                                                                                                                                                                                                        if csock is None:
                                                                                                                                                                                                                                                                                                                                            return None
                                                                                                                                                                                                                                                                                                                                        csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                            csock = self._csock
                                                                                                                                                                                                                                                                                                                                            if csock is None:
                                                                                                                                                                                                                                                                                                                                                return None
                                                                                                                                                                                                                                                                                                                                            csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                csock = self._csock
                                                                                                                                                                                                                                                                                                                                                if csock is None:
                                                                                                                                                                                                                                                                                                                                                    return None
                                                                                                                                                                                                                                                                                                                                                csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                                    csock = self._csock
                                                                                                                                                                                                                                                                                                                                                    if csock is None:
                                                                                                                                                                                                                                                                                                                                                        return None
                                                                                                                                                                                                                                                                                                                                                    csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                                        csock = self._csock
                                                                                                                                                                                                                                                                                                                                                        if csock is None:
                                                                                                                                                                                                                                                                                                                                                            return None
                                                                                                                                                                                                                                                                                                                                                        csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                                            csock = self._csock
                                                                                                                                                                                                                                                                                                                                                            if csock is None:
                                                                                                                                                                                                                                                                                                                                                                return None
                                                                                                                                                                                                                                                                                                                                                            csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                                csock = self._csock
                                                                                                                                                                                                                                                                                                                                                                if csock is None:
                                                                                                                                                                                                                                                                                                                                                                    return None
                                                                                                                                                                                                                                                                                                                                                                csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                                                    csock = self._csock
                                                                                                                                                                                                                                                                                                                                                                    if csock is None:
                                                                                                                                                                                                                                                                                                                                                                        return None
                                                                                                                                                                                                                                                                                                                                                                    csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                                                        csock = self._csock
                                                                                                                                                                                                                                                                                                                                                                        if csock is None:
                                                                                                                                                                                                                                                                                                                                                                            return None
                                                                                                                                                                                                                                                                                                                                                                        csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                                                            csock = self._csock
                                                                                                                                                                                                                                                                                                                                                                            if csock is None:
                                                                                                                                                                                                                                                                                                                                                                                return None
                                                                                                                                                                                                                                                                                                                                                                            csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                                                csock = self._csock
                                                                                                                                                                                                                                                                                                                                                                                if csock is None:
                                                                                                                                                                                                                                                                                                                                                                                    return None
                                                                                                                                                                                                                                                                                                                                                                                csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                                                                    csock = self._csock
                                                                                                                                                                                                                                                                                                                                                                                    if csock is None:
                                                                                                                                                                                                                                                                                                                                                                                        return None
                                                                                                                                                                                                                                                                                                                                                                                    csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                                                                        csock = self._csock
                                                                                                                                                                                                                                                                                                                                                                                        if csock is None:
                                                                                                                                                                                                                                                                                                                                                                                            return None
                                                                                                                                                                                                                                                                                                                                                                                        csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                                                                            csock = self._csock
                                                                                                                                                                                                                                                                                                                                                                                            if csock is None:
                                                                                                                                                                                                                                                                                                                                                                                                return None
                                                                                                                                                                                                                                                                                                                                                                                            csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                                                                csock = self._csock
                                                                                                                                                                                                                                                                                                                                                                                                if csock is None:
                                                                                                                                                                                                                                                                                                                                                                                                    return None
                                                                                                                                                                                                                                                                                                                                                                                                csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                                                                                    csock = self._csock
                                                                                                                                                                                                                                                                                                                                                                                                    if csock is None:
                                                                                                                                                                                                                                                                                                                                                                                                        return None
                                                                                                                                                                                                                                                                                                                                                                                                    csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                                                                                        csock = self._csock
                                                                                                                                                                                                                                                                                                                                                                                                        if csock is None:
                                                                                                                                                                                                                                                                                                                                                                                                            return None
                                                                                                                                                                                                                                                                                                                                                                                                        csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                                                                                            csock = self._csock
                                                                                                                                                                                                                                                                                                                                                                                                            if csock is None:
                                                                                                                                                                                                                                                                                                                                                                                                                return None
                                                                                                                                                                                                                                                                                                                                                                                                            csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                                                                                csock = self._csock
                                                                                                                                                                                                                                                                                                                                                                                                                if csock is None:
                                                                                                                                                                                                                                                                                                                                                                                                                    return None
                                                                                                                                                                                                                                                                                                                                                                                                                csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                                                                                                    csock = self._csock
                                                                                                                                                                                                                                                                                                                                                                                                                    if csock is None:
                                                                                                                                                                                                                                                                                                                                                                                                                        return None
                                                                                                                                                                                                                                                                                                                                                                                                                    csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                                                                                                        csock = self._csock
                                                                                                                                                                                                                                                                                                                                                                                                                        if csock is None:
                                                                                                                                                                                                                                                                                                                                                                                                                            return None
                                                                                                                                                                                                                                                                                                                                                                                                                        csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                                                                                                            csock = self._csock
                                                                                                                                                                                                                                                                                                                                                                                                                            if csock is None:
                                                                                                                                                                                                                                                                                                                                                                                                                                return None
                                                                                                                                                                                                                                                                                                                                                                                                                            csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                                                                                                csock = self._csock
                                                                                                                                                                                                                                                                                                                                                                                                                                if csock is None:
                                                                                                                                                                                                                                                                                                                                                                                                                                    return None
                                                                                                                                                                                                                                                                                                                                                                                                                                csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                                                                                                                    csock = self._csock
                                                                                                                                                                                                                                                                                                                                                                                                                                    if csock is None:
                                                                                                                                                                                                                                                                                                                                                                                                                                        return None
                                                                                                                                                                                                                                                                                                                                                                                                                                    csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                                                                                                                        csock = self._csock
                                                                                                                                                                                                                                                                                                                                                                                                                                        if csock is None:
                                                                                                                                                                                                                                                                                                                                                                                                                                            return None
                                                                                                                                                                                                                                                                                                                                                                                                                                        csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                                                                                                                            csock = self._csock
                                                                                                                                                                                                                                                                                                                                                                                                                                            if csock is None:
                                                                                                                                                                                                                                                                                                                                                                                                                                                return None
                                                                                                                                                                                                                                                                                                                                                                                                                                            csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                                                                                                                csock = self._csock
                                                                                                                                                                                                                                                                                                                                                                                                                                                if csock is None:
                                                                                                                                                                                                                                                                                                                                                                                                                                                    return None
                                                                                                                                                                                                                                                                                                                                                                                                                                                csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                                                                                                                                    csock = self._csock
                                                                                                                                                                                                                                                                                                                                                                                                                                                    if csock is None:
                                                                                                                                                                                                                                                                                                                                                                                                                                                        return None
                                                                                                                                                                                                                                                                                                                                                                                                                                                    csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                                                                                                                                        csock = self._csock
                                                                                                                                                                                                                                                                                                                                                                                                                                                        if csock is None:
                                                                                                                                                                                                                                                                                                                                                                                                                                                            return None
                                                                                                                                                                                                                                                                                                                                                                                                                                                        csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                                                                                                                                            csock = self._csock
                                                                                                                                                                                                                                                                                                                                                                                                                                                            if csock is None:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                return None
                                                                                                                                                                                                                                                                                                                                                                                                                                                            csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                                                                                                                                csock = self._csock
                                                                                                                                                                                                                                                                                                                                                                                                                                                                if csock is None:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                    return None
                                                                                                                                                                                                                                                                                                                                                                                                                                                                csock.send(b'\x00')
                                                                                                                                                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                                                                                                                                                    csock = self._csock
                                                                                                                                                                                                                                                                                                                                                                                                                                                                    if csock is None:
                                                                                                                                                                                                                                                                                                                                               