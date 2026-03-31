
from typing import Any
from common.data.base_parser import DumpDict
from common.parser.elf.defines import ELFCLASS32
from common.parser.elf.elf import ELF
from common.parser.elf_preamble.preamble import Preamble
from common.parser.hash_segment.defines import AUTHORITY_OEM
from common.parser.parser_image_info_interface import ELF_PROPERTIES, ImageProperties

class ELFWithPreamble(ELF):
    
    def __init__(self = None, data = None, **kwargs):
        self.preamble = None
        if data:
            self.preamble = Preamble(data)
            offset = self.preamble.get_size()
            data = data[offset:]
    # WARNING: Decompyle incomplete

    
    def create_default(self = None, *, elf_class, **_):
        raise RuntimeError(f'''Default creation of {self.class_type_string()} images is not supported.''')

    
    def pack(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def is_type(cls = None, data = None):
        ''' Detect whether the data is of an ELFWithPreamble image.'''
        match = Preamble.is_type(data)
        if match:
            elf_offset = Preamble(memoryview(data)).get_size()
            match = super().is_type(data[elf_offset:])
        return match

    is_type = None(is_type)
    
    def get_dump_files(self = None, directory = None):
        pass
    # WARNING: Decompyle incomplete

    
    def __repr__(self = None):
        return self._repr_compression_format() + 'Preamble:\n' + str(self.preamble) + '\n\n' + self._repr_elf()

    
    def get_image_properties(self = None, _ = None):
        elf_properties = super().get_image_properties()
        elf_properties[ELF_PROPERTIES].set_contains_preamble(True)
        return elf_properties

    __classcell__ = None

