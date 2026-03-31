
from os import listdir
from os.path import abspath, join, exists
from sys import path as sys_path
from common.utils import is_linux, is_windows, SECTOOLS_PATH

def prepend_to_sys_path(directory):
    if exists(directory):
        sys_path.insert(1, directory)
        for module in listdir(directory):
            sys_path.insert(1, join(directory, module))
    return None

prepend_to_sys_path(abspath(join(SECTOOLS_PATH, 'ext')))
if is_linux():
    prepend_to_sys_path(abspath(join(SECTOOLS_PATH, 'ext_LIN')))
    return None
if None():
    prepend_to_sys_path(abspath(join(SECTOOLS_PATH, 'ext_WIN')))
    return None
None(abspath(join(SECTOOLS_PATH, 'ext_MAC')))
