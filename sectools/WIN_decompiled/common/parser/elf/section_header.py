
from common.parser.elf.bit32.section_header import SectionHeader32
from common.parser.elf.bit64.section_header import SectionHeader64
from common.parser.elf.defines import ELFCLASS32, ELFCLASS64
SECTION_HEADER_CLASSES = {
    ELFCLASS64: SectionHeader64,
    ELFCLASS32: SectionHeader32 }
