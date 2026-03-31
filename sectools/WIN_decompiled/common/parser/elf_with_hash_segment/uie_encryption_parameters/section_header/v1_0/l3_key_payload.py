
from binascii import hexlify
from typing import List, Tuple
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section_header.v1_0.l2_key_payload import L2KeyPayload

class L3KeyPayload(L2KeyPayload):
    l3_key_payload: bytes = 'L3KeyPayload'
    
    def get_fields(cls = None):
        return [
            'l3_key_payload']

    get_fields = None(get_fields)
    
    def get_properties(self = None):
        return [
            ('L3 Key:', '0x' + hexlify(self.l3_key_payload).decode())]


