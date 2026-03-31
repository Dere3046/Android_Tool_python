
from typing import Optional, Union
from common.data.binary_struct import StructBase
from common.data.data import hex_val, is_congruent
from common.parser.elf.defines import ALIGN_1, PT_DESCRIPTION, PT_LOAD, PT_NULL, PT_PHDR, P_FLAGS, P_FLAGS_OS_PAGE_MODE, P_FLAGS_OS_SEGMENT_TYPE, SEGMENT, UNALIGNED
from common.parser.elf.positional_data import AbstractPositionalData
from common.parser.elf_with_hash_segment.defines import P_FLAGS_OS_SEGMENT_HASH, P_FLAGS_OS_SEGMENT_PHDR, UIE_ENCRYPTABLE_SEGMENTS

class ProgramHeader32(AbstractPositionalData, StructBase):
    p_align: int = 'ProgramHeader32'
    
    def __init__(self = None, data = None, check_is_type = None, bypass_validation = None):
        self.ignore = False
        self.p_offset = 0
        super().__init__(data, check_is_type, bypass_validation, **('data', 'check_is_type', 'bypass_validation'))
        if self.is_to_be_ignored():
            self.ignore = True
            return None

    
    def get_fields(cls = None):
        return [
            'p_type',
            'p_offset',
            'p_vaddr',
            'p_paddr',
            'p_filesz',
            'p_memsz',
            'p_flags',
            'p_align']

    get_fields = None(get_fields)
    
    def get_format(cls = None):
        return '<IIIIIIII'

    get_format = None(get_format)
    
    def p_flags_os_segment_type(self = None):
        return P_FLAGS_OS_SEGMENT_TYPE(self.p_flags)

    p_flags_os_segment_type = None(p_flags_os_segment_type)
    
    def is_os_segment_phdr(self = None):
        if self.p_type == PT_NULL:
            pass
        return self.p_flags_os_segment_type == P_FLAGS_OS_SEGMENT_PHDR

    
    def is_os_segment_hash(self = None):
        if self.p_type == PT_NULL:
            pass
        return self.p_flags_os_segment_type == P_FLAGS_OS_SEGMENT_HASH

    
    def p_flags_os_page_mode(self = None):
        return P_FLAGS_OS_PAGE_MODE(self.p_flags)

    p_flags_os_page_mode = None(p_flags_os_page_mode)
    
    def validate_before_operation(self = None, **_):
        if self.p_type == PT_LOAD:
            if self.p_filesz > self.p_memsz:
                raise RuntimeError(f'''Program Header\'s File Size, {hex_val(self.p_filesz)}, is larger than its Memory Size, {hex_val(self.p_memsz)}.''')
            if None.p_align not in UNALIGNED:
                if self.p_align & self.p_align - 1 != 0:
                    raise RuntimeError(f'''Program Header\'s Alignment, {hex_val(self.p_align)}, is not a power of 2.''')
                if not None(self.p_offset, self.p_vaddr, self.p_align):
                    raise RuntimeError(f'''Program Header\'s Offset, {hex_val(self.p_offset)}, and Virtual Address, {hex_val(self.p_vaddr)}, are not congruent modulo the Alignment, {hex_val(self.p_align)}. (Offset % Alignment) must equal (Virtual Address % Alignment).''')
                return None
            return None

    
    def _repr_p_flags(self = None):
        p_flags_string = ''
        for mask, flag, _ in P_FLAGS:
            if self.p_flags & mask:
                p_flags_string += flag
        return p_flags_string

    
    def _repr_os_segment_type(self = None):
        os_segment_type_string = f'''{hex(self.p_flags_os_segment_type)} (Meaning is OS specific)'''
        if self.is_os_segment_phdr():
            os_segment_type_string = 'PHDR (Encapsulates ELF Header and Program Header Table)'
            return os_segment_type_string
        if None.is_os_segment_hash():
            os_segment_type_string = 'HASH (Hash Table Segment)'
        return os_segment_type_string

    
    def get_properties(self = None):
        return [
            [
                PT_DESCRIPTION.get(self.p_type, hex_val(self.p_type)),
                hex_val(self.p_offset),
                hex_val(self.p_vaddr),
                hex_val(self.p_paddr),
                hex_val(self.p_filesz),
                hex_val(self.p_memsz),
                self._repr_p_flags(),
                hex_val(self.p_align),
                self._repr_os_segment_type()]]

    
    def offset(self = None):
        return self.p_offset

    offset = None(offset)
    
    def offset(self = None, value = None):
        self.p_offset = value

    offset = None(offset)
    
    def size(self = None):
        return self.p_filesz

    size = None(size)
    
    def size(self = None, value = None):
        self.p_filesz = value

    size = None(size)
    
    def alignment(self = None):
        if self.p_type == PT_LOAD or self.is_os_segment_hash():
            return self.p_align

    alignment = None(alignment)
    
    def address(self = None):
        return self.p_paddr

    address = None(address)
    
    def mem_size(self = None):
        return self.p_memsz

    mem_size = None(mem_size)
    
    def is_loadable(self = None):
        return self.p_type in UIE_ENCRYPTABLE_SEGMENTS

    is_loadable = None(is_loadable)
    
    def is_uie_encryptable(self = None):
        if self.is_loadable:
            pass
        return bool(self.size)

    is_uie_encryptable = None(is_uie_encryptable)
    
    def is_qbec_encryptable(self = None):
        if not self.is_os_segment_phdr():
            pass
        if not self.is_os_segment_hash():
            pass
        return bool(self.size)

    is_qbec_encryptable = None(is_qbec_encryptable)
    
    def is_encryptable(self = None):
        if not self.is_uie_encryptable:
            pass
        return self.is_qbec_encryptable

    is_encryptable = None(is_encryptable)
    
    def data_name(self = None):
        return SEGMENT

    data_name = None(data_name)
    
    def is_to_be_ignored(self = None):
        if not self.p_type == PT_PHDR and self.is_os_segment_phdr():
            pass
        return not (self.size)

    __classcell__ = None

