
from binascii import hexlify
from os import urandom
from typing import Any, Dict, List, Optional, Tuple, Union
from common.data.binary_struct import StructBase
from common.data.data import hex_val
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section.defines import FLAGS, FLAGS_DESCRIPTION, NONCE_SIZE, Q_VALUE

class Q(StructBase):
    value: int = 'Q'
    
    def get_fields(cls = None):
        return [
            'value']

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        return {
            'value': Q_VALUE }

    get_field_defaults = None(get_field_defaults)
    
    def get_format(cls = None):
        return '>H'

    get_format = None(get_format)
    
    def validate_before_operation(self = None, **_):
        if self.value != Q_VALUE:
            raise RuntimeError(f'''B0 contains invalid Q: {self.value}.''')



class B0(StructBase):
    nonce: bytes = 'B0'
    
    def __init__(self = None, data = None, check_is_type = None, bypass_validation = None):
        self.q = None
        super().__init__(data, check_is_type, bypass_validation, **('data', 'check_is_type', 'bypass_validation'))

    
    def get_fields(cls = None):
        return [
            'flags',
            'nonce']

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        return {
            'flags': FLAGS,
            'nonce': urandom(NONCE_SIZE) }

    get_field_defaults = None(get_field_defaults)
    
    def get_complex_defaults(cls = None):
        return {
            'q': Q() }

    get_complex_defaults = None(get_complex_defaults)
    
    def get_format(cls = None):
        return f'''<B{NONCE_SIZE}s'''

    get_format = None(get_format)
    
    def unpack_post_process(self = None):
        if self.data:
            self.q = Q(self.data[super().get_size():])
            return None

    
    def pack_pre_process(self = None):
        pass

    
    def pack(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_size(cls = None):
        return super().get_size() + Q.get_size()

    get_size = None(get_size)
    
    def validate_before_operation(self = None, **kwargs):
        if self.flags != FLAGS:
            raise RuntimeError(f'''B0 contains invalid Flags: {self.flags}.''')
    # WARNING: Decompyle incomplete

    
    def get_properties(self = None):
        pass
    # WARNING: Decompyle incomplete

    __classcell__ = None

