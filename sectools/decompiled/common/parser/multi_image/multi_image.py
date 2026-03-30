
from contextlib import suppress
from operator import attrgetter
from typing import Any, Type
import profile
from common.data.base_parser import DumpDict
from common.data.data import ceil_to_multiple, properties_repr
from common.data.defines import SHA_DESCRIPTION_TO_FUNCTION
from common.parser.elf.bit32.program_header import ProgramHeader32
from common.parser.elf.bit64.program_header import ProgramHeader64
from common.parser.elf.defines import ELFCLASS32, PT_LOAD
from common.parser.elf.elf import ELF
from common.parser.elf.program_header import PROGRAM_HEADER_CLASSES
from common.parser.elf_with_hash_segment.elf_with_hash_segment import ELFWithHashTableSegment
from common.parser.hash_segment.defines import AUTHORITY_OEM, AUTHORITY_QTI, HASH_SEGMENT_V3
from common.parser.multi_image.defines import MULTI_IMAGE, MULTI_IMAGE_HASH_ALGO_DESCRIPTION, MULTI_IMAGE_HASH_ALGO_SHA256, MULTI_IMAGE_HASH_ALGO_SHA384
from common.parser.multi_image.image_entry.sha256.image_entry import MultiImageSegmentEntrySHA256
from common.parser.multi_image.image_entry.sha384.image_entry import MultiImageSegmentEntrySHA384
from common.parser.multi_image.v0.multi_image_segment_header import MultiImageSegmentHeaderV0
from common.parser.parser_image_info_interface import ImageProperties, VOUCH_SEGMENT_PROPERTIES
from profile.defines import ANY, START
from profile.profile_core import SecurityProfile
from profile.schema import VouchSegmentProperties
MULTI_IMAGE_ENTRY_CLASSES: dict[(int, Type[MultiImageSegmentEntrySHA256 | MultiImageSegmentEntrySHA384])] = {
    MULTI_IMAGE_HASH_ALGO_SHA384: MultiImageSegmentEntrySHA384,
    MULTI_IMAGE_HASH_ALGO_SHA256: MultiImageSegmentEntrySHA256 }

class MultiImage(ELFWithHashTableSegment):
    
    def __init__(self = None, data = None, **kwargs):
        ''' Parse the data of an image containing a Multi-Image segment. '''
        self.multi_image_segment_phdr = None
        self.multi_image_segment_idx = 0
        self.multi_image_segment_header = None
        self.image_entries = []
    # WARNING: Decompyle incomplete

    
    def class_type_string(cls = None):
        return MULTI_IMAGE

    class_type_string = None(class_type_string)
    
    def image_type_string(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def create_default(self = None, *, elf_class, hash_table_segment_version, hash_table_segment_address, multi_image_hash_algorithm, multi_image_segment_address, **_):
        ELF.create_default(self, elf_class, **('elf_class',))
    # WARNING: Decompyle incomplete

    
    def unpack(self = None, data = None):
        super().unpack(data)
        load_phdr = None
        for phdr in self.phdrs:
            if phdr.p_type == PT_LOAD:
                if not load_phdr:
                    load_phdr = phdr
                    continue
                raise RuntimeError(f'''ELF contains multiple LOAD segments. {self.class_type_string()} images must only contain 1 LOAD segment.''')
            if load_phdr:
                self.multi_image_segment_phdr = load_phdr
                multi_image_segment_data = self.segments[load_phdr]
            else:
                raise RuntimeError(f'''ELF does not contain a {self.class_type_string()} Segment.''')
            self.multi_image_segment_header = None(multi_image_segment_data)
            offset = self.multi_image_segment_header.get_size()
            image_entry_class = MULTI_IMAGE_ENTRY_CLASSES[self.multi_image_segment_header.hash_algorithm]
            for _ in range(self.multi_image_segment_header.num_entries):
                self.image_entries.append(image_entry_class(multi_image_segment_data[offset:]))
                offset += image_entry_class.get_size()
            return None

    
    def add_entry(self = None, data_to_hash = None, software_id = None, secondary_software_id = (0,)):
        pass
    # WARNING: Decompyle incomplete

    
    def pack_multi_image_segment(self = None):
        data = bytearray()
    # WARNING: Decompyle incomplete

    
    def get_size(self = None):
        size = 0
        if self.multi_image_segment_header:
            size += self.multi_image_segment_header.get_size()
        for image_entry in self.image_entries:
            size += image_entry.get_size()
        return size

    
    def is_type(cls = None, data = None):
        ''' Detect whether the data is of an ELF MBN image containing a Multi-Image segment. '''
        match = False
        if super().is_type(data):
            with suppress(Exception):
                elf = ELF(memoryview(data))
                load_phdrs = (lambda .0: [ phdr for phdr in .0 if phdr.p_type == PT_LOAD ])(elf.phdrs)
                if len(load_phdrs) == 1:
                    pass
            match = MultiImageSegmentHeaderV0.is_type(elf.segments[load_phdrs[0]])
        None(None, None, None)
        return match
    # WARNING: Decompyle incomplete

    is_type = None(is_type)
    
    def supports_multi_image(self = None):
        return False

    
    def get_dump_files(self = None, directory = None):
        dump_files = super().get_dump_files(directory)
    # WARNING: Decompyle incomplete

    
    def __repr__(self = None):
        string = super().__repr__()
        if self.multi_image_segment_header:
            string += f'''\n\n{self.class_type_string()} Segment Header:\n''' + properties_repr(self.multi_image_segment_header.get_properties())
        if self.image_entries:
            string += f'''\n\n{self.class_type_string()} Segment Entries:\n'''
            properties = [
                ('Index', 'Software ID', 'Secondary Software ID', 'Hash')]
            for idx, image_entry in enumerate(self.image_entries):
                properties.append((str(idx),) + image_entry.get_properties()[0])
            string += properties_repr(properties, [
                0], **('sep_rows',))
        return string

    
    def get_image_properties(self = None, authority = None):
        pass
    # WARNING: Decompyle incomplete

    
    def _get_errors_table(self = None, security_profile = None, path = None):
        errors_table = super()._get_errors_table(security_profile, path)
    # WARNING: Decompyle incomplete

    __classcell__ = None

