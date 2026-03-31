
from common.data.binary_struct import StructBase
from common.data.data import hex_val
from common.parser.elf_preamble.defines import FLASH_CODE_WORD, MAGIC_NUM, PREAMBLE_MAGIC_NUMS

class PreambleHeaderStart(StructBase):
    magic_number: int = 'PreambleHeaderStart'
    
    def get_fields(cls):
        return [
            'flash_code_word',
            'magic',
            'magic_number']

    get_fields = classmethod(get_fields)
    
    def get_format(cls):
        return '<III'

    get_format = classmethod(get_format)
    
    def validate_critical_fields(self):
        ''' The data is not an ELFPreamble if it does not contain the code word and magic numbers '''
        if self.flash_code_word != FLASH_CODE_WORD:
            raise RuntimeError(f'''Preamble header contains invalid Flash Code Word: {self.flash_code_word}.''')
        if None.magic != MAGIC_NUM:
            raise RuntimeError(f'''Preamble header contains invalid Magic: {self.magic}.''')
        if None.magic_number not in PREAMBLE_MAGIC_NUMS:
            raise RuntimeError(f'''Preamble header contains invalid Magic Number: {self.magic_number}.''')

    
    def validate(self):
        self.validate_critical_fields()

    
    def get_properties(self):
        return [
            (hex_val(self.flash_code_word), hex_val(self.magic), hex_val(self.magic_number))]


