
from typing import Any
from common.data.base_parser import DumpDict
from common.data.binary_struct import DetailsTuple, StructDynamic
from common.data.defines import SHA_DESCRIPTION_TO_SIZE
from common.logging.logger import log_debug
from common.parser.elf_with_hash_segment.hash_table_segment_header import HashTableSegmentHeaderCommon
from common.parser.elf_with_hash_segment.hash_table_segment_header_getters_interface import HashTableSegmentHeaderGettersInterface
from common.parser.elf_with_hash_segment.v6.hash_table_segment_header import HashTableSegmentHeaderV6
from common.parser.elf_with_hash_segment.v6.metadata.metadata import MetadataCommon
from common.parser.elf_with_hash_segment.v7.defines import HASH_TABLE_ALGO_DESCRIPTION, HASH_TABLE_ALGO_NA
from common.parser.elf_with_hash_segment.v7.metadata import defines
from common.parser.elf_with_hash_segment.v7.metadata.common.v0_0.common_metadata_0_0 import CommonMetadataV00
from common.parser.elf_with_hash_segment.v7.metadata.common.v0_1.common_metadata_0_1 import CommonMetadataV01
from common.parser.elf_with_hash_segment.v7.metadata.defines import COMMON_METADATA_MAJOR_VERSION_0, COMMON_METADATA_MINOR_VERSION_0, COMMON_METADATA_MINOR_VERSION_1, METADATA_MAJOR_VERSION_2, METADATA_MAJOR_VERSION_3, METADATA_MINOR_VERSION_0, METADATA_MINOR_VERSION_1
from common.parser.elf_with_hash_segment.v7.metadata.v2_0.metadata_2_0 import MetadataV20
from common.parser.elf_with_hash_segment.v7.metadata.v3_0.metadata_3_0 import MetadataV30
from common.parser.elf_with_hash_segment.v7.metadata.v3_1.metadata_3_1 import MetadataV31
from common.parser.hash_segment.defines import HASH_SEGMENT_V7

class HashTableSegmentHeaderV7(HashTableSegmentHeaderGettersInterface, HashTableSegmentHeaderV6):
    METADATA_SIZE_TO_CLASS = {
        MetadataV20.get_size(): MetadataV20 }
    METADATA_CLASSES = {
        (METADATA_MAJOR_VERSION_3, METADATA_MINOR_VERSION_1): MetadataV31,
        (METADATA_MAJOR_VERSION_3, METADATA_MINOR_VERSION_0): MetadataV30,
        (METADATA_MAJOR_VERSION_2, METADATA_MINOR_VERSION_0): MetadataV20 }
    COMMON_METADATA_CLASSES = {
        (COMMON_METADATA_MAJOR_VERSION_0, COMMON_METADATA_MINOR_VERSION_1): CommonMetadataV01,
        (COMMON_METADATA_MAJOR_VERSION_0, COMMON_METADATA_MINOR_VERSION_0): CommonMetadataV00 }
    VERSION = HASH_SEGMENT_V7
    oem_certificate_chain_size: int = defines.FALSE
    
    def __init__(self = None, data = None, check_is_type = None, bypass_validation = None):
        self.common_metadata = None
        super().__init__(data, check_is_type, bypass_validation, **('data', 'check_is_type', 'bypass_validation'))

    
    def get_fields(cls = None):
        return HashTableSegmentHeaderCommon.get_fields() + [
            'common_metadata_size',
            'qti_metadata_size',
            'oem_metadata_size',
            cls.FIELD_6,
            'qti_signature_size',
            'qti_certificate_chain_size',
            'oem_signature_size',
            'oem_certificate_chain_size']

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        return {
            'oem_certificate_chain_size': 0,
            'oem_signature_size': 0,
            'qti_certificate_chain_size': 0,
            'qti_signature_size': 0,
            cls.FIELD_6: 0,
            'oem_metadata_size': 0,
            'qti_metadata_size': 0,
            'common_metadata_size': CommonMetadataV00.get_size(),
            'version': HASH_SEGMENT_V7,
            'reserved': 0 }

    get_field_defaults = None(get_field_defaults)
    
    def get_complex_defaults(cls = None):
        return {
            'common_metadata': list(cls.COMMON_METADATA_CLASSES.values())[0]() }

    get_complex_defaults = None(get_complex_defaults)
    
    def get_format(cls = None):
        return HashTableSegmentHeaderCommon.get_format() + 'IIIIIIII'

    get_format = None(get_format)
    
    def unpack_post_process(self = None):
        offset = self.get_size()
    # WARNING: Decompyle incomplete

    
    def validate_before_operation(self = None, **kwargs):
        pass
    # WARNING: Decompyle incomplete

    
    def pack_metadata(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_dump_files(self = None, directory = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_properties(self, qti_signature = None, qti_certificate_chain = None, oem_signature = None, oem_certificate_chain = ('qti_signature', memoryview, 'qti_certificate_chain', memoryview, 'oem_signature', memoryview, 'oem_certificate_chain', memoryview, 'return', list[tuple[(str, Any)]])):
        if not self.qti_metadata:
            qti_metadata = memoryview(bytearray())
        elif self.qti_metadata.data:
            pass
        
        qti_metadata = self.qti_metadata.data[:self.qti_metadata.get_size()](self.qti_metadata.pack())
        if not self.oem_metadata:
            oem_metadata = memoryview(bytearray())
        elif self.oem_metadata.data:
            pass
        
        oem_metadata = self.oem_metadata.data[:self.oem_metadata.get_size()](self.oem_metadata.pack())
        qti_sig_size_str = HashTableSegmentHeaderCommon.format_size_string('QTI Signature Size', self.qti_signature_size, qti_signature)
        qti_certificate_chain_str = HashTableSegmentHeaderCommon.format_size_string('QTI Certificate Chain Size', self.qti_certificate_chain_size, qti_certificate_chain)
        oem_sig_size_str = HashTableSegmentHeaderCommon.format_size_string('OEM Signature Size', self.oem_signature_size, oem_signature)
        oem_certificate_chain_str = HashTableSegmentHeaderCommon.format_size_string('OEM Certificate Chain Size', self.oem_certificate_chain_size, oem_certificate_chain)
        qti_metadata_size_str = HashTableSegmentHeaderCommon.format_size_string('QTI Metadata Size', self.qti_metadata_size, qti_metadata)
        oem_metadata_size_str = HashTableSegmentHeaderCommon.format_size_string('OEM Metadata Size', self.oem_metadata_size, oem_metadata)
        properties = [
            ('Version:', self.version),
            ('Common Metadata Size:', f'''{self.common_metadata_size} (bytes)'''),
            (qti_metadata_size_str, f'''{self.qti_metadata_size} (bytes)'''),
            (oem_metadata_size_str, f'''{self.oem_metadata_size} (bytes)'''),
            (self.FIELD_6_STR, f'''{getattr(self, self.FIELD_6)} (bytes)'''),
            (qti_sig_size_str, f'''{self.qti_signature_size} (bytes)'''),
            (qti_certificate_chain_str, f'''{self.qti_certificate_chain_size} (bytes)'''),
            (oem_sig_size_str, f'''{self.oem_signature_size} (bytes)'''),
            (oem_certificate_chain_str, f'''{self.oem_certificate_chain_size} (bytes)''')]
        return properties

    
    def get_details(self = None, authority = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_metadata_member(self = None, authority = None, member = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_hash_table_algorithm_properties(self = None, _ = None):
        properties = []
    # WARNING: Decompyle incomplete

    
    def get_segment_hash_algorithm(self = None, _ = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_hash_table_algorithm(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def prep_for_zi_segment_hash(self = None):
        if self.common_metadata.minor_version == COMMON_METADATA_MINOR_VERSION_0:
            log_debug('Scaling up Common Metadata to allow ZI Segment Hash Algorithm.')
            self.common_metadata = CommonMetadataV01.from_common_metadata00(self.common_metadata)
            return None

    __classcell__ = None

