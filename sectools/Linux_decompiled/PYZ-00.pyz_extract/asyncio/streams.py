
__all__ = ('StreamReader', 'StreamWriter', 'StreamReaderProtocol', 'open_connection', 'start_server')
import socket
import sys
import warnings
import weakref
if hasattr(socket, 'AF_UNIX'):
    __all__ += ('open_unix_connection', 'start_unix_server')
from  import coroutines
from  import events
from  import exceptions
from  import format_helpers
from  import protocols
from log import logger
from tasks import sleep
_DEFAULT_LIMIT = 65536

async def open_connection(host = None, port = (None, None), *, limit, **kwds):
    """A wrapper for create_connection() returning a (reader, writer) pair.

    The reader returned is a StreamReader instance; the writer is a
    StreamWriter instance.

    The arguments are all the usual arguments to create_connection()
    except protocol_factory; most common are positional host and port,
    with various optional keyword arguments following.

    Additional optional keyword arguments are loop (to set the event loop
    instance to use) and limit (to set the buffer limit passed to the
    StreamReader).

    (If you want to customize the StreamReader and/or
    StreamReaderProtocol classes, just copy the code -- there's
    really nothing special here except some convenience.)
    """
    loop = events.get_running_loop()
    reader = StreamReader(limit, loop, **('limit', 'loop'))
    protocol = StreamReaderProtocol(reader, loop, **('loop',))
# WARNING: Decompyle incomplete


async def start_server(client_connected_cb = None, host = (None, None), port = {
    'limit': _DEFAULT_LIMIT }, *, limit, **kwds):
    '''Start a socket server, call back for each client connected.

    The first parameter, `client_connected_cb`, takes two parameters:
    client_reader, client_writer.  client_reader is a StreamReader
    object, while client_writer is a StreamWriter object.  This
    parameter can either be a plain callback function or a coroutine;
    if it is a coroutine, it will be automatically converted into a
    Task.

    The rest of the arguments are all the usual arguments to
    loop.create_server() except protocol_factory; most common are
    positional host and port, with various optional keyword arguments
    following.  The return value is the same as loop.create_server().

    Additional optional keyword arguments are loop (to set the event loop
    instance to use) and limit (to set the buffer limit passed to the
    StreamReader).

    The return value is the same as loop.create_server(), i.e. a
    Server object which can be used to stop the service.
    '''
    loop = events.get_running_loop()
    
    def factory():
        reader = StreamReader(limit, loop, **('limit', 'loop'))
        protocol = StreamReaderProtocol(reader, client_connected_cb, loop, **('loop',))
        return protocol

# WARNING: Decompyle incomplete

if hasattr(socket, 'AF_UNIX'):
    
    async def open_unix_connection(path = None, *, limit, **kwds):
        '''Similar to `open_connection` but works with UNIX Domain Sockets.'''
        loop = events.get_running_loop()
        reader = StreamReader(limit, loop, **('limit', 'loop'))
        protocol = StreamReaderProtocol(reader, loop, **('loop',))
    # WARNING: Decompyle incomplete

    
    async def start_unix_server(client_connected_cb = None, path = (None,), *, limit, **kwds):
        '''Similar to `start_server` but works with UNIX Domain Sockets.'''
        loop = events.get_running_loop()
        
        def factory():
            reader = StreamReader(limit, loop, **('limit', 'loop'))
            protocol = StreamReaderProtocol(reader, client_connected_cb, loop, **('loop',))
            return protocol

    # WARNING: Decompyle incomplete


class FlowControlMixin(protocols.Protocol):
    '''Reusable flow control logic for StreamWriter.drain().

    This implements the protocol methods pause_writing(),
    resume_writing() and connection_lost().  If the subclass overrides
    these it must call the super methods.

    StreamWriter.drain() must wait for _drain_helper() coroutine.
    '''
    
    def __init__(self, loop = (None,)):
        if loop is None:
            self._loop = events._get_event_loop(4, **('stacklevel',))
        else:
            self._loop = loop
        self._paused = False
        self._drain_waiter = None
        self._connection_lost = False

    
    def pause_writing(self):
        pass
    # WARNING: Decompyle incomplete

    
    def resume_writing(self):
        pass
    # WARNING: Decompyle incomplete

    
    def connection_lost(self, exc):
        self._connection_lost = True
        if not self._paused:
            return None
        waiter = None._drain_waiter
        if waiter is None:
            return None
        self._drain_waiter = None
        if waiter.done():
            return None
        if None is None:
            waiter.set_result(None)
            return None
        None.set_exception(exc)

    
    async def _drain_helper(self):
        if self._connection_lost:
            raise ConnectionResetError('Connection lost')
        if not None._paused:
            return None
        waiter = None._drain_waiter
    # WARNING: Decompyle incomplete

    
    def _get_close_waiter(self, stream):
        raise NotImplementedError



class StreamReaderProtocol(protocols.Protocol, FlowControlMixin):
    '''Helper class to adapt between Protocol and StreamReader.

    (This is a helper class instead of making StreamReader itself a
    Protocol subclass, because the StreamReader has other potential
    uses, and to prevent the user of the StreamReader to accidentally
    call inappropriate methods of the protocol.)
    '''
    _source_traceback = None
    
    def __init__(self = None, stream_reader = None, client_connected_cb = None, loop = None):
        super().__init__(loop, **('loop',))
        if stream_reader is not None:
            self._stream_reader_wr = weakref.ref(stream_reader)
            self._source_traceback = stream_reader._source_traceback
        else:
            self._stream_reader_wr = None
        if client_connected_cb is not None:
            self._strong_reader = stream_reader
        self._reject_connection = False
        self._stream_writer = None
        self._transport = None
        self._client_connected_cb = client_connected_cb
        self._over_ssl = False
        self._closed = self._loop.create_future()

    
    def _stream_reader(self):
        if self._stream_reader_wr is None:
            return None
        return None._stream_reader_wr()

    _stream_reader = property(_stream_reader)
    
    def connection_made(self, transport):
        if self._reject_connection:
            context = {
                'message': 'An open stream was garbage collected prior to establishing network connection; call "stream.close()" explicitly.' }
            if self._source_traceback:
                context['source_traceback'] = self._source_traceback
            self._loop.call_exception_handler(context)
            transport.abort()
            return None
        self._transport = None
        reader = self._stream_reader
        if reader is not None:
            reader.set_transport(transport)
        self._over_ssl = transport.get_extra_info('sslcontext') is not None
        if self._client_connected_cb is not None:
            self._stream_writer = StreamWriter(transport, self, reader, self._loop)
            res = self._client_connected_cb(reader, self._stream_writer)
            if coroutines.iscoroutine(res):
                self._loop.create_task(res)
            self._strong_reader = None
            return None

    
    def connection_lost(self = None, exc = None):
        reader = self._stream_reader
        if reader is not None:
            if exc is None:
                reader.feed_eof()
            else:
                reader.set_exception(exc)
        if not self._closed.done():
            if exc is None:
                self._closed.set_result(None)
            else:
                self._closed.set_exception(exc)
        super().connection_lost(exc)
        self._stream_reader_wr = None
        self._stream_writer = None
        self._transport = None

    
    def data_received(self, data):
        reader = self._stream_reader
        if reader is not None:
            reader.feed_data(data)
            return None

    
    def eof_received(self):
        reader = self._stream_reader
        if reader is not None:
            reader.feed_eof()
        if self._over_ssl:
            return False

    
    def _get_close_waiter(self, stream):
        return self._closed

    
    def __del__(self):
        pass
    # WARNING: Decompyle incomplete

    __classcell__ = None


class StreamWriter:
    '''Wraps a Transport.

    This exposes write(), writelines(), [can_]write_eof(),
    get_extra_info() and close().  It adds drain() which returns an
    optional Future on which you can wait for flow control.  It also
    adds a transport property which references the Transport
    directly.
    '''
    
    def __init__(self, transport, protocol, reader, loop):
        self._transport = transport
        self._protocol = protocol
    # WARNING: Decompyle incomplete

    
    def __repr__(self):
        info = [
            self.__class__.__name__,
            f'''transport={self._transport!r}''']
        if self._reader is not None:
            info.append(f'''reader={self._reader!r}''')
        return '<{}>'.format(' '.join(info))

    
    def transport(self):
        return self._transport

    transport = property(transport)
    
    def write(self, data):
        self._transport.write(data)

    
    def writelines(self, data):
        self._transport.writelines(data)

    
    def write_eof(self):
        return self._transport.write_eof()

    
    def can_write_eof(self):
        return self._transport.can_write_eof()

    
    def close(self):
        return self._transport.close()

    
    def is_closing(self):
        return self._transport.is_closing()

    
    async def wait_closed(self):
        await self._protocol._get_close_waiter(self)

    
    def get_extra_info(self, name, default = (None,)):
        return self._transport.get_extra_info(name, default)

    
    async def drain(self):
        '''Flush the write buffer.

        The intended use is to write

          w.write(data)
          await w.drain()
        '''
        if self._reader is not None:
            exc = self._reader.exception()
            if exc is not None:
                raise exc
            if None._transport.is_closing():
                await sleep(0)
        await self._protocol._drain_helper()



class StreamReader:
    _source_traceback = None
    
    def __init__(self, limit, loop = (_DEFAULT_LIMIT, None)):
        if limit <= 0:
            raise ValueError('Limit cannot be <= 0')
        self._limit = None
        if loop is None:
            self._loop = events._get_event_loop()
        else:
            self._loop = loop
        self._buffer = bytearray()
        self._eof = False
        self._waiter = None
        self._exception = None
        self._transport = None
        self._paused = False
        if self._loop.get_debug():
            self._source_traceback = format_helpers.extract_stack(sys._getframe(1))
            return None

    
    def __repr__(self):
        info = [
            'StreamReader']
        if self._buffer:
            info.append(f'''{len(self._buffer)} bytes''')
        if self._eof:
            info.append('eof')
        if self._limit != _DEFAULT_LIMIT:
            info.append(f'''limit={self._limit}''')
        if self._waiter:
            info.append(f'''waiter={self._waiter!r}''')
        if self._exception:
            info.append(f'''exception={self._exception!r}''')
        if self._transport:
            info.append(f'''transport={self._transport!r}''')
        if self._paused:
            info.append('paused')
        return '<{}>'.format(' '.join(info))

    
    def exception(self):
        return self._exception

    
    def set_exception(self, exc):
        self._exception = exc
        waiter = self._waiter
        if waiter is not None:
            self._waiter = None
            if not waiter.cancelled():
                waiter.set_exception(exc)
                return None
            return None

    
    def _wakeup_waiter(self):
        '''Wakeup read*() functions waiting for data or EOF.'''
        waiter = self._waiter
        if waiter is not None:
            self._waiter = None
            if not waiter.cancelled():
                waiter.set_result(None)
                return None
            return None

    
    def set_transport(self, transport):
        pass
    # WARNING: Decompyle incomplete

    
    def _maybe_resume_transport(self):
        if self._paused or len(self._buffer) <= self._limit:
            self._paused = False
            self._transport.resume_reading()
            return None
        return None

    
    def feed_eof(self):
        self._eof = True
        self._wakeup_waiter()

    
    def at_eof(self):
        """Return True if the buffer is empty and 'feed_eof' was called."""
        if self._eof:
            pass
        return not (self._buffer)

    
    def feed_data(self, data):
        pass
    # WARNING: Decompyle incomplete

    
    async def _wait_for_data(self, func_name):
        '''Wait until feed_data() or feed_eof() is called.

        If stream was paused, automatically resume it.
        '''
        if self._waiter is not None:
            raise RuntimeError(f'''{func_name}() called while another coroutine is already waiting for incoming data''')
    # WARNING: Decompyle incomplete

    
    async def readline(self):
        """Read chunk of data from the stream until newline (b'
') is found.

        On success, return chunk that ends with newline. If only partial
        line can be read due to EOF, return incomplete line without
        terminating newline. When EOF was reached while no bytes read, empty
        bytes object is returned.

        If limit is reached, ValueError will be raised. In that case, if
        newline was found, complete line including newline will be removed
        from internal buffer. Else, internal buffer will be cleared. Limit is
        compared against part of the line without newline.

        If stream was paused, this function will automatically resume it if
        needed.
        """
        sep = b'\n'
        seplen = len(sep)
    # WARNING: Decompyle incomplete

    
    async def readuntil(self, separator = (b'\n',)):
        '''Read data from the stream until ``separator`` is found.

        On success, the data and separator will be removed from the
        internal buffer (consumed). Returned data will include the
        separator at the end.

        Configured stream limit is used to check result. Limit sets the
        maximal length of data that can be returned, not counting the
        separator.

        If an EOF occurs and the complete separator is still not found,
        an IncompleteReadError exception will be raised, and the internal
        buffer will be reset.  The IncompleteReadError.partial attribute
        may contain the separator partially.

        If the data cannot be read because of over limit, a
        LimitOverrunError exception  will be raised, and the data
        will be left in the internal buffer, so it can be read again.
        '''
        seplen = len(separator)
        if seplen == 0:
            raise ValueError('Separator should be at least one-byte string')
        if None._exception is not None:
            raise self._exception
        offset = None
        buflen = len(self._buffer)
        if buflen - offset >= seplen:
            isep = self._buffer.find(separator, offset)
            if isep != -1:
                pass
            else:
                offset = buflen + 1 - seplen
                if offset > self._limit:
                    raise exceptions.LimitOverrunError('Separator is not found, and chunk exceed the limit', offset)
                if None._eof:
                    chunk = bytes(self._buffer)
                    self._buffer.clear()
                    raise exceptions.IncompleteReadError(chunk, None)
                await None._wait_for_data('readuntil')
            if isep > self._limit:
                raise exceptions.LimitOverrunError('Separator is found, but chunk is longer than limit', isep)
            chunk = None._buffer[:isep + seplen]
            del self._buffer[:isep + seplen]
            self._maybe_resume_transport()
            return bytes(chunk)

    
    async def read(self, n = (-1,)):
        '''Read up to `n` bytes from the stream.

        If n is not provided, or set to -1, read until EOF and return all read
        bytes. If the EOF was received and the internal buffer is empty, return
        an empty bytes object.

        If n is zero, return empty bytes object immediately.

        If n is positive, this function try to read `n` bytes, and may return
        less or equal bytes than requested, but at least one byte. If EOF was
        received before any byte is read, this function returns empty byte
        object.

        Returned value is not limited with limit, configured at stream
        creation.

        If stream was paused, this function will automatically resume it if
        needed.
        '''
        if self._exception is not None:
            raise self._exception
        if None == 0:
            return b''
        if None < 0:
            blocks = []
            await self.read(self._limit)
            block = <NODE:28>
            if not block:
                pass
            else:
                blocks.append(block)
            return b''.join(blocks)
        if not None._buffer and self._eof:
            await self._wait_for_data('read')
        data = bytes(self._buffer[:n])
        del self._buffer[:n]
        self._maybe_resume_transport()
        return data

    
    async def readexactly(self, n):
        '''Read exactly `n` bytes.

        Raise an IncompleteReadError if EOF is reached before `n` bytes can be
        read. The IncompleteReadError.partial attribute of the exception will
        contain the partial read bytes.

        if n is zero, return empty bytes object.

        Returned value is not limited with limit, configured at stream
        creation.

        If stream was paused, this function will automatically resume it if
        needed.
        '''
        if n < 0:
            raise ValueError('readexactly size can not be less than zero')
        if None._exception is not None:
            raise self._exception
        if None == 0:
            return b''
        if None(self._buffer) < n:
            if self._eof:
                incomplete = bytes(self._buffer)
                self._buffer.clear()
                raise exceptions.IncompleteReadError(incomplete, n)
            await None._wait_for_data('readexactly')
            if len(self._buffer) < n or len(self._buffer) == n:
                data = bytes(self._buffer)
                self._buffer.clear()
            else:
                data = bytes(self._buffer[:n])
                del self._buffer[:n]
        self._maybe_resume_transport()
        return data

    
    def __aiter__(self):
        return self

    
    async def __anext__(self):
        await self.readline()
        val = <NODE:28>
        if val == b'':
            raise StopAsyncIteration


