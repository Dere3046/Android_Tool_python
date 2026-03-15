"""ELF tool module."""

from .defines import (
    ELF_TOOL_NAME,
    ELF_TOOL_DESCRIPTION,
    GENERATE_OP,
    INSERT,
    COMBINE,
    REMOVE_SECTIONS,
    ELF_TOOL_GENERATE,
    ELF_TOOL_INSERT,
    ELF_TOOL_COMBINE,
    ELF_TOOL_REMOVE_SECTIONS,
)

from .core import ELFToolCore, log_info_wrap
from .utils import validate_args_for_elf_class, write_elf_outfile

__all__ = [
    'ELF_TOOL_NAME',
    'ELF_TOOL_DESCRIPTION',
    'GENERATE_OP',
    'INSERT',
    'COMBINE',
    'REMOVE_SECTIONS',
    'ELF_TOOL_GENERATE',
    'ELF_TOOL_INSERT',
    'ELF_TOOL_COMBINE',
    'ELF_TOOL_REMOVE_SECTIONS',
    'ELFToolCore',
    'log_info_wrap',
    'validate_args_for_elf_class',
    'write_elf_outfile',
]
