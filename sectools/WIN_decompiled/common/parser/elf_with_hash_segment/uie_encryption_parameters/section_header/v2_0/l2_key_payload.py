
from binascii import hexlify
from typing import Any, List, Optional, Tuple, Union
from common.data.binary_struct import StructBase
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section_header.v2_0.defines import L2_KEY_SIZE

class L2KeyPayloadECIESADLength(StructBase):
    value: int = 'L2KeyPayloadECIESADLength'
    
    def get_fields(cls = None):
        return [
            'value']

    get_fields = None(get_fields)
    
    def get_format(cls = None):
        return '>I'

    get_format = None(get_format)
    
    def validate(self = None):
        if self.value != L2_KEY_SIZE:
            raise RuntimeError(f'''L2 Key Length is invalid: {self.value}.''')



class L2KeyPayloadECIESAD(StructBase):
    l2_key_payload: bytes = 'L2KeyPayloadECIESAD'
    
    def __init__(self = None, data = None, check_is_type = None, bypass_validation = None):
        self.l2_key_payload_length = L2KeyPayloadECIESADLength(data, check_is_type, bypass_validation, **('data', 'check_is_type', 'bypass_validation'))
        super().__init__(data[self.l2_key_payload_length.get_size():] if data else data, check_is_type, bypass_validation, **('data', 'check_is_type', 'bypass_validation'))

    
    def get_fields(cls = None):
        return [
            'l2_key_payload']

    get_fields = None(get_fields)
    
    def get_format(cls = None):
        return '<32s'

    get_format = None(get_format)
    
    def pack(self = None):
        return self.l2_key_payload_length.pack() + super().pack()

    
    def get_size(cls = None):
        return L2KeyPayloadECIESADLength.get_size() + super().get_size()

    get_size = None(get_size)
    
    def get_properties(self = None):
        return [
            ('L2 Key Length:', self.l2_key_payload_length.value),
            ('L2 Key:', hexlify(self.l2_key_payload).decode())]

    __classcell__ = None

