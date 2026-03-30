
from dataclasses import dataclass
from math import ceil
from re import search
from cmd_line_interface.sectools import fuseblower
from common.data.defines import BIG_ENDIAN, LITTLE_ENDIAN
from common.parser.fuse_validator_payload.fuse_list.defines import FuseEntryUnion
from common.utils import get_start_and_end_indices, is_multi_bit
from core.fuse_blower.defines import FEC_FUSE_SIZE
from profile.schema import FuseRegion, ProfileParser
FuseDescription = dataclass(<NODE:12>)

def fuse_cmd_line_arg_string(fuse_name = None):
    return f'''--fuse-{fuse_name.replace(' ', '-').replace('_', '-').replace('.', '-').lower()}'''


def fuse_group_string(name = None):
    return name.strip().replace('_', '-').upper()


def fuse_parsed_arg_string(fuse_name = None):
    return f'''fuse_{fuse_name.replace(' ', '_').replace('.', '_').lower()}'''


def is_lsb(bit_number = None):
    return bit_number < 32


def is_fec_fuse(fuse_name = None):
    return bool(search('^FEC_[0-9]+(_[0-9]+)*$', fuse_name))


def contains_fec_fuses(fuse_row = None):
    return any((lambda .0: for fuse in .0:
if is_fec_fuse(fuse.name):
passis_multi_bit(fuse.bits))(fuse_row.fuse))


def compute_fec(data = None):
    '''
    computes 7 fec bits from a 56 bit data
    '''
    lfsr = 0
    for bit_position in range(0, 56):
        temp = lfsr & 1 ^ data >> bit_position & 1
        lfsr = (lfsr >> 1 & 1 ^ temp) << 0 | (lfsr >> 2 & 1) << 1 | (lfsr >> 3 & 1) << 2 | (lfsr >> 4 & 1) << 3 | (lfsr >> 5 & 1 ^ temp) << 4 | (lfsr >> 6 & 1) << 5 | temp << 6
    return lfsr & get_bit_mask(FEC_FUSE_SIZE)


def get_bit_mask(number_of_bits = None):
    return int(hex(pow(2, number_of_bits) - 1), 16)


def get_fuse_value_from_start_end_range(fuse = None, start_bit = None, end_bit = None, is_multi_row_full_region_fuse = ('fuse', FuseEntryUnion, 'start_bit', int, 'end_bit', int, 'is_multi_row_full_region_fuse', bool, 'return', int)):
    value = (fuse.lsb + (fuse.msb << 32) & sum((lambda .0: for i in .0:
1 << i)(range(start_bit, end_bit + 1)))) >> start_bit
    if is_multi_row_full_region_fuse:
        num_bytes_needed = ceil(((end_bit - start_bit) + 1) / 8)
        value = int.from_bytes(value.to_bytes(num_bytes_needed, LITTLE_ENDIAN, **('length', 'byteorder')), BIG_ENDIAN, **('byteorder',))
    return value


def get_recommended_fuse_value(fuse_arg = None):
    if fuse_arg in fuseblower.recommended_fuses_oem_values:
        return 'OEM Value'
    return None.recommended_fuses_qti_values.get(fuse_arg)


def get_fuse_descriptions(fuse_regions = None):
    fuse_descriptions = { }
    described_fuse_names = { }
    for fuse_region in fuse_regions:
        for fuse_row in fuse_region.fuse_row:
            for fuse_des in fuse_row.fuse:
                bits = get_start_and_end_indices(fuse_des.bits) if is_multi_bit(fuse_des.bits) else int(fuse_des.bits)
                if not fuse_des.description:
                    pass
                description = ' '.join(''.split())
                if description:
                    described_fuse_names[fuse_des.name] = description
                description = described_fuse_names.get(fuse_des.name, description)
                f_des = FuseDescription(fuse_region.get_id().upper().replace('_', ' '), bits, fuse_des.name, description, get_recommended_fuse_value(fuse_cmd_line_arg_string(fuse_des.name)))
                fuse_descriptions.setdefault(fuse_row.address.lower(), []).append(f_des)
    return fuse_descriptions

