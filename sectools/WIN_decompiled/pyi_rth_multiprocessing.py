
import multiprocessing
from multiprocessing.spawn import spawn
import os
import sys
from subprocess import _args_from_interpreter_flags
multiprocessing.process.ORIGINAL_DIR = None

def _freeze_support():
    if len(sys.argv) >= 2 and sys.argv[-2] == '-c' and sys.argv[-1].startswith(('from multiprocessing.semaphore_tracker import main', 'from multiprocessing.resource_tracker import main', 'from multiprocessing.forkserver import main')) and set(sys.argv[1:-2]) == set(_args_from_interpreter_flags()):
        exec(sys.argv[-1])
        sys.exit()
# WARNING: Decompyle incomplete

multiprocessing.freeze_support = spawn.freeze_support = _freeze_support
if sys.platform.startswith('win'):
    from multiprocessing.popen_spawn_win32 import popen_spawn_win32 as forking
else:
    from multiprocessing.popen_fork import popen_fork as forking
    from multiprocessing.popen_spawn_posix import popen_spawn_posix as spawning

class FrozenSupportMixIn:
    
    def __init__(self = None, *args, **kw):
        if hasattr(sys, 'frozen'):
            os.putenv('_MEIPASS2', sys._MEIPASS)
    # WARNING: Decompyle incomplete

    __classcell__ = None


class _Popen(forking.Popen, FrozenSupportMixIn):
    pass

forking.Popen = _Popen
if not sys.platform.startswith('win'):
    
    class _Spawning_Popen(spawning.Popen, FrozenSupportMixIn):
        pass

    spawning.Popen = _Spawning_Popen
    return None
