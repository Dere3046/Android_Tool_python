
import os
import sys
import runpy
import types
from  import get_start_method, set_start_method
from  import process
from context import reduction
from  import util
__all__ = [
    '_main',
    'freeze_support',
    'set_executable',
    'get_executable',
    'get_preparation_data',
    'get_command_line',
    'import_main_path']
if sys.platform != 'win32':
    WINEXE = False
    WINSERVICE = False
else:
    WINEXE = getattr(sys, 'frozen', False)
    WINSERVICE = sys.executable.lower().endswith('pythonservice.exe')
if WINSERVICE:
    _python_exe = os.path.join(sys.exec_prefix, 'python.exe')
else:
    _python_exe = sys.executable

def set_executable(exe):
    global _python_exe
    _python_exe = exe


def get_executable():
    return _python_exe


def is_forking(argv):
    '''
    Return whether commandline indicates we are forking
    '''
    if len(argv) >= 2 and argv[1] == '--multiprocessing-fork':
        return True


def freeze_support():
    '''
    Run code for process object if this in not the main process
    '''
    pass
# WARNING: Decompyle incomplete


def get_command_line(**kwds):
    '''
    Returns prefix of command line used for spawning a child process
    '''
    if getattr(sys, 'frozen', False):
        return [
            sys.executable,
            '--multiprocessing-fork'] + (lambda .0: [ '%s=%r' % item for item in .0 ])(kwds.items())
    prog = None
    prog %= ', '.join((lambda .0: for item in .0:
'%s=%r' % item)(kwds.items()))
    opts = util._args_from_interpreter_flags()
    return [
        _python_exe] + opts + [
        '-c',
        prog,
        '--multiprocessing-fork']


def spawn_main(pipe_handle, parent_pid, tracker_fd = (None, None)):
    '''
    Run code specified by data received over pipe
    '''
    pass
# WARNING: Decompyle incomplete


def _main(fd, parent_sentinel):
    pass
# WARNING: Decompyle incomplete


def _check_not_importing_main():
    if getattr(process.current_process(), '_inheriting', False):
        raise RuntimeError('\n        An attempt has been made to start a new process before the\n        current process has finished its bootstrapping phase.\n\n        This probably means that you are not using fork to start your\n        child processes and you have forgotten to use the proper idiom\n        in the main module:\n\n            if __name__ == \'__main__\':\n                freeze_support()\n                ...\n\n        The "freeze_support()" line can be omitted if the program\n        is not going to be frozen to produce an executable.')


def get_preparation_data(name):
    '''
    Return info about parent needed by child to unpickle process object
    '''
    _check_not_importing_main()
    d = dict(util._log_to_stderr, process.current_process().authkey, **('log_to_stderr', 'authkey'))
    if util._logger is not None:
        d['log_level'] = util._logger.getEffectiveLevel()
    sys_path = sys.path.copy()
# WARNING: Decompyle incomplete

old_main_modules = []

def prepare(data):
    '''
    Try to get current process ready to unpickle process object
    '''
    if 'name' in data:
        process.current_process().name = data['name']
    if 'authkey' in data:
        process.current_process().authkey = data['authkey']
    if 'log_to_stderr' in data and data['log_to_stderr']:
        util.log_to_stderr()
    if 'log_level' in data:
        util.get_logger().setLevel(data['log_level'])
    if 'sys_path' in data:
        sys.path = data['sys_path']
    if 'sys_argv' in data:
        sys.argv = data['sys_argv']
    if 'dir' in data:
        os.chdir(data['dir'])
    if 'orig_dir' in data:
        process.ORIGINAL_DIR = data['orig_dir']
    if 'start_method' in data:
        set_start_method(data['start_method'], True, **('force',))
    if 'init_main_from_name' in data:
        _fixup_main_from_name(data['init_main_from_name'])
        return None
    if None in data:
        _fixup_main_from_path(data['init_main_from_path'])
        return None


def _fixup_main_from_name(mod_name):
    current_main = sys.modules['__main__']
    if mod_name == '__main__' or mod_name.endswith('.__main__'):
        return None
    if None(current_main.__spec__, 'name', None) == mod_name:
        return None
    None.append(current_main)
    main_module = types.ModuleType('__mp_main__')
    main_content = runpy.run_module(mod_name, '__mp_main__', True, **('run_name', 'alter_sys'))
    main_module.__dict__.update(main_content)
    sys.modules['__main__'] = sys.modules['__mp_main__'] = main_module


def _fixup_main_from_path(main_path):
    current_main = sys.modules['__main__']
    main_name = os.path.splitext(os.path.basename(main_path))[0]
    if main_name == 'ipython':
        return None
    if None(current_main, '__file__', None) == main_path:
        return None
    None.append(current_main)
    main_module = types.ModuleType('__mp_main__')
    main_content = runpy.run_path(main_path, '__mp_main__', **('run_name',))
    main_module.__dict__.update(main_content)
    sys.modules['__main__'] = sys.modules['__mp_main__'] = main_module


def import_main_path(main_path):
    """
    Set sys.modules['__main__'] to module at main_path
    """
    _fixup_main_from_path(main_path)

