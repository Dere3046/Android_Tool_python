
from typing import Any
from common.data.binary_struct import StructBase
from common.data.data import comma_separated_string, get_enabled_bit_indices_from_byte, hex_val
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section.l2_associated_data.defines import L2_AD_KEY_LADDER_LENGTH, L2_AD_MAJOR_VERSION_1, L2_AD_MINOR_VERSION_0
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section.l2_associated_data.l2_associated_data import L2AssociatedDataLength

class L2AssociatedDataV10(StructBase):
    MAJOR_VERSION = L2_AD_MAJOR_VERSION_1
    MINOR_VERSION = L2_AD_MINOR_VERSION_0
    reserved_3: bytes = 31
    
    def __init__(self = None, data = None, check_is_type = None, bypass_validation = None):
        self.software_ids = []
        self.software_id_bitmap = 0
        self.associated_data_length = L2AssociatedDataLength(data, check_is_type, bypass_validation, **('data', 'check_is_type', 'bypass_validation'))
        super().__init__(data[L2AssociatedDataLength.get_size():] if data else data, check_is_type, bypass_validation, **('data', 'check_is_type', 'bypass_validation'))

    
    def get_fields(cls = None):
        return [
            'reserved_0',
            'reserved_1',
            'major_version',
            'minor_version',
            'key_ladder_length',
            'reserved_2',
            'software_id_bitmap',
            'reserved_3']

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        return {
            'reserved_0': 0,
            'reserved_1': 0,
            'major_version': cls.MAJOR_VERSION,
            'minor_version': cls.MINOR_VERSION,
            'key_ladder_length': L2_AD_KEY_LADDER_LENGTH,
            'reserved_2': 0,
            'software_id_bitmap': 0,
            'reserved_3': b'' }

    get_field_defaults = None(get_field_defaults)
    
    def pack(self = None):
        return self.associated_data_length.pack() + super().pack()

    
    def get_format(cls = None):
        return '<BBBBBBI20s'

    get_format = None(get_format)
    
    def unpack_post_process(self = None):
        self.software_ids = get_enabled_bit_indices_from_byte(self.software_id_bitmap)

    
    def validate_software_id(cls = None, software_id = None):
        if software_id > cls.MAX_SOFTWARE_ID:
            raise RuntimeError(f'''Cannot set Software ID of v{cls.MAJOR_VERSION}.{cls.MINOR_VERSION} L2 Associated Data to {hex(software_id)}. The maximum allowed Software ID is {hex(cls.MAX_SOFTWARE_ID)}.''')

    validate_software_id = None(validate_software_id)
    
    def pack_pre_process(self = None):
        self.software_id_bitmap = 0
        for software_id in self.software_ids:
            self.validate_software_id(software_id)
            self.software_id_bitmap |= 1 << software_id

    
    def get_size(cls = None):
        return L2AssociatedDataLength.get_size() + super().get_size()

    get_size = None(get_size)
    
    def validate_critical_fields(self):
        if (self.major_version, self.minor_version) != (self.MAJOR_VERSION, self.MINOR_VERSION):
            raise RuntimeError(f'''Wrapped L2 Associated Data has invalid Version: {self.major_version}.{self.minor_version}.''')

    
    def validate(self = None):
        self.validate_critical_fields()

    
    def validate_before_operation(self = None, **kwargs):
        pass
    # WARNING: Decompyle incomplete

    
    def get_properties(self = None):
        pass

    
    def get_software_id_properties(self = None):
        return [
            ('Software IDs:', self.repr_software_id_bitmap())]

    
    def repr_software_id_bitmap(self = None):
        software_id = (lambda .0: [ hex_val(software_id, True, **('strip_leading_zeros',)) for software_id in .0 ])(self.software_ids)
        if software_id:
            return comma_separated_string(software_id, 'and', **('final_separator',))

    
    def set_software_id(self = None, software_id = None):
        self.software_ids.append(software_id)

    __classcell__ = None

