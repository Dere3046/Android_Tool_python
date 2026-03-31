
from typing import Any, Optional, Union
from common.parser.elf.defines import ALIGN_1, ELFCLASS32, ELF_HEADER
from common.parser.elf.elf_header import ELFHeaderCommon
from common.parser.elf.positional_data import AbstractPositionalData

class ELFHeader32(AbstractPositionalData, ELFHeaderCommon):
    
    def __init__(self = None, data = None, check_is_type = None, bypass_validation = None):
        self.ignore = False
        super().__init__(data, check_is_type, bypass_validation, **('data', 'check_is_type', 'bypass_validation'))

    
    def get_fields(cls = None):
        return super().get_fields() + [
            'e_entry',
            'e_phoff',
            'e_shoff',
            'e_flags',
            'e_ehsize',
            'e_phentsize',
            'e_phnum',
            'e_shentsize',
            'e_shnum',
            'e_shstrndx']

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        pass
    # WARNING: Decompyle incomplete

    get_field_defaults = None(get_field_defaults)
    
    def get_format(cls = None):
        return super().get_format() + 'IIIIHHHHHH'

    get_format = None(get_format)
    
    def validate(self = None):
        super().validate()
        if self.e_ident_class != ELFCLASS32:
            raise RuntimeError(f'''ELF is of invalid class: {self.e_ident_class}.''')

    
    def validate_before_operation(self = None, **kwargs):
        pass
    # WARNING: Decompyle incomplete

    
    def offset(self):
        return 0

    offset = property(offset)
    
    def offset(self, value):
        if value != 0:
            raise RuntimeError('ELF Header offset must be 0.')

    offset = offset.setter(offset)
    
    def size(self):
        return self.e_ehsize

    size = property(size)
    
    def size(self, value):
        if value != self.get_size():
            raise RuntimeError(f'''ELF Header size must be {self.get_size()}''')

    size = size.setter(size)
    
    def alignment(self):
        return ALIGN_1

    alignment = property(alignment)
    
    def data_name(self):
        return ELF_HEADER

    data_name = property(data_name)
    __classcell__ = None

