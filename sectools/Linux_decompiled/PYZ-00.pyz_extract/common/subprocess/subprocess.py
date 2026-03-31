
import os
import sys
from inspect import signature, Signature
from importlib.abc import Loader
from importlib.util import module_from_spec, spec_from_file_location
from typing import Callable, List, Optional

class FunctionSignatureException(RuntimeError):
    
    def __init__(self = None, message = None, function_signature = None):
        self.message = message
        self.function_signature = function_signature

    
    def __str__(self = None):
        return f'''{self.message}: {self.function_signature}'''



def get_function_from_script2(script_path = None, function_signature = None, function_name = None):
    ''' Allows multiple potential function signatures to be provided. '''
    exception = None
# WARNING: Decompyle incomplete


def format_signature(function_signature = None):
    '''
    The __repr__ for Signature objects may not include the full return annotation. This function can instead be used
    to create a string representation of a Signature object with the full return type annotation.
    '''
    unformatted_signature = str(function_signature).split('->')
    if len(unformatted_signature) == 1:
        return unformatted_signature[0].strip()
    parameters = None[0].strip()
    return_type = function_signature.return_annotation
    return f'''{parameters} -> {return_type}'''.replace('typing.', '')


def get_function_from_script(script_path = None, function_signature = None, function_name = None):
    ''' Allows a single function signatures to be provided. '''
    spec = spec_from_file_location(os.path.splitext(os.path.basename(script_path))[0], script_path)
    if not spec:
        raise RuntimeError(f'''{script_path} is not a Python script.'''), None
    module = module_from_spec(spec)
# WARNING: Decompyle incomplete

