
from typing import Any
from common.data.certificate import get_certificate_sequence_size, is_inactive_mrc_3_0_certificate
from common.parser.elf_with_hash_segment.hash_table_segment_header import HashTableSegmentHeaderCommon
from common.parser.elf_with_hash_segment.hash_table_segment_header_getters_interface import HashTableSegmentHeaderGettersInterface
from common.parser.elf_with_hash_segment.v7.hash_table_segment_header import HashTableSegmentHeaderV7
from common.parser.elf_with_hash_segment.v7.metadata.common.v0_0.common_metadata_0_0 import CommonMetadataV00
from common.parser.elf_with_hash_segment.v8.metadata.defines import METADATA_MAJOR_VERSION_4, METADATA_MINOR_VERSION_0
from common.parser.elf_with_hash_segment.v8.metadata.v4_0.metadata_4_0 import MetadataV40
from common.parser.hash_segment.defines import HASH_SEGMENT_V8

class HashTableSegmentHeaderV8(HashTableSegmentHeaderGettersInterface, HashTableSegmentHeaderV7):
    METADATA_SIZE_TO_CLASS = {
        MetadataV40.get_size(): MetadataV40 }
    METADATA_CLASSES = {
        (METADATA_MAJOR_VERSION_4, METADATA_MINOR_VERSION_0): MetadataV40 }
    oem_certificate_chain_2_size: int = HASH_SEGMENT_V8
    
    def qti_signature_size(self):
        return self.qti_signature_1_size

    qti_signature_size = property(qti_signature_size)
    
    def qti_signature_size(self = None, value = None):
        self.qti_signature_1_size = value

    qti_signature_size = None(qti_signature_size)
    
    def qti_certificate_chain_size(self):
        return self.qti_certificate_chain_1_size

    qti_certificate_chain_size = property(qti_certificate_chain_size)
    
    def qti_certificate_chain_size(self = None, value = None):
        self.qti_certificate_chain_1_size = value

    qti_certificate_chain_size = None(qti_certificate_chain_size)
    
    def oem_signature_size(self):
        return self.oem_signature_1_size

    oem_signature_size = property(oem_signature_size)
    
    def oem_signature_size(self = None, value = None):
        self.oem_signature_1_size = value

    oem_signature_size = None(oem_signature_size)
    
    def oem_certificate_chain_size(self):
        return self.oem_certificate_chain_1_size

    oem_certificate_chain_size = property(oem_certificate_chain_size)
    
    def oem_certificate_chain_size(self = None, value = None):
        self.oem_certificate_chain_1_size = value

    oem_certificate_chain_size = None(oem_certificate_chain_size)
    
    def get_mrc_index(self = None, _ = None, root_certificates = None):
        mrc_index = None
        for idx, root_certificate in enumerate(root_certificates):
            if not is_inactive_mrc_3_0_certificate(get_certificate_sequence_size(root_certificate)):
                mrc_index = idx
                return mrc_index
            return mrc_index

    
    def get_fields(cls = None):
        return HashTableSegmentHeaderCommon.get_fields() + [
            'common_metadata_size',
            'qti_metadata_size',
            'oem_metadata_size',
            cls.FIELD_6,
            'qti_signature_1_size',
            'qti_certificate_chain_1_size',
            'qti_signature_2_size',
            'qti_certificate_chain_2_size',
            'oem_signature_1_size',
            'oem_certificate_chain_1_size',
            'oem_signature_2_size',
            'oem_certificate_chain_2_size']

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        return {
            'oem_certificate_chain_2_size': 0,
            'oem_signature_2_size': 0,
            'oem_certificate_chain_1_size': 0,
            'oem_signature_1_size': 0,
            'qti_certificate_chain_2_size': 0,
            'qti_signature_2_size': 0,
            'qti_certificate_chain_1_size': 0,
            'qti_signature_1_size': 0,
            cls.FIELD_6: 0,
            'oem_metadata_size': 0,
            'qti_metadata_size': 0,
            'common_metadata_size': CommonMetadataV00.get_size(),
            'version': HASH_SEGMENT_V8,
            'reserved': 0 }

    get_field_defaults = None(get_field_defaults)
    
    def get_format(cls = None):
        return HashTableSegmentHeaderCommon.get_format() + 'IIIIIIIIIIII'

    get_format = None(get_format)
    
    def get_properties(self = None, qti_signature = None, qti_certificate_chain = None, oem_signature = None, oem_certificate_chain = None):
        qti_sig_1_size_str = HashTableSegmentHeaderCommon.format_size_string('QTI Signature 1 Size', self.qti_signature_size, qti_signature)
        qti_certificate_chain_1_str = HashTableSegmentHeaderCommon.format_size_string('QTI Certificate Chain 1 Size', self.qti_certificate_chain_size, qti_certificate_chain)
        oem_sig_1_size_str = HashTableSegmentHeaderCommon.format_size_string('OEM Signature 1 Size', self.oem_signature_size, oem_signature)
        oem_certificate_chain_1_str = HashTableSegmentHeaderCommon.format_size_string('OEM Certificate Chain 1 Size', self.oem_certificate_chain_size, oem_certificate_chain)
        additions = [
            (qti_sig_1_size_str, f'''{self.qti_signature_size} (bytes)'''),
            (qti_certificate_chain_1_str, f'''{self.qti_certificate_chain_size} (bytes)'''),
            ('QTI Signature 2 Size:', f'''{self.qti_signature_2_size} (bytes)'''),
            ('QTI Certificate Chain 2 Size:', f'''{self.qti_certificate_chain_2_size} (bytes)'''),
            (oem_sig_1_size_str, f'''{self.oem_signature_size} (bytes)'''),
            (oem_certificate_chain_1_str, f'''{self.oem_certificate_chain_size} (bytes)'''),
            ('OEM Signature 2 Size:', f'''{self.oem_signature_2_size} (bytes)'''),
            ('OEM Certificate Chain 2 Size:', f'''{self.oem_certificate_chain_2_size} (bytes)''')]
        return super().get_properties(qti_signature, qti_certificate_chain, oem_signature, oem_certificate_chain)[:5] + additions

    __classcell__ = None

