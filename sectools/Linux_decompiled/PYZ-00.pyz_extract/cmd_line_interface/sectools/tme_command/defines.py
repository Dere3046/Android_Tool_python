
from cmd_line_interface.base_defines import HELP, HELP_ABBREV, HELP_GROUP, HELP_HELP, KWARGS_ACTION, KWARGS_HELP
from cmd_line_interface.basecmdline import BaseCMDLine, CMDLineArgs
from cmd_line_interface.sectools.cmd_line_common.defines import SUBFEATURE
TME_COMMAND_NAME = 'tme-command'
TME_COMMAND_DESCRIPTION = 'Tool for generating TME Command images.'
TME_COMMAND_EPILOG = f'''For help menu of a specific {SUBFEATURE}: {BaseCMDLine.TOOL_NAME} {TME_COMMAND_NAME} <{SUBFEATURE}> {HELP_ABBREV}'''
TME_COMMAND: CMDLineArgs = {
    HELP_GROUP: [
        ([
            HELP_ABBREV,
            HELP], {
            KWARGS_HELP: HELP_HELP,
            KWARGS_ACTION: KWARGS_HELP })] }
