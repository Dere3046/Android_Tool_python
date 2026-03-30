
from binascii import hexlify
from os import urandom
from typing import Dict, List, Tuple
from common.data.binary_struct import StructBase

class BaseIV(StructBase):
    base_iv: bytes = 'BaseIV'
    
    def get_fields(cls = None):
        return [
            'base_iv']

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        return {
            'base_iv': urandom(cls.get_size()) }

    get_field_defaults = None(get_field_defaults)
    
    def get_format(cls = None):
        return '>16s'

    get_format = None(get_format)
    
    def get_properties(self = None):
        return [
            ('Base IV:', '0x' + hexlify(self.base_iv).decode())]


