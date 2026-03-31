
'''
This file contains the changes and new arguments for the "Help" group as differs from the
cmd_line_interface.sectools.cmd_line_common.defines.
'''
from cmd_line_interface.base_defines import DYNAMIC_HELP_PLURAL, HELP, HELP_ABBREV, HELP_HELP, KWARGS_ACTION, KWARGS_COUNT, KWARGS_DEFAULT, KWARGS_HELP, KWARGS_STORE_TRUE
from cmd_line_interface.basecmdline import CMDLineGroup
from cmd_line_interface.sectools.cmd_line_common.base_defines import AVAILABLE_SIGNATURE_FORMATS
from cmd_line_interface.sectools.cmd_line_common.defines import AVAILABLE_DEVICE_RESTRICTIONS, AVAILABLE_DEVICE_RESTRICTIONS_COMMON_HELP, AVAILABLE_SEGMENT_HASH_ALGORITHMS, AVAILABLE_VARIANTS, EXTENDED_AVAILABLE_SIGNATURE_FORMATS_HELP, EXTENDED_AVAILABLE_VARIANTS_HELP, SIGNING_HELP, SIGNING_HELP_HELP, VERBOSE, VERBOSE_ABBREV, VERBOSE_HELP
from cmd_line_interface.sectools.metadata import CONSUMES, NA
from cmd_line_interface.sectools.secure_image.defines import EXTENDED_AVAILABLE_SEGMENT_HASH_ALGORITHMS_HELP
TME_EPILOG = f'''Some {DYNAMIC_HELP_PLURAL}'''
TME_HELP_HELP = f'''{HELP_HELP} {TME_EPILOG}'''
TME_HELP_GROUP: CMDLineGroup = [
    ([
        HELP_ABBREV,
        HELP], {
        KWARGS_HELP: TME_HELP_HELP,
        KWARGS_ACTION: KWARGS_STORE_TRUE }, {
        CONSUMES: [
            NA] }),
    ([
        VERBOSE_ABBREV,
        VERBOSE], {
        KWARGS_HELP: VERBOSE_HELP,
        KWARGS_DEFAULT: 0,
        KWARGS_ACTION: KWARGS_COUNT }, {
        CONSUMES: [
            NA] }),
    ([
        AVAILABLE_VARIANTS], {
        KWARGS_HELP: EXTENDED_AVAILABLE_VARIANTS_HELP,
        KWARGS_ACTION: KWARGS_STORE_TRUE }),
    ([
        AVAILABLE_SEGMENT_HASH_ALGORITHMS], {
        KWARGS_HELP: EXTENDED_AVAILABLE_SEGMENT_HASH_ALGORITHMS_HELP,
        KWARGS_ACTION: KWARGS_STORE_TRUE }),
    ([
        AVAILABLE_DEVICE_RESTRICTIONS], {
        KWARGS_HELP: AVAILABLE_DEVICE_RESTRICTIONS_COMMON_HELP,
        KWARGS_ACTION: KWARGS_STORE_TRUE }),
    ([
        SIGNING_HELP], {
        KWARGS_HELP: SIGNING_HELP_HELP,
        KWARGS_ACTION: KWARGS_STORE_TRUE }),
    ([
        AVAILABLE_SIGNATURE_FORMATS], {
        KWARGS_HELP: EXTENDED_AVAILABLE_SIGNATURE_FORMATS_HELP,
        KWARGS_ACTION: KWARGS_STORE_TRUE })]
