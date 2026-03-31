
__all__ = ('create_subprocess_exec', 'create_subprocess_shell')
import subprocess
from  import events
from  import protocols
from  import streams
from  import tasks
from log import logger
PIPE = subprocess.PIPE
STDOUT = subprocess.STDOUT
DEVNULL = subprocess.DEVNULL

class SubprocessStreamProtocol(protocols.SubprocessProtocol, streams.FlowControlMixin):
    '''Like StreamReaderProtocol, but for a subprocess.'''
    
    def __init__(self = None, limit = None, loop = None):
        super().__init__(loop, **('loop',))
        self._limit = limit
        self.stdin = None
        self.stdout = None
        self.stderr = None
        self._transport = None
        self._process_exited = False
        self._pipe_fds = []
        self._stdin_closed = self._loop.create_future()

    
    def __repr__(self):
        info = [
            self.__class__.__name__]
        if self.stdin is not None:
            info.append(f'''stdin={self.stdin!r}''')
        if self.stdout is not None:
            info.append(f'''stdout={self.stdout!r}''')
        if self.stderr is not None:
            info.append(f'''stderr={self.stderr!r}''')
        return '<{}>'.format(' '.join(info))

    
    def connection_made(self, transport):
        self._transport = transport
        stdout_transport = transport.get_pipe_transport(1)
        if stdout_transport is not None:
            self.stdout = streams.StreamReader(self._limit, self._loop, **('limit', 'loop'))
            self.stdout.set_transport(stdout_transport)
            self._pipe_fds.append(1)
        stderr_transport = transport.get_pipe_transport(2)
        if stderr_transport is not None:
            self.stderr = streams.StreamReader(self._limit, self._loop, **('limit', 'loop'))
            self.stderr.set_transport(stderr_transport)
            self._pipe_fds.append(2)
        stdin_transport = transport.get_pipe_transport(0)
        if stdin_transport is not None:
            self.stdin = streams.StreamWriter(stdin_transport, self, None, self._loop, **('protocol', 'reader', 'loop'))
            return None

    
    def pipe_data_received(self, fd, data):
        if fd == 1:
            reader = self.stdout
        elif fd == 2:
            reader = self.stderr
        else:
            reader = None
        if reader is not None:
            reader.feed_data(data)
            return None

    
    def pipe_connection_lost(self, fd, exc):
        if fd == 0:
            pipe = self.stdin
            if pipe is not None:
                pipe.close()
            self.connection_lost(exc)
            if exc is None:
                self._stdin_closed.set_result(None)
                return None
            None._stdin_closed.set_exception(exc)
            return None
        if None == 1:
            reader = self.stdout
        elif fd == 2:
            reader = self.stderr
        else:
            reader = None
        if reader is not None:
            if exc is None:
                reader.feed_eof()
            else:
                reader.set_exception(exc)
        if fd in self._pipe_fds:
            self._pipe_fds.remove(fd)
        self._maybe_close_transport()

    
    def process_exited(self):
        self._process_exited = True
        self._maybe_close_transport()

    
    def _maybe_close_transport(self):
        if len(self._pipe_fds) == 0 or self._process_exited:
            self._transport.close()
            self._transport = None
            return None
        return None

    
    def _get_close_waiter(self, stream):
        if stream is self.stdin:
            return self._stdin_closed

    __classcell__ = None


class Process:
    
    def __init__(self, transport, protocol, loop):
        self._transport = transport
        self._protocol = protocol
        self._loop = loop
        self.stdin = protocol.stdin
        self.stdout = protocol.stdout
        self.stderr = protocol.stderr
        self.pid = transport.get_pid()

    
    def __repr__(self):
        return f'''<{self.__class__.__name__} {self.pid}>'''

    
    def returncode(self):
        return self._transport.get_returncode()

    returncode = property(returncode)
    
    async def wait(self):
        '''Wait until the process exit and return the process return code.'''
        await self._transport._wait()
        return <NODE:28>

    
    def send_signal(self, signal):
        self._transport.send_signal(signal)

    
    def terminate(self):
        self._transport.terminate()

    
    def kill(self):
        self._transport.kill()

    
    async def _feed_stdin(self, input):
        debug = self._loop.get_debug()
        self.stdin.write(input)
        if debug:
            logger.debug('%r communicate: feed stdin (%s bytes)', self, len(input))
    # WARNING: Decompyle incomplete

    
    async def _noop(self):
        pass

    
    async def _read_stream(self, fd):
        transport = self._transport.get_pipe_transport(fd)
        if fd == 2:
            stream = self.stderr
    # WARNING: Decompyle incomplete

    
    async def communicate(self, input = (None,)):
        if input is not None:
            stdin = self._feed_stdin(input)
        else:
            stdin = self._noop()
        if self.stdout is not None:
            stdout = self._read_stream(1)
        else:
            stdout = self._noop()
        if self.stderr is not None:
            stderr = self._read_stream(2)
        else:
            stderr = self._noop()
        await tasks.gather(stdin, stdout, stderr)
        (stdin, stdout, stderr) = <NODE:28>
        await self.wait()
        return (stdout, stderr)



async def create_subprocess_shell(cmd, stdin, stdout, stderr, limit = (None, None, None, streams._DEFAULT_LIMIT), **kwds):
    loop = events.get_running_loop()
    
    protocol_factory = lambda : SubprocessStreamProtocol(limit, loop, **('limit', 'loop'))
# WARNING: Decompyle incomplete


async def create_subprocess_exec(program = None, *, stdin, stdout, stderr, limit, *args, **kwds):
    loop = events.get_running_loop()
    
    protocol_factory = lambda : SubprocessStreamProtocol(limit, loop, **('limit', 'loop'))
# WARNING: Decompyle incomplete

