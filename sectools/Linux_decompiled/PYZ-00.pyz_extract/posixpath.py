
'''Common operations on Posix pathnames.

Instead of importing this module directly, import os and refer to
this module as os.path.  The "os.path" name is an alias for this
module on Posix systems; on other systems (e.g. Windows),
os.path provides the same operations in a manner specific to that
platform, and is an alias to another module (e.g. ntpath).

Some of this can actually be useful on non-Posix systems too, e.g.
for manipulation of the pathname component of URLs.
'''
curdir = '.'
pardir = '..'
extsep = '.'
sep = '/'
pathsep = ':'
defpath = '/bin:/usr/bin'
altsep = None
devnull = '/dev/null'
import os
import sys
import stat
import genericpath
from genericpath import *
__all__ = [
    'normcase',
    'isabs',
    'join',
    'splitdrive',
    'split',
    'splitext',
    'basename',
    'dirname',
    'commonprefix',
    'getsize',
    'getmtime',
    'getatime',
    'getctime',
    'islink',
    'exists',
    'lexists',
    'isdir',
    'isfile',
    'ismount',
    'expanduser',
    'expandvars',
    'normpath',
    'abspath',
    'samefile',
    'sameopenfile',
    'samestat',
    'curdir',
    'pardir',
    'sep',
    'pathsep',
    'defpath',
    'altsep',
    'extsep',
    'devnull',
    'realpath',
    'supports_unicode_filenames',
    'relpath',
    'commonpath']

def _get_sep(path):
    if isinstance(path, bytes):
        return b'/'


def normcase(s):
    '''Normalize case of pathname.  Has no effect under Posix'''
    return os.fspath(s)


def isabs(s):
    '''Test whether a path is absolute'''
    s = os.fspath(s)
    sep = _get_sep(s)
    return s.startswith(sep)


def join(a, *p):
    """Join two or more pathname components, inserting '/' as needed.
    If any component is an absolute path, all previous path components
    will be discarded.  An empty last part will result in a path that
    ends with a separator."""
    a = os.fspath(a)
    sep = _get_sep(a)
    path = a
# WARNING: Decompyle incomplete


def split(p):
    '''Split a pathname.  Returns tuple "(head, tail)" where "tail" is
    everything after the final slash.  Either part may be empty.'''
    p = os.fspath(p)
    sep = _get_sep(p)
    i = p.rfind(sep) + 1
    head = p[:i]
    tail = p[i:]
    if head and head != sep * len(head):
        head = head.rstrip(sep)
    return (head, tail)


def splitext(p):
    p = os.fspath(p)
    if isinstance(p, bytes):
        sep = b'/'
        extsep = b'.'
    else:
        sep = '/'
        extsep = '.'
    return genericpath._splitext(p, sep, None, extsep)

splitext.__doc__ = genericpath._splitext.__doc__

def splitdrive(p):
    '''Split a pathname into drive and path. On Posix, drive is always
    empty.'''
    p = os.fspath(p)
    return (p[:0], p)


def basename(p):
    '''Returns the final component of a pathname'''
    p = os.fspath(p)
    sep = _get_sep(p)
    i = p.rfind(sep) + 1
    return p[i:]


def dirname(p):
    '''Returns the directory component of a pathname'''
    p = os.fspath(p)
    sep = _get_sep(p)
    i = p.rfind(sep) + 1
    head = p[:i]
    if head and head != sep * len(head):
        head = head.rstrip(sep)
    return head


def islink(path):
    '''Test whether a path is a symbolic link'''
    pass
# WARNING: Decompyle incomplete


def lexists(path):
    '''Test whether a path exists.  Returns True for broken symbolic links'''
    pass
# WARNING: Decompyle incomplete


def ismount(path):
    '''Test whether a path is a mount point'''
    pass
# WARNING: Decompyle incomplete


def expanduser(path):
    '''Expand ~ and ~user constructions.  If user or $HOME is unknown,
    do nothing.'''
    path = os.fspath(path)
    if isinstance(path, bytes):
        tilde = b'~'
    else:
        tilde = '~'
    if not path.startswith(tilde):
        return path
    sep = None(path)
    i = path.find(sep, 1)
    if i < 0:
        i = len(path)
# WARNING: Decompyle incomplete

_varprog = None
_varprogb = None

def expandvars(path):
    '''Expand shell variables of form $var and ${var}.  Unknown variables
    are left unchanged.'''
    global _varprogb, _varprog
    path = os.fspath(path)
    if isinstance(path, bytes):
        if b'$' not in path:
            return path
        if not None:
            import re
            _varprogb = re.compile(b'\\$(\\w+|\\{[^}]*\\})', re.ASCII)
        search = _varprogb.search
        start = b'{'
        end = b'}'
        environ = getattr(os, 'environb', None)
    elif '$' not in path:
        return path
    if not _varprog:
        import re
        _varprog = re.compile('\\$(\\w+|\\{[^}]*\\})', re.ASCII)
    search = _varprog.search
    start = '{'
    end = '}'
    environ = os.environ
    i = 0
    m = search(path, i)
    if not m:
        return path
    (i, j) = None.span(0)
    name = m.group(1)
    if name.startswith(start) and name.endswith(end):
        name = name[1:-1]
# WARNING: Decompyle incomplete


def normpath(path):
    '''Normalize path, eliminating double slashes, etc.'''
    path = os.fspath(path)
    if isinstance(path, bytes):
        sep = b'/'
        empty = b''
        dot = b'.'
        dotdot = b'..'
    else:
        sep = '/'
        empty = ''
        dot = '.'
        dotdot = '..'
    if path == empty:
        return dot
    initial_slashes = None.startswith(sep)
    if not initial_slashes and path.startswith(sep * 2) and path.startswith(sep * 3):
        initial_slashes = 2
    comps = path.split(sep)
    new_comps = []
    for comp in comps:
        if comp in (empty, dot):
            continue
        if not comp != dotdot:
            if (initial_slashes or new_comps or new_comps) and new_comps[-1] == dotdot:
                new_comps.append(comp)
                continue
        if new_comps:
            new_comps.pop()
    comps = new_comps
    path = sep.join(comps)
    if initial_slashes:
        path = sep * initial_slashes + path
    if not path:
        pass
    return dot


def abspath(path):
    '''Return an absolute path.'''
    path = os.fspath(path)
    if not isabs(path):
        if isinstance(path, bytes):
            cwd = os.getcwdb()
        else:
            cwd = os.getcwd()
        path = join(cwd, path)
    return normpath(path)


def realpath(filename = None, *, strict):
    '''Return the canonical path of the specified filename, eliminating any
symbolic links encountered in the path.'''
    filename = os.fspath(filename)
    (path, ok) = _joinrealpath(filename[:0], filename, strict, { })
    return abspath(path)


def _joinrealpath(path, rest, strict, seen):
    if isinstance(path, bytes):
        sep = b'/'
        curdir = b'.'
        pardir = b'..'
    else:
        sep = '/'
        curdir = '.'
        pardir = '..'
    if isabs(rest):
        rest = rest[1:]
        path = sep
# WARNING: Decompyle incomplete

supports_unicode_filenames = sys.platform == 'darwin'

def relpath(path, start = (None,)):
    '''Return a relative version of a path'''
    if not path:
        raise ValueError('no path specified')
    path = None.fspath(path)
    if isinstance(path, bytes):
        curdir = b'.'
        sep = b'/'
        pardir = b'..'
    else:
        curdir = '.'
        sep = '/'
        pardir = '..'
    if start is None:
        start = curdir
    else:
        start = os.fspath(start)
# WARNING: Decompyle incomplete


def commonpath(paths):
    '''Given a sequence of path names, returns the longest common sub-path.'''
    if not paths:
        raise ValueError('commonpath() arg is an empty sequence')
    paths = None(map(os.fspath, paths))
    if isinstance(paths[0], bytes):
        sep = b'/'
        curdir = b'.'
    else:
        sep = '/'
        curdir = '.'
# WARNING: Decompyle incomplete

