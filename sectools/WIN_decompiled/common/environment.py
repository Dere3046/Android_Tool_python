
from contextlib import contextmanager
from os import environ
from typing import Generator
from common.logging.logger import log_debug

def set_environment_variable(variable = None, value = None):
    log_debug(f'''Setting environment variable {variable} to {value}.''')
    original_value = None
    if variable in environ and original_value = environ[variable] != value:
        log_debug(f'''Environment variable {variable} is already set to {original_value}. It will be temporarily replaced.''')
# WARNING: Decompyle incomplete

set_environment_variable = None(set_environment_variable)
