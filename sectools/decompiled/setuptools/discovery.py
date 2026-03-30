
'''Automatic discovery of Python modules and packages (for inclusion in the
distribution) and other config values.

For the purposes of this module, the following nomenclature is used:

- "src-layout": a directory representing a Python project that contains a "src"
  folder. Everything under the "src" folder is meant to be included in the
  distribution when packaging the project. Example::

    .
    ├── tox.ini
    ├── pyproject.toml
    └── src/
        └── mypkg/
            ├── __init__.py
            ├── mymodule.py
            └── my_data_file.txt

- "flat-layout": a Python project that does not use "src-layout" but instead
  have a directory under the project root for each package::

    .
    ├── tox.ini
    ├── pyproject.toml
    └── mypkg/
        ├── __init__.py
        ├── mymodule.py
        └── my_data_file.txt

- "single-module": a project that contains a single Python script direct under
  the project root (no directory used)::

    .
    ├── tox.ini
    ├── pyproject.toml
    └── mymodule.py

'''
import itertools
import os
from fnmatch import fnmatchcase
from glob import glob
from pathlib import Path
from typing import TYPE_CHECKING, Callable, Dict, Iterable, Iterator, List, Mapping, Optional, Tuple, Union
import _distutils_hack.override as _distutils_hack
from distutils import log
from distutils.util import convert_path
_Path = Union[(str, os.PathLike)]
_Filter = Callable[([
    str], bool)]
StrIter = Iterator[str]
chain_iter = itertools.chain.from_iterable
if TYPE_CHECKING:
    from setuptools import Distribution

def _valid_name(path = None):
    return os.path.basename(path).isidentifier()


class _Finder:
    '''Base class that exposes functionality for module/package finders'''
    ALWAYS_EXCLUDE: Tuple[(str, ...)] = ()
    DEFAULT_EXCLUDE: Tuple[(str, ...)] = ()
    
    def find(cls = None, where = None, exclude = classmethod, include = ('.', (), ('*',))):
