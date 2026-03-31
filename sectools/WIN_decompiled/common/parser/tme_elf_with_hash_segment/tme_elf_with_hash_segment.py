
from typing import List, Optional
from common.parser.elf_with_hash_segment.elf_with_hash_segment import ELFWithHashTableSegment
from common.parser.hash_segment.defines import HASH_SEGMENT_V7
from common.parser.tme.tme_parser.tme import TME
from common.parser.tme_elf.tme_elf import TMEELF

class TMEELFWithHashTableSegment(TMEELF, ELFWithHashTableSegment):
    
    def create_default(self = None, *, elf_class, hash_table_segment_version, hash_table_segment_address, tme_segment_address, tme_objects, **_):
        TMEELF.create_default(self, elf_class, tme_segment_address, tme_objects, **('elf_class', 'tme_segment_address', 'tme_objects'))
        ELFWithHashTableSegment.create_default(self, hash_table_segment_version, hash_table_segment_address, **('hash_table_segment_version', 'hash_table_segment_address'))

    
    def class_type_string(cls = None):
        return f'''TME {ELFWithHashTableSegment.class_type_string()}'''

    class_type_string = None(class_type_string)
    
    def transformable_parsers(cls):
        return [
            TMEELF]

    transformable_parsers = classmethod(transformable_parsers)

