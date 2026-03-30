
import operator
from typing import Any, List, Optional, Union
from common.data.base_parser import BaseParserGenerator, DumpDict
from common.data.data import properties_repr
from common.parser.elf.bit32.elf_header import ELFHeader32
from common.parser.elf.bit32.program_header import ProgramHeader32
from common.parser.elf.bit64.elf_header import ELFHeader64
from common.parser.elf.bit64.program_header import ProgramHeader64
from common.parser.elf.defines import ALIGN_1, ELFCLASS32, ELFCLASS64, EM_ARM, PHDR_TABLE
from common.parser.elf.elf_header import ELFHeaderCommon
from common.parser.elf.positional_data import AbstractPositionalData, PositionalData
from common.parser.elf.program_header import PROGRAM_HEADER_CLASSES
ELF_HEADER_CLASSES = {
    ELFCLASS64: ELFHeader64,
    ELFCLASS32: ELFHeader32 }

class MDT(BaseParserGenerator):
    
    def __init__(self = None, data = None, **kwargs):
        self.elf_header = None
        self.phdrs = []
    # WARNING: Decompyle incomplete

    
    def phdr_table_offset(self = None):
        pass
    # WARNING: Decompyle incomplete

    phdr_table_offset = None(phdr_table_offset)
    
    def create_default(self = None, *, elf_class, e_entry, e_machine, **_):
        if not self.elf_header:
            if elf_class in ELF_HEADER_CLASSES:
                self.elf_header = ELF_HEADER_CLASSES[elf_class].from_fields(e_entry, e_machine, **('e_entry', 'e_machine'))
                return None
            raise None(f'''Creation of class {elf_class} {self.class_type_string()}s is not supported.''')

    
    def unpack(self = None, data = None):
        elf_class = ELFHeaderCommon(data).e_ident_class
        self.elf_header = ELF_HEADER_CLASSES[elf_class](data)
        phdr_class = PROGRAM_HEADER_CLASSES[elf_class]
        for phdr_index in range(self.elf_header.e_phnum):
            if self.elf_header.e_phentsize < phdr_class.get_size():
                raise RuntimeError(f'''ELF has invalid Program Header entry size: {self.elf_header.e_phentsize}, expected size is {phdr_class.get_size()}.''')
            phdr = None(data[self.phdr_table_offset + phdr_index * self.elf_header.e_phentsize:])
            self.phdrs.append(phdr)

    
    def pack(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_dump_files(self = None, directory = None):
        pass
    # WARNING: Decompyle incomplete

    
    def __repr__(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def _repr_phdrs(self = None):
        return properties_repr(self._get_phdr_properties(), [
            0], **('sep_rows',))

    
    def _get_phdr_properties(self = None):
        property_titles = [
            'Index',
            'Type',
            'Offset',
            'VirtAddr',
            'PhysAddr',
            'FileSize',
            'MemSize',
            'Flags',
            'Align',
            'OS Segment Type']
        properties = [
            property_titles]
        for idx, phdr in enumerate(self.phdrs):
            phdr_properties = phdr.get_properties()
            phdr_properties[0].insert(0, idx)
            properties += phdr_properties
        return properties

    
    def get_shdr_positional_entries(self = None):
        return []

    
    def get_paddings_entries(self = None):
        return []

    
    def get_positional_entries(self = None, include_phdr_table = None, include_elf_header = None, ignore_voids = (True, True, False)):
        positional_entries = []
    # WARNING: Decompyle incomplete

    
    def get_phdr_table_positional_entry(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_last_entry(entries = None):
        return sorted(entries, operator.attrgetter('end'), **('key',))[-1]

    get_last_entry = None(get_last_entry)
    
    def is_type(cls = None, data = None):
        '''
        Check if the size of the data exactly matches the size of the ELF Header plus the size of the Program Header
        Table as indicated in the ELF Header.
        '''
        match = False
        if ELFHeaderCommon.is_type(data):
            elf_header = ELF_HEADER_CLASSES[ELFHeaderCommon(data).e_ident_class](data)
            match = len(data) == elf_header.e_ehsize + elf_header.e_phentsize * elf_header.e_phnum
        return match

    is_type = None(is_type)
    
    def get_size(self):
        pass
    # WARNING: Decompyle incomplete

    __classcell__ = None

