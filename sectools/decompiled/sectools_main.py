
from os import environ
from common.utils import check_supported_environment
check_supported_environment()
import argcomplete
from contextlib import suppress
from cmd_line_interface.sectools.cmdline import SectoolsCMDLine
from typing import Any, Callable
from cmd_line_interface.sectools.cmd_line_common.base_defines import HIDDEN_ARGS
NONPUBLIC_HIDDEN_ARGS: list[str] = []
nonpublic_log_info: Callable[([
    Any], None)] | None = None
with suppress(ModuleNotFoundError):
    from cmd_line_interface.nonpublic.nonpublic_cmd_line_interface import NONPUBLIC_HIDDEN_ARGS
    from cmd_line_interface.sectools.nonpublic.nonpublic_sectools_cmd_line import nonpublic_log_info
    None(None, None, None)
# WARNING: Decompyle incomplete
