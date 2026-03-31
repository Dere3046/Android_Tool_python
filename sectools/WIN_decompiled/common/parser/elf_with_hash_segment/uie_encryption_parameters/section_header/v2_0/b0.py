
from binascii import hexlify
from typing import Any, Dict, List, Optional, Tuple, Union
from common.data.binary_struct import StructBase
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section.l2_associated_data.defines import L2_AD_SIZE

class AssociatedDataLength(StructBase):
    value: int = 'AssociatedDataLength'
    
    def get_fields(cls = None):
        return [
            'value']

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        return {
            'value': L2_AD_SIZE }

    get_field_defaults = None(get_field_defaults)
    
    def get_format(cls = None):
        return '>I'

    get_format = None(get_format)
    
    def validate_before_operation(self = None, **_):
        if self.value != L2_AD_SIZE:
            raise RuntimeError(f'''Associated Data Length is invalid: {self.value}.''')



class B0ECIESAD(StructBase):
    ecc_curve_coordinate_y: bytes = 'B0ECIESAD'
    
    def __init__(self = None, data = None, check_is_type = None, bypass_validation = None):
        super().__init__(data, check_is_type, bypass_validation, **('data', 'check_is_type', 'bypass_validation'))
        self.associated_data_length = AssociatedDataLength(data[super().get_size():] if data else data, check_is_type, bypass_validation, **('data', 'check_is_type', 'bypass_validation'))

    
    def get_fields(cls = None):
        return [
            'ecc_curve_coordinate_x',
            'ecc_curve_coordinate_y']

    get_fields = None(get_fields)
    
    def get_format(cls = None):
        return '<32s32s'

    get_format = None(get_format)
    
    def validate_before_operation(self = None, **kwargs):
        pass
    # WARNING: Decompyle incomplete

    
    def pack(self = None):
        return super().pack() + self.associated_data_length.pack()

    
    def get_size(cls = None):
        return super().get_size() + AssociatedDataLength.get_size()

    get_size = None(get_size)
    
    def get_properties(self = None):
        return [
            ('ECC Curve X Coordinate:', '0x' + hexlify(self.ecc_curve_coordinate_x).decode()),
            ('ECC Curve Y Coordinate:', '0x' + hexlify(self.ecc_curve_coordinate_y).decode()),
            ('Associated Data Length:', f'''{self.associated_data_length.value} (bytes)''')]

    __classcell__ = None

