
import io
import posixpath
import zipfile
import itertools
import contextlib
import sys
import pathlib
if sys.version_info < (3, 7):
    from collections import OrderedDict
else:
    OrderedDict = dict
__all__ = [
    'Path']

def _parents(path):
    """
    Given a path with elements separated by
    posixpath.sep, generate all parents of that path.

    >>> list(_parents('b/d'))
    ['b']
    >>> list(_parents('/b/d/'))
    ['/b']
    >>> list(_parents('b/d/f/'))
    ['b/d', 'b']
    >>> list(_parents('b'))
    []
    >>> list(_parents(''))
    []
    """
    return itertools.islice(_ancestry(path), 1, None)


def _ancestry(path):
    """
    Given a path with elements separated by
    posixpath.sep, generate all elements of that path

    >>> list(_ancestry('b/d'))
    ['b/d', 'b']
    >>> list(_ancestry('/b/d/'))
    ['/b/d', '/b']
    >>> list(_ancestry('b/d/f/'))
    ['b/d/f', 'b/d', 'b']
    >>> list(_ancestry('b'))
    ['b']
    >>> list(_ancestry(''))
    []
    """
    path = path.rstrip(posixpath.sep)
    if path or path != posixpath.sep:
        yield path
        (path, tail) = posixpath.split(path)
        if path:
            if not path != posixpath.sep:
                return None
            return None
        return None

_dedupe = OrderedDict.fromkeys

def _difference(minuend, subtrahend):
    '''
    Return items in minuend not in subtrahend, retaining order
    with O(1) lookup.
    '''
    return itertools.filterfalse(set(subtrahend).__contains__, minuend)


class CompleteDirs(zipfile.ZipFile):
    '''
    A ZipFile subclass that ensures that implied directories
    are always included in the namelist.
    '''
    
    def _implied_dirs(names):
        parents = itertools.chain.from_iterable(map(_parents, names))
        as_dirs = (lambda .0: for p in .0:
p + posixpath.sep)(parents)
        return _dedupe(_difference(as_dirs, names))

    _implied_dirs = staticmethod(_implied_dirs)
    
    def namelist(self = None):
        names = super(CompleteDirs, self).namelist()
        return names + list(self._implied_dirs(names))

    
    def _name_set(self):
        return set(self.namelist())

    
    def resolve_dir(self, name):
        '''
        If the name represents a directory, return that name
        as a directory (with the trailing slash).
        '''
        names = self._name_set()
        dirname = name + '/'
        if name not in names:
            pass
        dir_match = dirname in names
        if dir_match:
            return dirname

    
    def make(cls, source):
        '''
        Given a source (filename or zipfile), return an
        appropriate CompleteDirs subclass.
        '''
        if isinstance(source, CompleteDirs):
            return source
        if not None(source, zipfile.ZipFile):
            return cls(_pathlib_compat(source))
        if None not in source.mode:
            cls = CompleteDirs
        source.__class__ = cls
        return source

    make = classmethod(make)
    __classcell__ = None


class FastLookup(CompleteDirs):
    '''
    ZipFile subclass to ensure implicit
    dirs exist and are resolved rapidly.
    '''
    
    def namelist(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def _name_set(self = None):
        pass
    # WARNING: Decompyle incomplete

    __classcell__ = None


def _pathlib_compat(path):
    '''
    For path-like objects, convert to a filename for compatibility
    on Python 3.6.1 and earlier.
    '''
    pass
# WARNING: Decompyle incomplete


class Path:
    """
    A pathlib-compatible interface for zip files.

    Consider a zip file with this structure::

        .
        ├── a.txt
        └── b
            ├── c.txt
            └── d
                └── e.txt

    >>> data = io.BytesIO()
    >>> zf = zipfile.ZipFile(data, 'w')
    >>> zf.writestr('a.txt', 'content of a')
    >>> zf.writestr('b/c.txt', 'content of c')
    >>> zf.writestr('b/d/e.txt', 'content of e')
    >>> zf.filename = 'mem/abcde.zip'

    Path accepts the zipfile object itself or a filename

    >>> root = Path(zf)

    From there, several path operations are available.

    Directory iteration (including the zip file itself):

    >>> a, b = root.iterdir()
    >>> a
    Path('mem/abcde.zip', 'a.txt')
    >>> b
    Path('mem/abcde.zip', 'b/')

    name property:

    >>> b.name
    'b'

    join with divide operator:

    >>> c = b / 'c.txt'
    >>> c
    Path('mem/abcde.zip', 'b/c.txt')
    >>> c.name
    'c.txt'

    Read text:

    >>> c.read_text()
    'content of c'

    existence:

    >>> c.exists()
    True
    >>> (b / 'missing.txt').exists()
    False

    Coercion to string:

    >>> import os
    >>> str(c).replace(os.sep, posixpath.sep)
    'mem/abcde.zip/b/c.txt'

    At the root, ``name``, ``filename``, and ``parent``
    resolve to the zipfile. Note these attributes are not
    valid and will raise a ``ValueError`` if the zipfile
    has no filename.

    >>> root.name
    'abcde.zip'
    >>> str(root.filename).replace(os.sep, posixpath.sep)
    'mem/abcde.zip'
    >>> str(root.parent)
    'mem'
    """
    __repr = '{self.__class__.__name__}({self.root.filename!r}, {self.at!r})'
    
    def __init__(self, root, at = ('',)):
        '''
        Construct a Path from a ZipFile or filename.

        Note: When the source is an existing ZipFile object,
        its type (__class__) will be mutated to a
        specialized type. If the caller wishes to retain the
        original type, the caller should either create a
        separate ZipFile object or pass a filename.
        '''
        self.root = FastLookup.make(root)
        self.at = at

    
    def open(self = None, mode = ('r',), *, pwd, *args, **kwargs):
        '''
        Open this entry as text or binary following the semantics
        of ``pathlib.Path.open()`` by passing arguments through
        to io.TextIOWrapper().
        '''
        if self.is_dir():
            raise IsADirectoryError(self)
        zip_mode = None[0]
        if self.exists() and zip_mode == 'r':
            raise FileNotFoundError(self)
        stream = None.root.open(self.at, zip_mode, pwd, **('pwd',))
        if 'b' in mode:
            if args or kwargs:
                raise ValueError('encoding args invalid for binary operation')
            return None
    # WARNING: Decompyle incomplete

    
    def name(self):
        if not pathlib.Path(self.at).name:
            pass
        return self.filename.name

    name = property(name)
    
    def suffix(self):
        if not pathlib.Path(self.at).suffix:
            pass
        return self.filename.suffix

    suffix = property(suffix)
    
    def suffixes(self):
        if not pathlib.Path(self.at).suffixes:
            pass
        return self.filename.suffixes

    suffixes = property(suffixes)
    
    def stem(self):
        if not pathlib.Path(self.at).stem:
            pass
        return self.filename.stem

    stem = property(stem)
    
    def filename(self):
        return pathlib.Path(self.root.filename).joinpath(self.at)

    filename = property(filename)
    
    def read_text(self, *args, **kwargs):
        pass
    # WARNING: Decompyle incomplete

    
    def read_bytes(self):
        pass
    # WARNING: Decompyle incomplete

    
    def _is_child(self, path):
        return posixpath.dirname(path.at.rstrip('/')) == self.at.rstrip('/')

    
    def _next(self, at):
        return self.__class__(self.root, at)

    
    def is_dir(self):
        if not not (self.at):
            pass
        return self.at.endswith('/')

    
    def is_file(self):
        if self.exists():
            pass
        return not self.is_dir()

    
    def exists(self):
        return self.at in self.root._name_set()

    
    def iterdir(self):
        if not self.is_dir():
            raise ValueError("Can't listdir a file")
        subs = None(self._next, self.root.namelist())
        return filter(self._is_child, subs)

    
    def __str__(self):
        return posixpath.join(self.root.filename, self.at)

    
    def __repr__(self):
        return self.__repr.format(self, **('self',))

    
    def joinpath(self, *other):
        pass
    # WARNING: Decompyle incomplete

    __truediv__ = joinpath
    
    def parent(self):
        if not self.at:
            return self.filename.parent
        parent_at = None.dirname(self.at.rstrip('/'))
        if parent_at:
            parent_at += '/'
        return self._next(parent_at)

    parent = property(parent)

