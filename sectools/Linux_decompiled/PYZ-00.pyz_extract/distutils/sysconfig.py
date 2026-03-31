
__doc__ = "Provide access to Python's configuration information.  The specific\nconfiguration variables available depend heavily on the platform and\nconfiguration.  The values may be retrieved using\nget_config_var(name), and the list of variables is available via\nget_config_vars().keys().  Additional convenience functions are also\navailable.\n\nWritten by:   Fred L. Drake, Jr.\nEmail:        <fdrake@acm.org>\n"
import _imp
import os
import re
import sys
import warnings
from functools import partial
from errors import DistutilsPlatformError
from sysconfig import _PREFIX as PREFIX, _BASE_PREFIX as BASE_PREFIX, _EXEC_PREFIX as EXEC_PREFIX, _BASE_EXEC_PREFIX as BASE_EXEC_PREFIX, _PROJECT_BASE as project_base, _PYTHON_BUILD as python_build, _init_posix as sysconfig_init_posix, parse_config_h as sysconfig_parse_config_h, _init_non_posix, _is_python_source_dir, _sys_home, _variable_rx, _findvar1_rx, _findvar2_rx, expand_makefile_vars, is_python_build, get_config_h_filename, get_config_var, get_config_vars, get_makefile_filename, get_python_version
_config_vars = get_config_vars()
if os.name == 'nt':
    from sysconfig import _fix_pcbuild
warnings.warn('The distutils.sysconfig module is deprecated, use sysconfig instead', DeprecationWarning, 2, **('stacklevel',))

def parse_config_h(fp, g = (None,)):
    return sysconfig_parse_config_h(fp, g, **('vars',))

_python_build = partial(is_python_build, True, **('check_home',))
_init_posix = partial(sysconfig_init_posix, _config_vars)
_init_nt = partial(_init_non_posix, _config_vars)

def parse_makefile(fn, g = (None,)):
    '''Parse a Makefile-style file.
    A dictionary containing name/value pairs is returned.  If an
    optional dictionary is passed in as the second argument, it is
    used instead of a new dictionary.
    '''
    TextFile = TextFile
    import distutils.text_file
    fp = TextFile(fn, 1, 1, 1, 'surrogateescape', **('strip_comments', 'skip_blanks', 'join_lines', 'errors'))
    if g is None:
        g = { }
    done = { }
    notdone = { }
    line = fp.readline()
    if line is None:
        pass
# WARNING: Decompyle incomplete

build_flags = ''
# WARNING: Decompyle incomplete
