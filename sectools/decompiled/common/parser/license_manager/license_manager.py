
from contextlib import suppress
from typing import Any, Type
import profile
from common.data.base_parser import BaseParserGenerator, DumpDict
from common.data.data import ceil_to_multiple, properties_repr
from common.parser.elf.bit32.program_header import ProgramHeader32
from common.parser.elf.bit64.program_header import ProgramHeader64
from common.parser.elf.defines import ELFCLASS32, PT_NOTE
from common.parser.elf.elf import ELF
from common.parser.elf.program_header import PROGRAM_HEADER_CLASSES
from common.parser.elf_with_hash_segment.elf_with_hash_segment import ELFWithHashTableSegment
from common.parser.hash_segment.defines import AUTHORITY_OEM, HASH_SEGMENT_V3
from common.parser.license_manager.license_manager_segment.v0.license_manager_segment import LicenseManagerSegmentV0
from common.parser.parser_image_info_interface import ImageProperties, LICENSE_MANAGER_SEGMENT_PROPERTIES
from profile.defines import ANY, START
from profile.schema import LicenseManagerSegmentProperties

class LicenseManager(ELFWithHashTableSegment):
    
    def __init__(self = None, data = None, transform = None, **kwargs):
        ''' Parse the data of a License Manager image. '''
        self.license_manager_segment_phdr = None
        self.license_manager_segment = None
    # WARNING: Decompyle incomplete

    
    def image_type_string(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def create_default_license_manager_segment(self = None, license_manager_client_id = None, license_manager_library_id = None):
        pass
    # WARNING: Decompyle incomplete

    
    def create_default(self = None, *, elf_class, hash_table_segment_version, hash_table_segment_address, license_manager_client_id, license_manager_library_id, **_):
        ELF.create_default(self, elf_class, **('elf_class',))
        self.create_default_license_manager_segment(license_manager_client_id, license_manager_library_id)
        self.create_default_hash_table_segment(hash_table_segment_version, hash_table_segment_address)

    
    def transform(self = None, persist_sections = None, hash_table_segment_version = None, hash_table_segment_address = None, license_manager_client_id = None, license_manager_library_id = None, **_):
        if not persist_sections:
            self.remove_sections()
        self.remove_elf_hdr_phdr_table_overlaps()
        if not self.license_manager_segment_phdr:
            self.create_default_license_manager_segment(license_manager_client_id, license_manager_library_id)
        if not self.hash_table_segment_phdr:
            super().transform(hash_table_segment_version, hash_table_segment_address, **('hash_table_segment_version', 'hash_table_segment_address'))
            return None

    
    def transformable_parsers(cls = None):
        return [
            ELF,
            ELFWithHashTableSegment]

    transformable_parsers = None(transformable_parsers)
    
    def unpack(self = None, data = None):
        super().unpack(data)
        for phdr in self.phdrs:
            if phdr.p_type == PT_NOTE and LicenseManagerSegmentV0.is_type(self.segments[phdr]):
                self.license_manager_segment_phdr = phdr
                self.license_manager_segment = LicenseManagerSegmentV0(self.segments[phdr])
                return None
            raise self.ExceptionNeedsTransform('ELF does not contain a License Manager Segment.')

    
    def pack(self = None):
        data = self.license_manager_segment.pack() if self.license_manager_segment else b''
    # WARNING: Decompyle incomplete

    
    def is_type(cls = None, data = None):
        ''' Detect whether the data is of an ELF MBN image containing a License Manager segment. '''
        match = False
    # WARNING: Decompyle incomplete

    is_type = None(is_type)
    
    def get_dump_files(self = None, directory = None):
        pass
    # WARNING: Decompyle incomplete

    
    def __repr__(self = None):
        string = super().__repr__()
        if self.license_manager_segment:
            string += '\n\nLicense Manager Segment:\n' + properties_repr(self.license_manager_segment.get_properties())
        return string

    
    def set_client_id_and_library_id(self = None, client_id = None, library_id = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_image_properties(self = None, authority = None):
        pass
    # WARNING: Decompyle incomplete

    __classcell__ = None

