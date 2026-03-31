
"""distutils.spawn

Provides the 'spawn()' function, a front-end to various platform-
specific functions for launching another program in a sub-process.
Also provides the 'find_executable()' to search the path for a given
executable name.
"""
import sys
import os
import subprocess
from distutils.errors import DistutilsPlatformError, DistutilsExecError
from distutils.debug import DEBUG
from distutils import log
if sys.platform == 'darwin':
    _cfg_target = None
    _cfg_target_split = None

def spawn(cmd, search_path, verbose, dry_run = (1, 0, 0)):
    """Run another program, specified as a command list 'cmd', in a new process.

    'cmd' is just the argument list for the new process, ie.
    cmd[0] is the program to run and cmd[1:] are the rest of its arguments.
    There is no way to run a program with a name different from that of its
    executable.

    If 'search_path' is true (the default), the system's executable
    search path will be used to find the program; otherwise, cmd[0]
    must be the exact path to the executable.  If 'dry_run' is true,
    the command will not actually be run.

    Raise DistutilsExecError if running the program fails in any way; just
    return on success.
    """
    global _cfg_target, _cfg_target_split
    cmd = list(cmd)
    log.info(' '.join(cmd))
    if dry_run:
        return None
    if None:
        executable = find_executable(cmd[0])
        if executable is not None:
            cmd[0] = executable
    env = None
    if sys.platform == 'darwin':
        if _cfg_target is None:
            sysconfig = sysconfig
            import distutils
            if not sysconfig.get_config_var('MACOSX_DEPLOYMENT_TARGET'):
                pass
            _cfg_target = ''
            if _cfg_target:
                _cfg_target_split = (lambda .0: [ int(x) for x in .0 ])(_cfg_target.split('.'))
        if _cfg_target:
            cur_target = os.environ.get('MACOSX_DEPLOYMENT_TARGET', _cfg_target)
            cur_target_split = (lambda .0: [ int(x) for x in .0 ])(cur_target.split('.'))
            if _cfg_target_split[:2] >= [
                10,
                3] and cur_target_split[:2] < [
                10,
                3]:
                my_msg = '$MACOSX_DEPLOYMENT_TARGET mismatch: now "%s" but "%s" during configure;must use 10.3 or later' % (cur_target, _cfg_target)
                raise DistutilsPlatformError(my_msg)
            env = None(os.environ, cur_target, **('MACOSX_DEPLOYMENT_TARGET',))
# WARNING: Decompyle incomplete


def find_executable(executable, path = (None,)):
    """Tries to find 'executable' in the directories listed in 'path'.

    A string listing directories separated by 'os.pathsep'; defaults to
    os.environ['PATH'].  Returns the complete filename or None if not found.
    """
    (_, ext) = os.path.splitext(executable)
    if sys.platform == 'win32' and ext != '.exe':
        executable = executable + '.exe'
    if os.path.isfile(executable):
        return executable
# WARNING: Decompyle incomplete

