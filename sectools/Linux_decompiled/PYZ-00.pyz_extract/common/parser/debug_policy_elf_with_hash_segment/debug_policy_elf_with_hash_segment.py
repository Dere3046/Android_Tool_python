
from typing import Type
from common.data.base_parser import BaseParserGenerator
from common.parser.debug_policy_elf.debug_policy_elf import DebugPolicyELF
from common.parser.debug_policy_elf.defines import DEBUG_POLICY_V1
from common.parser.elf.defines import ELFCLASS32
from common.parser.elf_with_hash_segment.elf_with_hash_segment import ELFWithHashTableSegment
from common.parser.hash_segment.defines import AUTHORITY_OEM, HASH_SEGMENT_V3
from common.parser.parser_image_info_interface import ImageFormatType

class DebugPolicyELFWithHashTableSegment(DebugPolicyELF, ELFWithHashTableSegment):
    
    def create_default(self = None, *, elf_class, debug_policy_version, debug_policy_segment_address, hash_table_segment_version, hash_table_segment_address, **_):
        DebugPolicyELF.create_default(self, elf_class, debug_policy_version, debug_policy_segment_address, **('elf_class', 'debug_policy_version', 'debug_policy_segment_address'))
        ELFWithHashTableSegment.create_default(self, elf_class, hash_table_segment_version, hash_table_segment_address, **('elf_class', 'hash_table_segment_version', 'hash_table_segment_address'))

    
    def transformable_parsers(cls = None):
        return [
            DebugPolicyELF]

    transformable_parsers = None(transformable_parsers)
    
    def get_image_format(self = None, authority = None):
        return ELFWithHashTableSegment.get_image_format(self, authority) + DebugPolicyELF.get_image_format(self, authority)


