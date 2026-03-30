
from cmd_line_interface.base_defines import HELP, HELP_ABBREV, HELP_GROUP, HELP_HELP, KWARGS_ACTION, KWARGS_HELP
from cmd_line_interface.basecmdline import BaseCMDLine, CMDLineArgs
from cmd_line_interface.sectools.cmd_line_common.defines import OPERATION
ELF_TOOL_NAME = 'elf-tool'
ELF_TOOL_DESCRIPTION = 'Tool for generating, adding segments to, removing sections from, and combining ELF software images.'
ELF_TOOL_EPILOG = f'''For help menu of a specific {OPERATION}: {BaseCMDLine.TOOL_NAME} {ELF_TOOL_NAME} <{OPERATION}> {HELP_ABBREV}'''
ELF_TOOL: CMDLineArgs = {
    HELP_GROUP: [
        ([
            HELP_ABBREV,
            HELP], {
            KWARGS_HELP: HELP_HELP,
            KWARGS_ACTION: KWARGS_HELP })] }
