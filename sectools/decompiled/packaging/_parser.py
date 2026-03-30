
'''Handwritten parser of dependency specifiers.

The docstring for each __parse_* function contains EBNF-inspired grammar representing
the implementation.
'''
from __future__ import annotations
import ast
from typing import NamedTuple, Sequence, Tuple, Union
from _tokenizer import DEFAULT_RULES, Tokenizer

class Node:
    
    def __init__(self = None, value = None):
        self.value = value

    
    def __str__(self = None):
        return self.value

    
    def __repr__(self = None):
        return f'''<{self.__class__.__name__}(\'{self}\')>'''

    
    def serialize(self = None):
        raise NotImplementedError



class Variable(Node):
    
    def serialize(self = None):
        return str(self)



class Value(Node):
    
    def serialize(self = None):
        return f'''"{self}"'''



class Op(Node):
    
    def serialize(self = None):
        return str(self)


MarkerVar = Union[(Variable, Value)]
MarkerItem = Tuple[(MarkerVar, Op, MarkerVar)]
MarkerAtom = Union[(MarkerItem, Sequence['MarkerAtom'])]
MarkerList = Sequence[Union[('MarkerList', MarkerAtom, str)]]

class ParsedRequirement(NamedTuple):
    marker: 'MarkerList | None' = 'ParsedRequirement'


def parse_requirement(source = None):
    return _parse_requirement(Tokenizer(source, DEFAULT_RULES, **('rules',)))


def _parse_requirement(tokenizer = None):
    '''
    requirement = WS? IDENTIFIER WS? extras WS? requirement_details
    '''
    tokenizer.consume('WS')
    name_token = tokenizer.expect('IDENTIFIER', 'package name at the start of dependency specifier', **('expected',))
    name = name_token.text
    tokenizer.consume('WS')
    extras = _parse_extras(tokenizer)
    tokenizer.consume('WS')
    (url, specifier, marker) = _parse_requirement_details(tokenizer)
    tokenizer.expect('END', 'end of dependency specifier', **('expected',))
    return ParsedRequirement(name, url, extras, specifier, marker)


def _parse_requirement_details(tokenizer = None):
    '''
    requirement_details = AT URL (WS requirement_marker?)?
                        | specifier WS? (requirement_marker)?
    '''
    specifier = ''
    url = ''
    marker = None
    if tokenizer.check('AT'):
        tokenizer.read()
        tokenizer.consume('WS')
        url_start = tokenizer.position
        url = tokenizer.expect('URL', 'URL after @', **('expected',)).text
        if tokenizer.check('END', True, **('peek',)):
            return (url, specifier, marker)
        None.expect('WS', 'whitespace after URL', **('expected',))
        if tokenizer.check('END', True, **('peek',)):
            return (url, specifier, marker)
        marker = None(tokenizer, url_start, 'URL and whitespace', **('span_start', 'after'))
    else:
        specifier_start = tokenizer.position
        specifier = _parse_specifier(tokenizer)
        tokenizer.consume('WS')
        if tokenizer.check('END', True, **('peek',)):
            return (url, specifier, marker)
        marker = None(tokenizer, specifier_start, 'version specifier' if specifier else 'name and no valid version specifier', **('span_start', 'after'))
    return (url, specifier, marker)


def _parse_requirement_marker(tokenizer = None, *, span_start, after):
    '''
    requirement_marker = SEMICOLON marker WS?
    '''
    if not tokenizer.check('SEMICOLON'):
        tokenizer.raise_syntax_error(f'''Expected end or semicolon (after {after})''', span_start, **('span_start',))
    tokenizer.read()
    marker = _parse_marker(tokenizer)
    tokenizer.consume('WS')
    return marker


def _parse_extras(tokenizer = None):
    '''
    extras = (LEFT_BRACKET wsp* extras_list? wsp* RIGHT_BRACKET)?
    '''
    if not tokenizer.check('LEFT_BRACKET', True, **('peek',)):
        return []
# WARNING: Decompyle incomplete


def _parse_extras_list(tokenizer = None):
    """
    extras_list = identifier (wsp* ',' wsp* identifier)*
    """
    extras = []
    if not tokenizer.check('IDENTIFIER'):
        return extras
    None.append(tokenizer.read().text)
    tokenizer.consume('WS')
    if tokenizer.check('IDENTIFIER', True, **('peek',)):
        tokenizer.raise_syntax_error('Expected comma between extra names')
    elif not tokenizer.check('COMMA'):
        return extras
    tokenizer.read()
    tokenizer.consume('WS')
    extra_token = tokenizer.expect('IDENTIFIER', 'extra name after comma', **('expected',))
    extras.append(extra_token.text)
    continue


def _parse_specifier(tokenizer = None):
    '''
    specifier = LEFT_PARENTHESIS WS? version_many WS? RIGHT_PARENTHESIS
              | WS? version_many WS?
    '''
    pass
# WARNING: Decompyle incomplete


def _parse_version_many(tokenizer = None):
    '''
    version_many = (SPECIFIER (WS? COMMA WS? SPECIFIER)*)?
    '''
    parsed_specifiers = ''
    if tokenizer.check('SPECIFIER'):
        span_start = tokenizer.position
        parsed_specifiers += tokenizer.read().text
        if tokenizer.check('VERSION_PREFIX_TRAIL', True, **('peek',)):
            tokenizer.raise_syntax_error('.* suffix can only be used with `==` or `!=` operators', span_start, tokenizer.position + 1, **('span_start', 'span_end'))
        if tokenizer.check('VERSION_LOCAL_LABEL_TRAIL', True, **('peek',)):
            tokenizer.raise_syntax_error('Local version label can only be used with `==` or `!=` operators', span_start, tokenizer.position, **('span_start', 'span_end'))
        tokenizer.consume('WS')
        if not tokenizer.check('COMMA'):
            return parsed_specifiers
        None += tokenizer.read().text
        tokenizer.consume('WS')
        if not tokenizer.check('SPECIFIER'):
            return parsed_specifiers


def parse_marker(source = None):
    return _parse_full_marker(Tokenizer(source, DEFAULT_RULES, **('rules',)))


def _parse_full_marker(tokenizer = None):
    retval = _parse_marker(tokenizer)
    tokenizer.expect('END', 'end of marker expression', **('expected',))
    return retval


def _parse_marker(tokenizer = None):
    '''
    marker = marker_atom (BOOLOP marker_atom)+
    '''
    expression = [
        _parse_marker_atom(tokenizer)]
    if tokenizer.check('BOOLOP'):
        token = tokenizer.read()
        expr_right = _parse_marker_atom(tokenizer)
        expression.extend((token.text, expr_right))
        if not tokenizer.check('BOOLOP'):
            return expression


def _parse_marker_atom(tokenizer = None):
    '''
    marker_atom = WS? LEFT_PARENTHESIS WS? marker WS? RIGHT_PARENTHESIS WS?
                | WS? marker_item WS?
    '''
    tokenizer.consume('WS')
# WARNING: Decompyle incomplete


def _parse_marker_item(tokenizer = None):
    '''
    marker_item = WS? marker_var WS? marker_op WS? marker_var WS?
    '''
    tokenizer.consume('WS')
    marker_var_left = _parse_marker_var(tokenizer)
    tokenizer.consume('WS')
    marker_op = _parse_marker_op(tokenizer)
    tokenizer.consume('WS')
    marker_var_right = _parse_marker_var(tokenizer)
    tokenizer.consume('WS')
    return (marker_var_left, marker_op, marker_var_right)


def _parse_marker_var(tokenizer = None):
    '''
    marker_var = VARIABLE | QUOTED_STRING
    '''
    if tokenizer.check('VARIABLE'):
        return process_env_var(tokenizer.read().text.replace('.', '_'))
    if None.check('QUOTED_STRING'):
        return process_python_str(tokenizer.read().text)
    None.raise_syntax_error('Expected a marker variable or quoted string', **('message',))


def process_env_var(env_var = None):
    if env_var in ('platform_python_implementation', 'python_implementation'):
        return Variable('platform_python_implementation')
    return None(env_var)


def process_python_str(python_str = None):
    value = ast.literal_eval(python_str)
    return Value(str(value))


def _parse_marker_op(tokenizer = None):
    '''
    marker_op = IN | NOT IN | OP
    '''
    if tokenizer.check('IN'):
        tokenizer.read()
        return Op('in')
    if None.check('NOT'):
        tokenizer.read()
        tokenizer.expect('WS', "whitespace after 'not'", **('expected',))
        tokenizer.expect('IN', "'in' after 'not'", **('expected',))
        return Op('not in')
    if None.check('OP'):
        return Op(tokenizer.read().text)
    return None.raise_syntax_error('Expected marker operator, one of <=, <, !=, ==, >=, >, ~=, ===, in, not in')

