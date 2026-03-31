
from typing import Optional, Union
from common.data.binary_struct import StructBase
from common.data.data import hex_val
from common.parser.elf.defines import SHT_NULL, ST_DESCRIPTION, SECTION, SH_FLAGS, SHT_NOBITS, UNALIGNED, ALIGN_1
from common.parser.elf.positional_data import AbstractPositionalData

class SectionHeader32(AbstractPositionalData, StructBase):
    sh_entsize: int = 'SectionHeader32'
    
    def __init__(self = None, data = None, check_is_type = None, bypass_validation = None):
        self.ignore = False
        self.sh_offset = 0
        self.sh_name_str = ''
        super().__init__(data, check_is_type, bypass_validation, **('data', 'check_is_type', 'bypass_validation'))
        if not self.sh_type in (SHT_NOBITS, SHT_NULL) or self.size:
            self.ignore = True
            return None

    
    def get_fields(cls):
        return [
            'sh_name',
            'sh_type',
            'sh_flags',
            'sh_addr',
            'sh_offset',
            'sh_size',
            'sh_link',
            'sh_info',
            'sh_addralign',
            'sh_entsize']

    get_fields = classmethod(get_fields)
    
    def get_format(cls):
        return '<IIIIIIIIII'

    get_format = classmethod(get_format)
    
    def validate_before_operation(self = None, **_):
        if self.sh_type != SHT_NULL or self.sh_addralign not in UNALIGNED:
            if self.sh_addralign & self.sh_addralign - 1 != 0:
                raise RuntimeError(f'''Section Header\'s Alignment, {hex_val(self.sh_addralign)}, is not a power of 2''')
            if None.sh_addr % self.sh_addralign != 0:
                raise RuntimeError(f'''Section Header\'s Address, {hex_val(self.sh_addr)}, is not properly aligned to {hex_val(self.sh_addralign)}''')
            return None
        return None

    
    def __repr_sh_flags__(self):
        sh_flags_string = ''
        for mask, flag, _ in SH_FLAGS:
            if self.sh_flags & mask:
                sh_flags_string += flag
        return sh_flags_string

    
    def get_properties(self):
        return [
            (self.sh_name_str, ST_DESCRIPTION.get(self.sh_type, hex_val(self.sh_type)), hex_val(self.sh_addr), hex_val(self.sh_offset), hex_val(self.sh_size), hex_val(self.sh_entsize), self.__repr_sh_flags__(), self.sh_link, self.sh_info, self.sh_addralign)]

    
    def offset(self):
        return self.sh_offset

    offset = property(offset)
    
    def offset(self, value):
        self.sh_offset = value

    offset = offset.setter(offset)
    
    def size(self):
        if self.sh_type not in (SHT_NOBITS, SHT_NULL):
            return self.sh_size

    size = property(size)
    
    def size(self, value):
        self.sh_size = value

    size = size.setter(size)
    
    def alignment(self):
        if self.sh_type != SHT_NULL:
            return self.sh_addralign

    alignment = property(alignment)
    
    def data_name(self):
        return SECTION

    data_name = property(data_name)
    __classcell__ = None

