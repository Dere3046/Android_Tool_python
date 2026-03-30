
import argparse
import re
from abc import ABC, abstractmethod
from argparse import ArgumentParser, ArgumentTypeError, HelpFormatter, Namespace, SUPPRESS
from contextlib import suppress
from gettext import gettext
from pathlib import Path
from re import sub
from typing import Any, Type
from cmd_line_interface.base_defines import COMPATIBLE, KWARGS_ACTION, KWARGS_COUNT, KWARGS_HELP, OPTIONAL, get_cmd_member
from cmd_line_interface.sectools.cmd_line_common.base_defines import HIDDEN_ARGS
from common.utils import is_executable, is_windows
NONPUBLIC_HIDDEN_ARGS: list[str] = []
with suppress(ModuleNotFoundError):
    from cmd_line_interface.nonpublic.nonpublic_cmd_line_interface import NONPUBLIC_HIDDEN_ARGS
    None(None, None, None)
# WARNING: Decompyle incomplete
