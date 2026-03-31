import os
import shlex
import sys
import tempfile
import shutil
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
    # 无法恢复原始逻辑，返回默认值
    return False


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
    if not is_windows() or is_linux() or is_macos():
        raise RuntimeError(f'''{sys.platform} OS is not supported.''')
    return True


def create_temp_file(data=None, suffix=None, directory=None):
    """创建临时文件"""
    fd, temp_file_path = tempfile.mkstemp(suffix=suffix, dir=directory)
    try:
        if data:
            mode = 'w' if isinstance(data, str) else 'wb'
            with os.fdopen(fd, mode) as f:
                f.write(data)
        else:
            os.close(fd)
    except:
        os.close(fd)
        raise
    return temp_file_path


def write_file(path=None, data=None, text_encoding=None):
    """写入文件"""
    if path is None:
        raise ValueError("path is required")
    
    # 创建父目录
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    
    mode = 'w' if text_encoding else 'wb'
    with open(path, mode, encoding=text_encoding) as f:
        f.write(data)


def write_cmdline_file(file_path=None, data=None, cmd_line_arg=None, text_encoding='utf-8'):
    """创建命令行文件"""
    write_file(file_path, data, text_encoding)


@contextmanager
def temp_file_path(data=None, suffix=None):
    '''
    The context manager version. Creates a temp file and yields its path.
    '''
    file_name = create_temp_file(data, suffix) if suffix else create_temp_file(data)
    try:
        yield file_name
    finally:
        if os.path.exists(file_name):
            os.remove(file_name)


def delete_file(file_path=None):
    """删除文件"""
    if file_path and os.path.exists(file_path):
        os.remove(file_path)


def split(command=None):
    '''Make sure the shlex split works on Windows too.'''
    return shlex.split(command.replace("'", '"'), posix=False)


def get_start_and_end_indices(bits):
    (end, start) = map(lambda x: int(x), bits.split(':'))
    if end <= start:
        raise RuntimeError('bits must be of the form higher_index:lower_index.')
    return (start, end)


def is_multi_bit(val):
    """检查是否为多位"""
    if isinstance(val, str):
        return ':' in val
    return val is not None and val > 1


def get_num_bits_from_range(bits):
    '''Returns the number of bits in a colon-separated range. E.g. for 6:1 this function would return 6.'''
    ret = 1
    if is_multi_bit(bits):
        (start, end) = get_start_and_end_indices(bits)
        ret = (end - start) + 1
    return ret


def maximum_bits_value(bits):
    '''Return the maximum value of a colon-separated bit value. For example, the max value of 3:8 is 2**6 - 1 = 63.'''
    if isinstance(bits, str):
        return pow(2, get_num_bits_from_range(bits)) - 1
    return pow(2, bits) - 1


if is_executable():
    SECTOOLS_PATH = os.path.realpath(os.path.join(sys._MEIPASS))
else:
    SECTOOLS_PATH = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))


def generate_symmetric_key(length=32):
    return urandom(length)
