
'''
Path operations common to more than one OS
Do not use directly.  The OS specific modules import the appropriate
functions from this module themselves.
'''
import os
import stat
__all__ = [
    'commonprefix',
    'exists',
    'getatime',
    'getctime',
    'getmtime',
    'getsize',
    'isdir',
    'isfile',
    'samefile',
    'sameopenfile',
    'samestat']

def exists(path):
    '''Test whether a path exists.  Returns False for broken symbolic links'''
    pass
# WARNING: Decompyle incomplete


def isfile(path):
    '''Test whether a path is a regular file'''
    pass
# WARNING: Decompyle incomplete


def isdir(s):
    '''Return true if the pathname refers to an existing directory.'''
    pass
# WARNING: Decompyle incomplete


def getsize(filename):
    '''Return the size of a file, reported by os.stat().'''
    return os.stat(filename).st_size


def getmtime(filename):
    '''Return the last modification time of a file, reported by os.stat().'''
    return os.stat(filename).st_mtime


def getatime(filename):
    '''Return the last access time of a file, reported by os.stat().'''
    return os.stat(filename).st_atime


def getctime(filename):
    '''Return the metadata change time of a file, reported by os.stat().'''
    return os.stat(filename).st_ctime


def commonprefix(m):
    '''Given a list of pathnames, returns the longest common leading component'''
    if not m:
        return ''
    if not None(m[0], (list, tuple)):
        m = tuple(map(os.fspath, m))
    s1 = min(m)
    s2 = max(m)
    for i, c in enumerate(s1):
        if c != s2[i]:
            return s1[:i]
        return s1


def samestat(s1, s2):
    '''Test whether two stat buffers reference the same file'''
    if s1.st_ino == s2.st_ino:
        pass
    return s1.st_dev == s2.st_dev


def samefile(f1, f2):
    '''Test whether two pathnames reference the same actual file or directory

    This is determined by the device number and i-node number and
    raises an exception if an os.stat() call on either pathname fails.
    '''
    s1 = os.stat(f1)
    s2 = os.stat(f2)
    return samestat(s1, s2)


def sameopenfile(fp1, fp2):
    '''Test whether two open file objects reference the same file'''
    s1 = os.fstat(fp1)
    s2 = os.fstat(fp2)
    return samestat(s1, s2)


def _splitext(p, sep, altsep, extsep):
    '''Split the extension from a pathname.

    Extension is everything from the last dot to the end, ignoring
    leading dots.  Returns "(root, ext)"; ext may be empty.'''
    sepIndex = p.rfind(sep)
    if altsep:
        altsepIndex = p.rfind(altsep)
        sepIndex = max(sepIndex, altsepIndex)
    dotIndex = p.rfind(extsep)
    if dotIndex > sepIndex:
        filenameIndex = sepIndex + 1
        if filenameIndex < dotIndex:
            if p[filenameIndex:filenameIndex + 1] != extsep:
                return (p[:dotIndex], p[dotIndex:])
            None += 1
            if not filenameIndex < dotIndex:
                return (p, p[:0])


def _check_arg_types(funcname, *args):
    hasstr = hasbytes = False
    for s in args:
        if isinstance(s, str):
            hasstr = True
            continue
        if isinstance(s, bytes):
            hasbytes = True
            continue
        raise TypeError(f'''{funcname}() argument must be str, bytes, or os.PathLike object, not {s.__class__.__name__!r}'''), None
        if hasstr or hasbytes:
            raise TypeError("Can't mix strings and bytes in path components"), None
        return None
        return None

