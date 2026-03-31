
from cmd_line_interface.base_defines import HELP_GROUP
from cmd_line_interface.basecmdline import CMDLineArgs
from cmd_line_interface.sectools.cmd_line_common.defines import IMAGE_INPUTS_GROUP, IMAGE_OUTPUTS_GROUP
from cmd_line_interface.sectools.elf_tool.common.defines import COMMON_HELP, COMMON_IMAGE_INPUTS, COMMON_IMAGE_OUTPUTS
REMOVE_SECTIONS = 'remove-sections'
REMOVE_SECTIONS_DESCRIPTION = 'Remove Sections from an existing ELF software image.'
ELF_TOOL_REMOVE_SECTIONS: CMDLineArgs = {
    IMAGE_OUTPUTS_GROUP: COMMON_IMAGE_OUTPUTS,
    IMAGE_INPUTS_GROUP: COMMON_IMAGE_INPUTS,
    HELP_GROUP: COMMON_HELP }
