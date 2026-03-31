
from collections import defaultdict
from dataclasses import dataclass
from cmd_line_interface.base_defines import KWARGS_ACTION, KWARGS_CHOICES, KWARGS_DEFAULT, KWARGS_HELP, KWARGS_NARGS, KWARGS_STORE_TRUE, KWARGS_TYPE, XMLInfo, max_val_hex_type
from cmd_line_interface.basecmdline import CMDLineArgs
from cmd_line_interface.sectools import fuseblower
from cmd_line_interface.sectools.cmd_line_common.defines import GENERATE, SECURITY_PROFILE
from cmd_line_interface.sectools.fuseblower import FuseArgument
from cmd_line_interface.sectools.fuseblower.defines import FUSE_BLOWER, FUSE_BLOWER_NAME, FUSE_GROUP, FUSE_GROUPS_GROUP, FUSE_GROUP_HELP, RANDOM, RECOMMENDED_FUSES, RECOMMENDED_FUSES_GROUP, RECOMMENDED_FUSES_HELP
from cmd_line_interface.sectools.metadata import DEPENDS_ON
from common.logging.logger import log_debug
from common.utils import get_num_bits_from_range
from core.fuse_blower.utils import fuse_cmd_line_arg_string, fuse_group_string, is_fec_fuse
from core.fuseblower_profile_generator.defines import OEM_VALUE_XML
from profile.schema import FuseBlowing, Profile
EXPECTED_MULTI_ROW_FULL_REGION_FUSE_REGIONS_WITH_FEC = [
    'PK_HASH_0',
    'MRC_HASH',
    'PK_HASH',
    'OEM_PRODUCT_SEED',
    'TME_OEM_PRDT_SEED',
    'OEM_IMAGE_ENCRYPTION_KEY',
    'OEM_IMAGE_ENCRYPTION_KEY_0',
    'OEM_IMAGE_ENCRYPTION_KEY_1',
    'IMAGE_ENCRYPTION_KEY_1',
    'UIE_0',
    'UIE_1',
    'SEC_KEY_DERIVATION_KEY',
    'TME_OEM_MRC_HASH']
EXPECTED_MULTI_ROW_FULL_REGION_FUSE_REGIONS_WITHOUT_FEC = [
    'OEM_SPARE_0',
    'OEM_SPARE_1',
    'OEM_SPARE_2',
    'OEM_SPARE_3',
    'OEM_SPARE_27',
    'OEM_SPARE_28',
    'OEM_SPARE_29',
    'OEM_SPARE_30',
    'OEM_SPARE_31',
    'OEM_SPARE_REGION_31']
EXPECTED_MULTI_ROW_FULL_REGION_FUSE_REGIONS = EXPECTED_MULTI_ROW_FULL_REGION_FUSE_REGIONS_WITH_FEC + EXPECTED_MULTI_ROW_FULL_REGION_FUSE_REGIONS_WITHOUT_FEC
FuseArgumentInfo = dataclass(<NODE:12>)

def process_security_profile(profile = None):
    parsed_profile = profile.parsed_xml
    if float(parsed_profile.schema_version) < 1.3:
        raise RuntimeError(f'''Provided {SECURITY_PROFILE} is of schema version {parsed_profile.schema_version}. {FUSE_BLOWER_NAME} only supports {SECURITY_PROFILE} of schema version 1.3 or higher.''')
    if not None.fuse_blowing:
        raise RuntimeError(f'''Provided {SECURITY_PROFILE} does not support fuse-blowing features.''')
    return None.fuse_blowing


def get_non_fec_fuse_names_from_row(row = None):
    return list((lambda .0: pass# WARNING: Decompyle incomplete
)(row))


def compute_and_validate_multi_row_fuses(security_profile_data = None):
    log_debug('Computing list of multi-row fuses from Security Profile.')
    multi_row_full_region_fuses = { }
    multi_row_partial_region_fuses = { }
# WARNING: Decompyle incomplete


def set_multi_row_fuses():
    pass
# WARNING: Decompyle incomplete


def add_fuse_argument_to_commandline_dictionary(fuse_arg_name = None, fuse_arg_info = None, commandline_dictionary = None):
    if fuse_arg_info.number_of_bits > 1:
        is_byte_array = fuse_arg_name in fuseblower.multi_row_full_region_fuses
        arg_properties = {
            KWARGS_HELP: fuse_arg_info.description,
            KWARGS_TYPE: max_val_hex_type(pow(2, fuse_arg_info.number_of_bits) - 1, [
                RANDOM], is_byte_array, **('is_byte_array',)) }
    else:
        arg_properties = {
            KWARGS_HELP: fuse_arg_info.description,
            KWARGS_DEFAULT: False,
            KWARGS_ACTION: KWARGS_STORE_TRUE }
    commandline_dictionary[fuse_arg_info.argument_group].append(([
        fuse_arg_name], arg_properties, {
        DEPENDS_ON: [
            GENERATE] }))


def update_fuseblower_security_profile_arguments(security_profile = None):
    fuseblower.security_profile_data = process_security_profile(security_profile)
    set_multi_row_fuses()
    fuse_args = { }
    fuse_dict_updater = { }
# WARNING: Decompyle incomplete

