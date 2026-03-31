
import os
import sys
from abc import ABC
from typing import cast
from _api import BaseFileLock
has_fcntl = False
if sys.platform == 'win32':
    
    class UnixFileLock(ABC, BaseFileLock):
        '''Uses the :func:`fcntl.flock` to hard lock the lock file on unix systems.'''
        pass

# WARNING: Decompyle incomplete
