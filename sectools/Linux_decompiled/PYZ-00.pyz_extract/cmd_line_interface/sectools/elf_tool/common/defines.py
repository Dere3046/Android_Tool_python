
from cmd_line_interface.base_defines import AutoCloseFileType, HELP, HELP_ABBREV, HELP_HELP, KWARGS_ACTION, KWARGS_CHOICES, KWARGS_COUNT, KWARGS_DEFAULT, KWARGS_HELP, KWARGS_REQUIRED, KWARGS_TYPE, KWARGS_WRITE_BINARY, OUTFILE_COMMON_HELP
from cmd_line_interface.basecmdline import CMDLineGroup
from cmd_line_interface.sectools.cmd_line_common.auto_close_image_type import AutoCloseImageType
from cmd_line_interface.sectools.cmd_line_common.defines import INFILE, INFILE_COMMON_HELP, OUTFILE, VERBOSE, VERBOSE_ABBREV, VERBOSE_HELP, eight_byte_hex, four_byte_hex
from common.parser.elf.defines import PT_DESCRIPTION, PT_LOAD, PT_NOTE, PT_NULL
from common.parser.elf.elf import ELF
DATA = '--data'
DATA_HELP = 'File path of segment data.'
INFILE_HELP = f'''{INFILE_COMMON_HELP} ELF image'''
OUTFILE_HELP = f'''{OUTFILE_COMMON_HELP} ELF image.'''
DEFAULT_0 = '0x0'
DEFAULTS_TO_0 = f'''Defaults to {DEFAULT_0}.'''
ELF_CONFIGURATION_GROUP = 'ELF Configuration'
ELF_ENTRY = '--elf-entry'
ELF_ENTRY_COMMON_HELP = 'Entry point address.'
SEGMENT_CONFIGURATION_GROUP = 'Segment Configuration'
SEGMENT_CONFIGURATION_DESCRIPTION = f'''Program Header values of segment containing {DATA}.'''
TYPE = '--type'
TYPE_HELP = 'Defaults to LOAD.'
OFFSET = '--offset'
OFFSET_HELP = 'Defaults to the lowest available offset following the ELF Header and Program Header Table.'
VADDR = '--vaddr'
PADDR = '--paddr'
MEMSZ = '--memsz'
MEMSZ_HELP = f'''Defaults to size of {DATA}.'''
FLAGS = '--flags'
ALIGN = '--align'
COMMON_HELP: CMDLineGroup = [
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
        KWARGS_ACTION: KWARGS_COUNT })]
COMMON_SEGMENT_CONFIGURATION: CMDLineGroup = [
    ([
        TYPE], {
        KWARGS_DEFAULT: PT_DESCRIPTION[PT_LOAD],
        KWARGS_HELP: TYPE_HELP,
        KWARGS_CHOICES: [
            PT_DESCRIPTION[PT_NULL],
            PT_DESCRIPTION[PT_LOAD],
            PT_DESCRIPTION[PT_NOTE]] }),
    ([
        OFFSET], {
        KWARGS_DEFAULT: DEFAULT_0,
        KWARGS_HELP: OFFSET_HELP,
        KWARGS_TYPE: eight_byte_hex }),
    ([
        VADDR], {
        KWARGS_DEFAULT: DEFAULT_0,
        KWARGS_HELP: DEFAULTS_TO_0,
        KWARGS_TYPE: eight_byte_hex }),
    ([
        PADDR], {
        KWARGS_DEFAULT: DEFAULT_0,
        KWARGS_HELP: DEFAULTS_TO_0,
        KWARGS_TYPE: eight_byte_hex }),
    ([
        MEMSZ], {
        KWARGS_HELP: MEMSZ_HELP,
        KWARGS_TYPE: eight_byte_hex }),
    ([
        FLAGS], {
        KWARGS_DEFAULT: DEFAULT_0,
        KWARGS_HELP: DEFAULTS_TO_0,
        KWARGS_TYPE: four_byte_hex }),
    ([
        ALIGN], {
        KWARGS_DEFAULT: DEFAULT_0,
        KWARGS_HELP: DEFAULTS_TO_0,
        KWARGS_TYPE: eight_byte_hex })]
COMMON_IMAGE_INPUTS: CMDLineGroup = [
    ([
        INFILE], {
        KWARGS_HELP: f'''{INFILE_HELP}.''',
        KWARGS_TYPE: AutoCloseImageType((ELF,), True, **('return_path',)) })]
COMMON_IMAGE_OUTPUTS: CMDLineGroup = [
    ([
        OUTFILE], {
        KWARGS_HELP: OUTFILE_HELP,
        KWARGS_REQUIRED: True,
        KWARGS_TYPE: AutoCloseFileType(KWARGS_WRITE_BINARY) })]
