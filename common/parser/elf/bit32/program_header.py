"""ELF 32-bit program header implementation."""

from common.data.binary_struct import StructBase
from common.parser.elf.defines import (
    PT_DESCRIPTION, PT_LOAD, PT_NULL, PT_PHDR,
    P_FLAGS, P_FLAGS_OS_PAGE_MODE, P_FLAGS_OS_SEGMENT_TYPE,
    P_FLAGS_OS_SEGMENT_PHDR, P_FLAGS_OS_SEGMENT_HASH,
    UIE_ENCRYPTABLE_SEGMENTS, UNALIGNED,
)
from common.parser.elf.positional_data import AbstractPositionalData


class ProgramHeader32(AbstractPositionalData, StructBase):
    """ELF 32-bit program header."""

    STRUCT_FORMAT = '<IIIIIIII'
    STRUCT_FIELDS = (
        'p_type', 'p_offset', 'p_vaddr', 'p_paddr',
        'p_filesz', 'p_memsz', 'p_flags', 'p_align',
    )

    def __init__(self, data=None, check_is_type=None, bypass_validation=False):
        StructBase.__init__(self, data, check_is_type, bypass_validation)
        AbstractPositionalData.__init__(self, data, check_is_type, bypass_validation)
        self.ignore = False
        if self.is_to_be_ignored():
            self.ignore = True

    def p_flags_os_segment_type(self):
        return P_FLAGS_OS_SEGMENT_TYPE(self.p_flags)

    def is_os_segment_phdr(self):
        if self.p_type == PT_NULL:
            return False
        return self.p_flags_os_segment_type() == P_FLAGS_OS_SEGMENT_PHDR

    def is_os_segment_hash(self):
        if self.p_type == PT_NULL:
            return False
        return self.p_flags_os_segment_type() == P_FLAGS_OS_SEGMENT_HASH

    def p_flags_os_page_mode(self):
        return P_FLAGS_OS_PAGE_MODE(self.p_flags)

    def validate_before_operation(self, **kwargs):
        if self.p_type == PT_LOAD:
            if self.p_filesz > self.p_memsz:
                raise RuntimeError(
                    f"Program Header's File Size, 0x{self.p_filesz:x}, "
                    f"is larger than its Memory Size, 0x{self.p_memsz:x}."
                )
            if self.p_align not in (UNALIGNED, 0):
                if self.p_align & (self.p_align - 1) != 0:
                    raise RuntimeError(
                        f"Program Header's Alignment, 0x{self.p_align:x}, "
                        f"is not a power of 2."
                    )

    def _repr_p_flags(self):
        p_flags_string = ''
        if hasattr(P_FLAGS, '__iter__'):
            for mask, flag, _ in P_FLAGS:
                if self.p_flags & mask:
                    p_flags_string += flag
        else:
            p_flags_string = hex(self.p_flags)
        return p_flags_string

    def _repr_os_segment_type(self):
        os_segment_type_string = f"0x{self.p_flags_os_segment_type():x} (Meaning is OS specific)"
        if self.is_os_segment_phdr():
            os_segment_type_string = 'PHDR (Encapsulates ELF Header and Program Header Table)'
        elif self.is_os_segment_hash():
            os_segment_type_string = 'HASH (Hash Table Segment)'
        return os_segment_type_string

    def get_properties(self):
        return [[
            PT_DESCRIPTION.get(self.p_type, hex(self.p_type)),
            hex(self.p_offset), hex(self.p_vaddr), hex(self.p_paddr),
            hex(self.p_filesz), hex(self.p_memsz),
            self._repr_p_flags(), hex(self.p_align),
            self._repr_os_segment_type()
        ]]

    def offset(self):
        return self.p_offset

    def size(self):
        return self.p_filesz

    def alignment(self):
        if self.p_type == PT_LOAD or self.is_os_segment_hash():
            return self.p_align
        return 0

    def address(self):
        return self.p_paddr

    def mem_size(self):
        return self.p_memsz

    def is_loadable(self):
        return self.p_type in UIE_ENCRYPTABLE_SEGMENTS

    def is_uie_encryptable(self):
        return bool(self.size()) if self.is_loadable() else False

    def is_qbec_encryptable(self):
        if not self.is_os_segment_phdr() and not self.is_os_segment_hash():
            return bool(self.size())
        return False

    def is_encryptable(self):
        return self.is_uie_encryptable() or self.is_qbec_encryptable()

    def data_name(self):
        return 'SEGMENT'

    def end(self):
        return self.offset() + self.size()

    def is_to_be_ignored(self):
        if self.p_type == PT_PHDR and self.is_os_segment_phdr():
            return not bool(self.size())
        return False
