
import sys
import marshal
import contextlib
import dis
from setuptools.extern.packaging import version
from _imp import find_module, PY_COMPILED, PY_FROZEN, PY_SOURCE
from  import _imp
__all__ = [
    'Require',
    'find_module',
    'get_module_constant',
    'extract_constant']

class Require:
    '''A prerequisite to building or installing a distribution'''
    
    def __init__(self, name, requested_version, module, homepage, attribute, format = ('', None, None)):
        if format is None and requested_version is not None:
            format = version.Version
        if format is not None:
            requested_version = format(requested_version)
            if attribute is None:
                attribute = '__version__'
        self.__dict__.update(locals())
        del self.self

    
    def full_name(self):
        '''Return full package/distribution name, w/version'''
        if self.requested_version is not None:
            return '%s-%s' % (self.name, self.requested_version)
        return None.name

    
    def version_ok(self, version):
        """Is 'version' sufficiently up-to-date?"""
        if self.attribute is None and self.format is None and str(version) != 'unknown':
            pass
        return self.format(version) >= self.requested_version

    
    def get_version(self, paths, default = (None, 'unknown')):
        """Get version number of installed module, 'None', or 'default'

        Search 'paths' for module.  If not found, return 'None'.  If found,
        return the extracted version attribute, or 'default' if no version
        attribute was specified, or the value cannot be determined without
        importing the module.  The version is formatted according to the
        requirement's version format (if any), unless it is 'None' or the
        supplied 'default'.
        """
        pass
    # WARNING: Decompyle incomplete

    
    def is_present(self, paths = (None,)):
        """Return true if dependency is present on 'paths'"""
        return self.get_version(paths) is not None

    
    def is_current(self, paths = (None,)):
        """Return true if dependency is present and up-to-date on 'paths'"""
        version = self.get_version(paths)
        if version is None:
            return False
        return None.version_ok(str(version))



def maybe_close(f):
    
    def empty():
        yield None

    empty = contextlib.contextmanager(empty)
    if not f:
        return empty()
    return None.closing(f)


def get_module_constant(module, symbol, default, paths = (-1, None)):
    """Find 'module' by searching 'paths', and extract 'symbol'

    Return 'None' if 'module' does not exist on 'paths', or it does not define
    'symbol'.  If the module defines 'symbol' as a constant, return the
    constant.  Otherwise, return 'default'."""
    pass
# WARNING: Decompyle incomplete


def extract_constant(code, symbol, default = (-1,)):
    '''Extract the constant value of \'symbol\' from \'code\'

    If the name \'symbol\' is bound to a constant value by the Python code
    object \'code\', return that value.  If \'symbol\' is bound to an expression,
    return \'default\'.  Otherwise, return \'None\'.

    Return value is based on the first assignment to \'symbol\'.  \'symbol\' must
    be a global, or at least a non-"fast" local in the code block.  That is,
    only \'STORE_NAME\' and \'STORE_GLOBAL\' opcodes are checked, and \'symbol\'
    must be present in \'code.co_names\'.
    '''
    if symbol not in code.co_names:
        return None
    name_idx = None(code.co_names).index(symbol)
    STORE_NAME = 90
    STORE_GLOBAL = 97
    LOAD_CONST = 100
    const = default
    for byte_code in dis.Bytecode(code):
        op = byte_code.opcode
        arg = byte_code.arg
        if op == LOAD_CONST:
            const = code.co_consts[arg]
            continue
        if arg == name_idx:
            if op == STORE_NAME or op == STORE_GLOBAL:
                return const
            const = None
            continue
            return None


def _update_globals():
    """
    Patch the globals to remove the objects not available on some platforms.

    XXX it'd be better to test assertions about bytecode instead.
    """
    if sys.platform.startswith('java') and sys.platform != 'cli':
        return None
    incompatible = None
    for name in incompatible:
        del globals()[name]
        __all__.remove(name)

_update_globals()
