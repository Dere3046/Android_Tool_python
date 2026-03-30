
__doc__ = 'genpy.py - The worker for makepy.  See makepy.py for more details\n\nThis code was moved simply to speed Python in normal circumstances.  As the makepy.py\nis normally run from the command line, it reparses the code each time.  Now makepy\nis nothing more than the command line handler and public interface.\n\nThe makepy command line etc handling is also getting large enough in its own right!\n'
import os
import sys
import time
import win32com
import pythoncom
from  import build
error = 'makepy.error'
makepy_version = '0.5.01'
GEN_FULL = 'full'
GEN_DEMAND_BASE = 'demand(base)'
GEN_DEMAND_CHILD = 'demand(child)'
# WARNING: Decompyle incomplete
