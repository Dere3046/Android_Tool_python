
from functools import reduce
from typing import Any, Callable, Dict
from  import formats
from error_reporting import detailed_errors, ValidationError
from extra_validations import EXTRA_VALIDATIONS
from fastjsonschema_exceptions import JsonSchemaException, JsonSchemaValueException
from fastjsonschema_validations import validate as _validate
__all__ = [
    'validate',
    'FORMAT_FUNCTIONS',
    'EXTRA_VALIDATIONS',
    'ValidationError',
    'JsonSchemaException',
    'JsonSchemaValueException']
FORMAT_FUNCTIONS: Dict[(str, Callable[([
    str], bool)])] = (lambda .0: pass# WARNING: Decompyle incomplete
)(formats.__dict__.values())

def validate(data = None):
    '''Validate the given ``data`` object using JSON Schema
    This function raises ``ValidationError`` if ``data`` is invalid.
    '''
    with detailed_errors():
        _validate(data, FORMAT_FUNCTIONS, **('custom_formats',))
        None(None, None, None)
# WARNING: Decompyle incomplete

