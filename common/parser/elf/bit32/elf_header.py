"""ELF 32-bit header implementation."""

from common.data.binary_struct import StructBase
from common.parser.elf.defines import ELFCLASS32, EV_CURRENT


class ELFHeader32(StructBase):
    """ELF 32-bit header."""

    STRUCT_FORMAT = '<16sHHIIIIIHHHHHH'
    STRUCT_FIELDS = (
        'e_ident', 'e_type', 'e_machine', 'e_version', 'e_entry',
        'e_phoff', 'e_shoff', 'e_flags', 'e_ehsize', 'e_phentsize',
        'e_phnum', 'e_shentsize', 'e_shnum', 'e_shstrndx',
    )

    def __init__(self, data=None, check_is_type=None, bypass_validation=False):
        super().__init__(data, check_is_type, bypass_validation)
        if data and self.e_ident[:4] != b'\x7fELF':
            raise ValueError("Invalid ELF magic number")

    @property
    def e_ident_class(self):
        return self.e_ident[4] if len(self.e_ident) >= 5 else ELFCLASS32

    def validate_before_operation(self):
        if self.e_ident[:4] != b'\x7fELF':
            raise ValueError("Invalid ELF magic number")
        if self.e_version != EV_CURRENT:
            raise ValueError(f"Unsupported ELF version: {self.e_version}")
        if self.e_ehsize != 52:
            raise ValueError(f"Invalid ELF header size: {self.e_ehsize}")
        if self.e_phentsize != 32:
            raise ValueError(f"Invalid program header entry size: {self.e_phentsize}")

    def offset(self):
        return 0

    def size(self):
        return 52

    def end(self):
        return 52
