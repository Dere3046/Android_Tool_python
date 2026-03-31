
import subprocess
import sys
import io

class Popen(subprocess.Popen):
    if not sys.platform == 'win32' or isinstance(sys.stdout, io.IOBase):
        
        def _get_handles(self = None, stdin = None, stdout = None, stderr = None):
            (stdin, stdout, stderr) = (lambda .0: for pipe in .0:
subprocess.DEVNULL if pipe is None else pipe)((stdin, stdout, stderr))
            return super()._get_handles(stdin, stdout, stderr)

        __classcell__ = None
        return None
    __classcell__ = None
    return None
    __classcell__ = None

subprocess.Popen = Popen
