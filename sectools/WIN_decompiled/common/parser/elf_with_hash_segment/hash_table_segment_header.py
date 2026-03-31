
from typing import Type
from common.data.base_parser import DumpDict, DumpInterface
from common.data.binary_struct import StructBase
from common.data.defines import PAD_BYTE_0, PAD_BYTE_1, SHA_SIZE_TO_DESCRIPTION
from common.parser.elf_with_hash_segment.v6.metadata.metadata import MetadataCommon
from common.parser.elf_with_hash_segment.v7.metadata.common.v0_0.common_metadata_0_0 import CommonMetadataV00
from common.parser.hash_segment.defines import HASH_SEGMENT_V3, HASH_SEGMENT_V5, HASH_SEGMENT_V6, HASH_SEGMENT_V7, HASH_SEGMENT_V8

class HashTableSegmentHeaderCommon(DumpInterface, StructBase):
    FIELD_6 = 'hash_table_size'
    FIELD_6_STR = 'Hash Table Size:'
    IMAGE_SIZE_STR = ' (Size of data following Hash Table Segment Header)'
    HEADER_STR = 'Hash Table Segment Header'
    METADATA_CLASSES: dict[(tuple[(int, int)], Type[MetadataCommon])] = { }
    hash_table_size: int = { }
    
    def get_fields(cls = None):
        return [
            'reserved',
            'version']

    get_fields = None(get_fields)
    
    def get_format(cls = None):
        return '<II'

    get_format = None(get_format)
    
    def format_size_string(string = None, header_field_size = None, data = staticmethod):
        if header_field_size:
            if data:
                if data or data == PAD_BYTE_0 * len(data) or data == PAD_BYTE_1 * len(data):
                    string += ' (all padding):'
                    return string
                None += ':'
                return string
            None += ':'
            return string

    format_size_string = None(format_size_string)
    
    def validate_critical_fields(self = None):
        if self.version not in (HASH_SEGMENT_V3, HASH_SEGMENT_V5, HASH_SEGMENT_V6, HASH_SEGMENT_V7, HASH_SEGMENT_V8):
            raise RuntimeError(f'''{self.HEADER_STR} has invalid version: {self.version}.''')

    
    def get_dump_files(self = None, directory = None):
        return {
            f'''{directory}/{self.HEADER_STR.lower().replace(' ', '_')}.bin''': self.pack() }

    
    def get_hash_table_algorithm_properties(self = None, num_entries = None):
        hash_size = int(self.hash_table_size / num_entries)
        return [
            ('Hash Table Algorithm:', SHA_SIZE_TO_DESCRIPTION.get(hash_size, 'Unknown')),
            ('Hash Table Entry Size:', f'''{hash_size} (bytes)''')]

    
    def get_segment_hash_algorithm(self = None, num_hashable_entries = None):
        pass
    # WARNING: Decompyle incomplete

    
    def prep_for_zi_segment_hash(self = None):
        raise RuntimeError(f'''{self.class_type_string()} does not support ZI hashing.''')


