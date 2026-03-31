
import os
import msvcrt
import signal
import sys
import _winapi
from context import reduction, get_spawning_popen, set_spawning_popen
from  import spawn
from  import util
__all__ = [
    'Popen']
TERMINATE = 65536
if sys.platform == 'win32':
    pass
WINEXE = getattr(sys, 'frozen', False)
WINSERVICE = sys.executable.lower().endswith('pythonservice.exe')

def _path_eq(p1, p2):
    if not p1 == p2:
        pass
    return os.path.normcase(p1) == os.path.normcase(p2)

WINENV = not _path_eq(sys.executable, sys._base_executable)

def _close_handles(*handles):
    for handle in handles:
        _winapi.CloseHandle(handle)


class Popen(object):
    '''
    Start a subprocess to run the code of a process object
    '''
    method = 'spawn'
    
    def __init__(self, process_obj):
        prep_data = spawn.get_preparation_data(process_obj._name)
        (rhandle, whandle) = _winapi.CreatePipe(None, 0)
        wfd = msvcrt.open_osfhandle(whandle, 0)
        cmd = spawn.get_command_line(os.getpid(), rhandle, **('parent_pid', 'pipe_handle'))
        cmd = ' '.join((lambda .0: for x in .0:
'"%s"' % x)(cmd))
        python_exe = spawn.get_executable()
        if WINENV and _path_eq(python_exe, sys.executable):
            python_exe = sys._base_executable
            env = os.environ.copy()
            env['__PYVENV_LAUNCHER__'] = sys.executable
        else:
            env = None
    # WARNING: Decompyle incomplete

    
    def duplicate_for_child(self, handle):
        pass
    # WARNING: Decompyle incomplete

    
    def wait(self, timeout = (None,)):
        if self.returncode is None:
            if timeout is None:
                msecs = _winapi.INFINITE
            else:
                msecs = max(0, int(timeout * 1000 + 0.5))
            res = _winapi.WaitForSingleObject(int(self._handle), msecs)
            if res == _winapi.WAIT_OBJECT_0:
                code = _winapi.GetExitCodeProcess(self._handle)
                if code == TERMINATE:
                    code = -(signal.SIGTERM)
                self.returncode = code
        return self.returncode

    
    def poll(self):
        return self.wait(0, **('timeout',))

    
    def terminate(self):
        pass
    # WARNING: Decompyle incomplete

    kill = terminate
    
    def close(self):
        self.finalizer()


