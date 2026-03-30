
from common.parser.elf.bit32.elf_header import ELFHeader32
from common.parser.elf.defines import ELFCLASS64
from common.parser.elf.elf_header import ELFHeaderCommon

class ELFHeader64(ELFHeader32):
    
    def get_field_defaults(cls = None):
        pass
    # WARNING: Decompyle incomplete

    get_field_defaults = None(get_field_defaults)
    
    def get_format(cls):
        return ELFHeaderCommon.get_format() + 'QQQIHHHHHH'

    get_format = classmethod(get_format)
    
    def validate(self):
        ELFHeaderCommon.validate(self)
        if self.e_ident_class != ELFCLASS64:
            raise RuntimeError(f'''ELF is of invalid class: {self.e_ident_class}.''')

    __classcell__ = None

