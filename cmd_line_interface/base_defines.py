"""Base command line defines."""

KWARGS_ACTION = 'action'
KWARGS_CHOICES = 'choices'
KWARGS_COUNT = 'count'
KWARGS_DEFAULT = 'default'
KWARGS_HELP = 'help'
KWARGS_READ_BINARY = 'rb'
KWARGS_REQUIRED = 'required'
KWARGS_TYPE = 'type'
KWARGS_WRITE_BINARY = 'wb'
KWARGS_STORE_TRUE = 'store_true'
KWARGS_NARGS = 'nargs'

HELP = 'help'
HELP_ABBREV = 'h'
HELP_GROUP = 'help_group'
HELP_HELP = 'Show this help message and exit'

OUTFILE_COMMON_HELP = 'File path for the output'
INFILE_COMMON_HELP = 'File path for the input'

OPTIONAL = 'optional'
COMPATIBLE = 'compatible'


class AutoCloseFileType:
    """Auto-close file type."""

    def __init__(self, mode, **kwargs):
        self.mode = mode
        self.kwargs = kwargs

    def __call__(self, value):
        return value


class AutoCloseImageType:
    """Auto-close image type."""

    def __init__(self, types, return_path=False, **kwargs):
        self.types = types
        self.return_path = return_path
        self.kwargs = kwargs

    def __call__(self, value):
        return value
