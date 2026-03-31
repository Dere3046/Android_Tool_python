
import functools
import os
import pathlib
import types
import warnings
from typing import Union, Iterable, ContextManager, BinaryIO, TextIO, Any
from  import _common
Package = Union[(types.ModuleType, str)]
Resource = str

def deprecated(func):
    
    def wrapper(*args, **kwargs):
        warnings.warn(f'''{func.__name__} is deprecated. Use files() instead. Refer to https://importlib-resources.readthedocs.io/en/latest/using.html#migrating-from-legacy for migration advice.''', DeprecationWarning, 2, **('stacklevel',))
    # WARNING: Decompyle incomplete

    wrapper = None(wrapper)
    return wrapper


def normalize_path(path):
    '''Normalize a path by ensuring it is a string.

    If the resulting string contains path separators, an exception is raised.
    '''
    str_path = str(path)
    (parent, file_name) = os.path.split(str_path)
    if parent:
        raise ValueError(f'''{path!r} must be only a file name''')


def open_binary(package = None, resource = None):
    '''Return a file-like object opened for binary reading of the resource.'''
    return (_common.files(package) / normalize_path(resource)).open('rb')

open_binary = None(open_binary)

def read_binary(package = None, resource = None):
    '''Return the binary contents of the resource.'''
    return (_common.files(package) / normalize_path(resource)).read_bytes()

read_binary = None(read_binary)

def open_text(package = None, resource = None, encoding = deprecated, errors = ('utf-8', 'strict')):
    '''Return a file-like object opened for text reading of the resource.'''
    return (_common.files(package) / normalize_path(resource)).open('r', encoding, errors, **('encoding', 'errors'))

open_text = None(open_text)

def read_text(package = None, resource = None, encoding = deprecated, errors = ('utf-8', 'strict')):
    '''Return the decoded string of the resource.

    The decoding-related arguments have the same semantics as those of
    bytes.decode().
    '''
    pass
# WARNING: Decompyle incomplete

read_text = None(read_text)

def contents(package = None):
    '''Return an iterable of entries in `package`.

    Note that not all entries are resources.  Specifically, directories are
    not considered resources.  Use `is_resource()` on each entry returned here
    to check if it is a resource or not.
    '''
    return (lambda .0: [ path.name for path in .0 ])(_common.files(package).iterdir())

contents = None(contents)

def is_resource(package = None, name = None):
    '''True if `name` is a resource inside `package`.

    Directories are *not* resources.
    '''
    resource = normalize_path(name)
    return None((lambda .0 = None: for traversable in .0:
if traversable.name == resource:
passtraversable.is_file())(_common.files(package).iterdir()))

is_resource = None(is_resource)

def path(package = None, resource = None):
    '''A context manager providing a file path object to the resource.

    If the resource does not already exist on its own on the file system,
    a temporary file will be created. If the file was created, the file
    will be deleted upon exiting the context manager (no exception is
    raised if the file was deleted prior to the context manager
    exiting).
    '''
    return _common.as_file(_common.files(package) / normalize_path(resource))

path = None(path)
