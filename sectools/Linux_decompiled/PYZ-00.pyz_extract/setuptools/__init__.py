
"""Extensions to the 'distutils' for large or complex distributions"""
from fnmatch import fnmatchcase
import functools
import os
import re
import _distutils_hack.override as _distutils_hack
import distutils.core as distutils
from distutils.errors import DistutilsOptionError
from distutils.util import convert_path
from _deprecation_warning import SetuptoolsDeprecationWarning
import setuptools.version as setuptools
from setuptools.extension import Extension
from setuptools.dist import Distribution
from setuptools.depends import Require
from  import monkey
from  import logging
__all__ = [
    'setup',
    'Distribution',
    'Command',
    'Extension',
    'Require',
    'SetuptoolsDeprecationWarning',
    'find_packages',
    'find_namespace_packages']
__version__ = setuptools.version.__version__
bootstrap_install_from = None

class PackageFinder:
    '''
    Generate a list of all Python packages found within a directory
    '''
    
    def find(cls, where, exclude, include = ('.', (), ('*',))):
        '''Return a list all Python packages found within directory \'where\'

        \'where\' is the root directory which will be searched for packages.  It
        should be supplied as a "cross-platform" (i.e. URL-style) path; it will
        be converted to the appropriate local path syntax.

        \'exclude\' is a sequence of package names to exclude; \'*\' can be used
        as a wildcard in the names, such that \'foo.*\' will exclude all
        subpackages of \'foo\' (but not \'foo\' itself).

        \'include\' is a sequence of package names to include.  If it\'s
        specified, only the named packages will be included.  If it\'s not
        specified, all found packages will be included.  \'include\' can contain
        shell style wildcard patterns just like \'exclude\'.
        '''
        pass
    # WARNING: Decompyle incomplete

    find = classmethod(find)
    
    def _find_packages_iter(cls, where, exclude, include):
        """
        All the packages found in 'where' that pass the 'include' filter, but
        not the 'exclude' filter.
        """
        for root, dirs, files in os.walk(where, True, **('followlinks',)):
            all_dirs = dirs[:]
            dirs[:] = []
            for dir in all_dirs:
                full_path = os.path.join(root, dir)
                rel_path = os.path.relpath(full_path, where)
                package = rel_path.replace(os.path.sep, '.')
                if not '.' in dir or cls._looks_like_package(full_path):
                    continue
                if not include(package) and exclude(package):
                    yield package
                dirs.append(dir)

    _find_packages_iter = classmethod(_find_packages_iter)
    
    def _looks_like_package(path):
        '''Does a directory look like a package?'''
        return os.path.isfile(os.path.join(path, '__init__.py'))

    _looks_like_package = staticmethod(_looks_like_package)
    
    def _build_filter(*patterns):
        '''
        Given a list of patterns, return a callable that will be true only if
        the input matches at least one of the patterns.
        '''
        return (lambda name = None: None((lambda .0 = None: for pat in .0:
fnmatchcase(name, pat, **('pat',)))(patterns))
)

    _build_filter = staticmethod(_build_filter)


class PEP420PackageFinder(PackageFinder):
    
    def _looks_like_package(path):
        return True

    _looks_like_package = staticmethod(_looks_like_package)

find_packages = PackageFinder.find
find_namespace_packages = PEP420PackageFinder.find

def _install_setup_requires(attrs):
    
    class MinimalDistribution(distutils.core.Distribution):
        __qualname__ = '_install_setup_requires.<locals>.MinimalDistribution'
        __doc__ = '\n        A minimal version of a distribution for supporting the\n        fetch_build_eggs interface.\n        '
        
        def __init__(self = None, attrs = None):
            _incl = ('dependency_links', 'setup_requires')
            filtered = (lambda .0 = None: pass# WARNING: Decompyle incomplete
)(set(_incl) & set(attrs))
            super().__init__(filtered)

        
        def finalize_options(self):
            '''
            Disable finalize_options to avoid building the working set.
            Ref #2158.
            '''
            pass

        __classcell__ = None

    dist = MinimalDistribution(attrs)
    dist.parse_config_files(True, **('ignore_option_errors',))
    if dist.setup_requires:
        dist.fetch_build_eggs(dist.setup_requires)
        return None


def setup(**attrs):
    logging.configure()
    _install_setup_requires(attrs)
# WARNING: Decompyle incomplete

setup.__doc__ = distutils.core.setup.__doc__
_Command = monkey.get_unpatched(distutils.core.Command)

class Command(_Command):
    __doc__ = _Command.__doc__
    command_consumes_arguments = False
    
    def __init__(self = None, dist = None, **kw):
        '''
        Construct the command for dist, updating
        vars(self) with any keyword parameters.
        '''
        super().__init__(dist)
        vars(self).update(kw)

    
    def _ensure_stringlike(self, option, what, default = (None,)):
        val = getattr(self, option)
        if val is None:
            setattr(self, option, default)
            return default
        if not None(val, str):
            raise DistutilsOptionError("'%s' must be a %s (got `%s`)" % (option, what, val))

    
    def ensure_string_list(self, option):
        '''Ensure that \'option\' is a list of strings.  If \'option\' is
        currently a string, we split it either on /,\\s*/ or /\\s+/, so
        "foo bar baz", "foo,bar,baz", and "foo,   bar baz" all become
        ["foo", "bar", "baz"].
        '''
        val = getattr(self, option)
        if val is None:
            return None
        if None(val, str):
            setattr(self, option, re.split(',\\s*|\\s+', val))
            return None
        if None(val, list):
            ok = all((lambda .0: for v in .0:
isinstance(v, str))(val))
        else:
            ok = False
        if not ok:
            raise DistutilsOptionError("'%s' must be a list of strings (got %r)" % (option, val))

    
    def reinitialize_command(self, command, reinit_subcommands = (0,), **kw):
        cmd = _Command.reinitialize_command(self, command, reinit_subcommands)
        vars(cmd).update(kw)
        return cmd

    __classcell__ = None


def _find_all_simple(path):
    """
    Find all files under 'path'
    """
    results = (lambda .0: for base, dirs, files in .0:
for file in files:
os.path.join(base, file))(os.walk(path, True, **('followlinks',)))
    return filter(os.path.isfile, results)


def findall(dir = (os.curdir,)):
    """
    Find all files under 'dir' and return the list of full filenames.
    Unless dir is '.', return full filenames with dir prepended.
    """
    files = _find_all_simple(dir)
    if dir == os.curdir:
        make_rel = functools.partial(os.path.relpath, dir, **('start',))
        files = map(make_rel, files)
    return list(files)


class sic(str):
    '''Treat this string as-is (https://en.wikipedia.org/wiki/Sic)'''
    pass

monkey.patch_all()
