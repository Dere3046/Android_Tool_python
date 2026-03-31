
import io
import os
from context import reduction, set_spawning_popen
if not reduction.HAVE_SEND_HANDLE:
    raise ImportError('No support for sending fds between processes')
from  import forkserver
from  import popen_fork
from  import spawn
from  import util
__all__ = [
    'Popen']

class _DupFd(object):
    
    def __init__(self, ind):
        self.ind = ind

    
    def detach(self):
        return forkserver.get_inherited_fds()[self.ind]



class Popen(popen_fork.Popen):
    method = 'forkserver'
    DupFd = _DupFd
    
    def __init__(self = None, process_obj = None):
        self._fds = []
        super().__init__(process_obj)

    
    def duplicate_for_child(self, fd):
        self._fds.append(fd)
        return len(self._fds) - 1

    
    def _launch(self, process_obj):
        prep_data = spawn.get_preparation_data(process_obj._name)
        buf = io.BytesIO()
        set_spawning_popen(self)
    # WARNING: Decompyle incomplete

    
    def poll(self, flag = (os.WNOHANG,)):
        if self.returncode is None:
            wait = wait
            import multiprocessing.connection
            timeout = 0 if flag == os.WNOHANG else None
            if not wait([
                self.sentinel], timeout):
                return None
            self.returncode = forkserver.read_signed(self.sentinel)
        return self.returncode
    # WARNING: Decompyle incomplete

    __classcell__ = None

