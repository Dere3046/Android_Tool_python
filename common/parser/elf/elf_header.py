"""
ELF头部模块
基于反编译分析实现
"""

from typing import Dict, Type, Union
from common.parser.elf.bit32.elf_header import ELFHeader32
from common.parser.elf.bit64.elf_header import ELFHeader64
from common.parser.elf.defines import ELFCLASS32, ELFCLASS64

ELF_HEADER_CLASSES: Dict[int, Type[Union[ELFHeader32, ELFHeader64]]] = {
    ELFCLASS32: ELFHeader32,
    ELFCLASS64: ELFHeader64
}


class ELFHeaderCommon:
    """ELF头部通用基类"""
    
    def __init__(self, data=None, **kwargs):
        """初始化ELF头部通用基类"""
        pass
    
    def get_ident(self) -> dict:
        """获取标识字段（子类实现）"""
        raise NotImplementedError