
import sys
import os
is_pypy = '__pypy__' in sys.builtin_module_names

def warn_distutils_present():
    if 'distutils' not in sys.modules:
        return None
    if None and sys.version_info < (3, 7):
        return None
    import warnings
    warnings.warn('Distutils was imported before Setuptools, but importing Setuptools also replaces the `distutils` module in `sys.modules`. This may lead to undesirable behaviors or errors. To avoid these issues, avoid using distutils directly, ensure that setuptools is installed in the traditional way (e.g. not an editable install), and/or make sure that setuptools is always imported before distutils.')


def clear_distutils():
    if 'distutils' not in sys.modules:
        return None
    import warnings
    warnings.warn('Setuptools is replacing distutils.')
    mods = (lambda .0: [ name for name in .0 if name.startswith('distutils.') ])(sys.modules)
    for name in mods:
        del sys.modules[name]


def enabled():
    '''
    Allow selection of distutils by environment variable.
    '''
    which = os.environ.get('SETUPTOOLS_USE_DISTUTILS', 'local')
    return which == 'local'


def ensure_local_distutils():
    import importlib
    clear_distutils()
    with shim():
        importlib.import_module('distutils')
        None(None, None, None)
# WARNING: Decompyle incomplete


def do_override():
    '''
    Ensure that the local copy of distutils is preferred over stdlib.

    See https://github.com/pypa/setuptools/issues/417#issuecomment-392298401
    for more motivation.
    '''
    if enabled():
        warn_distutils_present()
        ensure_local_distutils()
        return None


class _TrivialRe:
    
    def __init__(self, *patterns):
        self._patterns = patterns

    
    def match(self, string):
        return None((lambda .0 = None: for pat in .0:
pat in string)(self._patterns))



class DistutilsMetaFinder:
    
    def find_spec(self, fullname, path, target = (None,)):
        if path is not None:
            return None
    # WARNING: Decompyle incomplete

    
    def spec_for_distutils(self):
        if self.is_cpython():
            return None
        import importlib
        import importlib.abc as importlib
        import importlib.util as importlib
    # WARNING: Decompyle incomplete

    
    def is_cpython():
        '''
        Suppress supplying distutils for CPython (build and tests).
        Ref #2965 and #3007.
        '''
        return os.path.isfile('pybuilddir.txt')

    is_cpython = staticmethod(is_cpython)
    
    def spec_for_pip(self):
        '''
        Ensure stdlib distutils when running under pip.
        See pypa/pip#8761 for rationale.
        '''
        if self.pip_imported_during_build():
            return None
        None()
        
        self.spec_for_distutils = lambda : pass

    
    def spec_for_setuptools(self):
        """
        get-pip imports setuptools solely for the purpose of
        determining if it's installed. In this case, provide
        a stubbed spec to represent setuptools being present
        without invoking any behavior.

        Workaround for pypa/get-pip#137. Ref #2993.
        """
        if not self.is_script('get-pip'):
            return None
        import importlib
        
        class StubbedLoader(importlib.abc.Loader):
            __qualname__ = 'DistutilsMetaFinder.spec_for_setuptools.<locals>.StubbedLoader'
            
            def create_module(self, spec):
                import types
                return types.ModuleType('setuptools')

            
            def exec_module(self, module):
                pass


        return importlib.util.spec_from_loader('setuptools', StubbedLoader())

    
    def pip_imported_during_build(cls):
        '''
        Detect if pip is being imported in a build script. Ref #2355.
        '''
        import traceback
        return None((lambda .0 = None: for frame, line in .0:
cls.frame_file_is_setup(frame))(traceback.walk_stack(None)))

    pip_imported_during_build = classmethod(pip_imported_during_build)
    
    def is_script(name):
        pass
    # WARNING: Decompyle incomplete

    is_script = staticmethod(is_script)
    
    def frame_file_is_setup(frame):
        '''
        Return True if the indicated frame suggests a setup.py file.
        '''
        return frame.f_globals.get('__file__', '').endswith('setup.py')

    frame_file_is_setup = staticmethod(frame_file_is_setup)

DISTUTILS_FINDER = DistutilsMetaFinder()

def add_shim():
    if not DISTUTILS_FINDER in sys.meta_path:
        insert_shim()
        return None


class shim:
    
    def __enter__(self):
        insert_shim()

    
    def __exit__(self, exc, value, tb):
        remove_shim()



def insert_shim():
    sys.meta_path.insert(0, DISTUTILS_FINDER)


def remove_shim():
    pass
# WARNING: Decompyle incomplete

