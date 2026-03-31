
from typing import Any
from common.parser.elf_with_hash_segment.v3.hash_table_segment_header import HashTableSegmentHeaderV3
from common.parser.mbn.mbn_header import MBNHeader

class MBNHeaderV3(HashTableSegmentHeaderV3, MBNHeader):
    _code_size: int = '_code_size'
    
    def update_defaults(self = None, boot_image_id = None, image_dest_ptr = None, **_):
        self.boot_image_id = boot_image_id
        self.image_dest_ptr = image_dest_ptr

    
    def code_size(self = None):
        return self._code_size

    code_size = None(code_size)
    
    def code_size(self = None, size = None):
        self._code_size = size
        self.update_oem_signature_ptr()
        self.update_oem_certificate_chain_ptr()

    code_size = None(code_size)

