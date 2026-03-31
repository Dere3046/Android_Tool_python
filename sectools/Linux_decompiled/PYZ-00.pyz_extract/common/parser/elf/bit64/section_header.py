
from common.data.data import hex_val
from common.parser.elf.bit32.section_header import SectionHeader32
from common.parser.elf.defines import ST_DESCRIPTION

class SectionHeader64(SectionHeader32):
    
    def get_format(cls):
        return '<IIQQQQIIQQ'

    get_format = classmethod(get_format)
    
    def get_properties(self):
        return [
            (self.sh_name_str, ST_DESCRIPTION.get(self.sh_type, hex_val(self.sh_type, 16, **('num_chars',))), hex_val(self.sh_addr, 16, **('num_chars',)), hex_val(self.sh_offset, 16, **('num_chars',)), hex_val(self.sh_size, 16, **('num_chars',)), hex_val(self.sh_entsize, 16, **('num_chars',)), self.__repr_sh_flags__(), self.sh_link, self.sh_info, self.sh_addralign)]


