"""
ELF程序头模块
基于反编译分析实现
"""

from typing import Dict, Type, Union
from common.parser.elf.bit32.program_header import ProgramHeader32
from common.parser.elf.bit64.program_header import ProgramHeader64
from common.parser.elf.defines import ELFCLASS32, ELFCLASS64

PROGRAM_HEADER_CLASSES: Dict[int, Type[Union[ProgramHeader32, ProgramHeader64]]] = {
    ELFCLASS32: ProgramHeader32,
    ELFCLASS64: ProgramHeader64
}