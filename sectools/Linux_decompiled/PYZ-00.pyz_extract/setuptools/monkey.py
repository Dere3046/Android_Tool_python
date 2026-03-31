
'''
Monkey patching of distutils.
'''
import sys
import distutils.filelist as distutils
import platform
import types
import functools
from importlib import import_module
import inspect
import setuptools
__all__ = []

def _get_mro(cls):
    '''
    Returns the bases classes for cls sorted by the MRO.

    Works around an issue on Jython where inspect.getmro will not return all
    base classes if multiple classes share the same name. Instead, this
    function will return a tuple containing the class itself, and the contents
    of cls.__bases__. See https://github.com/pypa/setuptools/issues/1024.
    '''
    if platform.python_implementation() == 'Jython':
        return (cls,) + cls.__bases__
    return None.getmro(cls)


def get_unpatched(item):
    if isinstance(item, type):
        pass
    elif isinstance(item, types.FunctionType):
        pass
    
    
    lookup = lambda item: pass
    return lookup(item)


def get_unpatched_class(cls):
    '''Protect against re-patching the distutils if reloaded

    Also ensures that no other distutils extension monkeypatched the distutils
    first.
    '''
    external_bases = (lambda .0: for cls in .0:
if not cls.__module__.startswith('setuptools'):
clscontinueNone)(_get_mro(cls))
    base = next(external_bases)
    if not base.__module__.startswith('distutils'):
        msg = 'distutils has already been patched by %r' % cls
        raise AssertionError(msg)


def patch_all():
    distutils.core.Command = setuptools.Command
    has_issue_12885 = sys.version_info <= (3, 5, 3)
    if has_issue_12885:
        distutils.filelist.findall = setuptools.findall
    if not sys.version_info < (2, 7, 13):
        if sys.version_info < sys.version_info:
            pass
        elif not sys.version_info < (3, 4, 6):
            pass
    needs_warehouse = sys.version_info < (3, 4, 6) if sys.version_info < sys.version_info else sys.version_info <= (3, 5, 3)
    if needs_warehouse:
        warehouse = 'https://upload.pypi.org/legacy/'
        distutils.config.PyPIRCCommand.DEFAULT_REPOSITORY = warehouse
    _patch_distribution_metadata()
    for module in (distutils.dist, distutils.core, distutils.cmd):
        module.Distribution = setuptools.dist.Distribution
    distutils.core.Extension = setuptools.extension.Extension
    distutils.extension.Extension = setuptools.extension.Extension
    if 'distutils.command.build_ext' in sys.modules:
        sys.modules['distutils.command.build_ext'].Extension = setuptools.extension.Extension
    patch_for_msvc_specialized_compiler()


def _patch_distribution_metadata():
    '''Patch write_pkg_file and read_pkg_file for higher metadata standards'''
    for attr in ('write_pkg_file', 'read_pkg_file', 'get_metadata_version'):
        new_val = getattr(setuptools.dist, attr)
        setattr(distutils.dist.DistributionMetadata, attr, new_val)


def patch_func(replacement, target_mod, func_name):
    '''
    Patch func_name in target_mod with replacement

    Important - original must be resolved by name to avoid
    patching an already patched function.
    '''
    original = getattr(target_mod, func_name)
    vars(replacement).setdefault('unpatched', original)
    setattr(target_mod, func_name, replacement)


def get_unpatched_function(candidate):
    return getattr(candidate, 'unpatched')


def patch_for_msvc_specialized_compiler():
    '''
    Patch functions in distutils to use standalone Microsoft Visual C++
    compilers.
    '''
    msvc = import_module('setuptools.msvc')
    if platform.system() != 'Windows':
        return None
    
    def patch_params(mod_name = None, func_name = None):
        '''
        Prepare the parameters for patch_func to patch indicated function.
        '''
        repl_prefix = 'msvc9_' if 'msvc9' in mod_name else 'msvc14_'
        repl_name = repl_prefix + func_name.lstrip('_')
        repl = getattr(msvc, repl_name)
        mod = import_module(mod_name)
        if not hasattr(mod, func_name):
            raise ImportError(func_name)
        return (None, mod, func_name)

    msvc9 = functools.partial(patch_params, 'distutils.msvc9compiler')
    msvc14 = functools.partial(patch_params, 'distutils._msvccompiler')
# WARNING: Decompyle incomplete

