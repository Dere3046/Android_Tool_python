
from typing import Any, Dict, List, Tuple
from common.data.binary_struct import StructBase
from common.data.data import hex_val, reverse
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section_header.defines import EPSH_MAG, ROOT_KEY_TYPE_DESCRIPTION, ROOT_KEY_TYPE_OTP_OEM
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section_header.v1_0.defines import KEY_LADDER_ALGO_AES, KEY_LADDER_ALGO_DESCRIPTION, KEY_LADDER_MODE_CCM, KEY_LADDER_MODE_DESCRIPTION, SECTION_SIZE

class SectionHeaderV1(StructBase):
    reserved_1: int = 'SectionHeaderV1'
    
    def get_fields(cls = None):
        return [
            'magic',
            'section_size',
            'key_ladder_algorithm',
            'key_ladder_mode',
            'reserved_0',
            'root_key_type',
            'root_key_info_id',
            'reserved_1']

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        return {
            'magic': EPSH_MAG,
            'section_size': SECTION_SIZE,
            'key_ladder_algorithm': KEY_LADDER_ALGO_AES,
            'key_ladder_mode': KEY_LADDER_MODE_CCM,
            'reserved_0': 0,
            'root_key_type': ROOT_KEY_TYPE_OTP_OEM,
            'root_key_info_id': 0,
            'reserved_1': 0 }

    get_field_defaults = None(get_field_defaults)
    
    def get_format(cls = None):
        return '<4sHBBBBHI'

    get_format = None(get_format)
    
    def validate_critical_fields(self):
        if self.magic != EPSH_MAG:
            raise RuntimeError(f'''Encryption Parameter Section Header contains invalid Magic: {self.magic}.''')

    
    def validate(self = None):
        self.validate_critical_fields()

    
    def validate_before_operation(self = None, **_):
        if self.section_size != SECTION_SIZE:
            raise RuntimeError(f'''Encryption Parameter Section Header specifies invalid Section Size: {self.section_size}.''')
        if None.key_ladder_algorithm not in KEY_LADDER_ALGO_DESCRIPTION:
            raise RuntimeError(f'''Encryption Parameter Section Header specifies invalid Key Ladder Algorithm: {self.key_ladder_algorithm}.''')
        if None.key_ladder_mode not in KEY_LADDER_MODE_DESCRIPTION:
            raise RuntimeError(f'''Encryption Parameter Section Header specifies invalid Key Ladder Mode: {self.key_ladder_mode}.''')
        if None.root_key_type not in ROOT_KEY_TYPE_DESCRIPTION:
            raise RuntimeError(f'''Encryption Parameter Section Header specifies invalid Root Key Type: {self.root_key_type}.''')

    
    def get_properties(self = None):
        pass
    # WARNING: Decompyle incomplete


