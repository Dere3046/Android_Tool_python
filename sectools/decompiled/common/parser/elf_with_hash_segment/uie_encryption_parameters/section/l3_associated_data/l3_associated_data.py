
from typing import Any, Dict, List, Optional, Tuple, Union
from common.data.binary_struct import StructBase
from common.data.data import comma_separated_string, get_enabled_bit_indices_from_byte
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section.l2_associated_data.l2_associated_data import L2AssociatedDataLength
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section.l3_associated_data.defines import IMAGE_ENCRYPTION_ALGO_AES, IMAGE_ENCRYPTION_ALGO_DESCRIPTION, IMAGE_ENCRYPTION_MODE_CBC_CTS, IMAGE_ENCRYPTION_MODE_DESCRIPTION, L3_AD_SIZE

class L3AssociatedDataLength(L2AssociatedDataLength):
    
    def validate_before_operation(self = None, **_):
        if self.value != L3_AD_SIZE:
            raise RuntimeError(f'''L3 Associated Data Length is invalid: {self.value}.''')



class L3AssociatedData(StructBase):
    segment_bitmap_1: int = 'L3AssociatedData'
    
    def __init__(self = None, data = None, check_is_type = None, bypass_validation = None):
        self.encrypted_segment_indices = []
        self.number_of_encrypted_segments = 0
        (self.segment_bitmap_0, self.segment_bitmap_1) = (0, 0)
        self.associated_data_length = L3AssociatedDataLength(data)
        super().__init__(data[L3AssociatedDataLength.get_size():] if data else data, check_is_type, bypass_validation, **('data', 'check_is_type', 'bypass_validation'))

    
    def get_fields(cls = None):
        return [
            'reserved_0',
            'reserved_1',
            'image_encryption_algorithm',
            'image_encryption_mode',
            'reserved_2',
            'reserved_3',
            'reserved_4',
            'all_segments_encrypted',
            'number_of_encrypted_segments',
            'reserved_5',
            'reserved_6',
            'segment_bitmap_0',
            'segment_bitmap_1']

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        return {
            'reserved_0': 0,
            'reserved_1': 0,
            'image_encryption_algorithm': IMAGE_ENCRYPTION_ALGO_AES,
            'image_encryption_mode': IMAGE_ENCRYPTION_MODE_CBC_CTS,
            'reserved_2': 0,
            'reserved_3': 0,
            'reserved_4': 0,
            'all_segments_encrypted': True,
            'number_of_encrypted_segments': 0,
            'reserved_5': 0,
            'reserved_6': 0,
            'segment_bitmap_0': 0,
            'segment_bitmap_1': 0 }

    get_field_defaults = None(get_field_defaults)
    
    def unpack_post_process(self = None):
        self.encrypted_segment_indices = get_enabled_bit_indices_from_byte(self.segment_bitmap_0) + get_enabled_bit_indices_from_byte(self.segment_bitmap_1, 64)

    
    def pack_pre_process(self = None):
        self.number_of_encrypted_segments = len(self.encrypted_segment_indices)
        (self.segment_bitmap_0, self.segment_bitmap_1) = (0, 0)
        for encrypted_segment_index in self.encrypted_segment_indices:
            if encrypted_segment_index < 64:
                self.segment_bitmap_0 |= 1 << encrypted_segment_index
                continue
            if encrypted_segment_index < 128:
                self.segment_bitmap_1 |= 1 << encrypted_segment_index - 64
                continue
            raise RuntimeError(f'''Cannot set Encrypted Segment Index of L3 Associated Data to {encrypted_segment_index}. The maximum allowed index is 127.''')
            return None

    
    def pack(self = None):
        return self.associated_data_length.pack() + super().pack()

    
    def get_format(cls = None):
        return '<BBBBBBI?BBBQQ'

    get_format = None(get_format)
    
    def get_size(cls = None):
        return L3AssociatedDataLength.get_size() + super().get_size()

    get_size = None(get_size)
    
    def validate_before_operation(self = None, **kwargs):
        pass
    # WARNING: Decompyle incomplete

    
    def get_properties(self = None):
        return [
            ('Associated Data Length:', f'''{self.associated_data_length.value} (bytes)'''),
            ('Image Encryption Algorithm:', IMAGE_ENCRYPTION_ALGO_DESCRIPTION.get(self.image_encryption_algorithm, self.image_encryption_algorithm)),
            ('Image Encryption Mode:', IMAGE_ENCRYPTION_MODE_DESCRIPTION.get(self.image_encryption_mode, self.image_encryption_mode)),
            ('All Segments Encrypted:', self.all_segments_encrypted),
            ('Number of Encrypted Segments:', self.number_of_encrypted_segments),
            ('Encrypted Segment Indices:', self.__repr_segment_bitmap__())]

    
    def __repr_segment_bitmap__(self = None):
        if self.encrypted_segment_indices:
            return comma_separated_string(self.encrypted_segment_indices, 'and', **('final_separator',))

    __classcell__ = None

