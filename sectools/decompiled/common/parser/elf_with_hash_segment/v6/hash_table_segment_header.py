
from typing import Any
from common.data.base_parser import DumpDict
from common.data.binary_struct import DetailsTuple, NestedDetails, StructDynamic
from common.data.defines import PAD_BYTE_0
from common.parser.elf_with_hash_segment.hash_table_segment_header import HashTableSegmentHeaderCommon
from common.parser.elf_with_hash_segment.hash_table_segment_header_getters_interface import HashTableSegmentHeaderGettersInterface
from common.parser.elf_with_hash_segment.v5.hash_table_segment_header import HashTableSegmentHeaderV5Spec
from common.parser.elf_with_hash_segment.v6.metadata import defines
from common.parser.elf_with_hash_segment.v6.metadata.defines import METADATA_MAJOR_VERSION_0, METADATA_MAJOR_VERSION_1, METADATA_MINOR_VERSION_0
from common.parser.elf_with_hash_segment.v6.metadata.metadata import MetadataCommon
from common.parser.elf_with_hash_segment.v6.metadata.v0_0.metadata_0_0 import Metadata, MetadataV00
from common.parser.elf_with_hash_segment.v6.metadata.v1_0.metadata_1_0 import MetadataV10
from common.parser.hash_segment.defines import AUTHORITY_OEM, HASH_SEGMENT_V6

class HashTableSegmentHeaderV6(HashTableSegmentHeaderGettersInterface, HashTableSegmentHeaderV5Spec):
    METADATA_SIZE_TO_CLASS = {
        MetadataV00.get_size(): MetadataV00 }
    METADATA_CLASSES = {
        (METADATA_MAJOR_VERSION_1, METADATA_MINOR_VERSION_0): MetadataV10,
        (METADATA_MAJOR_VERSION_0, METADATA_MINOR_VERSION_0): MetadataV00 }
    VERSION = HASH_SEGMENT_V6
    oem_metadata_size: int = defines.FALSE
    
    def __init__(self = None, data = None, check_is_type = None, bypass_validation = None):
        self.qti_metadata = None
        self.oem_metadata = None
        super().__init__(data, check_is_type, bypass_validation, **('data', 'check_is_type', 'bypass_validation'))

    
    def get_fields(cls = None):
        return super().get_fields() + [
            'qti_metadata_size',
            'oem_metadata_size']

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        pass
    # WARNING: Decompyle incomplete

    get_field_defaults = None(get_field_defaults)
    
    def get_format(cls = None):
        return super().get_format() + 'II'

    get_format = None(get_format)
    
    def unpack_metadata_post_process(self = None, offset = None):
        pass
    # WARNING: Decompyle incomplete

    
    def unpack_post_process(self = None):
        self.unpack_metadata_post_process(self.get_size())

    
    def validate_before_operation(self = None, **kwargs):
        pass
    # WARNING: Decompyle incomplete

    
    def pack_metadata(self = None):
        data = bytearray()
        if self.qti_metadata:
            data += self.qti_metadata.pack().ljust(self.qti_metadata_size, PAD_BYTE_0)
        if self.oem_metadata:
            data += self.oem_metadata.pack().ljust(self.oem_metadata_size, PAD_BYTE_0)
        return memoryview(data)

    
    def pack(self = None):
        return memoryview(super().pack() + bytearray(self.pack_metadata()))

    
    def get_dump_files(self = None, directory = None):
        subdir = f'''{directory}/{self.HEADER_STR.lower().replace(' ', '_')}'''
        dump_files = {
            f'''{subdir}/header.bin''': super().pack() }
        if self.qti_metadata:
            dump_files[f'''{subdir}/qti_metadata.bin'''] = self.qti_metadata.pack().ljust(self.qti_metadata_size, PAD_BYTE_0)
        if self.oem_metadata:
            dump_files[f'''{subdir}/oem_metadata.bin'''] = self.oem_metadata.pack().ljust(self.oem_metadata_size, PAD_BYTE_0)
        return dump_files

    
    def get_properties(self = None, qti_signature = None, qti_certificate_chain = None, oem_signature = None, oem_certificate_chain = None):
        properties = super().get_properties(qti_signature, qti_certificate_chain, oem_signature, oem_certificate_chain)
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
        qti_metadata_size_str = HashTableSegmentHeaderCommon.format_size_string('QTI Metadata Size', self.qti_metadata_size, qti_metadata)
        oem_metadata_size_str = HashTableSegmentHeaderCommon.format_size_string('OEM Metadata Size', self.oem_metadata_size, oem_metadata)
        properties += [
            (qti_metadata_size_str, f'''{self.qti_metadata_size} (bytes)'''),
            (oem_metadata_size_str, f'''{self.oem_metadata_size} (bytes)''')]
        return properties

    
    def get_metadata_details(self, authority = None, fields = None, format_string = None, nested_fields = ('authority', str, 'fields', list[str], 'format_string', str, 'nested_fields', NestedDetails, 'return', DetailsTuple)):
        if self.qti_metadata:
            (fields_list, format_str, nested_details) = self.qti_metadata.get_details(authority)
            fields += (lambda .0: [ 'qti_metadata_' + field for field in .0 ])(fields_list)
            format_string = StructDynamic.concatenate_formats(format_string, format_str)
            for key, value in nested_details.items():
                nested_fields[f'''qti_metadata_{key}'''] = value
        if self.oem_metadata:
            (fields_list, format_str, nested_details) = self.oem_metadata.get_details(authority)
            fields += (lambda .0: [ 'oem_metadata_' + field for field in .0 ])(fields_list)
            format_string = StructDynamic.concatenate_formats(format_string, format_str)
            for key, value in nested_details.items():
                nested_fields[f'''oem_metadata_{key}'''] = value
        return (fields, format_string, nested_fields)

    
    def get_details(self = None, authority = None):
        (fields, format_string, nested_fields) = super().get_details(authority)
        return self.get_metadata_details(authority, fields, format_string, nested_fields)

    
    def is_oem_exclusive_signed(self = None, _ = None):
        if self.oem_signature_size and not (self.qti_signature_size):
            pass
        return bool(not (self.qti_metadata_size))

    
    def is_qti_exclusive_signed(self = None, _ = None):
        if self.qti_signature_size and not (self.oem_signature_size):
            pass
        return bool(not (self.oem_metadata_size))

    
    def is_oem_signed_double_signable(self = None, _ = None):
        if self.oem_signature_size and not (self.qti_signature_size):
            pass
        return bool(self.qti_metadata_size)

    
    def is_qti_signed_double_signable(self = None, _ = None):
        if self.qti_signature_size and not (self.oem_signature_size):
            pass
        return bool(self.oem_metadata_size)

    
    def get_metadata_member(self = None, authority = None, member = None):
        value = None
        metadata = self.get_authority_metadata(authority)
        if not metadata and metadata.is_all_padding():
            value = getattr(metadata, member, None)
        return value

    
    def get_software_id(self = None, authority = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_secondary_software_id(self = None, authority = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_mrc_index(self = None, authority = None, _ = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_root_revoke_activate_enable(self = None, authority = None):
        return self.get_metadata_member(authority, 'root_revoke_activate_enable') not in (self.FALSE, None)

    
    def get_hash_table_algorithm(self = None):
        pass

    
    def get_oem_id(self = None, authority = None):
        metadata = self.get_authority_metadata(authority)
        oem_id = self.get_metadata_member(authority, 'oem_id') if metadata and metadata.get_oem_id_bound() else None
    # WARNING: Decompyle incomplete

    
    def get_oem_product_id(self = None, authority = None):
        metadata = self.get_authority_metadata(authority)
        oem_product_id = self.get_metadata_member(authority, 'oem_product_id') if metadata and metadata.get_oem_product_id_bound() else None
    # WARNING: Decompyle incomplete

    
    def get_soc_hw_versions(self = None, authority = None):
        metadata = self.get_authority_metadata(authority)
        if metadata and metadata.get_soc_hw_vers_bound():
            return set(self.get_metadata_member(authority, 'soc_hw_vers')) - {
                0}
        return None()

    
    def get_authority_metadata(self = None, authority = None):
        if authority == AUTHORITY_OEM:
            return self.oem_metadata
        return None.qti_metadata

    
    def refresh_ou_data(self = None, authority = None, attestation_certificate = None):
        pass

    __classcell__ = None

