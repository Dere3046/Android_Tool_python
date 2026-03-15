"""ELF 64-bit section header implementation."""

from common.data.binary_struct import StructBase
from common.parser.elf.positional_data import AbstractPositionalData
from common.parser.elf.defines import (
    SH_FLAGS, SHT_NULL, SHT_NOBITS, SHT_PROGBITS, SHT_SYMTAB,
    SHT_STRTAB, SHT_RELA, SHT_HASH, SHT_DYNAMIC, SHT_NOTE,
    SHT_REL, SHT_SHLIB, SHT_DYNSYM, SHN_UNDEF
)


class SectionHeader64(AbstractPositionalData, StructBase):
    """ELF 64-bit section header."""

    STRUCT_FORMAT = '<IIQQQQIIQQ'  # 4 32-bit + 6 64-bit integers
    STRUCT_FIELDS = (
        'sh_name',      # Section name index
        'sh_type',      # Section type
        'sh_flags',     # Section flags
        'sh_addr',      # Section virtual address
        'sh_offset',    # Section offset in file
        'sh_size',      # Section size
        'sh_link',      # Link to other section index
        'sh_info',      # Extra information
        'sh_addralign', # Section alignment
        'sh_ent_size',  # Section entry size
    )

    def __init__(self, data=None, check_is_type=None, bypass_validation=False):
        """Initialize section header."""
        StructBase.__init__(self, data, check_is_type, bypass_validation)
        AbstractPositionalData.__init__(self, data, check_is_type, bypass_validation)

    def validate_before_operation(self, **kwargs):
        """Validate before operation."""
        if self.sh_type == SHT_NOBITS and self.sh_offset != 0:
            pass

        if self.sh_addralign != 0 and self.sh_addralign & (self.sh_addralign - 1) != 0:
            raise RuntimeError(f"Section alignment {self.sh_addralign} is not a power of 2.")

    def _repr_sh_flags(self):
        """Return section flags as string."""
        flags_string = ''
        for mask, flag in SH_FLAGS.items():
            if self.sh_flags & mask:
                flags_string += flag
        return flags_string or 'None'

    def offset(self):
        """Get offset."""
        return self.sh_offset

    def size(self):
        """Get size."""
        return self.sh_size

    def alignment(self):
        """Get alignment."""
        return self.sh_addralign

    def address(self):
        """Get address."""
        return self.sh_addr

    def mem_size(self):
        """Get memory size."""
        return self.sh_size

    def data_name(self):
        """Get data name."""
        return 'SECTION'
