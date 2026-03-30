
'''
Filename globbing utility. Mostly a copy of `glob` from Python 3.5.

Changes include:
 * `yield from` and PEP3102 `*` removed.
 * Hidden files are not ignored.
'''
import os
import re
import fnmatch
__all__ = [
    'glob',
    'iglob',
    'escape']

def glob(pathname, recursive = (False,)):
    """Return a list of paths matching a pathname pattern.

    The pattern may contain simple shell-style wildcards a la
    fnmatch. However, unlike fnmatch, filenames starting with a
    dot are special cases that are not matched by '*' and '?'
    patterns.

    If recursive is true, the pattern '**' will match any files and
    zero or more directories and subdirectories.
    """
    return list(iglob(pathname, recursive, **('recursive',)))


def iglob(pathname, recursive = (False,)):
    """Return an iterator which yields the paths matching a pathname pattern.

    The pattern may contain simple shell-style wildcards a la
    fnmatch. However, unlike fnmatch, filenames starting with a
    dot are special cases that are not matched by '*' and '?'
    patterns.

    If recursive is true, the pattern '**' will match any files and
    zero or more directories and subdirectories.
    """
    it = _iglob(pathname, recursive)
# WARNING: Decompyle incomplete


def _iglob(pathname, recursive):
    (dirname, basename) = os.path.split(pathname)
    glob_in_dir = glob2 if recursive and _isrecursive(basename) else glob1
    if not has_magic(pathname):
        if basename:
            if os.path.lexists(pathname):
                yield pathname
            return None
        if None.path.isdir(dirname):
            yield pathname
        return None
    if not None:
        yield from glob_in_dir(dirname, basename)
        return None
    if None != pathname and has_magic(dirname):
        dirs = _iglob(dirname, recursive)
    else:
        dirs = [
            dirname]
    if not has_magic(basename):
        glob_in_dir = glob0
    for dirname in dirs:
        for name in glob_in_dir(dirname, basename):
            yield os.path.join(dirname, name)


def glob1(dirname, pattern):
    if not dirname:
        if isinstance(pattern, bytes):
            dirname = os.curdir.encode('ASCII')
        else:
            dirname = os.curdir
# WARNING: Decompyle incomplete


def glob0(dirname, basename):
    if not basename:
        if os.path.isdir(dirname):
            return [
                basename]
        return None
    if None.path.lexists(os.path.join(dirname, basename)):
        return [
            basename]


def glob2(dirname, pattern):
    pass
# WARNING: Decompyle incomplete


def _rlistdir(dirname):
    if not dirname:
        if isinstance(dirname, bytes):
            dirname = os.curdir.encode('ASCII')
        else:
            dirname = os.curdir
# WARNING: Decompyle incomplete

magic_check = re.compile('([*?[])')
magic_check_bytes = re.compile(b'([*?[])')

def has_magic(s):
    if isinstance(s, bytes):
        match = magic_check_bytes.search(s)
        return match is not None
    match = None.search(s)
    return match is not None


def _isrecursive(pattern):
    if isinstance(pattern, bytes):
        return pattern == b'**'
    return None == '**'


def escape(pathname):
    '''Escape all special characters.
    '''
    (drive, pathname) = os.path.splitdrive(pathname)
    if isinstance(pathname, bytes):
        pathname = magic_check_bytes.sub(b'[\\1]', pathname)
        return drive + pathname
    pathname = None.sub('[\\1]', pathname)
    return drive + pathname

