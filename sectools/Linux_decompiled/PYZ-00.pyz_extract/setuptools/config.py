
import ast
import io
import os
import sys
import warnings
import functools
import importlib
from collections import defaultdict
from functools import partial
from functools import wraps
from glob import iglob
import contextlib
from distutils.errors import DistutilsOptionError, DistutilsFileError
from setuptools.extern.packaging.version import Version, InvalidVersion
from setuptools.extern.packaging.specifiers import SpecifierSet

class StaticModule:
    '''
    Attempt to load the module by the name
    '''
    
    def __init__(self, name):
        spec = importlib.util.find_spec(name)
        with open(spec.origin) as strm:
            src = strm.read()
            None(None, None, None)
    # WARNING: Decompyle incomplete

    
    def __getattr__(self, attr):
        pass
    # WARNING: Decompyle incomplete



def patch_path(path):
    '''
    Add path to front of sys.path for the duration of the context.
    '''
    pass
# WARNING: Decompyle incomplete

patch_path = contextlib.contextmanager(patch_path)

def read_configuration(filepath, find_others, ignore_option_errors = (False, False)):
    '''Read given configuration file and returns options from it as a dict.

    :param str|unicode filepath: Path to configuration file
        to get options from.

    :param bool find_others: Whether to search for other configuration files
        which could be on in various places.

    :param bool ignore_option_errors: Whether to silently ignore
        options, values of which could not be resolved (e.g. due to exceptions
        in directives such as file:, attr:, etc.).
        If False exceptions are propagated as expected.

    :rtype: dict
    '''
    Distribution = Distribution
    _Distribution = _Distribution
    import setuptools.dist
    filepath = os.path.abspath(filepath)
    if not os.path.isfile(filepath):
        raise DistutilsFileError('Configuration file %s does not exist.' % filepath)
    current_directory = None.getcwd()
    os.chdir(os.path.dirname(filepath))
# WARNING: Decompyle incomplete


def _get_option(target_obj, key):
    '''
    Given a target object and option key, get that option from
    the target object, either through a get_{key} method or
    from an attribute directly.
    '''
    pass
# WARNING: Decompyle incomplete


def configuration_to_dict(handlers):
    '''Returns configuration data gathered by given handlers as a dict.

    :param list[ConfigHandler] handlers: Handlers list,
        usually from parse_configuration()

    :rtype: dict
    '''
    config_dict = defaultdict(dict)
    for handler in handlers:
        for option in handler.set_options:
            value = _get_option(handler.target_obj, option)
            config_dict[handler.section_prefix][option] = value
    return config_dict


def parse_configuration(distribution, command_options, ignore_option_errors = (False,)):
    '''Performs additional parsing of configuration options
    for a distribution.

    Returns a list of used option handlers.

    :param Distribution distribution:
    :param dict command_options:
    :param bool ignore_option_errors: Whether to silently ignore
        options, values of which could not be resolved (e.g. due to exceptions
        in directives such as file:, attr:, etc.).
        If False exceptions are propagated as expected.
    :rtype: list
    '''
    options = ConfigOptionsHandler(distribution, command_options, ignore_option_errors)
    options.parse()
    meta = ConfigMetadataHandler(distribution.metadata, command_options, ignore_option_errors, distribution.package_dir)
    meta.parse()
    return (meta, options)


class ConfigHandler:
    '''Handles metadata supplied in configuration files.'''
    section_prefix = None
    aliases = { }
    
    def __init__(self, target_obj, options, ignore_option_errors = (False,)):
        sections = { }
        section_prefix = self.section_prefix
        for section_name, section_options in options.items():
            if not section_name.startswith(section_prefix):
                continue
            section_name = section_name.replace(section_prefix, '').strip('.')
            sections[section_name] = section_options
        self.ignore_option_errors = ignore_option_errors
        self.target_obj = target_obj
        self.sections = sections
        self.set_options = []

    
    def parsers(self):
        '''Metadata item name to parser function mapping.'''
        raise NotImplementedError('%s must provide .parsers property' % self.__class__.__name__)

    parsers = property(parsers)
    
    def __setitem__(self, option_name, value):
        unknown = tuple()
        target_obj = self.target_obj
        option_name = self.aliases.get(option_name, option_name)
        current_value = getattr(target_obj, option_name, unknown)
        if current_value is unknown:
            raise KeyError(option_name)
        if None:
            return None
        skip_option = None
        parser = self.parsers.get(option_name)
    # WARNING: Decompyle incomplete

    
    def _parse_list(cls, value, separator = (',',)):
        '''Represents value as a list.

        Value is split either by separator (defaults to comma) or by lines.

        :param value:
        :param separator: List items separator character.
        :rtype: list
        '''
        if isinstance(value, list):
            return value
        if None in value:
            value = value.splitlines()
        else:
            value = value.split(separator)
        return (lambda .0: [ chunk.strip() for chunk in .0 if chunk.strip() ])(value)

    _parse_list = classmethod(_parse_list)
    
    def _parse_list_glob(cls, value, separator = (',',)):
        '''Equivalent to _parse_list() but expands any glob patterns using glob().

        However, unlike with glob() calls, the results remain relative paths.

        :param value:
        :param separator: List items separator character.
        :rtype: list
        '''
        glob_characters = ('*', '?', '[', ']', '{', '}')
        values = cls._parse_list(value, separator, **('separator',))
        expanded_values = []
        for None in values:
            value = None
            if None((lambda .0 = None: for char in .0:
char in value)(glob_characters)):
                expanded_values.extend(sorted((lambda .0: for path in .0:
os.path.relpath(path, os.getcwd()))(iglob(os.path.abspath(value)))))
                continue
        return expanded_values

    _parse_list_glob = classmethod(_parse_list_glob)
    
    def _parse_dict(cls, value):
        '''Represents value as a dict.

        :param value:
        :rtype: dict
        '''
        separator = '='
        result = { }
        for line in cls._parse_list(value):
            (key, sep, val) = line.partition(separator)
            if sep != separator:
                raise DistutilsOptionError('Unable to parse option value to dict: %s' % value)
            result[key.strip()] = None.strip()
        return result

    _parse_dict = classmethod(_parse_dict)
    
    def _parse_bool(cls, value):
        '''Represents value as boolean.

        :param value:
        :rtype: bool
        '''
        value = value.lower()
        return value in ('1', 'true', 'yes')

    _parse_bool = classmethod(_parse_bool)
    
    def _exclude_files_parser(cls, key):
        '''Returns a parser function to make sure field inputs
        are not files.

        Parses a value after getting the key so error messages are
        more informative.

        :param key:
        :rtype: callable
        '''
        
        def parser(value = None):
            exclude_directive = 'file:'
            if value.startswith(exclude_directive):
                raise ValueError('Only strings are accepted for the {0} field, files are not accepted'.format(key))

        return parser

    _exclude_files_parser = classmethod(_exclude_files_parser)
    
    def _parse_file(cls, value):
        """Represents value as a string, allowing including text
        from nearest files using `file:` directive.

        Directive is sandboxed and won't reach anything outside
        directory with setup.py.

        Examples:
            file: README.rst, CHANGELOG.md, src/file.txt

        :param str value:
        :rtype: str
        """
        include_directive = 'file:'
        if not isinstance(value, str):
            return value
        if not None.startswith(include_directive):
            return value
        spec = None[len(include_directive):]
        filepaths = (lambda .0: for path in .0:
os.path.abspath(path.strip()))(spec.split(','))
        return None((lambda .0 = None: for path in .0:
if not cls._assert_local(path):
passif os.path.isfile(path):
cls._read_file(path)continueNone)(filepaths))

    _parse_file = classmethod(_parse_file)
    
    def _assert_local(filepath):
        if not filepath.startswith(os.getcwd()):
            raise DistutilsOptionError('`file:` directive can not access %s' % filepath)

    _assert_local = staticmethod(_assert_local)
    
    def _read_file(filepath):
        pass
    # WARNING: Decompyle incomplete

    _read_file = staticmethod(_read_file)
    
    def _parse_attr(cls, value, package_dir = (None,)):
        '''Represents value as a module attribute.

        Examples:
            attr: package.attr
            attr: package.module.attr

        :param str value:
        :rtype: str
        '''
        attr_directive = 'attr:'
        if not value.startswith(attr_directive):
            return value
        attrs_path = None.replace(attr_directive, '').strip().split('.')
        attr_name = attrs_path.pop()
        module_name = '.'.join(attrs_path)
        if not module_name:
            pass
        module_name = '__init__'
        parent_path = os.getcwd()
        if package_dir:
            if attrs_path[0] in package_dir:
                custom_path = package_dir[attrs_path[0]]
                parts = custom_path.rsplit('/', 1)
                if len(parts) > 1:
                    parent_path = os.path.join(os.getcwd(), parts[0])
                    module_name = parts[1]
                else:
                    module_name = custom_path
            elif '' in package_dir:
                parent_path = os.path.join(os.getcwd(), package_dir[''])
    # WARNING: Decompyle incomplete

    _parse_attr = classmethod(_parse_attr)
    
    def _get_parser_compound(cls, *parse_methods):
        '''Returns parser function to represents value as a list.

        Parses a value applying given methods one after another.

        :param parse_methods:
        :rtype: callable
        '''
        
        def parse(value = None):
            parsed = value
            for method in parse_methods:
                parsed = method(parsed)
            return parsed

        return parse

    _get_parser_compound = classmethod(_get_parser_compound)
    
    def _parse_section_to_dict(cls, section_options, values_parser = (None,)):
        '''Parses section options into a dictionary.

        Optionally applies a given parser to values.

        :param dict section_options:
        :param callable values_parser:
        :rtype: dict
        '''
        value = { }
        if not values_parser:
            pass
        
        values_parser = lambda val: val
        for _, val in section_options.items():
            value[key] = values_parser(val)
        return value

    _parse_section_to_dict = classmethod(_parse_section_to_dict)
    
    def parse_section(self, section_options):
        '''Parses configuration file section.

        :param dict section_options:
        '''
        pass
    # WARNING: Decompyle incomplete

    
    def parse(self):
        '''Parses configuration file items from one
        or more related sections.

        '''
        for section_name, section_options in self.sections.items():
            method_postfix = ''
            if section_name:
                method_postfix = '_%s' % section_name
            section_parser_method = getattr(self, ('parse_section%s' % method_postfix).replace('.', '__'), None)
            if section_parser_method is None:
                raise DistutilsOptionError('Unsupported distribution option section: [%s.%s]' % (self.section_prefix, section_name))
            None(section_options)

    
    def _deprecated_config_handler(self, func, msg, warning_class):
        '''this function will wrap around parameters that are deprecated

        :param msg: deprecation message
        :param warning_class: class of warning exception to be raised
        :param func: function to be wrapped around
        '''
        
        def config_handler(*args, **kwargs):
            warnings.warn(msg, warning_class)
        # WARNING: Decompyle incomplete

        config_handler = None(config_handler)
        return config_handler



class ConfigMetadataHandler(ConfigHandler):
    section_prefix = 'metadata'
    aliases = {
        'home_page': 'url',
        'summary': 'description',
        'classifier': 'classifiers',
        'platform': 'platforms' }
    strict_mode = False
    
    def __init__(self = None, target_obj = None, options = None, ignore_option_errors = None, package_dir = None):
        super(ConfigMetadataHandler, self).__init__(target_obj, options, ignore_option_errors)
        self.package_dir = package_dir

    
    def parsers(self):
        '''Metadata item name to parser function mapping.'''
        parse_list = self._parse_list
        parse_file = self._parse_file
        parse_dict = self._parse_dict
        exclude_files_parser = self._exclude_files_parser
        return {
            'platforms': parse_list,
            'keywords': parse_list,
            'provides': parse_list,
            'requires': self._deprecated_config_handler(parse_list, 'The requires parameter is deprecated, please use install_requires for runtime dependencies.', DeprecationWarning),
            'obsoletes': parse_list,
            'classifiers': self._get_parser_compound(parse_file, parse_list),
            'license': exclude_files_parser('license'),
            'license_file': self._deprecated_config_handler(exclude_files_parser('license_file'), 'The license_file parameter is deprecated, use license_files instead.', DeprecationWarning),
            'license_files': parse_list,
            'description': parse_file,
            'long_description': parse_file,
            'version': self._parse_version,
            'project_urls': parse_dict }

    parsers = property(parsers)
    
    def _parse_version(self, value):
        '''Parses `version` option value.

        :param value:
        :rtype: str

        '''
        version = self._parse_file(value)
    # WARNING: Decompyle incomplete

    __classcell__ = None


class ConfigOptionsHandler(ConfigHandler):
    section_prefix = 'options'
    
    def parsers(self):
        '''Metadata item name to parser function mapping.'''
        parse_list = self._parse_list
        parse_list_semicolon = partial(self._parse_list, ';', **('separator',))
        parse_bool = self._parse_bool
        parse_dict = self._parse_dict
        parse_cmdclass = self._parse_cmdclass
        return {
            'zip_safe': parse_bool,
            'include_package_data': parse_bool,
            'package_dir': parse_dict,
            'scripts': parse_list,
            'eager_resources': parse_list,
            'dependency_links': parse_list,
            'namespace_packages': parse_list,
            'install_requires': parse_list_semicolon,
            'setup_requires': parse_list_semicolon,
            'tests_require': parse_list_semicolon,
            'packages': self._parse_packages,
            'entry_points': self._parse_file,
            'py_modules': parse_list,
            'python_requires': SpecifierSet,
            'cmdclass': parse_cmdclass }

    parsers = property(parsers)
    
    def _parse_cmdclass(self, value):
        
        def resolve_class(qualified_class_name):
            idx = qualified_class_name.rfind('.')
            class_name = qualified_class_name[idx + 1:]
            pkg_name = qualified_class_name[:idx]
            module = __import__(pkg_name)
            return getattr(module, class_name)

        return (lambda .0 = None: pass# WARNING: Decompyle incomplete
)(self._parse_dict(value).items())

    
    def _parse_packages(self, value):
        '''Parses `packages` option value.

        :param value:
        :rtype: list
        '''
        find_directives = [
            'find:',
            'find_namespace:']
        trimmed_value = value.strip()
        if trimmed_value not in find_directives:
            return self._parse_list(value)
        findns = None == find_directives[1]
        find_kwargs = self.parse_section_packages__find(self.sections.get('packages.find', { }))
        if findns:
            find_packages = find_namespace_packages
            import setuptools
        else:
            find_packages = find_packages
            import setuptools
    # WARNING: Decompyle incomplete

    
    def parse_section_packages__find(self, section_options):
        '''Parses `packages.find` configuration file section.

        To be used in conjunction with _parse_packages().

        :param dict section_options:
        '''
        section_data = self._parse_section_to_dict(section_options, self._parse_list)
        valid_keys = [
            'where',
            'include',
            'exclude']
        find_kwargs = None((lambda .0 = None: [ (k, v) for k, v in .0 if v ])(section_data.items()))
        where = find_kwargs.get('where')
        if where is not None:
            find_kwargs['where'] = where[0]
        return find_kwargs

    
    def parse_section_entry_points(self, section_options):
        '''Parses `entry_points` configuration file section.

        :param dict section_options:
        '''
        parsed = self._parse_section_to_dict(section_options, self._parse_list)
        self['entry_points'] = parsed

    
    def _parse_package_data(self, section_options):
        parsed = self._parse_section_to_dict(section_options, self._parse_list)
        root = parsed.get('*')
        if root:
            parsed[''] = root
            del parsed['*']
        return parsed

    
    def parse_section_package_data(self, section_options):
        '''Parses `package_data` configuration file section.

        :param dict section_options:
        '''
        self['package_data'] = self._parse_package_data(section_options)

    
    def parse_section_exclude_package_data(self, section_options):
        '''Parses `exclude_package_data` configuration file section.

        :param dict section_options:
        '''
        self['exclude_package_data'] = self._parse_package_data(section_options)

    
    def parse_section_extras_require(self, section_options):
        '''Parses `extras_require` configuration file section.

        :param dict section_options:
        '''
        parse_list = partial(self._parse_list, ';', **('separator',))
        self['extras_require'] = self._parse_section_to_dict(section_options, parse_list)

    
    def parse_section_data_files(self, section_options):
        '''Parses `data_files` configuration file section.

        :param dict section_options:
        '''
        parsed = self._parse_section_to_dict(section_options, self._parse_list_glob)
        self['data_files'] = (lambda .0: [ (k, v) for k, v in .0 ])(parsed.items())


