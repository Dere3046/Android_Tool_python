
from copy import deepcopy
from cmd_line_interface.base_defines import AutoCloseFileType, KWARGS_ACTION, KWARGS_DEFAULT, KWARGS_HELP, KWARGS_REQUIRED, KWARGS_STORE_TRUE, KWARGS_TYPE, KWARGS_WRITE_BINARY
from cmd_line_interface.basecmdline import BaseCMDLine, CMDLineArgs
from cmd_line_interface.sectools.cmd_line_common.defines import OPTIONAL_ARGUMENTS, OUTFILE, REQUIRED_ARGUMENTS
from cmd_line_interface.sectools.fuse_validator.cmd_line_common.defines import COMPARE_NAME, FUSE_VALIDATOR_COMMON, SHOW_ON_TARGET_RESULTS_NAME
from cmd_line_interface.sectools.fuse_validator.defines import FUSE_VALIDATOR_NAME
GENERATE_PAYLOAD_DESCRIPTION = 'Generates a payload request. When sent to a device, the payload request specifies which fuse values to report back for fuse comparison.'
ON_TARGET = '--on-target'
OUTFILE_HELP = 'File path of the payload request.'
ON_TARGET_HELP = f'''If provided, the payload request is generated for on-target fuse comparison and the returned payload response is viewed via \'{BaseCMDLine.TOOL_NAME} {FUSE_VALIDATOR_NAME} {SHOW_ON_TARGET_RESULTS_NAME}\'. If not provided, the payload request is generated for off-target comparison and the returned payload response is compared via \'{BaseCMDLine.TOOL_NAME} {FUSE_VALIDATOR_NAME} {COMPARE_NAME}\'.'''
GENERATE_PAYLOAD: CMDLineArgs = deepcopy(FUSE_VALIDATOR_COMMON)
GENERATE_PAYLOAD[REQUIRED_ARGUMENTS] += [
    ([
        OUTFILE], {
        KWARGS_HELP: OUTFILE_HELP,
        KWARGS_REQUIRED: True,
        KWARGS_TYPE: AutoCloseFileType(KWARGS_WRITE_BINARY) })]
GENERATE_PAYLOAD[OPTIONAL_ARGUMENTS] = [
    ([
        ON_TARGET], {
        KWARGS_HELP: ON_TARGET_HELP,
        KWARGS_DEFAULT: False,
        KWARGS_ACTION: KWARGS_STORE_TRUE })]
