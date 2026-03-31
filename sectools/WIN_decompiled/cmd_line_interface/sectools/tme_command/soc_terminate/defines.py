
from cmd_line_interface.base_defines import AutoCloseFileType, COMPATIBLE, HELP, HELP_ABBREV, HELP_GROUP, HELP_HELP, KWARGS_ACTION, KWARGS_CHOICES, KWARGS_COUNT, KWARGS_DEFAULT, KWARGS_HELP, KWARGS_READ_BINARY, KWARGS_REQUIRED, KWARGS_TYPE, KWARGS_WRITE_BINARY, OPTIONAL, OUTFILE_COMMON_HELP
from cmd_line_interface.basecmdline import BaseCMDLine, CMDLineArgs
from cmd_line_interface.sectools.cmd_line_common.defines import GENERATE_OP, IMAGE_INPUTS_GROUP, IMAGE_OUTPUTS_GROUP, OPERATION, OUTFILE, VERBOSE, VERBOSE_ABBREV, VERBOSE_HELP, eight_byte_hex, four_byte_hex
from cmd_line_interface.sectools.elf_tool.common.defines import ALIGN, DEFAULTS_TO_0, DEFAULT_0, ELF_CONFIGURATION_GROUP, FLAGS, PADDR, SEGMENT_CONFIGURATION_GROUP
from cmd_line_interface.sectools.elf_tool.generate.defines import ELF_CLASS, ELF_CLASS_HELP
from cmd_line_interface.sectools.tme_command.defines import TME_COMMAND_NAME
from common.parser.elf.defines import ELFCLASS32, ELFCLASS64, ELFCLASS_TO_INT
SOC_TERMINATE = 'soc-terminate'
SOC_TERMINATE_DESCRIPTION = 'Tool for generating SoC Terminate Request images.'
SOC_TERMINATE_EPILOG = f'''For help menu of a specific {OPERATION}: {BaseCMDLine.TOOL_NAME} {TME_COMMAND_NAME} {SOC_TERMINATE} <{OPERATION}> {HELP_ABBREV}'''
SOC_TERMINATE_GENERATE_DESCRIPTION = 'Generate a TME ELF software image containing an SoC Terminate Request.'
ALLOWED_SOC_TERMINATE_OPERATIONS = [
    GENERATE_OP]
DEFAULT_4K = '0x1000'
DEFAULT_4K_HELP = f'''Defaults to {DEFAULT_4K}.'''
PADDR_HELP = 'Physical address.'
OUTFILE_HELP = f'''{OUTFILE_COMMON_HELP} TME ELF.'''
COMMAND_ENTITLEMENT_CERTIFICATE = '--command-entitlement-certificate'
COMMAND_ENTITLEMENT_CERTIFICATE_HELP = 'File path of the Command Entitlement Certificate to use for SoC Terminate Request generation.'
SEGMENT_CONFIGURATION_DESCRIPTION = 'Program Header values of segment containing the SoC Terminate Request.'
SOC_TERMINATE_ARGS: CMDLineArgs = {
    HELP_GROUP: [
        ([
            HELP_ABBREV,
            HELP], {
            KWARGS_HELP: HELP_HELP,
            KWARGS_ACTION: KWARGS_HELP })] }
SOC_TERMINATE_GENERATE: CMDLineArgs = {
    (SEGMENT_CONFIGURATION_GROUP, SEGMENT_CONFIGURATION_DESCRIPTION, COMPATIBLE, OPTIONAL): [
        ([
            PADDR], {
            KWARGS_HELP: PADDR_HELP,
            KWARGS_REQUIRED: True,
            KWARGS_TYPE: eight_byte_hex }),
        ([
            ALIGN], {
            KWARGS_HELP: DEFAULT_4K_HELP,
            KWARGS_DEFAULT: DEFAULT_4K,
            KWARGS_TYPE: eight_byte_hex }),
        ([
            FLAGS], {
            KWARGS_DEFAULT: DEFAULT_0,
            KWARGS_HELP: DEFAULTS_TO_0,
            KWARGS_TYPE: four_byte_hex })],
    ELF_CONFIGURATION_GROUP: [
        ([
            ELF_CLASS], {
            KWARGS_HELP: ELF_CLASS_HELP,
            KWARGS_DEFAULT: ELFCLASS_TO_INT[ELFCLASS64],
            KWARGS_CHOICES: [
                ELFCLASS_TO_INT[ELFCLASS32],
                ELFCLASS_TO_INT[ELFCLASS64]],
            KWARGS_TYPE: int })],
    IMAGE_OUTPUTS_GROUP: [
        ([
            OUTFILE], {
            KWARGS_HELP: OUTFILE_HELP,
            KWARGS_REQUIRED: True,
            KWARGS_TYPE: AutoCloseFileType(KWARGS_WRITE_BINARY) })],
    IMAGE_INPUTS_GROUP: [
        ([
            COMMAND_ENTITLEMENT_CERTIFICATE], {
            KWARGS_HELP: COMMAND_ENTITLEMENT_CERTIFICATE_HELP,
            KWARGS_REQUIRED: True,
            KWARGS_TYPE: AutoCloseFileType(KWARGS_READ_BINARY) })],
    HELP_GROUP: [
        ([
            HELP_ABBREV,
            HELP], {
            KWARGS_HELP: HELP_HELP,
            KWARGS_ACTION: KWARGS_HELP }),
        ([
            VERBOSE_ABBREV,
            VERBOSE], {
            KWARGS_HELP: VERBOSE_HELP,
            KWARGS_DEFAULT: 0,
            KWARGS_ACTION: KWARGS_COUNT })] }
