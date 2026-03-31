
'''runpy.py - locating and running Python code using the module namespace

Provides support for locating and running Python scripts using the Python
module namespace instead of the native filesystem.

This allows Python code to play nicely with non-filesystem based PEP 302
importers when locating support scripts as well as when importing modules.
'''
import sys
import importlib.machinery as importlib
import importlib.util as importlib
import io
import types
import os
__all__ = [
    'run_module',
    'run_path']

class _TempModule(object):
    '''Temporarily replace a module in sys.modules with an empty namespace'''
    
    def __init__(self, mod_name):
        self.mod_name = mod_name
        self.module = types.ModuleType(mod_name)
        self._saved_module = []

    
    def __enter__(self):
        mod_name = self.mod_name
    # WARNING: Decompyle incomplete

    
    def __exit__(self, *args):
        if self._saved_module:
            sys.modules[self.mod_name] = self._saved_module[0]
        else:
            del sys.modules[self.mod_name]
        self._saved_module = []



class _ModifiedArgv0(object):
    
    def __init__(self, value):
        self.value = value
        self._saved_value = self._sentinel = object()

    
    def __enter__(self):
        if self._saved_value is not self._sentinel:
            raise RuntimeError('Already preserving saved value')
        self._saved_value = None.argv[0]
        sys.argv[0] = self.value

    
    def __exit__(self, *args):
        self.value = self._sentinel
        sys.argv[0] = self._saved_value



def _run_code(code, run_globals, init_globals, mod_name, mod_spec, pkg_name, script_name = (None, None, None, None, None)):
    '''Helper to run code in nominated namespace'''
    if init_globals is not None:
        run_globals.update(init_globals)
    if mod_spec is None:
        loader = None
        fname = script_name
        cached = None
    else:
        loader = mod_spec.loader
        fname = mod_spec.origin
        cached = mod_spec.cached
        if pkg_name is None:
            pkg_name = mod_spec.parent
    run_globals.update(mod_name, fname, cached, None, loader, pkg_name, mod_spec, **('__name__', '__file__', '__cached__', '__doc__', '__loader__', '__package__', '__spec__'))
    exec(code, run_globals)
    return run_globals


def _run_module_code(code, init_globals, mod_name, mod_spec, pkg_name, script_name = (None, None, None, None, None)):
    '''Helper to run code in new namespace with sys modified'''
    fname = script_name if mod_spec is None else mod_spec.origin
# WARNING: Decompyle incomplete


def _get_module_details(mod_name, error = (ImportError,)):
    if mod_name.startswith('.'):
        raise error('Relative module names not supported')
    (pkg_name, _, _) = None.rpartition('.')
# WARNING: Decompyle incomplete


class _Error(Exception):
    '''Error that _run_module_as_main() should report without a traceback'''
    pass


def _run_module_as_main(mod_name, alter_argv = (True,)):
    '''Runs the designated module in the __main__ namespace

       Note that the executed module will have full access to the
       __main__ namespace. If this is not desirable, the run_module()
       function should be used to run the module code in a fresh namespace.

       At the very least, these variables in __main__ will be overwritten:
           __name__
           __file__
           __cached__
           __loader__
           __package__
    '''
    pass
# WARNING: Decompyle incomplete


def run_module(mod_name, init_globals, run_name, alter_sys = (None, None, False)):
    """Execute a module's code without importing it

       Returns the resulting top level namespace dictionary
    """
    (mod_name, mod_spec, code) = _get_module_details(mod_name)
    if run_name is None:
        run_name = mod_name
    if alter_sys:
        return _run_module_code(code, init_globals, run_name, mod_spec)
    return None(code, { }, init_globals, run_name, mod_spec)


def _get_main_module_details(error = (ImportError,)):
    main_name = '__main__'
    saved_main = sys.modules[main_name]
    del sys.modules[main_name]
# WARNING: Decompyle incomplete


def _get_code_from_file(run_name, fname):
    read_code = read_code
    import pkgutil
    decoded_path = os.path.abspath(os.fsdecode(fname))
    with io.open_code(decoded_path) as f:
        code = read_code(f)
        None(None, None, None)
# WARNING: Decompyle incomplete


def run_path(path_name, init_globals, run_name = (None, None)):
    '''Execute code located at the specified filesystem location

       Returns the resulting top level namespace dictionary

       The file path may refer directly to a Python script (i.e.
       one that could be directly executed with execfile) or else
       it may refer to a zipfile or directory containing a top
       level __main__.py script.
    '''
    if run_name is None:
        run_name = '<run_path>'
    pkg_name = run_name.rpartition('.')[0]
    get_importer = get_importer
    import pkgutil
    importer = get_importer(path_name)
    is_NullImporter = False
    if type(importer).__module__ == 'imp' and type(importer).__name__ == 'NullImporter':
        is_NullImporter = True
    if isinstance(importer, type(None)) or is_NullImporter:
        (code, fname) = _get_code_from_file(run_name, path_name)
        return _run_module_code(code, init_globals, run_name, pkg_name, fname, **('pkg_name', 'script_name'))
    None.path.insert(0, path_name)
# WARNING: Decompyle incomplete

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('No module specified for execution', sys.stderr, **('file',))
        return None
    del None.argv[0]
    _run_module_as_main(sys.argv[0])
    return None
