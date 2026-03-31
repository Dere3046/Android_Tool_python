
import io
import os
from context import reduction, set_spawning_popen
from  import popen_fork
from  import spawn
from  import util
__all__ = [
    'Popen']

class _DupFd(object):
    
    def __init__(self, fd):
        self.fd = fd

    
    def detach(self):
        return self.fd



class Popen(popen_fork.Popen):
    method = 'spawn'
    DupFd = _DupFd
    
    def __init__(self = None, process_obj = None):
        self._fds = []
        super().__init__(process_obj)

    
    def duplicate_for_child(self, fd):
        self._fds.append(fd)
        return fd

    
    def _launch(self, process_obj):
        resource_tracker = resource_tracker
        import 
        tracker_fd = resource_tracker.getfd()
        self._fds.append(tracker_fd)
        prep_data = spawn.get_preparation_data(process_obj._name)
        fp = io.BytesIO()
        set_spawning_popen(self)
    # WARNING: Decompyle incomplete

    __classcell__ = None

