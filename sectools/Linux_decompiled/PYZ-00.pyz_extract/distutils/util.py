
"""distutils.util

Miscellaneous utility functions -- anything that doesn't fit into
one of the other *util.py modules.
"""
import os
import re
import importlib.util as importlib
import string
import sys
import distutils
from distutils.errors import DistutilsPlatformError
from distutils.dep_util import newer
from distutils.spawn import spawn
from distutils import log
from distutils.errors import DistutilsByteCompileError

def get_host_platform():
    """Return a string that identifies the current platform.  This is used mainly to
    distinguish platform-specific build directories and platform-specific built
    distributions.  Typically includes the OS name and version and the
    architecture (as supplied by 'os.uname()'), although the exact information
    included depends on the OS; eg. on Linux, the kernel version isn't
    particularly important.

    Examples of returned values:
       linux-i586
       linux-alpha (?)
       solaris-2.6-sun4u

    Windows will return one of:
       win-amd64 (64bit Windows on AMD64 (aka x86_64, Intel64, EM64T, etc)
       win32 (all others - specifically, sys.platform is returned)

    For other non-POSIX platforms, currently just returns 'sys.platform'.

    """
    if os.name == 'nt':
        if 'amd64' in sys.version.lower():
            return 'win-amd64'
        if None in sys.version.lower():
            return 'win-arm32'
        if None in sys.version.lower():
            return 'win-arm64'
        return None.platform
    if None in os.environ:
        return os.environ['_PYTHON_HOST_PLATFORM']
    if not None.name != 'posix' or hasattr(os, 'uname'):
        return sys.platform
    (osname, host, release, version, machine) = None.uname()
    osname = osname.lower().replace('/', '')
    machine = machine.replace(' ', '_')
    machine = machine.replace('/', '-')
    if osname[:5] == 'linux':
        return '%s-%s' % (osname, machine)
    if None[:5] == 'sunos':
        if release[0] >= '5':
            osname = 'solaris'
            release = '%d.%s' % (int(release[0]) - 3, release[2:])
            bitness = {
                2147483647: '32bit',
                0x7FFFFFFFFFFFFFFFL: '64bit' }
            machine += '.%s' % bitness[sys.maxsize]
        elif osname[:3] == 'aix':
            aix_platform = aix_platform
            import _aix_support
            return aix_platform()
    if osname[:6] == 'cygwin':
        osname = 'cygwin'
        rel_re = re.compile('[\\d.]+', re.ASCII)
        m = rel_re.match(release)
        if m:
            release = m.group()
        elif osname[:6] == 'darwin':
            import _osx_support
            import distutils.sysconfig as distutils
            (osname, release, machine) = _osx_support.get_platform_osx(distutils.sysconfig.get_config_vars(), osname, release, machine)
    return '%s-%s-%s' % (osname, release, machine)


def get_platform():
    if os.name == 'nt':
        TARGET_TO_PLAT = {
            'x86': 'win32',
            'x64': 'win-amd64',
            'arm': 'win-arm32' }
        if not TARGET_TO_PLAT.get(os.environ.get('VSCMD_ARG_TGT_ARCH')):
            pass
        return get_host_platform()
    return None()


def convert_path(pathname):
    """Return 'pathname' as a name that will work on the native filesystem,
    i.e. split it on '/' and put it back together again using the current
    directory separator.  Needed because filenames in the setup script are
    always supplied in Unix style, and have to be converted to the local
    convention before we can actually use them in the filesystem.  Raises
    ValueError on non-Unix-ish systems if 'pathname' either starts or
    ends with a slash.
    """
    if os.sep == '/':
        return pathname
    if not None:
        return pathname
    if None[0] == '/':
        raise ValueError("path '%s' cannot be absolute" % pathname)
    if None[-1] == '/':
        raise ValueError("path '%s' cannot end with '/'" % pathname)
    paths = None.split('/')
# WARNING: Decompyle incomplete


def change_root(new_root, pathname):
    '''Return \'pathname\' with \'new_root\' prepended.  If \'pathname\' is
    relative, this is equivalent to "os.path.join(new_root,pathname)".
    Otherwise, it requires making \'pathname\' relative and then joining the
    two, which is tricky on DOS/Windows and Mac OS.
    '''
    if os.name == 'posix':
        if not os.path.isabs(pathname):
            return os.path.join(new_root, pathname)
        return None.path.join(new_root, pathname[1:])
    if None.name == 'nt':
        (drive, path) = os.path.splitdrive(pathname)
        if path[0] == '\\':
            path = path[1:]
        return os.path.join(new_root, path)
    raise None("nothing known about platform '%s'" % os.name)

_environ_checked = 0

def check_environ():
    """Ensure that 'os.environ' has all the environment variables we
    guarantee that users can use in config files, command-line options,
    etc.  Currently this includes:
      HOME - user's home directory (Unix only)
      PLAT - description of the current platform, including hardware
             and OS (see 'get_platform()')
    """
    if _environ_checked:
        return None
# WARNING: Decompyle incomplete


def subst_vars(s, local_vars):
    """Perform shell/Perl-style variable substitution on 'string'.  Every
    occurrence of '$' followed by a name is considered a variable, and
    variable is substituted by the value found in the 'local_vars'
    dictionary, or in 'os.environ' if it's not in 'local_vars'.
    'os.environ' is first checked/augmented to guarantee that it contains
    certain values: see 'check_environ()'.  Raise ValueError for any
    variables not found in either 'local_vars' or 'os.environ'.
    """
    check_environ()
    
    def _subst(match, local_vars = (local_vars,)):
        var_name = match.group(1)
        if var_name in local_vars:
            return str(local_vars[var_name])
        return None.environ[var_name]

# WARNING: Decompyle incomplete


def grok_environment_error(exc, prefix = ('error: ',)):
    return prefix + str(exc)

_wordchars_re = None
_squote_re = None
_dquote_re = None

def _init_regex():
    global _wordchars_re, _squote_re, _dquote_re
    _wordchars_re = re.compile('[^\\\\\\\'\\"%s ]*' % string.whitespace)
    _squote_re = re.compile("'(?:[^'\\\\]|\\\\.)*'")
    _dquote_re = re.compile('"(?:[^"\\\\]|\\\\.)*"')


def split_quoted(s):
    '''Split a string up according to Unix shell-like rules for quotes and
    backslashes.  In short: words are delimited by spaces, as long as those
    spaces are not escaped by a backslash, or inside a quoted string.
    Single and double quotes are equivalent, and the quote characters can
    be backslash-escaped.  The backslash is stripped from any two-character
    escape sequence, leaving only the escaped character.  The quote
    characters are stripped from any quoted string.  Returns a list of
    words.
    '''
    if _wordchars_re is None:
        _init_regex()
    s = s.strip()
    words = []
    pos = 0
    if s:
        m = _wordchars_re.match(s, pos)
        end = m.end()
        if end == len(s):
            words.append(s[:end])
            return words
        if None[end] in string.whitespace:
            words.append(s[:end])
            s = s[end:].lstrip()
            pos = 0
        elif s[end] == '\\':
            s = s[:end] + s[end + 1:]
            pos = end + 1
        elif s[end] == "'":
            m = _squote_re.match(s, end)
        elif s[end] == '"':
            m = _dquote_re.match(s, end)
        else:
            raise RuntimeError("this can't happen (bad char '%c')" % s[end])
        if None is None:
            raise ValueError('bad string (mismatched %s quotes?)' % s[end])
        (beg, end) = None.span()
        s = s[:beg] + s[beg + 1:end - 1] + s[end:]
        pos = m.end() - 2
        if pos >= len(s):
            words.append(s)
            return words
        if not None:
            return words


def execute(func, args, msg, verbose, dry_run = (None, 0, 0)):
    '''Perform some action that affects the outside world (eg.  by
    writing to the filesystem).  Such actions are special because they
    are disabled by the \'dry_run\' flag.  This method takes care of all
    that bureaucracy for you; all you have to do is supply the
    function to call and an argument tuple for it (to embody the
    "external action" being performed), and an optional message to
    print.
    '''
    if msg is None:
        msg = '%s%r' % (func.__name__, args)
        if msg[-2:] == ',)':
            msg = msg[0:-2] + ')'
    log.info(msg)
# WARNING: Decompyle incomplete


def strtobool(val):
    """Convert a string representation of truth to true (1) or false (0).

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return 1
    if None in ('n', 'no', 'f', 'false', 'off', '0'):
        return 0
    raise None('invalid truth value %r' % (val,))


def byte_compile(py_files, optimize, force, prefix, base_dir, verbose, dry_run, direct = (0, 0, None, None, 1, 0, None)):
    '''Byte-compile a collection of Python source files to .pyc
    files in a __pycache__ subdirectory.  \'py_files\' is a list
    of files to compile; any files that don\'t end in ".py" are silently
    skipped.  \'optimize\' must be one of the following:
      0 - don\'t optimize
      1 - normal optimization (like "python -O")
      2 - extra optimization (like "python -OO")
    If \'force\' is true, all files are recompiled regardless of
    timestamps.

    The source filename encoded in each bytecode file defaults to the
    filenames listed in \'py_files\'; you can modify these with \'prefix\' and
    \'basedir\'.  \'prefix\' is a string that will be stripped off of each
    source filename, and \'base_dir\' is a directory name that will be
    prepended (after \'prefix\' is stripped).  You can supply either or both
    (or neither) of \'prefix\' and \'base_dir\', as you wish.

    If \'dry_run\' is true, doesn\'t actually do anything that would
    affect the filesystem.

    Byte-compilation is either done directly in this interpreter process
    with the standard py_compile module, or indirectly by writing a
    temporary script and executing it.  Normally, you should let
    \'byte_compile()\' figure out to use direct compilation or not (see
    the source for details).  The \'direct\' flag is used by the script
    generated in indirect mode; unless you know what you\'re doing, leave
    it set to None.
    '''
    import subprocess
    if sys.dont_write_bytecode:
        raise DistutilsByteCompileError('byte-compiling is disabled.')
    if None is None:
        direct = optimize == 0
# WARNING: Decompyle incomplete


def rfc822_escape(header):
    '''Return a version of the string escaped for inclusion in an
    RFC-822 header, by ensuring there are 8 spaces space after each newline.
    '''
    lines = header.split('\n')
    sep = '\n        '
    return sep.join(lines)


def run_2to3(files, fixer_names, options, explicit = (None, None, None)):
    '''Invoke 2to3 on a list of Python files.
    The files should all come from the build area, as the
    modification is done in-place. To reduce the build time,
    only files modified since the last invocation of this
    function should be passed in the files argument.'''
    if not files:
        return None
    RefactoringTool = RefactoringTool
    get_fixers_from_package = get_fixers_from_package
    import lib2to3.refactor
    
    class DistutilsRefactoringTool(RefactoringTool):
        __qualname__ = 'run_2to3.<locals>.DistutilsRefactoringTool'
        
        def log_error(self, msg, *args, **kw):
            pass
        # WARNING: Decompyle incomplete

        
        def log_message(self, msg, *args):
            pass
        # WARNING: Decompyle incomplete

        
        def log_debug(self, msg, *args):
            pass
        # WARNING: Decompyle incomplete


    if fixer_names is None:
        fixer_names = get_fixers_from_package('lib2to3.fixes')
    r = DistutilsRefactoringTool(fixer_names, options, **('options',))
    r.refactor(files, True, **('write',))


def copydir_run_2to3(src, dest, template, fixer_names, options, explicit = (None, None, None, None)):
    """Recursively copy a directory, only copying new and changed files,
    running run_2to3 over all newly copied Python modules afterward.

    If you give a template string, it's parsed like a MANIFEST.in.
    """
    mkpath = mkpath
    import distutils.dir_util
    copy_file = copy_file
    import distutils.file_util
    FileList = FileList
    import distutils.filelist
    filelist = FileList()
    curdir = os.getcwd()
    os.chdir(src)
# WARNING: Decompyle incomplete


class Mixin2to3:
    '''Mixin class for commands that run 2to3.
    To configure 2to3, setup scripts may either change
    the class variables, or inherit from individual commands
    to override how 2to3 is invoked.'''
    fixer_names = None
    options = None
    explicit = None
    
    def run_2to3(self, files):
        return run_2to3(files, self.fixer_names, self.options, self.explicit)


