
from binascii import hexlify
from typing import List, Tuple
from common.data.binary_struct import StructBase
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section_header.v1_0.defines import KEY_PAYLOAD_SIZE

class L2KeyMAC(StructBase):
    l2_mac: bytes = 'L2KeyMAC'
    
    def get_fields(cls = None):
        return [
            'l2_mac']

    get_fields = None(get_fields)
    
    def get_format(cls = None):
        return f'''<{KEY_PAYLOAD_SIZE}s'''

    get_format = None(get_format)
    
    def get_properties(self = None):
        return [
            ('L2 MAC:', '0x' + hexlify(self.l2_mac).decode())]


