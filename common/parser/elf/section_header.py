"""
ELF节头模块
基于反编译分析实现
"""

from typing import Dict, Type, Union
from common.parser.elf.bit32.section_header import SectionHeader32
from common.parser.elf.bit64.section_header import SectionHeader64
from common.parser.elf.defines import ELFCLASS32, ELFCLASS64

SECTION_HEADER_CLASSES: Dict[int, Type[Union[SectionHeader32, SectionHeader64]]] = {
    ELFCLASS32: SectionHeader32,
    ELFCLASS64: SectionHeader64
}