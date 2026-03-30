
import collections
import functools
import os
import re
import struct
import sys
import warnings
from typing import IO, Dict, Iterator, NamedTuple, Optional, Tuple

class _ELFFileHeader:
    
    class _InvalidELFFileHeader(ValueError):
        __qualname__ = '_ELFFileHeader._InvalidELFFileHeader'
        __doc__ = '\n        An invalid ELF file header was found.\n        '

    ELF_MAGIC_NUMBER = 2135247942
    ELFCLASS32 = 1
    ELFCLASS64 = 2
    ELFDATA2LSB = 1
    ELFDATA2MSB = 2
    EM_386 = 3
    EM_S390 = 22
    EM_ARM = 40
    EM_X86_64 = 62
    EF_ARM_ABIMASK = 0xFF000000L
    EF_ARM_ABI_VER5 = 83886080
    EF_ARM_ABI_FLOAT_HARD = 1024
    
    def __init__(self = None, file = None):
        
        def unpack(fmt = None):
            pass
        # WARNING: Decompyle incomplete

        self.e_ident_magic = unpack('>I')
        if self.e_ident_magic != self.ELF_MAGIC_NUMBER:
            raise _ELFFileHeader._InvalidELFFileHeader()
        self.e_ident_class = None('B')
        if self.e_ident_class not in {
            self.ELFCLASS32,
            self.ELFCLASS64}:
            raise _ELFFileHeader._InvalidELFFileHeader()
        self.e_ident_data = None('B')
        if self.e_ident_data not in {
            self.ELFDATA2LSB,
            self.ELFDATA2MSB}:
            raise _ELFFileHeader._InvalidELFFileHeader()
        self.e_ident_version = None('B')
        self.e_ident_osabi = unpack('B')
        self.e_ident_abiversion = unpack('B')
        self.e_ident_pad = file.read(7)
        format_h = '<H' if self.e_ident_data == self.ELFDATA2LSB else '>H'
        format_i = '<I' if self.e_ident_data == self.ELFDATA2LSB else '>I'
        format_q = '<Q' if self.e_ident_data == self.ELFDATA2LSB else '>Q'
        format_p = format_i if self.e_ident_class == self.ELFCLASS32 else format_q
        self.e_type = unpack(format_h)
        self.e_machine = unpack(format_h)
        self.e_version = unpack(format_i)
        self.e_entry = unpack(format_p)
        self.e_phoff = unpack(format_p)
        self.e_shoff = unpack(format_p)
        self.e_flags = unpack(format_i)
        self.e_ehsize = unpack(format_h)
        self.e_phentsize = unpack(format_h)
        self.e_phnum = unpack(format_h)
        self.e_shentsize = unpack(format_h)
        self.e_shnum = unpack(format_h)
        self.e_shstrndx = unpack(format_h)



def _get_elf_header():
    pass
# WARNING: Decompyle incomplete


def _is_linux_armhf():
    elf_header = _get_elf_header()
    if elf_header is None:
        return False
    result = None.e_ident_class == elf_header.ELFCLASS32
    result &= (elf_header.e_ident_data == elf_header.ELFDATA2LSB)
    result &= (elf_header.e_machine == elf_header.EM_ARM)
    result &= (elf_header.e_flags & elf_header.EF_ARM_ABIMASK == elf_header.EF_ARM_ABI_VER5)
    result &= (elf_header.e_flags & elf_header.EF_ARM_ABI_FLOAT_HARD == elf_header.EF_ARM_ABI_FLOAT_HARD)
    return result


def _is_linux_i686():
    elf_header = _get_elf_header()
    if elf_header is None:
        return False
    result = None.e_ident_class == elf_header.ELFCLASS32
    result &= (elf_header.e_ident_data == elf_header.ELFDATA2LSB)
    result &= (elf_header.e_machine == elf_header.EM_386)
    return result


def _have_compatible_abi(arch = None):
    if arch == 'armv7l':
        return _is_linux_armhf()
    if None == 'i686':
        return _is_linux_i686()
    return None in frozenset({'aarch64', 'ppc64le', 's390x', 'ppc64', 'x86_64'})

_LAST_GLIBC_MINOR: Dict[(int, int)] = collections.defaultdict((lambda : 50))

class _GLibCVersion(NamedTuple):
    minor: int = '_GLibCVersion'


def _glibc_version_string_confstr():
    '''
    Primary implementation of glibc_version_string using os.confstr.
    '''
    pass
# WARNING: Decompyle incomplete


def _glibc_version_string_ctypes():
    '''
    Fallback implementation of glibc_version_string using ctypes.
    '''
    pass
# WARNING: Decompyle incomplete


def _glibc_version_string():
    '''Returns glibc version string, 