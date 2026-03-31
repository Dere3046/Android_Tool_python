
from copy import deepcopy
from cmd_line_interface.base_defines import AutoCloseFileType, KWARGS_HELP, KWARGS_READ_BINARY, KWARGS_REQUIRED, KWARGS_TYPE
from cmd_line_interface.basecmdline import BaseCMDLine, CMDLineArgs
from cmd_line_interface.sectools.cmd_line_common.defines import REQUIRED_ARGUMENTS
from cmd_line_interface.sectools.fuse_validator.cmd_line_common.defines import FUSE_VALIDATOR_COMMON, GENERATE_PAYLOAD_NAME
from cmd_line_interface.sectools.fuse_validator.defines import FUSE_VALIDATOR_NAME
COMPARE_DESCRIPTION = f'''Compares one or more Fuse Blower images against a fuse payload received from a device. The fuse payload is received from the device after sending the fuse payload generated via \'{BaseCMDLine.TOOL_NAME} {FUSE_VALIDATOR_NAME} {GENERATE_PAYLOAD_NAME}\' to the device.'''
PAYLOAD = '--payload'
PAYLOAD_HELP = 'File path of the fuse payload received from the device. The payload contains the fuse values of the device.'
COMPARE: CMDLineArgs = deepcopy(FUSE_VALIDATOR_COMMON)
COMPARE[REQUIRED_ARGUMENTS] += [
    ([
        PAYLOAD], {
        KWARGS_HELP: PAYLOAD_HELP,
        KWARGS_REQUIRED: True,
        KWARGS_TYPE: AutoCloseFileType(KWARGS_READ_BINARY) })]
