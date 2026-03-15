"""ELF 64-bit program header implementation."""

from common.parser.elf.bit32.program_header import ProgramHeader32
from common.parser.elf.defines import PT_DESCRIPTION
from common.data.data import hex_val


class ProgramHeader64(ProgramHeader32):
    """ELF 64-bit program header."""

    STRUCT_FORMAT = '<IIQQQQQQ'
    STRUCT_FIELDS = (
        'p_type', 'p_flags', 'p_offset', 'p_vaddr', 'p_paddr',
        'p_filesz', 'p_memsz', 'p_align',
    )

    def __init__(self, data=None, check_is_type=None, bypass_validation=False):
        super().__init__(data, check_is_type, bypass_validation)

    def get_properties(self):
        return [[
            PT_DESCRIPTION.get(self.p_type, hex_val(self.p_type, 16)),
            hex_val(self.p_offset, 16), hex_val(self.p_vaddr, 16),
            hex_val(self.p_paddr, 16), hex_val(self.p_filesz, 16),
            hex_val(self.p_memsz, 16), self._repr_p_flags(),
            hex_val(self.p_align, 16), self._repr_os_segment_type()
        ]]
