
from typing import Any, Type
from common.data.base_parser import DumpDict
from common.data.binary_struct import DetailsTuple, StructDynamic
from common.parser.elf_with_hash_segment.elf_with_hash_segment import HashTableSegmentCommon
from common.parser.elf_with_hash_segment.hash_table_segment_header import HashTableSegmentHeaderCommon
from common.parser.hash_segment.defines import AUTHORITY_OEM, HASH_SEGMENT_V3, HASH_SEGMENT_V5, HASH_SEGMENT_V6, HASH_SEGMENT_V7, HASH_SEGMENT_V8
from common.parser.mbn.v3.mbn_header import MBNHeaderV3
from common.parser.mbn.v5.mbn_header import MBNHeaderV5
from common.parser.mbn.v6.mbn_header import MBNHeaderV6
from common.parser.mbn.v7.mbn_header import MBNHeaderV7
from common.parser.mbn.v8.mbn_header import MBNHeaderV8
from common.parser.parser_image_info_interface import ImageFormatType, ImageInfoInterface, ImageProperties, MBN_PROPERTIES
from profile.schema import ImageFormat, MBNProperties
MBN_HEADER_CLASSES: dict[(int, Type[MBNHeaderV3 | MBNHeaderV5 | MBNHeaderV6 | MBNHeaderV7 | MBNHeaderV8])] = {
    HASH_SEGMENT_V8: MBNHeaderV8,
    HASH_SEGMENT_V7: MBNHeaderV7,
    HASH_SEGMENT_V6: MBNHeaderV6,
    HASH_SEGMENT_V5: MBNHeaderV5,
    HASH_SEGMENT_V3: MBNHeaderV3 }

class MBN(ImageInfoInterface, HashTableSegmentCommon):
    
    def __init__(self = None, data = None, **kwargs):
        ''' Parse the data of an MBN image. '''
        self.code = memoryview(b'')
    # WARNING: Decompyle incomplete

    
    def hash_segment_type(cls = None):
        return 'MBN'

    hash_segment_type = None(hash_segment_type)
    
    def image_type_string(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def create_default(self = None, *, mbn_version, code, **kwargs):
        self.code = code
    # WARNING: Decompyle incomplete

    
    def unpack_hash_table_or_code(self = None, data = None):
        pass
    # WARNING: Decompyle incomplete

    
    def unpack_header(self = None, data = None, version = None):
        self.header = MBN_HEADER_CLASSES[version](data)

    
    def pack_hash_table_or_code(self = None):
        return memoryview(self.code)

    
    def get_details_hash_table_or_code(self = None, authority = None, details = None):
        (details_fields, format_str, details_dict) = details
        if self.code:
            details_fields.append('code')
            format_str = StructDynamic.concatenate_formats(format_str, f'''<{len(self.code)}s''')
        return (details_fields, format_str, details_dict)

    
    def unpack_encryption_parameters(self = None, remaining_data = None):
        pass

    
    def pack_encryption_parameters(self = None):
        return memoryview(b'')

    
    def contains_encrypted_data(self = None):
        return False

    
    def __repr__(self = None):
        return self._repr_compression_format() + super().__repr__()

    
    def repr_hash_table_hashes(self = None):
        return ''

    
    def repr_encryption_parameters(self = None):
        return ''

    
    def repr_hash_table_algorithm(self = None):
        return []

    
    def is_type(cls = None, data = None):
        ''' Detect whether the data is of an MBN image. '''
        return HashTableSegmentHeaderCommon.is_type(data)

    is_type = None(is_type)
    
    def get_dump_files(self = None, directory = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_image_properties(self = None, authority = None):
        (metadata_version, common_metadata_version) = self.get_metadata_version(authority)
    # WARNING: Decompyle incomplete

    
    def get_image_format(self = None, authority = None):
        pass
    # WARNING: Decompyle incomplete

    __classcell__ = None

