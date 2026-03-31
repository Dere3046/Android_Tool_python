
from cmd_line_interface.base_defines import AutoCloseFileType, HELP, HELP_ABBREV, HELP_GROUP, HELP_HELP, KWARGS_ACTION, KWARGS_COUNT, KWARGS_DEFAULT, KWARGS_HELP, KWARGS_NARGS, KWARGS_READ_BINARY, KWARGS_TYPE
from cmd_line_interface.basecmdline import CMDLineArgs
from cmd_line_interface.sectools.cmd_line_common.defines import INFILE, REQUIRED_ARGUMENTS, VERBOSE, VERBOSE_ABBREV, VERBOSE_HELP
COMPARE_NAME = 'compare'
GENERATE_PAYLOAD_NAME = 'generate-payload'
SHOW_ON_TARGET_RESULTS_NAME = 'show-on-target-results'
INFILE_HELP = 'File path of one or more Fuse Blower images, typically named sec.elf or sec.dat, which were used to blow fuses on-target.'
FUSE_VALIDATOR_COMMON: CMDLineArgs = {
    REQUIRED_ARGUMENTS: [
        ([
            INFILE], {
            KWARGS_HELP: INFILE_HELP,
            KWARGS_NARGS: '+',
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
