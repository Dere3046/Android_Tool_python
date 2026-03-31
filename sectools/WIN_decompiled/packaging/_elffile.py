
'''
ELF file parser.

This provides a class ``ELFFile`` that parses an ELF executable in a similar
interface to ``ZipFile``. Only the read interface is implemented.

Based on: https://gist.github.com/lyssdod/f51579ae8d93c8657a5564aefc2ffbca
ELF header: https://refspecs.linuxfoundation.org/elf/gabi4+/ch4.eheader.html
'''
from __future__ import annotations
import enum
import os
import struct
from typing import IO

class ELFInvalid(ValueError):
    pass


class EIClass(enum.IntEnum):
    C32 = 1
    C64 = 2


class EIData(enum.IntEnum):
    Lsb = 1
    Msb = 2


class EMachine(enum.IntEnum):
    I386 = 3
    S390 = 22
    Arm = 40
    X8664 = 62
    AArc64 = 183


class ELFFile:
    '''
    Representation of an ELF executable.
    '''
    
    def __init__(self = None, f = None):
        self._f = f
    # WARNING: Decompyle incomplete

    
    def _read(self = None, fmt = None):
        return struct.unpack(fmt, self._f.read(struct.calcsize(fmt)))

    
    def interpreter(self = None):
        '''
        The path recorded in the ``PT_INTERP`` section header.
        '''
        pass
    # WARNING: Decompyle incomplete

    interpreter = None(interpreter)

