
from typing import Any, Dict, List, Tuple
from common.data.binary_struct import StructBase
from common.data.data import reverse
from common.parser.elf_with_hash_segment.uie_encryption_parameters.defines import EPIH_MAG, NUM_EPS, RESERVED
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section_header.defines import EPS_MAJOR_VERSION_1, EPS_MAJOR_VERSION_2, EPS_MINOR_VERSION_0

class InfoHeader(StructBase):
    eps2_minor_version: int = 'InfoHeader'
    
    def get_fields(cls = None):
        return [
            'magic',
            'num_eps',
            'reserved_0',
            'reserved_1',
            'reserved_2',
            'eps1_offset',
            'eps1_major_version',
            'eps1_minor_version',
            'eps2_offset',
            'eps2_major_version',
            'eps2_minor_version']

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        return {
            'magic': EPIH_MAG,
            'num_eps': NUM_EPS,
            'reserved_0': 0,
            'reserved_1': 0,
            'reserved_2': 0,
            'eps1_offset': cls.get_size(),
            'eps1_major_version': EPS_MAJOR_VERSION_1,
            'eps1_minor_version': EPS_MINOR_VERSION_0,
            'eps2_offset': 0,
            'eps2_major_version': 0,
            'eps2_minor_version': 0 }

    get_field_defaults = None(get_field_defaults)
    
    def get_format(cls = None):
        return '<4sBBBBHBBHBB'

    get_format = None(get_format)
    
    def validate_critical_fields(self):
        if self.magic != EPIH_MAG:
            raise RuntimeError(f'''Encryption Parameter Info Header contains invalid Magic: {self.magic}.''')

    
    def validate(self = None):
        self.validate_critical_fields()
        if self.num_eps != NUM_EPS:
            raise RuntimeError(f'''Encryption Parameter Info Header specifies unsupported number of Sections: {self.num_eps}.''')
        if None.eps1_offset != self.get_size():
            raise RuntimeError(f'''Encryption Parameter Section has invalid Offset: {self.eps1_offset}.''')
        if None.eps1_major_version not in (EPS_MAJOR_VERSION_1, EPS_MAJOR_VERSION_2):
            raise RuntimeError(f'''Encryption Parameter Section has invalid Major Version: {self.eps1_major_version}.''')
        if None.eps1_minor_version != EPS_MINOR_VERSION_0:
            raise RuntimeError(f'''Encryption Parameter Section has invalid Minor Version: {self.eps1_minor_version}.''')
        if None.eps2_offset != RESERVED:
            raise RuntimeError(f'''Encryption Parameter Section 2 has invalid Offset: {self.eps2_offset}.''')
        if None.eps2_major_version != RESERVED:
            raise RuntimeError(f'''Encryption Parameter Section 2 has invalid Major Version: {self.eps2_major_version}.''')
        if None.eps2_minor_version != RESERVED:
            raise RuntimeError(f'''Encryption Parameter Section 2 has invalid Minor Version: {self.eps2_minor_version}.''')

    
    def get_properties(self = None):
        pass
    # WARNING: Decompyle incomplete


