
__doc__ = "OS routines for NT or Posix depending on what system we're on.\n\nThis exports:\n  - all functions from posix or nt, e.g. unlink, stat, etc.\n  - os.path is either posixpath or ntpath\n  - os.name is either 'posix' or 'nt'\n  - os.curdir is a string representing the current directory (always '.')\n  - os.pardir is a string representing the parent directory (always '..')\n  - os.sep is the (or a most common) pathname separator ('/' or '\\\\')\n  - os.extsep is the extension separator (always '.')\n  - os.altsep is the alternate pathname separator (None or '/')\n  - os.pathsep is the component separator used in $PATH etc\n  - os.linesep is the line separator in text files ('\\r' or '\\n' or '\\r\\n')\n  - os.defpath is the default search path for executables\n  - os.devnull is the file path of the null device ('/dev/null', etc.)\n\nPrograms that import and use 'os' stand a better chance of being\nportable between different platforms.  Of course, they must then\nonly use functions that are defined by all platforms (e.g., unlink\nand opendir), and leave all pathname manipulation to os.path\n(e.g., split and join).\n"
import abc
import sys
import stat as st
from _collections_abc import _check_methods
GenericAlias = type(list[int])
_names = sys.builtin_module_names
__all__ = [
    'altsep',
    'curdir',
    'pardir',
    'sep',
    'pathsep',
    'linesep',
    'defpath',
    'name',
    'path',
    'devnull',
    'SEEK_SET',
    'SEEK_CUR',
    'SEEK_END',
    'fsencode',
    'fsdecode',
    'get_exec_path',
    'fdopen',
    'extsep']

def _exists(name):
    return name in globals()


def _get_exports_list(module):
    pass
# WARNING: Decompyle incomplete

# WARNING: Decompyle incomplete
