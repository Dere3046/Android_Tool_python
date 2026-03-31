
from typing import NamedTuple
from cmd_line_interface.sectools.cmd_line_common.base_defines import SECURITY_PROFILE
from cmd_line_interface.sectools.cmd_line_common.defines import FUSE_BLOWER_IMAGES
from common.data.data import a_or_an, hex_val
from common.logging.logger import log_debug, log_warning
from common.parser.sec_dat.sec_dat import SecDat
from common.parser.sec_elf.sec_elf import SecELF
from core.fuse_blower.utils import get_fuse_value_from_start_end_range
FuseAddress = NamedTuple('FuseAddress', [
    ('row_address', int),
    ('first_bit', int),
    ('last_bit', int)])

def get_fuse_value(fuse_names, field_name, default_val = None, fuse_name_to_addresses = None, retain_leading_zeros = None, fuse_blower_images = ('fuse_names', tuple[(str, list[str])], 'field_name', str, 'default_val', int | None, 'fuse_name_to_addresses', dict[(str, list[FuseAddress])], 'retain_leading_zeros', bool, 'fuse_blower_images', list[SecDat | SecELF], 'return', str | None)):
    (addresses, used_name) = _get_addresses_from_names(fuse_name_to_addresses, fuse_names)
    value = default_val
    if addresses:
        for fuse_blower_image in fuse_blower_images:
            fuse_blower_image_value = _get_combined_fuse_value(fuse_blower_image, addresses, retain_leading_zeros)
            if fuse_blower_image_value is not None:
                if value == default_val or fuse_blower_image_value != default_val:
                    if value not in (None, default_val, fuse_blower_image_value):
                        raise RuntimeError(f'''{FUSE_BLOWER_IMAGES} have conflicting values for {field_name}.''')
                    value = None
    else:
        log_warning(f'''{SECURITY_PROFILE} does not contain {a_or_an(field_name)} fuse.''')
    if addresses and value is None:
        log_warning(f'''None of the provided Fuse Blower images contain a {field_name}.''')
    if value is not None:
        if retain_leading_zeros:
            return f'''0x{value}'''
        return f'''{None:#x}'''


def _get_addresses_from_names(address_dict = None, possible_names = None):
    addresses = None
    used_name = ''
    (user_friendly_name, worksheet_names) = possible_names
    for name in worksheet_names:
        if addresses_at_name = address_dict.get(name):
            if addresses is None:
                addresses = addresses_at_name
                used_name = name
                continue
            raise RuntimeError(f'''{SECURITY_PROFILE} contains multiple fuse descriptions for {user_friendly_name}: {used_name} and {name}. Cannot determine which address to use for comparison.''')
        return (addresses, used_name)


def _get_combined_fuse_value(fuse_blower_image = None, fuse_addresses = None, retain_leading_zeros = None):
    complete_value_hex = ''
    complete_value = 0
    log_debug('Combining fuses to get complete value.')
    fuse_entries = fuse_blower_image.get_fuse_entries()
    is_multi_row_fuse = len((lambda .0: pass# WARNING: Decompyle incomplete
)(fuse_addresses)) > 1
    for address, start_bit, end_bit in sorted(fuse_addresses):
        relevant_fuse = None((lambda .0 = None: for fuse in .0:
if fuse.address == address:
fusecontinueNone)(fuse_entries), None)
        if relevant_fuse is None:
            continue
        value = get_fuse_value_from_start_end_range(relevant_fuse, start_bit, end_bit, is_multi_row_fuse)
        bit_length = (end_bit - start_bit) + 1
        complete_value = (complete_value << bit_length) + value
        complete_value_hex += hex_val(value, bit_length // 4, True, **('num_chars', 'without_0x'))
    if retain_leading_zeros:
        if complete_value:
            return complete_value_hex
        return None
    if not None:
        pass

