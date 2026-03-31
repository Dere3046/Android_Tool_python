
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section_header.v1_0.l2_mac import L2KeyMAC

class L2KeyMACECIES(L2KeyMAC):
    
    def get_format(cls = None):
        return '<32s'

    get_format = None(get_format)

