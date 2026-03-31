
__doc__ = 'Utilities to support packages.'
from collections import namedtuple
from functools import singledispatch as simplegeneric
import importlib
import importlib.util as importlib
import importlib.machinery as importlib
import os
import os.path as os
import sys
from types import ModuleType
import warnings
__all__ = [
    'get_importer',
    'iter_importers',
    'get_loader',
    'find_loader',
    'walk_packages',
    'iter_modules',
    'get_data',
    'ImpImporter',
    'ImpLoader',
    'read_code',
    'extend_path',
    'ModuleInfo']
ModuleInfo = namedtuple('ModuleInfo', 'module_finder name ispkg')
ModuleInfo.__doc__ = 'A namedtuple with minimal info about a module.'

def _get_spec(finder, name):
    '''Return the finder-specific module spec.'''
    pass
# WARNING: Decompyle incomplete


def read_code(stream):
    import marshal
    magic = stream.read(4)
    if magic != importlib.util.MAGIC_NUMBER:
        return None
    None.read(12)
    return marshal.load(stream)


def walk_packages(path, prefix, onerror = (None, '', None)):
    """Yields ModuleInfo for all modules recursively
    on path, or, if path is None, all accessible modules.

    'path' should be either None or a list of paths to look for
    modules in.

    'prefix' is a string to output on the front of every module name
    on output.

    Note that this function must import all *packages* (NOT all
    modules!) on the given path, in order to access the __path__
    attribute to find submodules.

    'onerror' is a function which gets called with one argument (the
    name of the package which was being imported) if any exception
    occurs while trying to import a package.  If no onerror function is
    supplied, ImportErrors are caught and ignored, while all other
    exceptions are propagated, terminating the search.

    Examples:

    # list all modules python can access
    walk_packages()

    # list all submodules of ctypes
    walk_packages(ctypes.__path__, ctypes.__name__+'.')
    """
    
    def seen(p, m = ({ },)):
        if p in m:
            return True
        m[p] = None

# WARNING: Decompyle incomplete


def iter_modules(path, prefix = (None, '')):
    """Yields ModuleInfo for all submodules on path,
    or, if path is None, all top-level modules on sys.path.

    'path' should be either None or a list of paths to look for
    modules in.

    'prefix' is a string to output on the front of every module name
    on output.
    """
    if path is None:
        importers = iter_importers()
    elif isinstance(path, str):
        raise ValueError('path must be None or list of paths to look for modules in')
    importers = map(get_importer, path)
    yielded = { }
    for i in importers:
        for name, ispkg in iter_importer_modules(i, prefix):
            if name not in yielded:
                yielded[name] = 1
                yield ModuleInfo(i, name, ispkg)


def iter_importer_modules(importer, prefix = ('',)):
    if not hasattr(importer, 'iter_modules'):
        return []
    return None.iter_modules(prefix)

iter_importer_modules = simplegeneric(iter_importer_modules)

def _iter_file_finder_modules(importer, prefix = ('',)):
    if not importer.path is None or os.path.isdir(importer.path):
        return None
    yielded = None
    import inspect
# WARNING: Decompyle incomplete

iter_importer_modules.register(importlib.machinery.FileFinder, _iter_file_finder_modules)

def _import_imp():
    global imp
    pass
# WARNING: Decompyle incomplete


class ImpImporter:
    '''PEP 302 Finder that wraps Python\'s "classic" import algorithm

    ImpImporter(dirname) produces a PEP 302 finder that searches that
    directory.  ImpImporter(None) produces a PEP 302 finder that searches
    the current sys.path, plus any modules that are frozen or built-in.

    Note that ImpImporter does not currently support being used by placement
    on sys.meta_path.
    '''
    
    def __init__(self, path = (None,)):
        warnings.warn("This emulation is deprecated and slated for removal in Python 3.12; use 'importlib' instead", DeprecationWarning)
        _import_imp()
        self.path = path

    
    def find_module(self, fullname, path = (None,)):
        subname = fullname.split('.')[-1]
        if subname != fullname and self.path is None:
            return None
        if None.path is None:
            path = None
        else:
            path = [
                os.path.realpath(self.path)]
    # WARNING: Decompyle incomplete

    
    def iter_modules(self, prefix = ('',)):
        if not self.path is None or os.path.isdir(self.path):
            return None
        yielded = None
        import inspect
    # WARNING: Decompyle incomplete



class ImpLoader:
    '''PEP 302 Loader that wraps Python\'s "classic" import algorithm
    '''
    code = None
    source = None
    
    def __init__(self, fullname, file, filename, etc):
        warnings.warn("This emulation is deprecated and slated for removal in Python 3.12; use 'importlib' instead", DeprecationWarning)
        _import_imp()
        self.file = file
        self.filename = filename
        self.fullname = fullname
        self.etc = etc

    
    def load_module(self, fullname):
        self._reopen()
    # WARNING: Decompyle incomplete

    
    def get_data(self, pathname):
        pass
    # WARNING: Decompyle incomplete

    
    def _reopen(self):
        if self.file or self.file.closed:
            mod_type = self.etc[2]
            if mod_type == imp.PY_SOURCE:
                self.file = open(self.filename, 'r')
                return None
            if None in (imp.PY_COMPILED, imp.C_EXTENSION):
                self.file = open(self.filename, 'rb')
                return None
            return None
        return None

    
    def _fix_name(self, fullname):
        if fullname is None:
            fullname = self.fullname
            return fullname
        if None != self.fullname:
            raise ImportError('Loader for module %s cannot handle module %s' % (self.fullname, fullname))

    
    def is_package(self, fullname):
        fullname = self._fix_name(fullname)
        return self.etc[2] == imp.PKG_DIRECTORY

    
    def get_code(self, fullname = (None,)):
        fullname = self._fix_name(fullname)
    # WARNING: Decompyle incomplete

    
    def get_source(self, fullname = (None,)):
        fullname = self._fix_name(fullname)
    # WARNING: Decompyle incomplete

    
    def _get_delegate(self):
        finder = ImpImporter(self.filename)
        spec = _get_spec(finder, '__init__')
        return spec.loader

    
    def get_filename(self, fullname = (None,)):
        fullname = self._fix_name(fullname)
        mod_type = self.etc[2]
        if mod_type == imp.PKG_DIRECTORY:
            return self._get_delegate().get_filename()
        if None in (imp.PY_SOURCE, imp.PY_COMPILED, imp.C_EXTENSION):
            return self.filename


# WARNING: Decompyle incomplete
