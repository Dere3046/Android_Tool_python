
from argparse import Action, ArgumentTypeError, FileType
from dataclasses import dataclass
from pathlib import Path
from textwrap import indent
from typing import Callable, Generic, Type, TypeVar
from inflect import engine
from cmd_line_interface.sectools.cmd_line_common.base_defines import SECURITY_PROFILE
from common.data.data import hex_string_validate, hex_val, or_separated
KWARGS_ACTION = 'action'
KWARGS_DEFAULT = 'default'
KWARGS_HELP = 'help'
KWARGS_READ_BINARY = 'rb'
KWARGS_STORE_TRUE = 'store_true'
KWARGS_TYPE = 'type'
KWARGS_CHOICES = 'choices'
KWARGS_APPEND = 'append'
KWARGS_NARGS = 'nargs'
KWARGS_WRITE_BINARY = 'wb'
KWARGS_READ = 'r'
KWARGS_WRITE = 'w'
KWARGS_COUNT = 'count'
KWARGS_REQUIRED = 'required'
KWARGS_VERSION = 'version'
MUTUALLY_EXCLUSIVE = True
COMPATIBLE = False
REQUIRED = True
OPTIONAL = False
HELP_GROUP = 'Help'
HELP = '--help'
HELP_ABBREV = '-h'
HELP_HELP = 'Show this help message and exit.'
DYNAMIC_HELP_PLURAL = f'''command-line arguments are generated dynamically based on the Security Profile. Provide {HELP} and {SECURITY_PROFILE} to see all the available options.'''
DYNAMIC_HELP_SINGULAR = f'''command-line argument is generated dynamically based on the Security Profile. Provide {HELP} and {SECURITY_PROFILE} to see if it is available.'''
OUTFILE_COMMON_HELP = 'File path of output'
SECURITY_PROFILE_OUTFILE_HELP = f'''{OUTFILE_COMMON_HELP} Security Profile.'''

def get_cmd_member(cmd_arg = None):
    '''Handles positional and key arguments.'''
    return cmd_arg.lstrip('-').replace('-', '_')


def get_cmd_name(cmd_arg = None):
    return get_cmd_member(cmd_arg).upper()


def get_cmd_arg(arg_name = None):
    return f'''--{arg_name.replace('_', '-')}'''


class AutoCloseFileType(FileType):
    
    class FileInfo:
        __qualname__ = 'AutoCloseFileType.FileInfo'
        
        def __init__(self, path, data = (b'',)):
            self.path = path
            self.data = data


    
    def __init__(self = None, mode = None, bufsize = None, encoding = None, errors = None, return_path = None, optional = None):
        self.return_path = return_path
        self.optional = optional
        super().__init__(mode, bufsize, encoding, errors, **('mode', 'bufsize', 'encoding', 'errors'))

    
    def __call__(self = None, path = None):
        pass
    # WARNING: Decompyle incomplete

    __classcell__ = None


class LimitedRangeInt:
    
    def __init__(self = None, lower_limit = None, upper_limit = None):
        pass
    # WARNING: Decompyle incomplete

    
    def __call__(self = None, user_value = None):
        pass
    # WARNING: Decompyle incomplete



def minimum_argument_action(minimum_number_of_arguments = None, error_string = None):
    
    def MinimumArgumentAction():
        '''minimum_argument_action.<locals>.MinimumArgumentAction'''
        __qualname__ = 'minimum_argument_action.<locals>.MinimumArgumentAction'
        
        def __call__(self = None, parser = None, namespace = None, values = None, option_string = None):
            if len(values) < minimum_number_of_arguments:
                raise ArgumentTypeError(f'''At least {engine().number_to_words(minimum_number_of_arguments)} {error_string} must be provided.''')
            None(namespace, self.dest, values)


    MinimumArgumentAction = None(MinimumArgumentAction, 'MinimumArgumentAction', Action)
    return MinimumArgumentAction


def max_val_hex_type(max_val = None, allowed_enums = None, is_byte_array = None):
    
    def enforce_maximum_value(value = None):
        if allowed_enums and value in allowed_enums:
            return value
        if not None(value):
            if allowed_enums:
                raise ArgumentTypeError(f'''"{value}" is neither a valid hex string nor {or_separated(allowed_enums)}.''')
            raise None(f'''{value} is not a valid hex string.''')
        if None and len(value) & 1:
            raise ArgumentTypeError(f'''"{value}" is not a valid byte array. Ensure it has an even number of hex characters.''')
        if int_value = None(value, 16) > max_val:
            raise ArgumentTypeError(f'''"{value}" exceeds maximum allowed value 0x{hex_val(max_val, True, True, **('strip_leading_zeros', 'without_0x')).upper()}.''')
        if None(value, 16):
            return value

    return enforce_maximum_value

T = TypeVar('T')

def XMLInfo():
    '''XMLInfo'''
    parsed_xml: T = 'XMLInfo'

XMLInfo = dataclass(<NODE:27>(XMLInfo, 'XMLInfo', Generic[T]))

def auto_close_xml_type(parser_function = None, optional = None):
    
    def get_xml_info(path = None):
        file_info = AutoCloseFileType(KWARGS_READ_BINARY, True, optional, **('mode', 'return_path', 'optional'))(path)
    # WARNING: Decompyle incomplete

    return get_xml_info

