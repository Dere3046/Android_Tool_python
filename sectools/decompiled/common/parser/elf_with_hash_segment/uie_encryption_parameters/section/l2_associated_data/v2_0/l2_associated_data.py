
from typing import Any
from common.data.data import hex_val
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section.l2_associated_data.defines import L2_AD_KEY_LADDER_LENGTH, L2_AD_MAJOR_VERSION_2, L2_AD_MINOR_VERSION_0
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section.l2_associated_data.v1_1.l2_associated_data import L2AssociatedDataV11

class L2AssociatedDataV20(L2AssociatedDataV11):
    MAJOR_VERSION = L2_AD_MAJOR_VERSION_2
    software_id: int = L2_AD_MINOR_VERSION_0
    
    def get_fields(cls = None):
        return [
            'reserved_0',
            'reserved_1',
            'major_version',
            'minor_version',
            'key_ladder_length',
            'reserved_2',
            'software_id',
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
            'software_id': 0,
            'reserved_3': b'' }

    get_field_defaults = None(get_field_defaults)
    
    def get_format(cls = None):
        return '<BBBBBBI20s'

    get_format = None(get_format)
    
    def unpack_post_process(self = None):
        self.software_ids = [
            self.software_id]

    
    def pack_pre_process(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_software_id_properties(self = None):
        return [
            ('Software ID:', hex_val(self.software_id, True, **('strip_leading_zeros',)))]

    
    def set_software_id(self = None, software_id = None):
        self.software_ids = [
            software_id]


