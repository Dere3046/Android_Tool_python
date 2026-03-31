
from contextlib import suppress
from typing import Any
import profile
from common.data.base_parser import DumpDict
from common.data.data import ceil_to_multiple
from common.parser.elf.bit32.program_header import ProgramHeader32
from common.parser.elf.bit64.program_header import ProgramHeader64
from common.parser.elf.defines import ELFCLASS32, PT_LOAD
from common.parser.elf.elf import ELF
from common.parser.elf.program_header import PROGRAM_HEADER_CLASSES
from common.parser.hash_segment.defines import AUTHORITY_OEM
from common.parser.parser_image_info_interface import ImageFormatType, ImageProperties, SEC_ELF_PROPERTIES
from common.parser.sec_dat.defines import SEC_DAT_VERSION_1
from common.parser.sec_dat.sec_dat import SecDat
from profile.defines import ANY, END, START
from profile.schema import FuseBlowing, SecELFProperties

class SecELF(ELF):
    
    def __init__(self = None, data = None, **kwargs):
        ''' Parse the data of an ELF image containing a Sec Dat segment. '''
        self.sec_dat_segment = None
        self.sec_dat_segment_phdr = None
        self.sec_dat_segment_phdr_idx = 0
    # WARNING: Decompyle incomplete

    
    def image_type_string(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def create_default(self = None, *, elf_class, sec_dat_version, sec_dat_segment_address, **_):
        super().create_default(elf_class, **('elf_class',))
    # WARNING: Decompyle incomplete

    
    def add_fuse_entries(self = None, fuse_entries = None):
        pass
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
                self.sec_dat_segment_phdr = load_phdr
                sec_dat_segment_data = self.segments[load_phdr]
            else:
                raise RuntimeError('ELF does not contain a Sec Dat Segment.')
            self.sec_dat_segment = None(memoryview(sec_dat_segment_data))
            return None

    
    def validate_before_operation(self = None, **kwargs):
        pass
    # WARNING: Decompyle incomplete

    
    def pack(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_fuse_entries(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def is_type(cls = None, data = None):
        ''' Detect whether the data is of an ELF image containing a Sec Dat segment. '''
        match = False
        if super().is_type(data):
            with suppress(Exception):
                elf = ELF(memoryview(data))
                load_phdrs = (lambda .0: [ phdr for phdr in .0 if phdr.p_type == PT_LOAD ])(elf.phdrs)
                if len(load_phdrs) == 1:
                    pass
            match = SecDat.is_type(elf.segments[load_phdrs[0]])
        None(None, None, None)
        return match
    # WARNING: Decompyle incomplete

    is_type = None(is_type)
    
    def get_dump_files(self = None, directory = None):
        pass
    # WARNING: Decompyle incomplete

    
    def __repr__(self = None):
        return super().__repr__() + '\n\n' + self.sec_dat_segment.__repr__()

    
    def get_segment_placement(self = None, phdr = None):
        if (self.phdrs[0] == phdr or self.phdrs[0].is_os_segment_phdr()) and self.phdrs[1] == phdr:
            return [
                START]
        return [
            None]

    
    def get_image_properties(self = None, _ = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_image_format(self = None, _ = None):
        pass
    # WARNING: Decompyle incomplete

    __classcell__ = None

