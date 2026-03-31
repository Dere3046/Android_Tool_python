
from common.parser.elf_with_hash_segment.v5.hash_table_segment_header import HashTableSegmentHeaderV5
from common.parser.mbn.mbn_header import MBNHeader

class MBNHeaderV5(HashTableSegmentHeaderV5, MBNHeader):
    
    def is_oem_exclusive_signed(self = None, contains_padding = None):
        return False

    
    def is_qti_exclusive_signed(self = None, contains_padding = None):
        return False

    
    def is_oem_signed_double_signable(self = None, contains_padding = None):
        if self.oem_signature_size:
            pass
        return bool(not (self.qti_signature_size))

    
    def is_qti_signed_double_signable(self = None, contains_padding = None):
        if self.qti_signature_size:
            pass
        return bool(not (self.oem_signature_size))


