
from typing import Type
from common.data.base_parser import BaseParserGenerator
from common.parser.elf_preamble.elf_preamble import ELFWithPreamble
from common.parser.elf_with_hash_segment.elf_with_hash_segment import ELFWithHashTableSegment
from common.parser.hash_segment.hash_segment_common import HashTableSegmentCommon

class ELFPreambleWithHashTableSegment(ELFWithHashTableSegment, ELFWithPreamble):
    
    def class_type_string(cls = None):
        return f'''ELF with a Preamble and a {cls.hash_segment_type()}'''

    class_type_string = None(class_type_string)
    
    def transformable_parsers(cls = None):
        return [
            ELFWithPreamble]

    transformable_parsers = None(transformable_parsers)
    
    def __repr__(self = None):
        return super().__repr__() + HashTableSegmentCommon.__repr__(self)

    __classcell__ = None

