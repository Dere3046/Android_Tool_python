
'''
Load setuptools configuration from ``pyproject.toml`` files.

**PRIVATE MODULE**: API reserved for setuptools internal usage only.
'''
import logging
import os
import warnings
from contextlib import contextmanager
from functools import partial
from typing import TYPE_CHECKING, Callable, Dict, Optional, Mapping, Union
from setuptools.errors import FileError, OptionError
from  import expand as _expand
from _apply_pyprojecttoml import apply as _apply
from _apply_pyprojecttoml import _PREVIOUSLY_DEFINED, _WouldIgnoreField
if TYPE_CHECKING:
    from setuptools.dist import Distribution
_Path = Union[(str, os.PathLike)]
_logger = logging.getLogger(__name__)

def load_file(filepath = None):
    tomli = tomli
    import setuptools.extern
# WARNING: Decompyle incomplete


def validate(config = None, filepath = None):
    validator = _validate_pyproject
    import 
    trove_classifier = validator.FORMAT_FUNCTIONS.get('trove-classifier')
    if hasattr(trove_classifier, '_disable_download'):
        trove_classifier._disable_download()
# WARNING: Decompyle incomplete


def apply_configuration(dist = None, filepath = None, ignore_option_errors = None):
    '''Apply the configuration from a ``pyproject.toml`` file into an existing
    distribution object.
    '''
    config = read_configuration(filepath, True, ignore_option_errors, dist)
    return _apply(dist, config, filepath)


def read_configuration(filepath = None, expand = None, ignore_option_errors = None, dist = (True, False, None)):
    '''Read given configuration file and returns options from it as a dict.

    :param str|unicode filepath: Path to configuration file in the ``pyproject.toml``
        format.

    :param bool expand: Whether to expand directives and other computed values
        (i.e. post-process the given configuration)

    :param bool ignore_option_errors: Whether to silently ignore
        options, values of which could not be resolved (e.g. due to exceptions
        in directives such as file:, attr:, etc.).
        If False exceptions are propagated as expected.

    :param Distribution|None: Distribution object to which the configuration refers.
        If not given a dummy object will be created and discarded after the
        configuration is read. This is used for auto-discovery of packages in the case
        a dynamic configuration (e.g. ``attr`` or ``cmdclass``) is expanded.
        When ``expand=False`` this object is simply ignored.

    :rtype: dict
    '''
    filepath = os.path.abspath(filepath)
    if not os.path.isfile(filepath):
        raise FileError(f'''Configuration file {filepath!r} does not exist.''')
    if not None(filepath):
        pass
    asdict = { }
    project_table = asdict.get('project', { })
    tool_table = asdict.get('tool', { })
    setuptools_table = tool_table.get('setuptools', { })
    if not (asdict or project_table) and setuptools_table:
        return { }
    if None:
        msg = 'Support for `[tool.setuptools]` in `pyproject.toml` is still *beta*.'
        warnings.warn(msg, _BetaConfiguration)
    orig_setuptools_table = setuptools_table.copy()
    if dist and getattr(dist, 'include_package_data') is not None:
        setuptools_table.setdefault('include-package-data', dist.include_package_data)
    else:
        setuptools_table.setdefault('include-package-data', True)
    asdict['tool'] = tool_table
    tool_table['setuptools'] = setuptools_table
# WARNING: Decompyle incomplete


def _skip_bad_config(project_cfg = None, setuptools_cfg = None, dist = None):
    '''Be temporarily forgiving with invalid ``pyproject.toml``'''
    if (dist is None or dist.metadata.name is None) and dist.metadata.version is None and dist.install_requires is None:
        return False
    if None:
        return False
    given_config = None(project_cfg.keys())
    popular_subset = {
        'version',
        'python_requires',
        'name',
        'requires-python'}
    if given_config <= popular_subset:
        warnings.warn(_InvalidFile.message(), _InvalidFile, 2, **('stacklevel',))
        return True


def expand_configuration(config = None, root_dir = None, ignore_option_errors = None, dist = (None, False, None)):
    '''Given a configuration with unresolved fields (e.g. dynamic, cmdclass, ...)
    find their final values.

    :param dict config: Dict containing the configuration for the distribution
    :param str root_dir: Top-level directory for the distribution/project
        (the same directory where ``pyproject.toml`` is place)
    :param bool ignore_option_errors: see :func:`read_configuration`
    :param Distribution|None: Distribution object to which the configuration refers.
        If not given a dummy object will be created and discarded after the
        configuration is read. Used in the case a dynamic configuration
        (e.g. ``attr`` or ``cmdclass``).

    :rtype: dict
    '''
    return _ConfigExpander(config, root_dir, ignore_option_errors, dist).expand()


class _ConfigExpander:
    
    def __init__(self = None, config = None, root_dir = None, ignore_option_errors = (None, False, None), dist = ('config', dict, 'root_dir', Optional[_Path], 'ignore_option_errors', bool, 'dist', Optional['Distribution'])):
        self.config = config
        if not root_dir:
            pass
        self.root_dir = os.getcwd()
        self.project_cfg = config.get('project', { })
        self.dynamic = self.project_cfg.get('dynamic', [])
        self.setuptools_cfg = config.get('tool', { }).get('setuptools', { })
        self.dynamic_cfg = self.setuptools_cfg.get('dynamic', { })
        self.ignore_option_errors = ignore_option_errors
        self._dist = dist

    
    def _ensure_dist(self = None):
        Distribution = Distribution
        import setuptools.dist
        attrs = {
            'src_root': self.root_dir,
            'name': self.project_cfg.get('name', None) }
        if not self._dist:
            pass
        return Distribution(attrs)

    
    def _process_field(self = None, container = None, field = None, fn = ('container', dict, 'field', str, 'fn', Callable)):
        pass
    # WARNING: Decompyle incomplete

    
    def _canonic_package_data(self, field = ('package-data',)):
        package_data = self.setuptools_cfg.get(field, { })
        return _expand.canonic_package_data(package_data)

    
    def expand(self):
        self._expand_packages()
        self._canonic_package_data()
        self._canonic_package_data('exclude-package-data')
        dist = self._ensure_dist()
        ctx = _EnsurePackagesDiscovered(dist, self.project_cfg, self.setuptools_cfg)
    # WARNING: Decompyle incomplete

    
    def _expand_packages(self):
        packages = self.setuptools_cfg.get('packages')
        if packages is None or isinstance(packages, (list, tuple)):
            return None
        find = None.get('find')
    # WARNING: Decompyle incomplete

    
    def _expand_data_files(self):
        data_files = partial(_expand.canonic_data_files, self.root_dir, **('root_dir',))
        self._process_field(self.setuptools_cfg, 'data-files', data_files)

    
    def _expand_cmdclass(self = None, package_dir = None):
        root_dir = self.root_dir
        cmdclass = partial(_expand.cmdclass, package_dir, root_dir, **('package_dir', 'root_dir'))
        self._process_field(self.setuptools_cfg, 'cmdclass', cmdclass)

    
    def _expand_all_dynamic(self = None, dist = None, package_dir = None):
        special = ('version', 'readme', 'entry-points', 'scripts', 'gui-scripts', 'classifiers', 'dependencies', 'optional-dependencies')
        obtained_dynamic = (lambda .0 = None: pass# WARNING: Decompyle incomplete
)(self.dynamic)
        if not self._obtain_entry_points(dist, package_dir):
            pass
        obtained_dynamic.update({ }, self._obtain_version(dist, package_dir), self._obtain_readme(dist), self._obtain_classifiers(dist), self._obtain_dependencies(dist), self._obtain_optional_dependencies(dist), **('version', 'readme', 'classifiers', 'dependencies', 'optional_dependencies'))
        updates = (lambda .0: pass# WARNING: Decompyle incomplete
)(obtained_dynamic.items())
        self.project_cfg.update(updates)

    
    def _ensure_previously_set(self = None, dist = None, field = None):
        previous = _PREVIOUSLY_DEFINED[field](dist)
        if not previous is None or self.ignore_option_errors:
            msg = f'''No configuration found for dynamic {field!r}.\nSome dynamic fields need to be specified via `tool.setuptools.dynamic`\nothers must be specified via the equivalent attribute in `setup.py`.'''
            raise OptionError(msg)
        return None

    
    def _expand_directive(self = None, specifier = None, directive = None, package_dir = ('specifier', str, 'package_dir', Mapping[(str, str)])):
        pass
    # WARNING: Decompyle incomplete

    
    def _obtain(self = None, dist = None, field = None, package_dir = ('dist', 'Distribution', 'field', str, 'package_dir', Mapping[(str, str)])):
        if field in self.dynamic_cfg:
            return self._expand_directive(f'''tool.setuptools.dynamic.{field}''', self.dynamic_cfg[field], package_dir)
        None._ensure_previously_set(dist, field)

    
    def _obtain_version(self = None, dist = None, package_dir = None):
        if 'version' in self.dynamic and 'version' in self.dynamic_cfg:
            return _expand.version(self._obtain(dist, 'version', package_dir))

    
    def _obtain_readme(self = None, dist = None):
        if 'readme' not in self.dynamic:
            return None
        dynamic_cfg = None.dynamic_cfg
        if 'readme' in dynamic_cfg:
            return {
                'text': self._obtain(dist, 'readme', { }),
                'content-type': dynamic_cfg['readme'].get('content-type', 'text/x-rst') }
        None._ensure_previously_set(dist, 'readme')

    
    def _obtain_entry_points(self = None, dist = None, package_dir = None):
        fields = ('entry-points', 'scripts', 'gui-scripts')
        if not None((lambda .0 = None: for field in .0:
field in self.dynamic)(fields)):
            return None
        text = None._obtain(dist, 'entry-points', package_dir)
        if text is None:
            return None
        groups = None.entry_points(text)
        expanded = {
            'entry-points': groups }
        
        def _set_scripts(field = None, group = None):
            if group in groups:
                value = groups.pop(group)
                if field not in self.dynamic:
                    msg = _WouldIgnoreField.message(field, value)
                    warnings.warn(msg, _WouldIgnoreField)
                expanded[field] = value
                return None

        _set_scripts('scripts', 'console_scripts')
        _set_scripts('gui-scripts', 'gui_scripts')
        return expanded

    
    def _obtain_classifiers(self = None, dist = None):
        if 'classifiers' in self.dynamic:
            value = self._obtain(dist, 'classifiers', { })
            if value:
                return value.splitlines()
            return None

    
    def _obtain_dependencies(self = None, dist = None):
        if 'dependencies' in self.dynamic:
            value = self._obtain(dist, 'dependencies', { })
            if value:
                return _parse_requirements_list(value)
            return None

    
    def _obtain_optional_dependencies(self = None, dist = None):
        if 'optional-dependencies' not in self.dynamic:
            return None
    # WARNING: Decompyle incomplete



def _parse_requirements_list(value):
    return (lambda .0: [ line for line in .0 if line.strip().startswith('#') ])(value.splitlines())


def _ignore_errors(ignore_option_errors = None):
    if not ignore_option_errors:
        yield None
        return None
    yield None
    :
        if not ignore_option_errors:
            yield None
            return None
        yield None
        :
            if not ignore_option_errors:
                yield None
                return None
            yield None
            :
                if not ignore_option_errors:
                    yield None
                    return None
                yield None
                :
                    if not ignore_option_errors:
                        yield None
                        return None
                    yield None
                    :
                        if not ignore_option_errors:
                            yield None
                            return None
                        yield None
                        :
                            if not ignore_option_errors:
                                yield None
                                return None
                            yield None
                            :
                                if not ignore_option_errors:
                                    yield None
                                    return None
                                yield None
                                :
                                    if not ignore_option_errors:
                                        yield None
                                        return None
                                    yield None
                                    :
                                        if not ignore_option_errors:
                                            yield None
                                            return None
                                        yield None
                                        :
                                            if not ignore_option_errors:
                                                yield None
                                                return None
                                            yield None
                                            :
                                                if not ignore_option_errors:
                                                    yield None
                                                    return None
                                                yield None
                                                :
                                                    if not ignore_option_errors:
                                                        yield None
                                                        return None
                                                    yield None
                                                    :
                                                        if not ignore_option_errors:
                                                            yield None
                                                            return None
                                                        yield None
                                                        :
                                                            if not ignore_option_errors:
                                                                yield None
                                                                return None
                                                            yield None
                                                            :
                                                                if not ignore_option_errors:
                                                                    yield None
                                                                    return None
                                                                yield None
                                                                :
                                                                    if not ignore_option_errors:
                                                                        yield None
                                                                        return None
                                                                    yield None
                                                                    :
                                                                        if not ignore_option_errors:
                                                                            yield None
                                                                            return None
                                                                        yield None
                                                                        :
                                                                            if not ignore_option_errors:
                                                                                yield None
                                                                                return None
                                                                            yield None
                                                                            :
                                                                                if not ignore_option_errors:
                                                                                    yield None
                                                                                    return None
                                                                                yield None
                                                                                :
                                                                                    if not ignore_option_errors:
                                                                                        yield None
                                                                                        return None
                                                                                    yield None
                                                                                    :
                                                                                        if not ignore_option_errors:
                                                                                            yield None
                                                                                            return None
                                                                                        yield None
                                                                                        :
                                                                                            if not ignore_option_errors:
                                                                                                yield None
                                                                                                return None
                                                                                            yield None
                                                                                            :
                                                                                                if not ignore_option_errors:
                                                                                                    yield None
                                                                                                    return None
                                                                                                yield None
                                                                                                :
                                                                                                    if not ignore_option_errors:
                                                                                                        yield None
                                                                                                        return None
                                                                                                    yield None
                                                                                                    :
                                                                                                        if not ignore_option_errors:
                                                                                                            yield None
                                                                                                            return None
                                                                                                        yield None
                                                                                                        :
                                                                                                            if not ignore_option_errors:
                                                                                                                yield None
                                                                                                                return None
                                                                                                            yield None
                                                                                                            :
                                                                                                                if not ignore_option_errors:
                                                                                                                    yield None
                                                                                                                    return None
                                                                                                                yield None
                                                                                                                :
                                                                                                                    if not ignore_option_errors:
                                                                                                                        yield None
                                                                                                                        return None
                                                                                                                    yield None
                                                                                                                    :
                                                                                                                        if not ignore_option_errors:
                                                                                                                            yield None
                                                                                                                            return None
                                                                                                                        yield None
                                                                                                                        :
                                                                                                                            if not ignore_option_errors:
                                                                                                                                yield None
                                                                                                                                return None
                                                                                                                            yield None
                                                                                                                            :
                                                                                                                                if not ignore_option_errors:
                                                                                                                                    yield None
                                                                                                                                    return None
                                                                                                                                yield None
                                                                                                                                :
                                                                                                                                    if not ignore_option_errors:
                                                                                                                                        yield None
                                                                                                                                        return None
                                                                                                                                    yield None
                                                                                                                                    :
                                                                                                                                        if not ignore_option_errors:
                                                                                                                                            yield None
                                                                                                                                            return None
                                                                                                                                        yield None
                                                                                                                                        :
                                                                                                                                            if not ignore_option_errors:
                                                                                                                                                yield None
                                                                                                                                                return None
                                                                                                                                            yield None
                                                                                                                                            :
                                                                                                                                                if not ignore_option_errors:
                                                                                                                                                    yield None
                                                                                                                                                    return None
                                                                                                                                                yield None
                                                                                                                                                :
                                                                                                                                                    if not ignore_option_errors:
                                                                                                                                                        yield None
                                                                                                                                                        return None
                                                                                                                                                    yield None
                                                                                                                                                    :
                                                                                                                                                        if not ignore_option_errors:
                                                                                                                                                            yield None
                                                                                                                                                            return None
                                                                                                                                                        yield None
                                                                                                                                                        :
                                                                                                                                                            if not ignore_option_errors:
                                                                                                                                                                yield None
                                                                                                                                                                return None
                                                                                                                                                            yield None
                                                                                                                                                            :
                                                                                                                                                                if not ignore_option_errors:
                                                                                                                                                                    yield None
                                                                                                                                                                    return None
                                                                                                                                                                yield None
                                                                                                                                                                :
                                                                                                                                                                    if not ignore_option_errors:
                                                                                                                                                                        yield None
                                                                                                                                                                        return None
                                                                                                                                                                    yield None
                                                                                                                                                                    :
                                                                                                                                                                        if not ignore_option_errors:
                                                                                                                                                                            yield None
                                                                                                                                                                            return None
                                                                                                                                                                        yield None
                                                                                                                                                                        :
                                                                                                                                                                            if not ignore_option_errors:
                                                                                                                                                                                yield None
                                                                                                                                                                                return None
                                                                                                                                                                            yield None
                                                                                                                                                                            :
                                                                                                                                                                                if not ignore_option_errors:
                                                                                                                                                                                    yield None
                                                                                                                                                                                    return None
                                                                                                                                                                                yield None
                                                                                                                                                                                :
                                                                                                                                                                                    if not ignore_option_errors:
                                                                                                                                                                                        yield None
                                                                                                                                                                                        return None
                                                                                                                                                                                    yield None
                                                                                                                                                                                    :
                                                                                                                                                                                        if not ignore_option_errors:
                                                                                                                                                                                            yield None
                                                                                                                                                                                            return None
                                                                                                                                                                                        yield None
                                                                                                                                                                                        :
                                                                                                                                                                                            if not ignore_option_errors:
                                                                                                                                                                                                yield None
                                                                                                                                                                                                return None
                                                                                                                                                                                            yield None
                                                                                                                                                                                            :
                                                                                                                                                                                                if not ignore_option_errors:
                                                                                                                                                                                                    yield None
                                                                                                                                                                                                    return None
                                                                                                                                                                                                yield None
                                                                                                                                                                                                :
                                                                                                                                                                                                    if not ignore_option_errors:
                                                                                                                                                                                                        yield None
                                                                                                                                                                                                        return None
                                                                                                                                                                                                    yield None
                                                                                                                                                                                                    :
                                                                                                                                                                                                        if not ignore_option_errors:
                                                                                                                                                                                                            yield None
                                                                                                                                                                                                            return None
                                                                                                                                                                                                        yield None
                                                                                                                                                                                                        :
                                                                                                                                                                                                            if not ignore_option_errors:
                                                                                                                                                                                                                yield None
                                                                                                                                                                                                                return None
                                                                                                                                                                                                            yield None
                                                                                                                                                                                                            :
                                                                                                                                                                                                                if not ignore_option_errors:
                                                                                                                                                                                                                    yield None
                                                                                                                                                                                                                    return None
                                                                                                                                                                                                                yield None
                                                                                                                                                                                                                :
                                                                                                                                                                                                                    if not ignore_option_errors:
                                                                                                                                                                                                                        yield None
                                                                                                                                                                                                                        return None
                                                                                                                                                                                                                    yield None
                                                                                                                                                                                                                    :
                                                                                                                                                                                                                        if not ignore_option_errors:
                                                                                                                                                                                                                            yield None
                                                                                                                                                                                                                            return None
                                                                                                                                                                                                                        yield None
                                                                                                                                                                                                                        :
                                                                                                                                                                                                                            if not ignore_option_errors:
                                                                                                                                                                                                                                yield None
                                                                                                                                                                                                                                return None
                                                                                                                                                                                                                            yield None
                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                if not ignore_option_errors:
                                                                                                                                                                                                                                    yield None
                                                                                                                                                                                                                                    return None
                                                                                                                                                                                                                                yield None
                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                    if not ignore_option_errors:
                                                                                                                                                                                                                                        yield None
                                                                                                                                                                                                                                        return None
                                                                                                                                                                                                                                    yield None
                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                        if not ignore_option_errors:
                                                                                                                                                                                                                                            yield None
                                                                                                                                                                                                                                            return None
                                                                                                                                                                                                                                        yield None
                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                            if not ignore_option_errors:
                                                                                                                                                                                                                                                yield None
                                                                                                                                                                                                                                                return None
                                                                                                                                                                                                                                            yield None
                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                if not ignore_option_errors:
                                                                                                                                                                                                                                                    yield None
                                                                                                                                                                                                                                                    return None
                                                                                                                                                                                                                                                yield None
                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                    if not ignore_option_errors:
                                                                                                                                                                                                                                                        yield None
                                                                                                                                                                                                                                                        return None
                                                                                                                                                                                                                                                    yield None
                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                        if not ignore_option_errors:
                                                                                                                                                                                                                                                            yield None
                                                                                                                                                                                                                                                            return None
                                                                                                                                                                                                                                                        yield None
                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                            if not ignore_option_errors:
                                                                                                                                                                                                                                                                yield None
                                                                                                                                                                                                                                                                return None
                                                                                                                                                                                                                                                            yield None
                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                if not ignore_option_errors:
                                                                                                                                                                                                                                                                    yield None
                                                                                                                                                                                                                                                                    return None
                                                                                                                                                                                                                                                                yield None
                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                    if not ignore_option_errors:
                                                                                                                                                                                                                                                                        yield None
                                                                                                                                                                                                                                                                        return None
                                                                                                                                                                                                                                                                    yield None
                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                        if not ignore_option_errors:
                                                                                                                                                                                                                                                                            yield None
                                                                                                                                                                                                                                                                            return None
                                                                                                                                                                                                                                                                        yield None
                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                            if not ignore_option_errors:
                                                                                                                                                                                                                                                                                yield None
                                                                                                                                                                                                                                                                                return None
                                                                                                                                                                                                                                                                            yield None
                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                if not ignore_option_errors:
                                                                                                                                                                                                                                                                                    yield None
                                                                                                                                                                                                                                                                                    return None
                                                                                                                                                                                                                                                                                yield None
                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                    if not ignore_option_errors:
                                                                                                                                                                                                                                                                                        yield None
                                                                                                                                                                                                                                                                                        return None
                                                                                                                                                                                                                                                                                    yield None
                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                        if not ignore_option_errors:
                                                                                                                                                                                                                                                                                            yield None
                                                                                                                                                                                                                                                                                            return None
                                                                                                                                                                                                                                                                                        yield None
                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                            if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                yield None
                                                                                                                                                                                                                                                                                                return None
                                                                                                                                                                                                                                                                                            yield None
                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                    yield None
                                                                                                                                                                                                                                                                                                    return None
                                                                                                                                                                                                                                                                                                yield None
                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                    if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                        yield None
                                                                                                                                                                                                                                                                                                        return None
                                                                                                                                                                                                                                                                                                    yield None
                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                        if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                            yield None
                                                                                                                                                                                                                                                                                                            return None
                                                                                                                                                                                                                                                                                                        yield None
                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                            if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                yield None
                                                                                                                                                                                                                                                                                                                return None
                                                                                                                                                                                                                                                                                                            yield None
                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                    yield None
                                                                                                                                                                                                                                                                                                                    return None
                                                                                                                                                                                                                                                                                                                yield None
                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                    if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                        yield None
                                                                                                                                                                                                                                                                                                                        return None
                                                                                                                                                                                                                                                                                                                    yield None
                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                        if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                            yield None
                                                                                                                                                                                                                                                                                                                            return None
                                                                                                                                                                                                                                                                                                                        yield None
                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                            if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                                yield None
                                                                                                                                                                                                                                                                                                                                return None
                                                                                                                                                                                                                                                                                                                            yield None
                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                                    yield None
                                                                                                                                                                                                                                                                                                                                    return None
                                                                                                                                                                                                                                                                                                                                yield None
                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                    if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                                        yield None
                                                                                                                                                                                                                                                                                                                                        return None
                                                                                                                                                                                                                                                                                                                                    yield None
                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                        if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                                            yield None
                                                                                                                                                                                                                                                                                                                                            return None
                                                                                                                                                                                                                                                                                                                                        yield None
                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                            if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                                                yield None
                                                                                                                                                                                                                                                                                                                                                return None
                                                                                                                                                                                                                                                                                                                                            yield None
                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                                                    yield None
                                                                                                                                                                                                                                                                                                                                                    return None
                                                                                                                                                                                                                                                                                                                                                yield None
                                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                                    if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                                                        yield None
                                                                                                                                                                                                                                                                                                                                                        return None
                                                                                                                                                                                                                                                                                                                                                    yield None
                                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                                        if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                                                            yield None
                                                                                                                                                                                                                                                                                                                                                            return None
                                                                                                                                                                                                                                                                                                                                                        yield None
                                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                                            if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                                                                yield None
                                                                                                                                                                                                                                                                                                                                                                return None
                                                                                                                                                                                                                                                                                                                                                            yield None
                                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                                if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                                                                    yield None
                                                                                                                                                                                                                                                                                                                                                                    return None
                                                                                                                                                                                                                                                                                                                                                                yield None
                                                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                                                    if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                                                                        yield None
                                                                                                                                                                                                                                                                                                                                                                        return None
                                                                                                                                                                                                                                                                                                                                                                    yield None
                                                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                                                        if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                                                                            yield None
                                                                                                                                                                                                                                                                                                                                                                            return None
                                                                                                                                                                                                                                                                                                                                                                        yield None
                                                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                                                            if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                                                                                yield None
                                                                                                                                                                                                                                                                                                                                                                                return None
                                                                                                                                                                                                                                                                                                                                                                            yield None
                                                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                                                if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                                                                                    yield None
                                                                                                                                                                                                                                                                                                                                                                                    return None
                                                                                                                                                                                                                                                                                                                                                                                yield None
                                                                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                                                                    if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                                                                                        yield None
                                                                                                                                                                                                                                                                                                                                                                                        return None
                                                                                                                                                                                                                                                                                                                                                                                    yield None
                                                                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                                                                        if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                                                                                            yield None
                                                                                                                                                                                                                                                                                                                                                                                            return None
                                                                                                                                                                                                                                                                                                                                                                                        yield None
                                                                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                                                                            if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                                                                                                yield None
                                                                                                                                                                                                                                                                                                                                                                                                return None
                                                                                                                                                                                                                                                                                                                                                                                            yield None
                                                                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                                                                if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                                                                                                    yield None
                                                                                                                                                                                                                                                                                                                                                                                                    return None
                                                                                                                                                                                                                                                                                                                                                                                                yield None
                                                                                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                                                                                    if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                                                                                                        yield None
                                                                                                                                                                                                                                                                                                                                                                                                        return None
                                                                                                                                                                                                                                                                                                                                                                                                    yield None
                                                                                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                                                                                        if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                                                                                                            yield None
                                                                                                                                                                                                                                                                                                                                                                                                            return None
                                                                                                                                                                                                                                                                                                                                                                                                        yield None
                                                                                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                                                                                            if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                                                                                                                yield None
                                                                                                                                                                                                                                                                                                                                                                                                                return None
                                                                                                                                                                                                                                                                                                                                                                                                            yield None
                                                                                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                                                                                if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                                                                                                                    yield None
                                                                                                                                                                                                                                                                                                                                                                                                                    return None
                                                                                                                                                                                                                                                                                                                                                                                                                yield None
                                                                                                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                                                                                                    if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                                                                                                                        yield None
                                                                                                                                                                                                                                                                                                                                                                                                                        return None
                                                                                                                                                                                                                                                                                                                                                                                                                    yield None
                                                                                                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                                                                                                        if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                                                                                                                            yield None
                                                                                                                                                                                                                                                                                                                                                                                                                            return None
                                                                                                                                                                                                                                                                                                                                                                                                                        yield None
                                                                                                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                                                                                                            if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                                                                                                                                yield None
                                                                                                                                                                                                                                                                                                                                                                                                                                return None
                                                                                                                                                                                                                                                                                                                                                                                                                            yield None
                                                                                                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                                                                                                if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                                                                                                                                    yield None
                                                                                                                                                                                                                                                                                                                                                                                                                                    return None
                                                                                                                                                                                                                                                                                                                                                                                                                                yield None
                                                                                                                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                                                                                                                    if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                                                                                                                                        yield None
                                                                                                                                                                                                                                                                                                                                                                                                                                        return None
                                                                                                                                                                                                                                                                                                                                                                                                                                    yield None
                                                                                                                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                                                                                                                        if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                                                                                                                                            yield None
                                                                                                                                                                                                                                                                                                                                                                                                                                            return None
                                                                                                                                                                                                                                                                                                                                                                                                                                        yield None
                                                                                                                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                                                                                                                            if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                                                                                                                                                yield None
                                                                                                                                                                                                                                                                                                                                                                                                                                                return None
                                                                                                                                                                                                                                                                                                                                                                                                                                            yield None
                                                                                                                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                                                                                                                if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                                                                                                                                                    yield None
                                                                                                                                                                                                                                                                                                                                                                                                                                                    return None
                                                                                                                                                                                                                                                                                                                                                                                                                                                yield None
                                                                                                                                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                                                                                                                                    if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                                                                                                                                                        yield None
                                                                                                                                                                                                                                                                                                                                                                                                                                                        return None
                                                                                                                                                                                                                                                                                                                                                                                                                                                    yield None
                                                                                                                                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                                                                                                                                        if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                                                                                                                                                            yield None
                                                                                                                                                                                                                                                                                                                                                                                                                                                            return None
                                                                                                                                                                                                                                                                                                                                                                                                                                                        yield None
                                                                                                                                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                                                                                                                                            if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                yield None
                                                                                                                                                                                                                                                                                                                                                                                                                                                                return None
                                                                                                                                                                                                                                                                                                                                                                                                                                                            yield None
                                                                                                                                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                                                                                                                                if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                    yield None
                                                                                                                                                                                                                                                                                                                                                                                                                                                                    return None
                                                                                                                                                                                                                                                                                                                                                                                                                                                                yield None
                                                                                                                                                                                                                                                                                                                                                                                                                                                                :
                                                                                                                                                                                                                                                                                                                                                                                                                                                                    if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                        yield None
                                                                                                                                                                                                                                                                                                                                                                                                                                                                        return None
                                                                                                                                                                                                                                                                                                                                                                                                                                                                    yield None
                                                                                                                                                                                                                                                                                                                                                                                                                                                                    :
                                                                                                                                                                                                                                                                                                                                                                                                                                                                        if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                            yield None
                                                                                                                                                                                                                                                                                                                                                                                                                                                                            return None
                                                                                                                                                                                                                                                                                                                                                                                                                                                                        yield None
                                                                                                                                                                                                                                                                                                                                                                                                                                                                        :
                                                                                                                                                                                                                                                                                                                                                                                                                                                                            if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                yield None
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                return None
                                                                                                                                                                                                                                                                                                                                                                                                                                                                            yield None
                                                                                                                                                                                                                                                                                                                                                                                                                                                                            :
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                if not ignore_option_errors:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    yield None
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    return None
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                yield None
                                                                                                    