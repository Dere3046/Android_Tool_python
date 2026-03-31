
from typing import Any
from common.data.data import hex_val
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section.l2_associated_data.defines import L2_AD_MINOR_VERSION_2
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section.l2_associated_data.v1_1.l2_associated_data import L2AssociatedDataV11

class L2AssociatedDataV12(L2AssociatedDataV11):
    feature_id: int = L2_AD_MINOR_VERSION_2
    
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
            'feature_id',
            'reserved_3']

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        pass
    # WARNING: Decompyle incomplete

    get_field_defaults = None(get_field_defaults)
    
    def get_format(cls = None):
        return '<BBBBBBQQI4s'

    get_format = None(get_format)
    
    def get_properties(self = None):
        return super().get_properties() + [
            ('Feature ID:', hex_val(self.feature_id, True, **('strip_leading_zeros',)))]

    __classcell__ = None

