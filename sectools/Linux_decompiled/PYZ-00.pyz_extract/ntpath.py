
__doc__ = 'Common pathname manipulations, WindowsNT/95 version.\n\nInstead of importing this module directly, import os and refer to this\nmodule as os.path.\n'
curdir = '.'
pardir = '..'
extsep = '.'
sep = '\\'
pathsep = ';'
altsep = '/'
defpath = '.;C:\\bin'
devnull = 'nul'
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
    'samefile',
    'sameopenfile',
    'samestat',
    'commonpath']

def _get_bothseps(path):
    if isinstance(path, bytes):
        return b'\\/'


def normcase(s):
    '''Normalize case of pathname.

    Makes all characters lowercase and all slashes into backslashes.'''
    s = os.fspath(s)
    if isinstance(s, bytes):
        return s.replace(b'/', b'\\').lower()
    return None.replace('/', '\\').lower()


def isabs(s):
    '''Test whether a path is absolute'''
    s = os.fspath(s)
    if isinstance(s, bytes):
        if s.replace(b'/', b'\\').startswith(b'\\\\?\\'):
            return True
    if s.replace('/', '\\').startswith('\\\\?\\'):
        return True
    s = None(s)[1]
    if len(s) > 0:
        pass
    return s[0] in _get_bothseps(s)


def join(path, *paths):
    path = os.fspath(path)
    if isinstance(path, bytes):
        sep = b'\\'
        seps = b'\\/'
        colon = b':'
    else:
        sep = '\\'
        seps = '\\/'
        colon = ':'
# WARNING: Decompyle incomplete


def splitdrive(p):
    '''Split a pathname into drive/UNC sharepoint and relative path specifiers.
    Returns a 2-tuple (drive_or_unc, path); either part may be empty.

    If you assign
        result = splitdrive(p)
    It is always true that:
        result[0] + result[1] == p

    If the path contained a drive letter, drive_or_unc will contain everything
    up to and including the colon.  e.g. splitdrive("c:/dir") returns ("c:", "/dir")

    If the path contained a UNC path, the drive_or_unc will contain the host name
    and share up to but not including the fourth directory separator character.
    e.g. splitdrive("//host/computer/dir") returns ("//host/computer", "/dir")

    Paths cannot contain both a drive letter and a UNC path.

    '''
    p = os.fspath(p)
    if len(p) >= 2:
        if isinstance(p, bytes):
            sep = b'\\'
            altsep = b'/'
            colon = b':'
        else:
            sep = '\\'
            altsep = '/'
            colon = ':'
        normp = p.replace(altsep, sep)
        if normp[0:2] == sep * 2 and normp[2:3] != sep:
            index = normp.find(sep, 2)
            if index == -1:
                return (p[:0], p)
            index2 = None.find(sep, index + 1)
            if index2 == index + 1:
                return (p[:0], p)
            if None == -1:
                index2 = len(p)
            return (p[:index2], p[index2:])
        if None[1:2] == colon:
            return (p[:2], p[2:])
        return (None[:0], p)


def split(p):
    '''Split a pathname.

    Return tuple (head, tail) where tail is everything after the final slash.
    Either part may be empty.'''
    p = os.fspath(p)
    seps = _get_bothseps(p)
    (d, p) = splitdrive(p)
    i = len(p)
    if i and p[i - 1] not in seps:
        i -= 1
        if i:
            if not p[i - 1] not in seps:
                head = p[:i]
                tail = p[i:]
                if not head.rstrip(seps):
                    pass
    head = head
    return (d + head, tail)


def splitext(p):
    p = os.fspath(p)
    if isinstance(p, bytes):
        return genericpath._splitext(p, b'\\', b'/', b'.')
    return None._splitext(p, '\\', '/', '.')

splitext.__doc__ = genericpath._splitext.__doc__

def basename(p):
    '''Returns the final component of a pathname'''
    return split(p)[1]


def dirname(p):
    '''Returns the directory component of a pathname'''
    return split(p)[0]


def islink(path):
    '''Test whether a path is a symbolic link.
    This will always return false for Windows prior to 6.0.
    '''
    pass
# WARNING: Decompyle incomplete


def lexists(path):
    '''Test whether a path exists.  Returns True for broken symbolic links'''
    pass
# WARNING: Decompyle incomplete

# WARNING: Decompyle incomplete
