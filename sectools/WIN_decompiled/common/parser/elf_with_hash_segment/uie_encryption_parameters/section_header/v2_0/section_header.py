
from typing import Any, Dict, List, Optional, Tuple, Union
from common.data.data import get_lsb, hex_val, reverse
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section_header.defines import EPSH_MAG, ROOT_KEY_TYPE_DESCRIPTION, ROOT_KEY_TYPE_OTP_OEM
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section_header.v1_0.section_header import SectionHeaderV1
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section_header.v2_0.defines import KEY_LADDER_ALGO_AES, KEY_LADDER_ALGO_DESCRIPTION, KEY_LADDER_ALGO_ECIESAD, KEY_LADDER_MODE_CCM, KEY_LADDER_MODE_DESCRIPTION, KEY_LADDER_MODE_ECCP256_HMACSHA256, SECTION_SIZE

class SectionHeaderV2(SectionHeaderV1):
    KEY_MODE_MASK = 15
    KEY_ALGORITHM_MASK = 240
    
    def __init__(self = None, data = None, check_is_type = None, bypass_validation = None):
        self.l2_key_algorithm_info = 0
        self.l3_key_algorithm_info = 0
        self.l2_key_algorithm = 0
        self.l2_key_mode = 0
        self.l3_key_algorithm = 0
        self.l3_key_mode = 0
        super().__init__(data, check_is_type, bypass_validation, **('data', 'check_is_type', 'bypass_validation'))

    
    def get_fields(cls = None):
        return [
            'magic',
            'section_size',
            'l2_key_algorithm_info',
            'l3_key_algorithm_info',
            'reserved_0',
            'root_key_type',
            'root_key_info_id',
            'reserved_1']

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        return {
            'magic': EPSH_MAG,
            'section_size': SECTION_SIZE,
            'l2_key_algorithm_info': KEY_LADDER_MODE_ECCP256_HMACSHA256 | KEY_LADDER_ALGO_ECIESAD << get_lsb(cls.KEY_ALGORITHM_MASK),
            'l3_key_algorithm_info': KEY_LADDER_MODE_CCM | KEY_LADDER_ALGO_AES << get_lsb(cls.KEY_ALGORITHM_MASK),
            'reserved_0': 0,
            'root_key_type': ROOT_KEY_TYPE_OTP_OEM,
            'root_key_info_id': 0,
            'reserved_1': 0 }

    get_field_defaults = None(get_field_defaults)
    
    def unpack_post_process(self = None):
        self.l2_key_mode = self.l2_key_algorithm_info & self.KEY_MODE_MASK
        self.l2_key_algorithm = (self.l2_key_algorithm_info & self.KEY_ALGORITHM_MASK) >> get_lsb(self.KEY_ALGORITHM_MASK)
        self.l3_key_mode = self.l3_key_algorithm_info & self.KEY_MODE_MASK
        self.l3_key_algorithm = (self.l3_key_algorithm_info & self.KEY_ALGORITHM_MASK) >> get_lsb(self.KEY_ALGORITHM_MASK)

    
    def pack_pre_process(self = None):
        self.l2_key_algorithm_info = self.l2_key_mode | self.l2_key_algorithm << get_lsb(self.KEY_ALGORITHM_MASK)
        self.l3_key_algorithm_info = self.l3_key_mode | self.l3_key_algorithm << get_lsb(self.KEY_ALGORITHM_MASK)

    
    def validate_before_operation(self = None, **_):
        if self.section_size != SECTION_SIZE:
            raise RuntimeError(f'''Encryption Parameter Section Header specifies invalid Section Size: {self.section_size}.''')
        if None.l2_key_algorithm not in KEY_LADDER_ALGO_DESCRIPTION:
            raise RuntimeError(f'''Encryption Parameter Section Header specifies invalid L2 Key Algorithm: {self.l2_key_algorithm}.''')
        if (None.l2_key_algorithm, self.l2_key_mode) not in KEY_LADDER_MODE_DESCRIPTION:
            raise RuntimeError(f'''Encryption Parameter Section Header specifies invalid L2 Key Mode: {self.l2_key_mode}.''')
        if None.l3_key_algorithm not in KEY_LADDER_ALGO_DESCRIPTION:
            raise RuntimeError(f'''Encryption Parameter Section Header specifies invalid L3 Key Algorithm: {self.l3_key_algorithm}.''')
        if (None.l3_key_algorithm, self.l3_key_mode) not in KEY_LADDER_MODE_DESCRIPTION:
            raise RuntimeError(f'''Encryption Parameter Section Header specifies invalid L3 Key Mode: {self.l3_key_mode}.''')
        if None.root_key_type not in ROOT_KEY_TYPE_DESCRIPTION:
            raise RuntimeError(f'''Encryption Parameter Section Header specifies invalid Root Key Type: {self.root_key_type}.''')

    
    def get_properties(self = None):
        pass
    # WARNING: Decompyle incomplete

    __classcell__ = None

