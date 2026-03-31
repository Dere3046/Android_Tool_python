
import os
import signal
from  import util
__all__ = [
    'Popen']

class Popen(object):
    method = 'fork'
    
    def __init__(self, process_obj):
        util._flush_std_streams()
        self.returncode = None
        self.finalizer = None
        self._launch(process_obj)

    
    def duplicate_for_child(self, fd):
        return fd

    
    def poll(self, flag = (os.WNOHANG,)):
        pass
    # WARNING: Decompyle incomplete

    
    def wait(self, timeout = (None,)):
        if self.returncode is None:
            if timeout is not None:
                wait = wait
                import multiprocessing.connection
                if not wait([
                    self.sentinel], timeout):
                    return None
                if timeout == 0:
                    return None.poll(os.WNOHANG)
                return None(None.poll)
            return None.returncode

    
    def _send_signal(self, sig):
        pass
    # WARNING: Decompyle incomplete

    
    def terminate(self):
        self._send_signal(signal.SIGTERM)

    
    def kill(self):
        self._send_signal(signal.SIGKILL)

    
    def _launch(self, process_obj):
        code = 1
        (parent_r, child_w) = os.pipe()
        (child_r, parent_w) = os.pipe()
        self.pid = os.fork()
    # WARNING: Decompyle incomplete

    
    def close(self):
        if self.finalizer is not None:
            self.finalizer()
            return None


