
VERSION = '2.15.3'
import re
from fastjsonschema_exceptions import JsonSchemaValueException
REGEX_PATTERNS = {
    '^.*$': re.compile('^.*$'),
    '.+': re.compile('.+'),
    '^.+$': re.compile('^.+$'),
    'idn-email_re_pattern': re.compile('^[^@]+@[^@]+\\.[^@]+\\Z') }
NoneType = type(None)

def validate(data, custom_formats, name_prefix = ({ }, None)):
    if not name_prefix:
        pass
    validate_https___packaging_python_org_en_latest_specifications_declaring_build_dependencies(data, custom_formats, 'data' + '')
    return data


def validate_https___packaging_python_org_en_latest_specifications_declaring_build_dependencies(data, custom_formats, name_prefix = ({ }, None)):
    pass
# WARNING: Decompyle incomplete


def validate_https___setuptools_pypa_io_en_latest_references_keywords_html(data, custom_formats, name_prefix = ({ }, None)):
    pass
# WARNING: Decompyle incomplete


def validate_https___setuptools_pypa_io_en_latest_references_keywords_html__definitions_file_directive(data, custom_formats, name_prefix = ({ }, None)):
    if not isinstance(data, dict):
        if not name_prefix:
            pass
        if not name_prefix:
            pass
        raise JsonSchemaValueException('' + 'data' + ' must be object', data, '' + 'data' + '', {
            '$id': '#/definitions/file-directive',
            'title': "'file:' directive",
            'description': 'Value is read from a file (or list of files and then concatenated)',
            'type': 'object',
            'additionalProperties': False,
            'properties': {
                'file': {
                    'oneOf': [
                        {
                            'type': 'string' },
                        {
                            'type': 'array',
                            'items': {
                                'type': 'string' } }] } },
            'required': [
                'file'] }, 'type', **('value', 'name', 'definition', 'rule'))
    data_is_dict = None(data, dict)
# WARNING: Decompyle incomplete


def validate_https___setuptools_pypa_io_en_latest_references_keywords_html__definitions_attr_directive(data, custom_formats, name_prefix = ({ }, None)):
    if not isinstance(data, dict):
        if not name_prefix:
            pass
        if not name_prefix:
            pass
        raise JsonSchemaValueException('' + 'data' + ' must be object', data, '' + 'data' + '', {
            'title': "'attr:' directive",
            '$id': '#/definitions/attr-directive',
            '$$description': [
                'Value is read from a module attribute. Supports callables and iterables;',
                'unsupported types are cast via ``str()``'],
            'type': 'object',
            'additionalProperties': False,
            'properties': {
                'attr': {
                    'type': 'string' } },
            'required': [
                'attr'] }, 'type', **('value', 'name', 'definition', 'rule'))
    data_is_dict = None(data, dict)
    if data_is_dict:
        data_len = len(data)
        if not None((lambda .0 = None: for prop in .0:
prop in data)(('attr',))):
            if not name_prefix:
                pass
            if not name_prefix:
                pass
            raise JsonSchemaValueException('' + 'data' + " must contain ['attr'] properties", data, '' + 'data' + '', {
                'title': "'attr:' directive",
                '$id': '#/definitions/attr-directive',
                '$$description': [
                    'Value is read from a module attribute. Supports callables and iterables;',
                    'unsupported types are cast via ``str()``'],
                'type': 'object',
                'additionalProperties': False,
                'properties': {
                    'attr': {
                        'type': 'string' } },
                'required': [
                    'attr'] }, 'required', **('value', 'name', 'definition', 'rule'))
        data_keys = None(data.keys())
        if 'attr' in data_keys:
            data_keys.remove('attr')
            data__attr = data['attr']
            if not isinstance(data__attr, str):
                if not name_prefix:
                    pass
                if not name_prefix:
                    pass
                raise JsonSchemaValueException('' + 'data' + '.attr must be string', data__attr, '' + 'data' + '.attr', {
                    'type': 'string' }, 'type', **('value', 'name', 'definition', 'rule'))
            if None:
                if not name_prefix:
                    pass
                if not name_prefix:
                    pass
                raise JsonSchemaValueException('' + 'data' + ' must not contain ' + str(data_keys) + ' properties', data, '' + 'data' + '', {
                    'title': "'attr:' directive",
                    '$id': '#/definitions/attr-directive',
                    '$$description': [
                        'Value is read from a module attribute. Supports callables and iterables;',
                        'unsupported types are cast via ``str()``'],
                    'type': 'object',
                    'additionalProperties': False,
                    'properties': {
                        'attr': {
                            'type': 'string' } },
                    'required': [
                        'attr'] }, 'additionalProperties', **('value', 'name', 'definition', 'rule'))
            return None


def validate_https___setuptools_pypa_io_en_latest_references_keywords_html__definitions_find_directive(data, custom_formats, name_prefix = ({ }, None)):
    if not isinstance(data, dict):
        if not name_prefix:
            pass
        if not name_prefix:
            pass
        raise JsonSchemaValueException('' + 'data' + ' must be object', data, '' + 'data' + '', {
            '$id': '#/definitions/find-directive',
            'title': "'find:' directive",
            'type': 'object',
            'additionalProperties': False,
            'properties': {
                'find': {
                    'type': 'object',
                    '$$description': [
                        'Dynamic `package discovery',
                        '<https://setuptools.pypa.io/en/latest/userguide/package_discovery.html>`_.'],
                    'additionalProperties': False,
                    'properties': {
                        'where': {
                            'description': 'Directories to be searched for packages (Unix-style relative path)',
                            'type': 'array',
                            'items': {
                                'type': 'string' } },
                        'exclude': {
                            'type': 'array',
                            '$$description': [
                                'Exclude packages that match the values listed in this field.',
                                "Can container shell-style wildcards (e.g. ``'pkg.*'``)"],
                            'items': {
                                'type': 'string' } },
                        'include': {
                            'type': 'array',
                            '$$description': [
                                'Restrict the found packages to just the ones listed in this field.',
                                "Can container shell-style wildcards (e.g. ``'pkg.*'``)"],
                            'items': {
                                'type': 'string' } },
                        'namespaces': {
                            'type': 'boolean',
                            '$$description': [
                                'When ``True``, directories without a ``__init__.py`` file will also',
                                'be scanned for :pep:`420`-style implicit namespaces'] } } } } }, 'type', **('value', 'name', 'definition', 'rule'))
    data_is_dict = None(data, dict)
# WARNING: Decompyle incomplete


def validate_https___docs_python_org_3_install(data, custom_formats, name_prefix = ({ }, None)):
    if not isinstance(data, dict):
        if not name_prefix:
            pass
        if not name_prefix:
            pass
        raise JsonSchemaValueException('' + 'data' + ' must be object', data, '' + 'data' + '', {
            '$schema': 'http://json-schema.org/draft-07/schema',
            '$id': 'https://docs.python.org/3/install/',
            'title': '``tool.distutils`` table',
            '$$description': [
                'Originally, ``distutils`` allowed developers to configure arguments for',
                '``setup.py`` scripts via `distutils configuration files',
                '<https://docs.python.org/3/install/#distutils-configuration-files>`_.',
                '``tool.distutils`` subtables could be used with the same purpose',
                '(NOT CURRENTLY IMPLEMENTED).'],
            'type': 'object',
            'properties': {
                'global': {
                    'type': 'object',
                    'description': 'Global options applied to all ``distutils`` commands' } },
            'patternProperties': {
                '.+': {
                    'type': 'object' } },
            '$comment': 'TODO: Is there a practical way of making this schema more specific?' }, 'type', **('value', 'name', 'definition', 'rule'))
    data_is_dict = None(data, dict)
# WARNING: Decompyle incomplete


def validate_https___packaging_python_org_en_latest_specifications_declaring_project_metadata(data, custom_formats, name_prefix = ({ }, None)):
    pass
# WARNING: Decompyle incomplete


def validate_https___packaging_python_org_en_latest_specifications_declaring_project_metadata___definitions_dependency(data, custom_formats, name_prefix = ({ }, None)):
    if not isinstance(data, str):
        if not name_prefix:
            pass
        if not name_prefix:
            pass
        raise JsonSchemaValueException('' + 'data' + ' must be string', data, '' + 'data' + '', {
            '$id': '#/definitions/dependency',
            'title': 'Dependency',
            'type': 'string',
            'description': 'Project dependency specification according to PEP 508',
            'format': 'pep508' }, 'type', **('value', 'name', 'definition', 'rule'))
    if not None(data, str) and custom_formats['pep508'](data):
        if not name_prefix:
            pass
        if not name_prefix:
            pass
        raise JsonSchemaValueException('' + 'data' + ' must be pep508', data, '' + 'data' + '', {
            '$id': '#/definitions/dependency',
            'title': 'Dependency',
            'type': 'string',
            'description': 'Project dependency specification according to PEP 508',
            'format': 'pep508' }, 'format', **('value', 'name', 'definition', 'rule'))


def validate_https___packaging_python_org_en_latest_specifications_declaring_project_metadata___definitions_entry_point_group(data, custom_formats, name_prefix = ({ }, None)):
    if not isinstance(data, dict):
        if not name_prefix:
            pass
        if not name_prefix:
            pass
        raise JsonSchemaValueException('' + 'data' + ' must be object', data, '' + 'data' + '', {
            '$id': '#/definitions/entry-point-group',
            'title': 'Entry-points',
            'type': 'object',
            '$$description': [
                'Entry-points are grouped together to indicate what sort of capabilities they',
                'provide.',
                'See the `packaging guides',
                '<https://packaging.python.org/specifications/entry-points/>`_',
                'and `setuptools docs',
                '<https://setuptools.pypa.io/en/latest/userguide/entry_point.html>`_',
                'for more information.'],
            'propertyNames': {
                'format': 'python-entrypoint-name' },
            'additionalProperties': False,
            'patternProperties': {
                '^.+$': {
                    'type': 'string',
                    '$$description': [
                        'Reference to a Python object. It is either in the form',
                        '``importable.module``, or ``importable.module:object.attr``.'],
                    'format': 'python-entrypoint-reference',
                    '$comment': 'https://packaging.python.org/specifications/entry-points/' } } }, 'type', **('value', 'name', 'definition', 'rule'))
    data_is_dict = None(data, dict)
# WARNING: Decompyle incomplete


def validate_https___packaging_python_org_en_latest_specifications_declaring_project_metadata___definitions_author(data, custom_formats, name_prefix = ({ }, None)):
    if not isinstance(data, dict):
        if not name_prefix:
            pass
        if not name_prefix:
            pass
        raise JsonSchemaValueException('' + 'data' + ' must be object', data, '' + 'data' + '', {
            '$id': '#/definitions/author',
            'title': 'Author or Maintainer',
            '$comment': 'https://www.python.org/dev/peps/pep-0621/#authors-maintainers',
            'type': 'object',
            'properties': {
                'name': {
                    'type': 'string',
                    '$$description': [
                        'MUST be a valid email name, i.e. whatever can be put as a name, before an',
                        'email, in :rfc:`822`.'] },
                'email': {
                    'type': 'string',
                    'format': 'idn-email',
                    'description': 'MUST be a valid email address' } } }, 'type', **('value', 'name', 'definition', 'rule'))
    data_is_dict = None(data, dict)
    if data_is_dict:
        data_keys = set(data.keys())
        if 'name' in data_keys:
            data_keys.remove('name')
            data__name = data['name']
            if not isinstance(data__name, str):
                if not name_prefix:
                    pass
                if not name_prefix:
                    pass
                raise JsonSchemaValueException('' + 'data' + '.name must be string', data__name, '' + 'data' + '.name', {
                    'type': 'string',
                    '$$description': [
                        'MUST be a valid email name, i.e. whatever can be put as a name, before an',
                        'email, in :rfc:`822`.'] }, 'type', **('value', 'name', 'definition', 'rule'))
            if None in data_keys:
                data_keys.remove('email')
                data__email = data['email']
                if not isinstance(data__email, str):
                    if not name_prefix:
                        pass
                    if not name_prefix:
                        pass
                    raise JsonSchemaValueException('' + 'data' + '.email must be string', data__email, '' + 'data' + '.email', {
                        'type': 'string',
                        'format': 'idn-email',
                        'description': 'MUST be a valid email address' }, 'type', **('value', 'name', 'definition', 'rule'))
                if not None(data__email, str) and REGEX_PATTERNS['idn-email_re_pattern'].match(data__email):
                    if not name_prefix:
                        pass
                    if not name_prefix:
                        pass
                    raise JsonSchemaValueException('' + 'data' + '.email must be idn-email', data__email, '' + 'data' + '.email', {
                        'type': 'string',
                        'format': 'idn-email',
                        'description': 'MUST be a valid email address' }, 'format', **('value', 'name', 'definition', 'rule'))
                return None

