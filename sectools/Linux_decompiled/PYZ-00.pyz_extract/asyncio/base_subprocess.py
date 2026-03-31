
import collections
import subprocess
import warnings
from  import protocols
from  import transports
from log import logger

class BaseSubprocessTransport(transports.SubprocessTransport):
    
    def __init__(self, loop, protocol = None, args = None, shell = None, stdin = None, stdout = None, stderr = None, bufsize = None, waiter = None, extra = ((None, None),), **kwargs):
        super().__init__(extra)
        self._closed = False
        self._protocol = protocol
        self._loop = loop
        self._proc = None
        self._pid = None
        self._returncode = None
        self._exit_waiters = []
        self._pending_calls = collections.deque()
        self._pipes = { }
        self._finished = False
        if stdin == subprocess.PIPE:
            self._pipes[0] = None
        if stdout == subprocess.PIPE:
            self._pipes[1] = None
        if stderr == subprocess.PIPE:
            self._pipes[2] = None
    # WARNING: Decompyle incomplete

    
    def __repr__(self):
        info = [
            self.__class__.__name__]
        if self._closed:
            info.append('closed')
        if self._pid is not None:
            info.append(f'''pid={self._pid}''')
        if self._returncode is not None:
            info.append(f'''returncode={self._returncode}''')
        elif self._pid is not None:
            info.append('running')
        else:
            info.append('not started')
        stdin = self._pipes.get(0)
        if stdin is not None:
            info.append(f'''stdin={stdin.pipe}''')
        stdout = self._pipes.get(1)
        stderr = self._pipes.get(2)
        if stdout is not None and stderr is stdout:
            info.append(f'''stdout=stderr={stdout.pipe}''')
        elif stdout is not None:
            info.append(f'''stdout={stdout.pipe}''')
        if stderr is not None:
            info.append(f'''stderr={stderr.pipe}''')
        return '<{}>'.format(' '.join(info))

    
    def _start(self, args, shell, stdin, stdout, stderr, bufsize, **kwargs):
        raise NotImplementedError

    
    def set_protocol(self, protocol):
        self._protocol = protocol

    
    def get_protocol(self):
        return self._protocol

    
    def is_closing(self):
        return self._closed

    
    def close(self):
        if self._closed:
            return None
        self._closed = None
        for proto in self._pipes.values():
            if proto is None:
                continue
            proto.pipe.close()
    # WARNING: Decompyle incomplete

    
    def __del__(self, _warn = (warnings.warn,)):
        if not self._closed:
            _warn(f'''unclosed transport {self!r}''', ResourceWarning, self, **('source',))
            self.close()
            return None

    
    def get_pid(self):
        return self._pid

    
    def get_returncode(self):
        return self._returncode

    
    def get_pipe_transport(self, fd):
        if fd in self._pipes:
            return self._pipes[fd].pipe

    
    def _check_proc(self):
        if self._proc is None:
            raise ProcessLookupError()

    
    def send_signal(self, signal):
        self._check_proc()
        self._proc.send_signal(signal)

    
    def terminate(self):
        self._check_proc()
        self._proc.terminate()

    
    def kill(self):
        self._check_proc()
        self._proc.kill()

    
    async def _connect_pipes(self, waiter):
        pass
    # WARNING: Decompyle incomplete

    
    def _call(self, cb, *data):
        if self._pending_calls is not None:
            self._pending_calls.append((cb, data))
            return None
    # WARNING: Decompyle incomplete

    
    def _pipe_connection_lost(self, fd, exc):
        self._call(self._protocol.pipe_connection_lost, fd, exc)
        self._try_finish()

    
    def _pipe_data_received(self, fd, data):
        self._call(self._protocol.pipe_data_received, fd, data)

    
    def _process_exited(self, returncode):
        pass
    # WARNING: Decompyle incomplete

    
    async def _wait(self):
        '''Wait until the process exit and return the process return code.

        This method is a coroutine.'''
        if self._returncode is not None:
            return self._returncode
        waiter = None._loop.create_future()
        self._exit_waiters.append(waiter)
        await waiter
        return <NODE:28>

    
    def _try_finish(self):
        pass
    # WARNING: Decompyle incomplete

    
    def _call_connection_lost(self, exc):
        pass
    # WARNING: Decompyle incomplete

    __classcell__ = None


class WriteSubprocessPipeProto(protocols.BaseProtocol):
    
    def __init__(self, proc, fd):
        self.proc = proc
        self.fd = fd
        self.pipe = None
        self.disconnected = False

    
    def connection_made(self, transport):
        self.pipe = transport

    
    def __repr__(self):
        return f'''<{self.__class__.__name__} fd={self.fd} pipe={self.pipe!r}>'''

    
    def connection_lost(self, exc):
        self.disconnected = True
        self.proc._pipe_connection_lost(self.fd, exc)
        self.proc = None

    
    def pause_writing(self):
        self.proc._protocol.pause_writing()

    
    def resume_writing(self):
        self.proc._protocol.resume_writing()



class ReadSubprocessPipeProto(protocols.Protocol, WriteSubprocessPipeProto):
    
    def data_received(self, data):
        self.proc._pipe_data_received(self.fd, data)


