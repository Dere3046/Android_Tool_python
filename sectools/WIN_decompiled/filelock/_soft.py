
import os
import sys
from errno import EACCES, EEXIST, ENOENT
from _api import BaseFileLock
from _util import raise_on_exist_ro_file

class SoftFileLock(BaseFileLock):
    '''Simply watches the existence of the lock file.'''
    
    def _acquire(self = None):
        raise_on_exist_ro_file(self._lock_file)
        mode = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_TRUNC
    # WARNING: Decompyle incomplete

    
    def _release(self = None):
        os.close(self._lock_file_fd)
        self._lock_file_fd = None
    # WARNING: Decompyle incomplete


__all__ = [
    'SoftFileLock']
