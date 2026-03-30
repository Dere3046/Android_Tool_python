
import re
SPLIT_RE = re.compile('[\\.\\[\\]]+')

class JsonSchemaException(ValueError):
    '''
    Base exception of ``fastjsonschema`` library.
    '''
    pass


class JsonSchemaValueException(JsonSchemaException):
    """
    Exception raised by validation function. Available properties:

     * ``message`` containing human-readable information what is wrong (e.g. ``data.property[index] must be smaller than or equal to 42``),
     * invalid ``value`` (e.g. ``60``),
     * ``name`` of a path in the data structure (e.g. ``data.property[index]``),
     * ``path`` as an array in the data structure (e.g. ``['data', 'property', 'index']``),
     * the whole ``definition`` which the ``value`` has to fulfil (e.g. ``{'type': 'number', 'maximum': 42}``),
     * ``rule`` which the ``value`` is breaking (e.g. ``maximum``)
     * and ``rule_definition`` (e.g. ``42``).

    .. versionchanged:: 2.14.0
        Added all extra properties.
    """
    
    def __init__(self = None, message = None, value = None, name = None, definition = None, rule = None):
        super().__init__(message)
        self.message = message
        self.value = value
        self.name = name
        self.definition = definition
        self.rule = rule

    
    def path(self):
        return (lambda .0: [ item for item in .0 if item != '' ])(SPLIT_RE.split(self.name))

    path = property(path)
    
    def rule_definition(self):
        if not self.rule or self.definition:
            return None
        return None.definition.get(self.rule)

    rule_definition = property(rule_definition)
    __classcell__ = None


class JsonSchemaDefinitionException(JsonSchemaException):
    '''
    Exception raised by generator of validation function.
    '''
    pass

