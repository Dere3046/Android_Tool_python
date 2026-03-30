
from cmd_line_interface.auto_close_security_profile_type import auto_close_security_profile_type
from cmd_line_interface.base_defines import HELP, HELP_ABBREV, HELP_GROUP, HELP_HELP, KWARGS_ACTION, KWARGS_COUNT, KWARGS_DEFAULT, KWARGS_HELP, KWARGS_NARGS, KWARGS_TYPE, KWARGS_VERSION
from cmd_line_interface.basecmdline import CMDLineArgs
from cmd_line_interface.sectools.cmd_line_common.defines import REQUIRED_ARGUMENTS, SECURITY_PROFILE_HELP, VERBOSE, VERBOSE_ABBREV, VERBOSE_HELP, VERSION, VERSION_HELP
from cmd_line_interface.sectools.defines import SECTOOLS_VERSION
from common.data.data import tuple_to_version_string
PROFILE_VALIDATOR_VERSION = (1, 9)
PROFILE_VALIDATOR_DESCRIPTION = f'''Profile Validator v{tuple_to_version_string(PROFILE_VALIDATOR_VERSION)}'''
SECURITY_PROFILE = 'security_profile'
SECURITY_PROFILE_VALIDATOR: CMDLineArgs = {
    REQUIRED_ARGUMENTS: [
        ([
            SECURITY_PROFILE], {
            KWARGS_HELP: SECURITY_PROFILE_HELP,
            KWARGS_NARGS: '+',
            KWARGS_TYPE: auto_close_security_profile_type })],
    HELP_GROUP: [
        ([
            HELP_ABBREV,
            HELP], {
            KWARGS_HELP: HELP_HELP,
            KWARGS_ACTION: KWARGS_HELP }),
        ([
            VERSION], {
            KWARGS_VERSION: f'''{tuple_to_version_string(PROFILE_VALIDATOR_VERSION)}-{tuple_to_version_string(SECTOOLS_VERSION)}''',
            KWARGS_HELP: VERSION_HELP,
            KWARGS_ACTION: KWARGS_VERSION }),
        ([
            VERBOSE_ABBREV,
            VERBOSE], {
            KWARGS_HELP: VERBOSE_HELP,
            KWARGS_DEFAULT: 0,
            KWARGS_ACTION: KWARGS_COUNT })] }
