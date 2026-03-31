
import io
import json
import logging
import os
import re
from contextlib import contextmanager
from textwrap import indent, wrap
from typing import Any, Dict, Iterator, List, Optional, Sequence, Union, cast
from fastjsonschema_exceptions import JsonSchemaValueException
_logger = logging.getLogger(__name__)
_MESSAGE_REPLACEMENTS = {
    'must be named by propertyName definition': 'keys must be named by',
    'one of contains definition': 'at least one item that matches',
    ' same as const definition:': '',
    'only specified items': 'only items matching the definition' }
_SKIP_DETAILS = ('must not be empty', 'is always invalid', 'must not be there')
_NEED_DETAILS = {
    'not',
    'items',
    'anyOf',
    'contains',
    'oneOf',
    'propertyNames'}
_CAMEL_CASE_SPLITTER = re.compile('\\W+|([A-Z][^A-Z\\W]*)')
_IDENTIFIER = re.compile('^[\\w_]+$', re.I)
_TOML_JARGON = {
    'object': 'table',
    'property': 'key',
    'properties': 'keys',
    'property names': 'keys' }

class ValidationError(JsonSchemaValueException):
    '''Report violations of a given JSON schema.

    This class extends :exc:`~fastjsonschema.JsonSchemaValueException`
    by adding the following properties:

    - ``summary``: an improved version of the ``JsonSchemaValueException`` error message
      with only the necessary information)

    - ``details``: more contextual information about the error like the failing schema
      itself and the value that violates the schema.

    Depending on the level of the verbosity of the ``logging`` configuration
    the exception message will be only ``summary`` (default) or a combination of
    ``summary`` and ``details`` (when the logging level is set to :obj:`logging.DEBUG`).
    '''
    summary = ''
    details = ''
    _original_message = ''
    
    def _from_jsonschema(cls = None, ex = None):
        formatter = _ErrorFormatting(ex)
        obj = cls(str(formatter), ex.value, formatter.name, ex.definition, ex.rule)
        debug_code = os.getenv('JSONSCHEMA_DEBUG_CODE_GENERATION', 'false').lower()
        if debug_code != 'false':
            obj.__cause__ = ex.__cause__
            obj.__traceback__ = ex.__traceback__
        obj._original_message = ex.message
        obj.summary = formatter.summary
        obj.details = formatter.details
        return obj

    _from_jsonschema = None(_from_jsonschema)


def detailed_errors():
    pass
# WARNING: Decompyle incomplete

detailed_errors = contextmanager(detailed_errors)

class _ErrorFormatting:
    
    def __init__(self = None, ex = None):
        self.ex = ex
        self.name = f'''`{self._simplify_name(ex.name)}`'''
        self._original_message = self.ex.message.replace(ex.name, self.name)
        self._summary = ''
        self._details = ''

    
    def __str__(self = None):
        if _logger.getEffectiveLevel() <= logging.DEBUG and self.details:
            return f'''{self.summary}\n\n{self.details}'''
        return None.summary

    
    def summary(self = None):
        if not self._summary:
            self._summary = self._expand_summary()
        return self._summary

    summary = None(summary)
    
    def details(self = None):
        if not self._details:
            self._details = self._expand_details()
        return self._details

    details = None(details)
    
    def _simplify_name(self, name):
        x = len('data.')
        if name.startswith('data.'):
            return name[x:]

    
    def _expand_summary(self):
        msg = self._original_message
        for bad, repl in _MESSAGE_REPLACEMENTS.items():
            msg = msg.replace(bad, repl)
        if None((lambda .0 = None: for substring in .0:
substring in msg)(_SKIP_DETAILS)):
            return msg
        schema = None.ex.rule_definition
        if self.ex.rule in _NEED_DETAILS and schema:
            summary = _SummaryWriter(_TOML_JARGON)
            return f'''{msg}:\n\n{indent(summary(schema), '    ')}'''

    
    def _expand_details(self = None):
        optional = []
        desc_lines = self.ex.definition.pop('$$description', [])
        if not self.ex.definition.pop('description', None):
            pass
        desc = ' '.join(desc_lines)
        if desc:
            description = '\n'.join(wrap(desc, 80, '    ', '    ', False, **('width', 'initial_indent', 'subsequent_indent', 'break_long_words')))
            optional.append(f'''DESCRIPTION:\n{description}''')
        schema = json.dumps(self.ex.definition, 4, **('indent',))
        value = json.dumps(self.ex.value, 4, **('indent',))
        defaults = [
            f'''GIVEN VALUE:\n{indent(value, '    ')}''',
            f'''OFFENDING RULE: {self.ex.rule!r}''',
            f'''DEFINITION:\n{indent(schema, '    ')}''']
        return '\n\n'.join(optional + defaults)



class _SummaryWriter:
    _IGNORE = {
        'title',
        'default',
        'examples',
        'description'}
    
    def __init__(self = None, jargon = None):
        if not jargon:
            pass
        self.jargon = { }
        self._terms = {
            'anyOf': 'at least one of the following',
            'oneOf': 'exactly one of the following',
            'allOf': 'all of the following',
            'not': '(*NOT* the following)',
            'prefixItems': f'''{self._jargon('items')} (in order)''',
            'items': 'items',
            'contains': 'contains at least one of',
            'propertyNames': f'''non-predefined acceptable {self._jargon('property names')}''',
            'patternProperties': f'''{self._jargon('properties')} named via pattern''',
            'const': 'predefined value',
            'enum': 'one of' }
        self._guess_inline_defs = [
            'enum',
            'const',
            'maxLength',
            'minLength',
            'pattern',
            'format',
            'minimum',
            'maximum',
            'exclusiveMinimum',
            'exclusiveMaximum',
            'multipleOf']

    
    def _jargon(self = None, term = None):
        if isinstance(term, list):
            return (lambda .0 = None: [ self.jargon.get(t, t) for t in .0 ])(term)
        return None.jargon.get(term, term)

    
    def __call__(self = None, schema = None, prefix = None, *, _path):
        if isinstance(schema, list):
            return self._handle_list(schema, prefix, _path)
        filtered = None._filter_unecessary(schema, _path)
        simple = self._handle_simple_dict(filtered, _path)
        if simple:
            return f'''{prefix}{simple}'''
        child_prefix = None._child_prefix(prefix, '  ')
        item_prefix = self._child_prefix(prefix, '- ')
        indent = len(prefix) * ' '
    # WARNING: Decompyle incomplete

    
    def _is_unecessary(self = None, path = None):
        if not self._is_property(path) or path:
            return False
        key = None[-1]
        if not None((lambda .0 = None: for k in .0:
key.startswith(k))('$_')):
            pass
        return key in self._IGNORE

    
    def _filter_unecessary(self = None, schema = None, path = None):
        return (lambda .0 = None: pass# WARNING: Decompyle incomplete
)(schema.items())

    
    def _handle_simple_dict(self = None, value = None, path = None):
        inline = None((lambda .0 = None: for p in .0:
p in value)(self._guess_inline_defs))
        simple = not any((lambda .0: for v in .0:
isinstance(v, (list, dict)))(value.values()))
        if inline or simple:
            return f'''{{{', '.join(self._inline_attrs(value, path))}}}\n'''

    
    def _handle_list(self = None, schemas = None, prefix = None, path = ('', ())):
        if self._is_unecessary(path):
            return ''
        repr_ = None(schemas)
        if all((lambda .0: for e in .0:
not isinstance(e, (dict, list)))(schemas)) and len(repr_) < 60:
            return f'''{repr_}\n'''
        item_prefix = None._child_prefix(prefix, '- ')
        return None((lambda .0 = None: for i, v in .0:
self(v, item_prefix, item_prefix[f'''[{i}]'''], **('_path',)))(enumerate(schemas)))

    
    def _is_property(self = None, path = None):
        '''Check if the given path can correspond to an arbitrarily named property'''
        counter = 0
        for key in path[-2::-1]:
            if key not in frozenset({'properties', 'patternProperties'}):
                pass
            else:
                counter += 1
            return counter % 2 == 1

    
    def _label(self = None, path = None):
        pass
    # WARNING: Decompyle incomplete

    
    def _value(self = None, value = None, path = None):
        if not path[-1] == 'type' and self._is_property(path):
            type_ = self._jargon(value)
            if isinstance(value, list):
                return f'''[{', '.join(type_)}]'''
            return None(str, type_)
        return None(value)

    
    def _inline_attrs(self = None, schema = None, path = None):
        for key, value in schema.items():
            child_path = None[key]
            yield f'''{self._label(child_path)}: {self._value(value, child_path)}'''

    
    def _child_prefix(self = None, parent_prefix = None, child_prefix = None):
        return len(parent_prefix) * ' ' + child_prefix



def _separate_terms(word = None):
    '''
    >>> _separate_terms("FooBar-foo")
    [\'foo\', \'bar\', \'foo\']
    '''
    return (lambda .0: [ w.lower() for w in .0 if w ])(_CAMEL_CASE_SPLITTER.split(word))

