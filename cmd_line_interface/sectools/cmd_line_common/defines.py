"""Command line common defines."""

from cmd_line_interface.base_defines import AutoCloseFileType, AutoCloseImageType

GENERATE_OP = 'generate'
INSERT = 'insert'
COMBINE = 'combine'
REMOVE_SECTIONS = 'remove-sections'

SUBFEATURE = 'subfeature'
OPERATION = 'operation'
OUTFILE = 'outfile'
INFILE = 'infile'
DATA = 'data'

OPTIONAL_ARGUMENTS = 'optional_arguments'
REQUIRED_ARGUMENTS = 'required_arguments'
HELP_GROUP = 'help_group'
IMAGE_INPUTS_GROUP = 'Image Inputs'
IMAGE_OUTPUTS_GROUP = 'Image Outputs'

VERBOSE = 'verbose'
VERBOSE_ABBREV = 'v'
VERBOSE_HELP = 'Increase verbosity level'

HELP = 'help'
HELP_ABBREV = 'h'
HELP_HELP = 'Show this help message and exit'

DEFAULT_0 = '0x0'

INFILE_COMMON_HELP = 'File path for the input'
OUTFILE_COMMON_HELP = 'File path for the output'


def four_byte_hex(value):
    """Convert string to 4-byte hex integer."""
    if isinstance(value, str):
        if value.startswith('0x') or value.startswith('0X'):
            value = value[2:]
        return int(value, 16) & 0xFFFFFFFF
    return value


def eight_byte_hex(value):
    """Convert string to 8-byte hex integer."""
    if isinstance(value, str):
        if value.startswith('0x') or value.startswith('0X'):
            value = value[2:]
        return int(value, 16) & 0xFFFFFFFFFFFFFFFF
    return value


def minimum_argument_action(min_args, dest):
    """Create action for minimum argument count."""
    class MinimumArgumentAction:
        def __init__(self, *args, **kwargs):
            pass
    return MinimumArgumentAction
