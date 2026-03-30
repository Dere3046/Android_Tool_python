
from copy import copy
from cmd_line_interface.base_defines import AutoCloseFileType, KWARGS_HELP, KWARGS_READ_BINARY, KWARGS_TYPE
from cmd_line_interface.basecmdline import BaseCMDLine, CMDLineArgs
from cmd_line_interface.sectools.cmd_line_common.defines import INFILE, REQUIRED_ARGUMENTS
from cmd_line_interface.sectools.fuse_validator.cmd_line_common.defines import FUSE_VALIDATOR_COMMON, GENERATE_PAYLOAD_NAME
from cmd_line_interface.sectools.fuse_validator.defines import FUSE_VALIDATOR_NAME
from cmd_line_interface.sectools.fuse_validator.generate_payload.defines import ON_TARGET
SHOW_ON_TARGET_RESULTS_DESCRIPTION = f'''Displays the mismatched fuses from an on-target fuse validator payload response. The fuse payload is received from the device after sending the fuse payload generated via: \'{BaseCMDLine.TOOL_NAME} {FUSE_VALIDATOR_NAME} {GENERATE_PAYLOAD_NAME} {ON_TARGET}\' to the device.'''
SHOW_ON_TARGET_RESULTS_INFILE_HELP = 'File path of on-target fuse validator response payload to be displayed.'
SHOW_ON_TARGET_RESULTS: CMDLineArgs = copy(FUSE_VALIDATOR_COMMON)
SHOW_ON_TARGET_RESULTS[REQUIRED_ARGUMENTS] = [
    ([
        INFILE], {
        KWARGS_HELP: SHOW_ON_TARGET_RESULTS_INFILE_HELP,
        KWARGS_TYPE: AutoCloseFileType(KWARGS_READ_BINARY) })]
