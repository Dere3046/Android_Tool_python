
from copy import deepcopy
from cmd_line_interface.base_defines import AutoCloseFileType, COMPATIBLE, HELP_GROUP, KWARGS_HELP, KWARGS_READ_BINARY, KWARGS_REQUIRED, KWARGS_TYPE, OPTIONAL
from cmd_line_interface.basecmdline import CMDLineArgs, CMDLineGroup, update_cmdline_arg
from cmd_line_interface.sectools.cmd_line_common.defines import IMAGE_INPUTS_GROUP, IMAGE_OUTPUTS_GROUP, INFILE
from cmd_line_interface.sectools.elf_tool.common.defines import COMMON_HELP, COMMON_IMAGE_INPUTS, COMMON_IMAGE_OUTPUTS, COMMON_SEGMENT_CONFIGURATION, DATA, DATA_HELP, OFFSET, SEGMENT_CONFIGURATION_DESCRIPTION, SEGMENT_CONFIGURATION_GROUP
INSERT = 'insert'
INSERT_DESCRIPTION = 'Add a segment specified via Segment Configuration arguments to an existing ELF software image.'
OFFSET_HELP = f'''Defaults to the lowest available offset following the ELF Header, Program Header Table, and existing segments. If {INFILE}\'s ELF Header, Program Header Table, Section Header Table, existing segments, or existing sections overlap {OFFSET}, the next available offset will be used.'''
IMAGE_INPUTS = list(COMMON_IMAGE_INPUTS)
IMAGE_INPUTS.append(([
    DATA], {
    KWARGS_HELP: DATA_HELP,
    KWARGS_REQUIRED: True,
    KWARGS_TYPE: AutoCloseFileType(KWARGS_READ_BINARY) }))
SEGMENT_CONFIGURATION: CMDLineGroup = deepcopy(COMMON_SEGMENT_CONFIGURATION)
ELF_TOOL_INSERT: CMDLineArgs = {
    (SEGMENT_CONFIGURATION_GROUP, SEGMENT_CONFIGURATION_DESCRIPTION, COMPATIBLE, OPTIONAL): SEGMENT_CONFIGURATION,
    IMAGE_OUTPUTS_GROUP: COMMON_IMAGE_OUTPUTS,
    IMAGE_INPUTS_GROUP: IMAGE_INPUTS,
    HELP_GROUP: COMMON_HELP }
update_cmdline_arg(ELF_TOOL_INSERT, OFFSET, OFFSET_HELP, **('cmd_help',))
