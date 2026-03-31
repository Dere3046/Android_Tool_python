
import re
from functools import partial
from itertools import chain
from operator import methodcaller
from typing import cast
from cmd_line_interface.sectools.cmd_line_common.auto_close_image_type import ImageWithPath
from cmd_line_interface.sectools.cmd_line_common.base_defines import SECURITY_PROFILE
from common.data.data import hex_val, plural_s
from common.data.defines import SHA384_SIZE, SHA_SIZE_TO_DESCRIPTION
from common.logging.logger import log_debug
from common.parser.hash_segment.defines import AUTHORITY_OEM, AUTHORITY_QTI
from common.parser.hash_segment.hash_segment_common import HashTableSegmentCommon
from common.parser.sec_dat.sec_dat import SecDat
from common.parser.sec_elf.sec_elf import SecELF
from common.parser.sec_elf_with_hash_segment.sec_elf_with_hash_segment import SecELFWithHashTableSegment
from core.fuse_blower.utils import get_fuse_descriptions
from core.secure_image.validate.fuse_value_getter import FuseAddress, get_fuse_value
from core.secure_image.validate.show_value_comparison_table import make_value_comparison_table
from profile.schema import FuseBlowing, FuseRegion
RCH_FUSE_NAMES = ('Root Certificate Hash', [
    'OEM_PK_HASH',
    'MRC_HASH',
    'PK_HASH',
    'PK_HASH_0',
    'TME_OEM_MRC_HASH'])
OEM_ID_FUSE_NAMES = ('OEM ID', [
    'OEM_HW_ID'])
OEM_PRODUCT_ID_FUSE_NAMES = ('OEM Product ID', [
    'OEM_PRODUCT_ID'])

def get_fuse_blower_images_mismatches(infile = None, fuse_blower_images = None, security_profile = None):
    errors_table = _get_fuse_mismatches(infile, fuse_blower_images, security_profile)
    if errors_table:
        return f'''The following values mismatch in validation against Fuse Blower Image{plural_s(fuse_blower_images)}.\n''' + make_value_comparison_table(errors_table)


def _get_fuse_mismatches(infile_with_path = None, fuse_blower_image_list = None, security_profile = None):
    fuse_name_to_addresses = _get_fuse_name_to_addresses(security_profile.fuse_regions.fuse_region)
    get_rch_from_fuses = partial(get_fuse_value, RCH_FUSE_NAMES, 'Root Certificate Hash', None, fuse_name_to_addresses, True)
    get_oem_id_from_fuses = partial(get_fuse_value, OEM_ID_FUSE_NAMES, 'OEM ID', 0, fuse_name_to_addresses, False)
    get_oem_prod_id_from_fuses = partial(get_fuse_value, OEM_PRODUCT_ID_FUSE_NAMES, 'OEM Product ID', 0, fuse_name_to_addresses, False)
    fuse_blower_images = (lambda .0: [ image_with_path.image for image_with_path in .0 ])(fuse_blower_image_list)
    fuse_values = (lambda .0 = None: pass# WARNING: Decompyle incomplete
)((('Root Certificate Hash', get_rch_from_fuses), ('OEM ID', get_oem_id_from_fuses), ('OEM Product ID', get_oem_prod_id_from_fuses)))
    get_oem_id_from_image = partial(_get_unique_bound_value_from_image, 'get_oem_id')
    get_oem_product_id_from_image = partial(_get_unique_bound_value_from_image, 'get_oem_product_id')
    mismatches = []
    for image, path in chain((infile_with_path.as_tuple(),), (lambda .0: for image_with_path in .0:
if isinstance(image_with_path.image, SecELFWithHashTableSegment):
image_with_path.as_tuple()continueNone)(fuse_blower_image_list)):
        for field_name, infile_getter, compare_function in (('Root Certificate Hash', _get_rchs_from_image, _compare_rchs), ('OEM ID', get_oem_id_from_image, _compare_optional_strs), ('OEM Product ID', get_oem_product_id_from_image, _compare_optional_strs)):
            log_debug(f'''Comparing {field_name}.''')
            for authority in (AUTHORITY_OEM, AUTHORITY_QTI):
                compare_res = compare_function(infile_getter(image, authority), fuse_values[field_name])
                if compare_res:
                    mismatches.append({
                        'Image Path': path,
                        'Attribute': field_name,
                        'Authority': authority } | compare_res)
    return mismatches


def _compare_optional_strs(image_value = None, fuse_value = None):
    if image_value is not None and image_value != fuse_value:
        return {
            'Image Value': image_value,
            'Fuse Blower Image Value': fuse_value }


def _compare_rchs(image_rchs = None, fuse_rch = None):
    compare_result = None
    if not fuse_rch is not None and len(image_rchs) > 0 and None(None((lambda x = None: if x:
passx == cast(str, fuse_rch)[:len(x)]), image_rchs)):
        if fuse_rch:
            last_nonzero_idx = list(re.finditer('[1-9a-fA-F]', fuse_rch))[-1].end()
            nearest_valid_hash_length = None(None((lambda x = None: x - last_nonzero_idx >= 0), sorted(map(len, image_rchs))))
            image_rch = None(None((lambda x = None: len(x) == nearest_valid_hash_length), image_rchs))
            fuse_rch = fuse_rch[:nearest_valid_hash_length]
        else:
            image_rch = next(filter((lambda x: len(x) == SHA384_SIZE + 2), image_rchs))
            fuse_rch = f'''0x{0