
from typing import Any
from common.data.data import get_enabled_bit_indices_from_byte
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section.l2_associated_data.defines import L2_AD_KEY_LADDER_LENGTH, L2_AD_MINOR_VERSION_1
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section.l2_associated_data.v1_0.l2_associated_data import L2AssociatedDataV10

class L2AssociatedDataV11(L2AssociatedDataV10):
    MINOR_VERSION = L2_AD_MINOR_VERSION_1
    software_id_bitmap_upper: int = 127
    
    def __init__(self = None, data = None, check_is_type = None, bypass_validation = None):
        self.software_ids = []
        self.software_id_bitmap_upper = 0
        self.software_id_bitmap_lower = 0
        super().__init__(data, check_is_type, bypass_validation, **('data', 'check_is_type', 'bypass_validation'))

    
    def get_fields(cls = None):
        return [
            'reserved_0',
            'reserved_1',
            'major_version',
            'minor_version',
            'key_ladder_length',
            'reserved_2',
            'software_id_bitmap_lower',
            'software_id_bitmap_upper',
            'reserved_3']

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        return {
            'reserved_0': 0,
            'reserved_1': 0,
            'major_version': cls.MAJOR_VERSION,
            'minor_version': cls.MINOR_VERSION,
            'key_ladder_length': L2_AD_KEY_LADDER_LENGTH,
            'reserved_2': 0,
            'software_id_bitmap_lower': 0,
            'software_id_bitmap_upper': 0,
            'reserved_3': b'' }

    get_field_defaults = None(get_field_defaults)
    
    def get_format(cls = None):
        return '<BBBBBBQQ8s'

    get_format = None(get_format)
    
    def unpack_post_process(self = None):
        self.software_ids = get_enabled_bit_indices_from_byte(self.software_id_bitmap_lower) + get_enabled_bit_indices_from_byte(self.software_id_bitmap_upper, 64)

    
    def pack_pre_process(self = None):
        (self.software_id_bitmap_lower, self.software_id_bitmap_upper) = (0, 0)
        for software_id in self.software_ids:
            self.validate_software_id(software_id)
            if software_id < 64:
                self.software_id_bitmap_lower |= 1 << software_id
                continue
            self.software_id_bitmap_upper |= 1 << software_id - 64

    __classcell__ = None

