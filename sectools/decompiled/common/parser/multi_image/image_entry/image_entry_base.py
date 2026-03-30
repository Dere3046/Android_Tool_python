
from abc import ABC, abstractmethod
from binascii import hexlify
from typing import Any, Callable, Dict, List, Tuple, Type, TypeVar
from common.data.binary_struct import StructBase
from common.data.data import hex_val
from common.parser.elf_with_hash_segment.elf_with_hash_segment import ELFWithHashTableSegment
T = TypeVar('T', 'MultiImageSegmentEntryBase', **('bound',))

class MultiImageSegmentEntryBase(ABC, StructBase):
    hash: bytes = 'MultiImageSegmentEntryBase'
    
    def IMAGE_HASH_FUNCTION(self = None):
        '''Implementation should define an appropriate hash function.'''
        pass

    IMAGE_HASH_FUNCTION = None(None(IMAGE_HASH_FUNCTION))
    
    def get_fields(cls = None):
        return [
            'software_id',
            'secondary_software_id',
            'hash']

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        return {
            'software_id': 0,
            'secondary_software_id': 0,
            'hash': b'' }

    get_field_defaults = None(get_field_defaults)
    
    def get_properties(self = None):
        return [
            (hex_val(self.software_id, True, **('strip_leading_zeros',)), hex_val(self.secondary_software_id, True, **('strip_leading_zeros',)), '0x' + hexlify(self.hash).decode())]

    
    def __str__(self = None):
        return f'''Software ID {self.software_id:#x}, Secondary Software ID {self.secondary_software_id:#x}'''

    
    def __eq__(self = None, o = None):
        return hash(self) == hash(o)

    
    def __hash__(self = None):
