
from cmd_line_interface.base_defines import HELP, HELP_ABBREV, HELP_GROUP, HELP_HELP, KWARGS_ACTION, KWARGS_HELP
from cmd_line_interface.basecmdline import BaseCMDLine, CMDLineArgs
from cmd_line_interface.sectools.cmd_line_common.defines import OPERATION
from cmd_line_interface.sectools.fuse_validator.cmd_line_common.defines import COMPARE_NAME, GENERATE_PAYLOAD_NAME, SHOW_ON_TARGET_RESULTS_NAME
FUSE_VALIDATOR_NAME = 'fuse-validator'
FUSE_VALIDATOR_DESCRIPTION = f'''Tool for validating a device\'s blown fuses. Payload requests generated via \'{GENERATE_PAYLOAD_NAME}\' are formatted for either on-target or off-target comparison. Devices respond to a payload request with a payload response of the same type. Off-target payload responses are compared via \'{COMPARE_NAME}\'. On-target payloads are displayed via \'{SHOW_ON_TARGET_RESULTS_NAME}\'.'''
FUSE_VALIDATOR_EPILOG = f'''For help menu of a specific operation: {BaseCMDLine.TOOL_NAME} {FUSE_VALIDATOR_NAME} <{OPERATION}> {HELP_ABBREV}'''
FUSE_VALIDATOR: CMDLineArgs = {
    HELP_GROUP: [
        ([
            HELP_ABBREV,
            HELP], {
            KWARGS_HELP: HELP_HELP,
            KWARGS_ACTION: KWARGS_HELP })] }
