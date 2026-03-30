
from struct import pack, unpack
from typing import Callable, NamedTuple, Optional
from cmd_line_interface.sectools.secure_image.defines import SECURE_IMAGE_NAME
from common.data.data import comma_separated_string, plural_s
from common.logging.logger import log_warning
from common.parser.tme.dpr.validation_utils import get_cmd_arg_by_consumed_tme_tag_name
from common.parser.tme.tme_parser.defines import CHIP_UNIQUE_IDENTIFIER_PATH, DP_CHIP_CONSTRAINTS_PATH
from common.parser.tme.tme_parser.tme import TME
from core.base_device_restrictions import BaseDeviceRestrictions
from profile.defines import JTAG_IDS, SOC_FEATURE_IDS, SOC_HW_VERSIONS

class Mapping(NamedTuple):
    merge_rule_func: Callable = '\n    TME Chip Constraints to Common Device Restrictions mapping record.\n    To keep variables descriptive and short, using abbreviations the "cc_..." for Chip Constraints\n    and "cdr_..." for the Common Device Restrictions.\n    '


def convert_str_to_int(tme_value):
    pass
# WARNING: Decompyle incomplete


def convert_str_to_int_array(tme_value):
    return [
        convert_str_to_int(tme_value)]


def convert_single_value_str_list_to_str(tme_value):
    '''
    In TME the value is a list, in ELF - scalar. However Sectools allows only one value for TME. Therefore that is
    similar to the scalar rule.
    '''
    pass
# WARNING: Decompyle incomplete


def convert_chip_unique_identifier_to_list(tme_value):
    '''
    A special converter that extracts multiple values from TME ChipUniqueIdentifier and converts these to a
    fully qualified list of device serial numbers.
    '''
    pass
# WARNING: Decompyle incomplete


def convert_soc_hw_versions_to_array(tme_value):
    '''A special case, have to keep only 2 most significant bytes (assuming 4 bytes integer).'''
    return [
        convert_str_to_int(tme_value) >> 16]


def scalar_rule(current_value, new_value, default_value):
    '''Bind only if both matching, otherwise fall into the default.'''
    if current_value != new_value:
        current_value = default_value
    return current_value


def array_to_array_rule(current_value, new_value, _):
    pass
# WARNING: Decompyle incomplete

MAPPINGS = [
    Mapping(f'''{DP_CHIP_CONSTRAINTS_PATH}/SocHardwareVersion''', SOC_HW_VERSIONS, convert_soc_hw_versions_to_array, array_to_array_rule),
    Mapping(f'''{DP_CHIP_CONSTRAINTS_PATH}/OemIdentifier''', 'oem_id', convert_str_to_int, scalar_rule),
    Mapping(f'''{DP_CHIP_CONSTRAINTS_PATH}/OemProductIdentifier''', 'oem_product_id', convert_str_to_int, scalar_rule),
    Mapping(f'''{DP_CHIP_CONSTRAINTS_PATH}/SocFeatureIdentifier''', SOC_FEATURE_IDS, convert_str_to_int_array, scalar_rule),
    Mapping(f'''{DP_CHIP_CONSTRAINTS_PATH}/SocJtagIdentifier''', JTAG_IDS, convert_str_to_int_array, scalar_rule),
    Mapping(f'''{DP_CHIP_CONSTRAINTS_PATH}/OemLifeCycleState''', 'oem_lifecycle_state', convert_single_value_str_list_to_str, scalar_rule),
    Mapping(CHIP_UNIQUE_IDENTIFIER_PATH, 'serial_number', convert_chip_unique_identifier_to_list, array_to_array_rule)]

def apply_chip_constraints_to_device_restrictions(device_restrictions = None, chip_constraints = None):
    '''
    Converts TME chip constraints to CommonDeviceRestrictions.
    The first device_restrictions can be None to indicate that there are no current bindings, and TME chip constraints
    will one-to-one converted to CommonDeviceRestrictions.
    '''
    if not device_restrictions:
        pass
    ret_cdr = BaseDeviceRestrictions(False, **('serial_numbers_fatal',))
    default_cdr = BaseDeviceRestrictions()
    for cc_path, cdr_property_name, tme_conversion_func, merge_rule_func in MAPPINGS:
        default_value = vars(default_cdr)[cdr_property_name]
        ret_value = default_value
        if chip_constraints.is_item(cc_path):
            new_value = tme_conversion_func(chip_constraints.get_item(cc_path))
            current_value = getattr(ret_cdr, cdr_property_name)
            if device_restrictions is None and current_value == default_value:
                current_value = new_value
            if current_value != default_value:
                ret_value = merge_rule_func(current_value, new_value, default_value)
            if ret_value == default_value:
                if current_value != default_value or new_value != default_value:
                    tmp_name = cc_path.split('/')[-1]
                    tmp_args = get_cmd_arg_by_consumed_tme_tag_name(cc_path)
                    log_warning(f'''The OEM Debug Policy ELF will not be bound to {tmp_name} as it contains two or more DPRs with incompatible device restrictions. If you require an OEM Debug Policy ELF bound to {tmp_name}, create DPRs which are all bound to {tmp_name} by using {comma_separated_string(tmp_args, 'and')} command-line argument{plural_s(tmp_args)}. Alternatively you can re-sign the OEM Debug Policy ELF via {SECURE_IMAGE_NAME} to achieve any desired Hash Table Segment device restrictions.''')
        setattr(ret_cdr, cdr_property_name, ret_value)
    return ret_cdr

