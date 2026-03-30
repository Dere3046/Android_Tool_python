
'''Utility functions to expand configuration directives or special values
(such glob patterns).

We can split the process of interpreting configuration files into 2 steps:

1. The parsing the file contents from strings to value objects
   that can be understand by Python (for example a string with a comma
   separated list of keywords into an actual Python list of strings).

2. The expansion (or post-processing) of these values according to the
   semantics ``setuptools`` assign to them (for example a configuration field
   with the ``file:`` directive should be expanded from a list of file paths to
   a single string with the contents of those files concatenated)

This module focus on the second step, and therefore allow sharing the expansion
functions among several configuration file formats.

**PRIVATE MODULE**: API reserved for setuptools internal usage only.
'''
import ast
import importlib
import io
import os
import pathlib
import sys
import warnings
from glob import iglob
from configparser import ConfigParser
from importlib.machinery import ModuleSpec
from itertools import chain
from typing import TYPE_CHECKING, Callable, Dict, Iterable, Iterator, List, Mapping, Optional, Tuple, TypeVar, Union, cast
from pathlib import Path
from types import ModuleType
from distutils.errors import DistutilsOptionError
from _path import same_path as _same_path
if TYPE_CHECKING:
    from setuptools.dist import Distribution
    from setuptools.discovery import ConfigDiscovery
    from distutils.dist import DistributionMetadata
chain_iter = chain.from_iterable
_Path = Union[(str, os.PathLike)]
_K = TypeVar('_K')
_V = TypeVar('_V', True, **('covariant',))

class StaticModule:
    '''Proxy to a module object that avoids executing arbitrary code.'''
    
    def __init__(self = None, name = None, spec = None):
        module = ast.parse(pathlib.Path(spec.origin).read_bytes())
        vars(self).update(locals())
        del self.self

    
    def _find_assignments(self = None):
        for None in self.module.body:
            statement = None
            if isinstance(statement, ast.Assign):
                yield from (lambda .0 = None: for target in .0:
(target, statement.value))(statement.targets)
                continue
            if isinstance(statement, ast.AnnAssign) and statement.value:
                yield (statement.target, statement.value)

    
    def __getattr__(self, attr):
        '''Attempt to load an attribute "statically", via :func:`ast.literal_eval`.'''
        pass
    # WARNING: Decompyle incomplete



def glob_relative(patterns = None, root_dir = None):
    '''Expand the list of glob patterns, but preserving relative paths.

    :param list[str] patterns: List of glob patterns
    :param str root_dir: Path to which globs should be relative
                         (current directory by default)
    :rtype: list
    '''
    glob_characters = {
        '*',
        '?',
        '{',
        ']',
        '}',
        '['}
    expanded_values = []
    if not root_dir:
        pass
    root_dir = os.getcwd()
    for path in patterns:
        value = None
        if None((lambda .0 = None: for char in .0:
char in value)(glob_characters)):
            glob_path = os.path.abspath(os.path.join(root_dir, value))
            None(None((lambda .0 = None: for path in .0:
os.path.relpath(path, root_dir).replace(os.sep, '/'))(iglob(glob_path, True, **('recursive',)))))
            continue
        expanded_values.append(path)
    return expanded_values


def read_files(filepaths = None, root_dir = None):
    """Return the content of the files concatenated using ``
`` as str

    This function is sandboxed and won't reach anything outside ``root_dir``

    (By default ``root_dir`` is the current directory).
    """
    always_iterable = always_iterable
    import setuptools.extern.more_itertools
    if not root_dir:
        pass
    root_dir = os.path.abspath(os.getcwd())
    _filepaths = (lambda .0 = None: for path in .0:
os.path.join(root_dir, path))(always_iterable(filepaths))
    return None((lambda .0 = None: for path in .0:
if _assert_local(path, root_dir):
_read_file(path)continueNone)(_filter_existing_files(_filepaths)))


def _filter_existing_files(filepaths = None):
    for path in filepaths:
        if os.path.isfile(path):
            yield path
            continue
        warnings.warn(f'''File {path!r} cannot be found''')


def _read_file(filepath = None):
    pass
# WARNING: Decompyle incomplete


def _assert_local(filepath = None, root_dir = None):
    if Path(os.path.abspath(root_dir)) not in Path(os.path.abspath(filepath)).parents:
        msg = f'''Cannot access {filepath!r} (or anything outside {root_dir!r})'''
        raise DistutilsOptionError(msg)


def read_attr(attr_desc = None, package_dir = None, root_dir = None):
    '''Reads the value of an attribute from a module.

    This function will try to read the attributed statically first
    (via :func:`ast.literal_eval`), and only evaluate the module if it fails.

    Examples:
        read_attr("package.attr")
        read_attr("package.module.attr")

    :param str attr_desc: Dot-separated string describing how to reach the
        attribute (see examples above)
    :param dict[str, str] package_dir: Mapping of package names to their
        location in disk (represented by paths relative to ``root_dir``).
    :param str root_dir: Path to directory containing all the packages in
        ``package_dir`` (current directory by default).
    :rtype: str
    '''
    if not root_dir:
        pass
    root_dir = os.getcwd()
    attrs_path = attr_desc.strip().split('.')
    attr_name = attrs_path.pop()
    module_name = '.'.join(attrs_path)
    if not module_name:
        pass
    module_name = '__init__'
    (_parent_path, path, module_name) = _find_module(module_name, package_dir, root_dir)
    spec = _find_spec(module_name, path)
# WARNING: Decompyle incomplete


def _find_spec(module_name = None, module_path = None):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if not spec:
        pass
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        raise ModuleNotFoundError(module_name)


def _load_spec(spec = None, module_name = None):
    name = getattr(spec, '__name__', module_name)
    if name in sys.modules:
        return sys.modules[name]
    module = None.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _find_module(module_name = None, package_dir = None, root_dir = None):
    '''Given a module (that could normally be imported by ``module_name``
    after the build is complete), find the path to the parent directory where
    it is contained and the canonical name that could be used to import it
    considering the ``package_dir`` in the build configuration and ``root_dir``
    '''
    parent_path = root_dir
    module_parts = module_name.split('.')
    if package_dir:
        if module_parts[0] in package_dir:
            custom_path = package_dir[module_parts[0]]
            parts = custom_path.rsplit('/', 1)
            if len(parts) > 1:
                parent_path = os.path.join(root_dir, parts[0])
                parent_module = parts[1]
            else:
                parent_module = custom_path
            module_name = None('.'.join)
        elif '' in package_dir:
            parent_path = os.path.join(root_dir, package_dir[''])
# WARNING: Decompyle incomplete


def resolve_class(qualified_class_name = None, package_dir = None, root_dir = None):
    '''Given a qualified class name, return the associated class object'''
    if not root_dir:
        pass
    root_dir = os.getcwd()
    idx = qualified_class_name.rfind('.')
    class_name = qualified_class_name[idx + 1:]
    pkg_name = qualified_class_name[:idx]
    (_parent_path, path, module_name) = _find_module(pkg_name, package_dir, root_dir)
    module = _load_spec(_find_spec(module_name, path), module_name)
    return getattr(module, class_name)


def cmdclass(values = None, package_dir = None, root_dir = None):
    '''Given a dictionary mapping command names to strings for qualified class
    names, apply :func:`resolve_class` to the dict values.
    '''
    return (lambda .0 = None: pass# WARNING: Decompyle incomplete
)(values.items())


def find_packages(*, namespaces, fill_package_dir, root_dir, **kwargs):
    '''Works similarly to :func:`setuptools.find_packages`, but with all
    arguments given as keyword arguments. Moreover, ``where`` can be given
    as a list (the results will be simply concatenated).

    When the additional keyword argument ``namespaces`` is ``True``, it will
    behave like :func:`setuptools.find_namespace_packages`` (i.e. include
    implicit namespaces as per :pep:`420`).

    The ``where`` argument will be considered relative to ``root_dir`` (or the current
    working directory when ``root_dir`` is not given).

    If the ``fill_package_dir`` argument is passed, this function will consider it as a
    similar data structure to the ``package_dir`` configuration parameter add fill-in
    any missing package location.

    :rtype: list
    '''
    construct_package_dir = construct_package_dir
    import setuptools.discovery
    unique_everseen = unique_everseen
    always_iterable = always_iterable
    import setuptools.extern.more_itertools
    if namespaces:
        PackageFinder = PEP420PackageFinder
        import setuptools.discovery
    else:
        PackageFinder = PackageFinder
        import setuptools.discovery
    if not root_dir:
        pass
    root_dir = os.curdir
    where = kwargs.pop('where', [
        '.'])
    packages = []
    fill_package_dir = { } if fill_package_dir is None else fill_package_dir
    search = list(unique_everseen(always_iterable(where)))
    if len(search) == 1 and None((lambda .0 = None: for x in .0:
not _same_path(search[0], x))(('.', root_dir))):
        fill_package_dir.setdefault('', search[0])
# WARNING: Decompyle incomplete


def _nest_path(parent = None, path = None):
    path = parent if path in frozenset({'', '.'}) else os.path.join(parent, path)
    return os.path.normpath(path)


def version(value = None):
    '''When getting the version directly from an attribute,
    it should be normalised to string.
    '''
    if callable(value):
        value = value()
    value = cast(Iterable[Union[(str, int)]], value)
    if not isinstance(value, str):
        if hasattr(value, '__iter__'):
            value = '.'.join(map(str, value))
            return value
        value = None % value
    return value


def canonic_package_data(package_data = None):
    if '*' in package_data:
        package_data[''] = package_data.pop('*')
    return package_data


def canonic_data_files(data_files = None, root_dir = None):
    '''For compatibility with ``setup.py``, ``data_files`` should be a list
    of pairs instead of a dict.

    This function also expands glob patterns.
    '''
    if isinstance(data_files, list):
        return data_files
    return (lambda .0 = None: [ (dest, glob_relative(patterns, root_dir)) for dest, patterns in .0 ])(data_files.items())


def entry_points(text = None, text_source = None):
    '''Given the contents of entry-points file,
    process it into a 2-level dictionary (``dict[str, dict[str, str]]``).
    The first level keys are entry-point groups, the second level keys are
    entry-point names, and the second level values are references to objects
    (that correspond to the entry-point value).
    '''
    parser = ConfigParser(None, ('=',), **('default_section', 'delimiters'))
    parser.optionxform = str
    parser.read_string(text, text_source)
    groups = (lambda .0: pass# WARNING: Decompyle incomplete
)(parser.items())
    groups.pop(parser.default_section, None)
    return groups


class EnsurePackagesDiscovered:
    '''Some expand functions require all the packages to already be discovered before
    they run, e.g. :func:`read_attr`, :func:`resolve_class`, :func:`cmdclass`.

    Therefore in some cases we will need to run autodiscovery during the evaluation of
    the configuration. However, it is better to postpone calling package discovery as
    much as possible, because some parameters can influence it (e.g. ``package_dir``),
    and those might not have been processed yet.
    '''
    
    def __init__(self = None, distribution = None):
        self._dist = distribution
        self._called = False

    
    def __call__(self):
        '''Trigger the automatic package discovery, if it is still necessary.'''
        if not self._called:
            self._called = True
            self._dist.set_defaults(False, **('name',))
            return None

    
    def __enter__(self):
        return self

    
    def __exit__(self, _exc_type, _exc_value, _traceback):
        if self._called:
            self._dist.set_defaults.analyse_name()
            return None

    
    def _get_package_dir(self = None):
        self()
        pkg_dir = self._dist.package_dir
        if pkg_dir is None:
            return { }

    
    def package_dir(self = None):
        '''Proxy to ``package_dir`` that may trigger auto-discovery when used.'''
        return LazyMappingProxy(self._get_package_dir)

    package_dir = None(package_dir)


def LazyMappingProxy():
    '''LazyMappingProxy'''
    __doc__ = 'Mapping proxy that delays resolving the target object, until really needed.\n\n    >>> def obtain_mapping():\n    ...     print("Running expensive function!")\n    ...     return {"key": "value", "other key": "other value"}\n    >>> mapping = LazyMappingProxy(obtain_mapping)\n    >>> mapping["key"]\n    Running expensive function!\n    \'value\'\n    >>> mapping["other key"]\n    \'other value\'\n    '
    
    def __init__(self = None, obtain_mapping_value = None):
        self._obtain = obtain_mapping_value
        self._value = None

    
    def _target(self = None):
        if self._value is None:
            self._value = self._obtain()
        return self._value

    
    def __getitem__(self = None, key = None):
        return self._target()[key]

    
    def __len__(self = None):
        return len(self._target())

    
    def __iter__(self = None):
        return iter(self._target())


LazyMappingProxy = <NODE:27>(LazyMappingProxy, 'LazyMappingProxy', Mapping[(_K, _V)])
