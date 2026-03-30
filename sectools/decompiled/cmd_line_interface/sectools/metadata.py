
from itertools import chain
from cmd_line_interface.base_defines import get_cmd_arg, get_cmd_member
from cmd_line_interface.basecmdline import CMDLineArgs, NamespaceWithGet
from common.data.data import and_separated, or_separated, plural_s
CONSUMES = '_consumes'
DEPENDS_ON = '_depends_on'
DEPENDS_ON_ANY_OF = '_depends_on_any_of'
VALUE_DEPENDS_ON_ANY_OF = '_value_depends_on_any_of'
VALUE_DEPENDS_ON = '_value_depends_on'
INCOMPATIBLE_WITH = '_incompatible_with'
INCOMPATIBLE_WITH_ALL_BUT = '_incompatible_with_all_but'
INCOMPATIBLE_WITH_VALUE = '_incompatible_with_value'
DEPENDS_NOT_FORCED = '_depends_not_forced'
DEPENDS_ON_VALUE = '_depends_on_value'
NA = '__NA__'

def validate_cmd_line_args_with_metadata(args = None, arguments = None):
    '''Generic metadata based validation.'''
    
    def get_missing(args_to_check = None):
        return (lambda .0 = None: [ arg for arg in .0 if args.get(arg) ])(args_to_check)

    args_to_process = { }
# WARNING: Decompyle incomplete

