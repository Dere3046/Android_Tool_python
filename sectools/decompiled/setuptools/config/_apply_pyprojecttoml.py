
'''Translation layer between pyproject config and setuptools distribution and
metadata objects.

The distribution and metadata objects are modeled after (an old version of)
core metadata, therefore configs in the format specified for ``pyproject.toml``
need to be processed before being applied.

**PRIVATE MODULE**: API reserved for setuptools internal usage only.
'''
import logging
import os
import warnings
from collections.abc import Mapping
from email.headerregistry import Address
from functools import partial, reduce
from itertools import chain
from types import MappingProxyType
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Set, Tuple, Type, Union
from setuptools._deprecation_warning import SetuptoolsDeprecationWarning
if TYPE_CHECKING:
    from setuptools._importlib import metadata
    from setuptools.dist import Distribution
EMPTY: Mapping = MappingProxyType({ })
_Path = Union[(os.PathLike, str)]
_DictOrStr = Union[(dict, str)]
_CorrespFn = Callable[([
    'Distribution',
    Any,
    _Path], None)]
_Correspondence = Union[(str, _CorrespFn)]
_logger = logging.getLogger(__name__)

def apply(dist = None, config = None, filename = None):
    '''Apply configuration dict read with :func:`read_configuration`'''
    if not config:
        return dist
    if not None.path.dirname(filename):
        pass
    root_dir = '.'
    _apply_project_table(dist, config, root_dir)
    _apply_tool_table(dist, config, filename)
    current_directory = os.getcwd()
    os.chdir(root_dir)
# WARNING: Decompyle incomplete


def _apply_project_table(dist = None, config = None, root_dir = None):
    project_table = config.get('project', { }).copy()
    if not project_table:
        return None
    None(dist, project_table)
    _unify_entry_points(project_table)
    for field, value in project_table.items():
        norm_key = json_compatible_key(field)
        corresp = PYPROJECT_CORRESPONDENCE.get(norm_key, norm_key)
        if callable(corresp):
            corresp(dist, value, root_dir)
            continue
        _set_config(dist, corresp, value)


def _apply_tool_table(dist = None, config = None, filename = None):
    tool_table = config.get('tool', { }).get('setuptools', { })
    if not tool_table:
        return None
    for field, value in None.items():
        norm_key = json_compatible_key(field)
        if norm_key in TOOL_TABLE_DEPRECATIONS:
            suggestion = TOOL_TABLE_DEPRECATIONS[norm_key]
            msg = f'''The parameter `{norm_key}` is deprecated, {suggestion}'''
            warnings.warn(msg, SetuptoolsDeprecationWarning)
        norm_key = TOOL_TABLE_RENAMES.get(norm_key, norm_key)
        _set_config(dist, norm_key, value)
    _copy_command_options(config, dist, filename)


def _handle_missing_dynamic(dist = None, project_table = None):
    '''Be temporarily forgiving with ``dynamic`` fields not listed in ``dynamic``'''
    dynamic = set(project_table.get('dynamic', []))
    for field, getter in _PREVIOUSLY_DEFINED.items():
        if not field in project_table and field in dynamic:
            value = getter(dist)
            if value:
                msg = _WouldIgnoreField.message(field, value)
                warnings.warn(msg, _WouldIgnoreField)


def json_compatible_key(key = None):
    '''As defined in :pep:`566#json-compatible-metadata`'''
    return key.lower().replace('-', '_')


def _set_config(dist = None, field = None, value = None):
    setter = getattr(dist.metadata, f'''set_{field}''', None)
    if setter:
        setter(value)
        return None
    if None(dist.metadata, field) or field in SETUPTOOLS_PATCHES:
        setattr(dist.metadata, field, value)
        return None
    None(dist, field, value)

_CONTENT_TYPES = {
    '.md': 'text/markdown',
    '.rst': 'text/x-rst',
    '.txt': 'text/plain' }

def _guess_content_type(file = None):
    (_, ext) = os.path.splitext(file.lower())
    if not ext:
        return None
    if None in _CONTENT_TYPES:
        return _CONTENT_TYPES[ext]
    valid = None.join((lambda .0: for k, v in .0:
f'''{k} ({v})''')(_CONTENT_TYPES.items()))
    msg = f'''only the following file extensions are recognized: {valid}.'''
    raise ValueError(f'''Undefined content type for {file}, {msg}''')


def _long_description(dist = None, val = None, root_dir = None):
    expand = expand
    import setuptools.config
    if isinstance(val, str):
        text = expand.read_files(val, root_dir)
        ctype = _guess_content_type(val)
    elif not val.get('text'):
        pass
    text = expand.read_files(val.get('file', []), root_dir)
    ctype = val['content-type']
    _set_config(dist, 'long_description', text)
    if ctype:
        _set_config(dist, 'long_description_content_type', ctype)
        return None
    return val.get('text')


def _license(dist = None, val = None, root_dir = None):
    expand = expand
    import setuptools.config
    if 'file' in val:
        _set_config(dist, 'license', expand.read_files([
            val['file']], root_dir))
        return None
    None(dist, 'license', val['text'])


def _people(dist = None, val = None, _root_dir = None, kind = ('dist', 'Distribution', 'val', List[dict], '_root_dir', _Path, 'kind', str)):
    field = []
    email_field = []
    for person in val:
        if 'name' not in person:
            email_field.append(person['email'])
            continue
        if 'email' not in person:
            field.append(person['name'])
            continue
        addr = Address(person['name'], person['email'], **('display_name', 'addr_spec'))
        email_field.append(str(addr))
    if field:
        _set_config(dist, kind, ', '.join(field))
    if email_field:
        _set_config(dist, f'''{kind}_email''', ', '.join(email_field))
        return None


def _project_urls(dist = None, val = None, _root_dir = None):
    _set_config(dist, 'project_urls', val)


def _python_requires(dist = None, val = None, _root_dir = None):
    SpecifierSet = SpecifierSet
    import setuptools.extern.packaging.specifiers
    _set_config(dist, 'python_requires', SpecifierSet(val))


def _dependencies(dist = None, val = None, _root_dir = None):
    if getattr(dist, 'install_requires', []):
        msg = '`install_requires` overwritten in `pyproject.toml` (dependencies)'
        warnings.warn(msg)
    _set_config(dist, 'install_requires', val)


def _optional_dependencies(dist = None, val = None, _root_dir = None):
    existing = getattr(dist, 'extras_require', { })
# WARNING: Decompyle incomplete


def _unify_entry_points(project_table = None):
    project = project_table
    entry_points = project.pop('entry-points', project.pop('entry_points', { }))
    renaming = {
        'scripts': 'console_scripts',
        'gui_scripts': 'gui_scripts' }
    for key, value in list(project.items()):
        norm_key = json_compatible_key(key)
        if norm_key in renaming and value:
            entry_points[renaming[norm_key]] = project.pop(key)
    if entry_points:
        project['entry-points'] = (lambda .0: pass# WARNING: Decompyle incomplete
)(entry_points.items())
        return None


def _copy_command_options(pyproject = None, dist = None, filename = None):
    tool_table = pyproject.get('tool', { })
    cmdclass = tool_table.get('setuptools', { }).get('cmdclass', { })
    valid_options = _valid_command_options(cmdclass)
    cmd_opts = dist.command_options
    for cmd, config in pyproject.get('tool', { }).get('distutils', { }).items():
        cmd = json_compatible_key(cmd)
        valid = valid_options.get(cmd, set())
        cmd_opts.setdefault(cmd, { })
        for key, value in config.items():
            key = json_compatible_key(key)
            cmd_opts[cmd][key] = (str(filename), value)
            if key not in valid:
                _logger.warning(f'''Command option {cmd}.{key} is not defined''')


def _valid_command_options(cmdclass = None):
    metadata = metadata
    import _importlib
    Distribution = Distribution
    import setuptools.dist
    valid_options = {
        'global': _normalise_cmd_options(Distribution.global_options) }
    unloaded_entry_points = metadata.entry_points('distutils.commands', **('group',))
    loaded_entry_points = (lambda .0: for ep in .0:
_load_ep(ep))(unloaded_entry_points)
    entry_points = (lambda .0: for ep in .0:
if ep:
epcontinueNone)(loaded_entry_points)
    for cmd, cmd_class in chain(entry_points, cmdclass.items()):
        opts = valid_options.get(cmd, set())
        opts = opts | _normalise_cmd_options(getattr(cmd_class, 'user_options', []))
        valid_options[cmd] = opts
    return valid_options


def _load_ep(ep = None):
    pass
# WARNING: Decompyle incomplete


def _normalise_cmd_option_key(name = None):
    return json_compatible_key(name).strip('_=')


def _normalise_cmd_options(desc = None):
    return (lambda .0: pass# WARNING: Decompyle incomplete
)(desc)


def _attrgetter(attr):
    '''
    Similar to ``operator.attrgetter`` but returns None if ``attr`` is not found
    >>> from types import SimpleNamespace
    >>> obj = SimpleNamespace(a=42, b=SimpleNamespace(c=13))
    >>> _attrgetter("a")(obj)
    42
    >>> _attrgetter("b.c")(obj)
    13
    >>> _attrgetter("d")(obj) is None
    True
    '''
    return partial(reduce, (lambda acc, x: getattr(acc, x, None)), attr.split('.'))


def _some_attrgetter(*items):
    '''
    Return the first "truth-y" attribute or None
    >>> from types import SimpleNamespace
    >>> obj = SimpleNamespace(a=42, b=SimpleNamespace(c=13))
    >>> _some_attrgetter("d", "a", "b.c")(obj)
    42
    >>> _some_attrgetter("d", "e", "b.c", "a")(obj)
    13
    >>> _some_attrgetter("d", "e", "f")(obj) is None
    True
    '''
    
    def _acessor(obj = None):
        values = (lambda .0 = None: for i in .0:
_attrgetter(i)(obj))(items)
        return next((lambda .0: for i in .0:
if i is not None:
icontinueNone)(values), None)

    return _acessor

PYPROJECT_CORRESPONDENCE: Dict[(str, _Correspondence)] = {
    'readme': _long_description,
    'license': _license,
    'authors': partial(_people, 'author', **('kind',)),
    'maintainers': partial(_people, 'maintainer', **('kind',)),
    'urls': _project_urls,
    'dependencies': _dependencies,
    'optional_dependencies': _optional_dependencies,
    'requires_python': _python_requires }
TOOL_TABLE_RENAMES = {
    'script_files': 'scripts' }
TOOL_TABLE_DEPRECATIONS = {
    'namespace_packages': 'consider using implicit namespaces instead (PEP 420).' }
SETUPTOOLS_PATCHES = {
    'provides_extras',
    'license_files',
    'long_description_content_type',
    'license_file',
    'project_urls'}
_PREVIOUSLY_DEFINED = {
    'name': _attrgetter('metadata.name'),
    'version': _attrgetter('metadata.version'),
    'description': _attrgetter('metadata.description'),
    'readme': _attrgetter('metadata.long_description'),
    'requires-python': _some_attrgetter('python_requires', 'metadata.python_requires'),
    'license': _attrgetter('metadata.license'),
    'authors': _some_attrgetter('metadata.author', 'metadata.author_email'),
    'maintainers': _some_attrgetter('metadata.maintainer', 'metadata.maintainer_email'),
    'keywords': _attrgetter('metadata.keywords'),
    'classifiers': _attrgetter('metadata.classifiers'),
    'urls': _attrgetter('metadata.project_urls'),
    'entry-points': _attrgetter('entry_points'),
    'dependencies': _some_attrgetter('_orig_install_requires', 'install_requires'),
    'optional-dependencies': _some_attrgetter('_orig_extras_require', 'extras_require') }

class _WouldIgnoreField(UserWarning):
    '''Inform users that ``pyproject.toml`` would overwrite previous metadata.'''
    MESSAGE = '    {field!r} defined outside of `pyproject.toml` would be ignored.\n    !!\n\n\n    ##########################################################################\n    # configuration would be ignored/result in error due to `pyproject.toml` #\n    ##########################################################################\n\n    The following seems to be defined outside of `pyproject.toml`:\n\n    `{field} = {value!r}`\n\n    According to the spec (see the link below), however, setuptools CANNOT\n    consider this value unless {field!r} is listed as `dynamic`.\n\n    https://packaging.python.org/en/latest/specifications/declaring-project-metadata/\n\n    For the time being, `setuptools` will still consider the given value (as a\n    **transitional** measure), but please note that future releases of setuptools will\n    follow strictly the standard.\n\n    To prevent this warning, you can list {field!r} under `dynamic` or alternatively\n    remove the `[project]` table from your file and rely entirely on other means of\n    configuration.\n    \n\n!!\n    '
    
    def message(cls, field, value):
        cleandoc = cleandoc
        import inspect
        return cleandoc(cls.MESSAGE.format(field, value, **('field', 'value')))

    message = classmethod(message)

