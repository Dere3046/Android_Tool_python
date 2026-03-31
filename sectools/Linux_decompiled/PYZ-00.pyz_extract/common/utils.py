
import os
import shlex
import sys
import tempfile
from contextlib import contextmanager
from os import urandom
from pathlib import Path
from platform import machine
from re import fullmatch
from typing import Any, Generator, Optional
REQUIRED_PYTHON_VERSION = (3, 10)

def is_executable():
    return getattr(sys, 'frozen', False)


def is_public_distro():
    public = False
# WARNING: Decompyle incomplete


def is_arm64():
    return machine() in ('arm64', 'aarch64')


def is_linux():
    return sys.platform.startswith('linux')


def is_windows():
    return sys.platform.startswith('win32')


def is_macos():
    return sys.platform.startswith('darwin')


def check_supported_environment():
    if sys.version_info[:len(REQUIRED_PYTHON_VERSION)] != REQUIRED_PYTHON_VERSION:
        raise RuntimeError(f'''Python {'.'.join(map(str, REQUIRED_PYTHON_VERSION))} is required. Running with {'.'.join(map(str, sys.version_info))}.''')
    if not None() or is_linux() or is_macos():
        raise RuntimeError(f'''{sys.platform} OS is not supported.''')
    return None
    return None


def create_temp_file(data = None, suffix = None, directory = None):
    pass
# WARNING: Decompyle incomplete


def write_file(path = None, data = None, text_encoding = None):
    pass
# WARNING: Decompyle incomplete


def write_cmdline_file(file_path = None, data = None, cmd_line_arg = None, text_encoding = (None,)):
    """ It creates directories as needed unlike Path.write_file which fails if parent directories are missing or
    the file can't be written due to lack of File Permission."""
    pass
# WARNING: Decompyle incomplete


def temp_file_path(data = None, suffix = None):
    '''
    The context manager version. Creates a temp file and yields its path. If suffix is defined, it is appended to
    the end of the name of the temporary file.
    '''
    file_name = create_temp_file(data, suffix) if suffix else create_temp_file(data)
# WARNING: Decompyle incomplete

temp_file_path = None(temp_file_path)

def delete_file(file_path = None):
    pass
# WARNING: Decompyle incomplete


def split(command = None):
    '''Make sure the shlex split works on Windows too.'''
    return shlex.split(command.replace("'", '"'), True, **('posix',))


def get_start_and_end_indices(bits = None):
    (end, start) = map((lambda x: int(x)), bits.split(':'))
    if end <= start:
        raise RuntimeError('bits must be of the form higher_index:lower_index.')
    return (None, end)


def is_multi_bit(val = None):
    pass
# WARNING: Decompyle incomplete


def get_num_bits_from_range(bits = None):
    '''Returns the number of bits in a colon-separated range. E.g. for 6:1 this function would return 6.'''
    ret = 1
    if is_multi_bit(bits):
        (start, end) = get_start_and_end_indices(bits)
        ret = (end - start) + 1
    return ret


def maximum_bits_value(bits = None):
    '''Return the maximum value of a colon-separated bit value. For example, the max value of 3:8 is 2**6 - 1 = 63.'''
    if isinstance(bits, str):
        return pow(2, get_num_bits_from_range(bits)) - 1
    return None(pow, 2) - 1

if is_executable():
    SECTOOLS_PATH = os.path.realpath(os.path.join(sys._MEIPASS))
else:
    SECTOOLS_PATH = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

def generate_symmetric_key(length = None):
    return urandom(length)

