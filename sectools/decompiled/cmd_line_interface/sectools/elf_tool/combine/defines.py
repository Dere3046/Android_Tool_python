
from cmd_line_interface.base_defines import HELP_GROUP, KWARGS_ACTION, KWARGS_HELP, KWARGS_NARGS, KWARGS_TYPE, minimum_argument_action
from cmd_line_interface.basecmdline import CMDLineArgs, CMDLineGroup
from cmd_line_interface.sectools.cmd_line_common.auto_close_image_type import AutoCloseImageType
from cmd_line_interface.sectools.cmd_line_common.defines import IMAGE_INPUTS_GROUP, IMAGE_OUTPUTS_GROUP, INFILE, eight_byte_hex
from cmd_line_interface.sectools.elf_tool.common.defines import COMMON_HELP, COMMON_IMAGE_OUTPUTS, ELF_CONFIGURATION_GROUP, ELF_ENTRY, ELF_ENTRY_COMMON_HELP, INFILE_HELP
from common.parser.elf.elf import ELF
COMBINE = 'combine'
COMBINE_DESCRIPTION = 'Combine multiple ELFs into a single ELF. Data contained within ELF sections will not be persisted unless they are encapsulated within segments.'
INFILE_HELP_COMBINE = f'''{INFILE_HELP}s.'''
ELF_ENTRY_HELP = f'''{ELF_ENTRY_COMMON_HELP} Defaults to entry point address of first {INFILE}.'''
IMAGE_INPUTS: CMDLineGroup = [
    ([
        INFILE], {
        KWARGS_ACTION: minimum_argument_action(2, f'''{INFILE}s'''),
        KWARGS_NARGS: '+',
        KWARGS_HELP: INFILE_HELP_COMBINE,
        KWARGS_TYPE: AutoCloseImageType((ELF,), True, **('return_path',)) })]
ELF_CONFIGURATION: CMDLineGroup = [
    ([
        ELF_ENTRY], {
        KWARGS_HELP: ELF_ENTRY_HELP,
        KWARGS_TYPE: eight_byte_hex })]
ELF_TOOL_COMBINE: CMDLineArgs = {
    ELF_CONFIGURATION_GROUP: ELF_CONFIGURATION,
    IMAGE_OUTPUTS_GROUP: COMMON_IMAGE_OUTPUTS,
    IMAGE_INPUTS_GROUP: IMAGE_INPUTS,
    HELP_GROUP: COMMON_HELP }
