
from typing import Type
from common.data.base_parser import BaseParserGenerator
from common.parser.elf.defines import ELFCLASS32
from common.parser.elf_with_hash_segment.elf_with_hash_segment import ELFWithHashTableSegment
from common.parser.hash_segment.defines import AUTHORITY_OEM, HASH_SEGMENT_V3
from common.parser.parser_image_info_interface import ImageFormatType
from common.parser.sec_dat.defines import SEC_DAT_VERSION_1
from common.parser.sec_elf.sec_elf import SecELF

class SecELFWithHashTableSegment(SecELF, ELFWithHashTableSegment):
    
    def create_default(self = None, *, elf_class, hash_table_segment_version, hash_table_segment_address, sec_dat_version, sec_dat_segment_address, **_):
        SecELF.create_default(self, elf_class, sec_dat_version, sec_dat_segment_address, **('elf_class', 'sec_dat_version', 'sec_dat_segment_address'))
        ELFWithHashTableSegment.create_default(self, elf_class, hash_table_segment_version, hash_table_segment_address, **('elf_class', 'hash_table_segment_version', 'hash_table_segment_address'))

    
    def transformable_parsers(cls = None):
        return [
            SecELF]

    transformable_parsers = None(transformable_parsers)
    
    def get_image_format(self = None, authority = None):
        return ELFWithHashTableSegment.get_image_format(self, authority) + SecELF.get_image_format(self, authority)


