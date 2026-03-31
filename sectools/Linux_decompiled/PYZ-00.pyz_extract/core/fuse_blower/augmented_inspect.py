
from math import ceil
import profile
from cmd_line_interface.sectools import fuseblower
from common.data.data import hex_val, properties_repr, split_long_row
from common.parser.fuse_validator_payload.fuse_list.defines import FuseEntryUnion
from common.parser.sec_dat.defines import BLOW_RANDOM_OPERATION
from core.fuse_blower.utils import FuseDescription, fuse_cmd_line_arg_string, get_fuse_descriptions, get_fuse_value_from_start_end_range, is_fec_fuse, is_lsb
NOT_IN_PROFILE_DESCRIPTION = 'Description not in Security Profile.'
RANDOM_VALUE = 'RANDOM'

def get_augmented_fuse_entries_table(fuse_entries = None):
    headers = [
        'Region',
        'Address',
        'Bits',
        'Fuse Name',
        'Fuse Value',
        'Fuse Description']
    if include_recommended_values = bool(fuseblower.recommended_fuses_qti_values):
        headers.insert(-1, 'Recommended Value')
    table = [
        tuple(headers)]
    sep_rows = []
    empty_row = tuple((lambda .0: for _ in .0:
'')(range(len(headers))))
# WARNING: Decompyle incomplete


def _get_properties_with_value(fuse_description = None, fuse_entry = None, include_recommended_value = None):
    '''Returns a tuple of properties which are displayed in the augmented inspect table for fuse blower images.'''
    if isinstance(fuse_description.bits, int):
        bits = str(fuse_description.bits)
        value = '1' if fuse_entry.lsb if is_lsb(fuse_description.bits) else fuse_entry.msb & 1 << fuse_description.bits % 32 else '0'
    else:
        bits = f'''{fuse_description.bits[1]}:{fuse_description.bits[0]}'''
        (start_bit, end_bit) = fuse_description.bits
        fuse_name = fuse_cmd_line_arg_string(fuse_description.name)
        value_int = get_fuse_value_from_start_end_range(fuse_entry, start_bit, end_bit, fuse_name in fuseblower.multi_row_full_region_fuses)
        value = hex_val(value_int, ceil(((end_bit - start_bit) + 1) / 4), fuse_name not in fuseblower.multi_row_full_region_fuses, **('num_chars', 'strip_leading_zeros'))
    returned_value = RANDOM_VALUE if fuse_entry.OPERATION_INT_TO_DESCRIPTION[fuse_entry.operation] == BLOW_RANDOM_OPERATION else value
    properties = [
        bits,
        fuse_description.name,
        returned_value,
        fuse_description.description]
    if include_recommended_value:
        properties.insert(-1, fuse_description.recommended_value if fuse_description.recommended_value is not None else '')
    return properties


def _get_descriptions_of_interest(descriptions_list = None, fuse_entry = None, use_recommended_value = None):
    descriptions_of_interest = []
    for description in descriptions_list:
        properties = _get_properties_with_value(description, fuse_entry, use_recommended_value)
        fuse_value = properties[2]
        if fuse_value == RANDOM_VALUE and description.description != NOT_IN_PROFILE_DESCRIPTION or is_fec_fuse(description.name) or fuse_value != RANDOM_VALUE:
            if len(descriptions_of_interest) or is_fec_fuse(description.name) or int(fuse_value, 16) != 0:
                descriptions_of_interest.append(tuple(properties))
    return descriptions_of_interest


def _add_missing_fuses(fuse_descriptions = None):
    filled_list = []
    end_bit = -1
    for fuse_description in fuse_descriptions:
        start_bit = fuse_description.bits[0] if isinstance(fuse_description.bits, tuple) else fuse_description.bits
        if start_bit > end_bit + 1:
            missing_bits = (end_bit + 1, start_bit - 1) if start_bit != end_bit + 2 else end_bit + 1
            filled_list.append(FuseDescription('', missing_bits, '', NOT_IN_PROFILE_DESCRIPTION, None))
        filled_list.append(fuse_description)
        end_bit = fuse_description.bits[1] if isinstance(fuse_description.bits, tuple) else fuse_description.bits
# WARNING: Decompyle incomplete

