
from cmd_line_interface.base_defines import AutoCloseFileType, HELP, HELP_ABBREV, HELP_GROUP, HELP_HELP, KWARGS_ACTION, KWARGS_CHOICES, KWARGS_COUNT, KWARGS_DEFAULT, KWARGS_HELP, KWARGS_READ_BINARY, KWARGS_REQUIRED, KWARGS_TYPE, KWARGS_WRITE_BINARY, OUTFILE_COMMON_HELP
from cmd_line_interface.basecmdline import BaseCMDLine, CMDLineArgs
from cmd_line_interface.sectools.cmd_line_common.defines import OPERATION, OPTIONAL_ARGUMENTS, OUTFILE, REQUIRED_ARGUMENTS, VERBOSE, VERBOSE_ABBREV, VERBOSE_HELP, four_byte_hex
from cmd_line_interface.sectools.elf_tool.common.defines import DATA, DEFAULT_0
from cmd_line_interface.sectools.metadata import DEPENDS_ON_VALUE
from common.parser.hash_segment.defines import HASH_SEGMENT_V3
from common.parser.mbn.defines import HASH_TABLE_SEGMENT_HEADER_CLASSES
MBN_TOOL_NAME = 'mbn-tool'
MBN_TOOL_DESCRIPTION = 'Tool to prepend an MBN Header to a binary image.'
MBN_GENERATE_DESCRIPTION = 'Prepend an MBN Header to a binary image.'
MBN_DATA_HELP = 'File path of data to prepend with an MBN Header.'
MBN_OUTFILE_HELP = f'''{OUTFILE_COMMON_HELP} MBN.'''
MBN_VERSION = '--mbn-version'
MBN_VERSION_HELP = f'''Version of MBN Header to prepend to {DATA}.'''
MBN_TOOL_EPILOG = f'''For help menu of a specific {OPERATION}: {BaseCMDLine.TOOL_NAME} {MBN_TOOL_NAME} <{OPERATION}> {HELP_ABBREV}'''
DATA_SIZE_ALIGNMENT = '--data-size-alignment'
DATA_SIZE_ALIGNMENT_HELP = f'''If provided, {DATA} will be padded such that the size of {DATA} is a multiple of the specified hex value.'''
BOOT_IMAGE_ID = '--boot-image-id'
BOOT_IMAGE_ID_HELP = f'''Specifies the image type (e.g., "OEM SBL", "AMSS", "APPS Boot Loader", etc.) as a hexadecimal value. Applicable for {MBN_VERSION} 3 images only.'''
IMAGE_DEST_PTR = '--image-dest-ptr'
IMAGE_DEST_PTR_HELP = f'''Pointer to the RAM address for storing the image and the entry point for image execution. Applicable for {MBN_VERSION} 3 images only.'''
MBN_TOOL: CMDLineArgs = {
    HELP_GROUP: [
        ([
            HELP_ABBREV,
            HELP], {
            KWARGS_HELP: HELP_HELP,
            KWARGS_ACTION: KWARGS_HELP })] }
MBN_TOOL_GENERATE: CMDLineArgs = {
    OPTIONAL_ARGUMENTS: [
        ([
            DATA_SIZE_ALIGNMENT], {
            KWARGS_DEFAULT: DEFAULT_0,
            KWARGS_REQUIRED: False,
            KWARGS_HELP: DATA_SIZE_ALIGNMENT_HELP,
            KWARGS_TYPE: four_byte_hex }),
        ([
            BOOT_IMAGE_ID], {
            KWARGS_REQUIRED: False,
            KWARGS_HELP: BOOT_IMAGE_ID_HELP,
            KWARGS_TYPE: four_byte_hex }, {
            DEPENDS_ON_VALUE: [
                (MBN_VERSION, [
                    HASH_SEGMENT_V3])] }),
        ([
            IMAGE_DEST_PTR], {
            KWARGS_REQUIRED: False,
            KWARGS_HELP: IMAGE_DEST_PTR_HELP,
            KWARGS_TYPE: four_byte_hex }, {
            DEPENDS_ON_VALUE: [
                (MBN_VERSION, [
                    HASH_SEGMENT_V3])] })],
    REQUIRED_ARGUMENTS: [
        ([
            DATA], {
            KWARGS_HELP: MBN_DATA_HELP,
            KWARGS_REQUIRED: True,
            KWARGS_TYPE: AutoCloseFileType(KWARGS_READ_BINARY) }),
        ([
            OUTFILE], {
            KWARGS_HELP: MBN_OUTFILE_HELP,
            KWARGS_REQUIRED: True,
            KWARGS_TYPE: AutoCloseFileType(KWARGS_WRITE_BINARY) }),
        ([
            MBN_VERSION], {
            KWARGS_HELP: MBN_VERSION_HELP,
            KWARGS_REQUIRED: True,
            KWARGS_CHOICES: HASH_TABLE_SEGMENT_HEADER_CLASSES.keys(),
            KWARGS_TYPE: int })],
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
