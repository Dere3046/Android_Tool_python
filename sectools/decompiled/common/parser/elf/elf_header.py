
from binascii import hexlify
from common.data.binary_struct import StructBase
from common.data.data import hex_val
from common.parser.elf.defines import ELFCLASS32, ELFCLASS64, ELFCLASS_DESCRIPTION, ELFDATA2LSB, ELFDATA2MSB, ELFDATA_DESCRIPTION, ELFMAG, ELFOSABI_DESCRIPTION, EM_ARM, EM_INT_TO_DESCRIPTION, ET_DESCRIPTION, EV_CURRENT, EV_DESCRIPTION, E_IDENT_SIZE

class ELFHeaderCommon(StructBase):
    e_entry: int = 'ELFHeaderCommon'
    
    def get_fields(cls):
        return [
            'e_ident_mag',
            'e_ident_class',
            'e_ident_data',
            'e_ident_version',
            'e_ident_osabi',
            'e_ident_abiver',
            'e_ident_pad',
            'e_type',
            'e_machine',
            'e_version']

    get_fields = classmethod(get_fields)
    
    def get_field_defaults(cls):
        return {
            'e_ident_mag': ELFMAG,
            'e_ident_class': ELFCLASS32,
            'e_ident_data': ELFDATA2LSB,
            'e_ident_version': EV_CURRENT,
            'e_ident_osabi': 0,
            'e_ident_abiver': 0,
            'e_ident_pad': b'',
            'e_type': 0,
            'e_machine': EM_ARM,
            'e_version': EV_CURRENT }

    get_field_defaults = classmethod(get_field_defaults)
    
    def get_format(cls):
        return '<4sBBBBB7sHHI'

    get_format = classmethod(get_format)
    
    def validate_critical_fields(self):
        ''' The data is not of an ELF Header if it does not contain the magic '''
        if self.e_ident_mag != ELFMAG:
            raise RuntimeError(f'''ELF contains invalid Magic: {self.e_ident_mag}.''')

    
    def validate(self):
        self.validate_critical_fields()
        if self.e_ident_class not in (ELFCLASS32, ELFCLASS64):
            raise RuntimeError(f'''ELF is of invalid class: {self.e_ident_class}.''')

    
    def validate_before_operation(self = None, **_):
        if self.e_ident_data not in (ELFDATA2LSB, ELFDATA2MSB):
            raise RuntimeError(f'''ELF is of invalid data encoding: {self.e_ident_data}.''')
        if None.e_ident_version != EV_CURRENT:
            raise RuntimeError(f'''ELF is of invalid version: {self.e_ident_version}.''')
        if None.e_version != EV_CURRENT:
            raise RuntimeError(f'''ELF is of invalid version: {self.e_version}.''')

    
    def get_properties(self):
        return [
            ('Magic:', hexlify(self.pack()[:E_IDENT_SIZE], ' ').decode()),
            ('Class:', ELFCLASS_DESCRIPTION.get(self.e_ident_class, self.e_ident_class)),
            ('Data:', ELFDATA_DESCRIPTION.get(self.e_ident_data, self.e_ident_data)),
            ('Version:', EV_DESCRIPTION.get(self.e_ident_version, self.e_ident_version)),
            ('OS/ABI:', ELFOSABI_DESCRIPTION.get(self.e_ident_osabi, self.e_ident_version)),
            ('ABI Version:', self.e_ident_abiver),
            ('Type:', ET_DESCRIPTION.get(self.e_type, hex_val(self.e_type, True, **('strip_leading_zeros',)))),
            ('Machine:', EM_INT_TO_DESCRIPTION.get(self.e_machine, hex_val(self.e_type, True, **('strip_leading_zeros',)))),
            ('Version:', hex_val(self.e_version, True, **('strip_leading_zeros',))),
            ('Entry point address:', hex_val(self.e_entry, 16, True, **('num_chars', 'strip_leading_zeros'))),
            ('Start of program headers:', f'''{self.e_phoff} (bytes into file)'''),
            ('Start of section headers:', f'''{self.e_shoff} (bytes into file)'''),
            ('Flags:', hex_val(self.e_flags, True, **('strip_leading_zeros',))),
            ('Size of this header:', f'''{self.e_ehsize} (bytes)'''),
            ('Size of program headers:', f'''{self.e_phentsize} (bytes)'''),
            ('Number of program headers:', self.e_phnum),
            ('Size of section headers:', f'''{self.e_shentsize} (bytes)'''),
            ('Number of section headers:', self.e_shnum),
            ('Section header string table index:', self.e_shstrndx)]


