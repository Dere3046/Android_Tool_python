
import os
import abc
import sys
from Cryptodome.Util.py3compat import byte_string
from Cryptodome.Util._file_system import pycryptodome_filename
if sys.version_info[0] < 3:
    import imp
    extension_suffixes = []
    for ext, mod, typ in imp.get_suffixes():
        if typ == imp.C_EXTENSION:
            extension_suffixes.append(ext)
else:
    from importlib import machinery
    extension_suffixes = machinery.EXTENSION_SUFFIXES
_buffer_type = (bytearray, memoryview)

class _VoidPointer(object):
    
    def get(self):
        '''Return the memory location we point to'''
        pass

    get = abc.abstractmethod(get)
    
    def address_of(self):
        '''Return a raw pointer to this pointer'''
        pass

    address_of = abc.abstractmethod(address_of)

# WARNING: Decompyle incomplete
