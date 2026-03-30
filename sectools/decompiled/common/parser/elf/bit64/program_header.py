
from common.data.data import hex_val
from common.parser.elf.bit32.program_header import ProgramHeader32
from common.parser.elf.defines import PT_DESCRIPTION

class ProgramHeader64(ProgramHeader32):
    
    def get_fields(cls = None):
        return [
            'p_type',
            'p_flags',
            'p_offset',
            'p_vaddr',
            'p_paddr',
            'p_filesz',
            'p_memsz',
            'p_align']

    get_fields = None(get_fields)
    
    def get_format(cls = None):
        return '<IIQQQQQQ'

    get_format = None(get_format)
    
    def get_properties(self = None):
        return [
            [
                PT_DESCRIPTION.get(self.p_type, hex_val(self.p_type, 16, **('num_chars',))),
                hex_val(self.p_offset, 16, **('num_chars',)),
                hex_val(self.p_vaddr, 16, **('num_chars',)),
                hex_val(self.p_paddr, 16, **('num_chars',)),
                hex_val(self.p_filesz, 16, **('num_chars',)),
                hex_val(self.p_memsz, 16, **('num_chars',)),
                self._repr_p_flags(),
                hex_val(self.p_align, 16, **('num_chars',)),
                self._repr_os_segment_type()]]


