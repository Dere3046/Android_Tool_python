
from binascii import hexlify
from typing import List, Tuple
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section_header.v1_0.l2_mac import L2KeyMAC

class L3KeyMAC(L2KeyMAC):
    l3_mac: bytes = 'L3KeyMAC'
    
    def get_fields(cls = None):
        return [
            'l3_mac']

    get_fields = None(get_fields)
    
    def get_properties(self = None):
        return [
            ('L3 MAC:', '0x' + hexlify(self.l3_mac).decode())]


