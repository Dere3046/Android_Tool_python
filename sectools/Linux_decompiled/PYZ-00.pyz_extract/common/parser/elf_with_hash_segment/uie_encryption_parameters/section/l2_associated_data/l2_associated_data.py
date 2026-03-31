
from common.data.binary_struct import StructBase
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section.l2_associated_data.defines import L2_AD_MAJOR_VERSION_1, L2_AD_MAJOR_VERSION_2, L2_AD_MINOR_VERSION_0, L2_AD_MINOR_VERSION_1, L2_AD_MINOR_VERSION_2, L2_AD_SIZE

class L2AssociatedData(StructBase):
    minor_version: int = 'L2AssociatedData'
    
    def get_fields(cls = None):
        return [
            'ignored',
            'major_version',
            'minor_version']

    get_fields = None(get_fields)
    
    def get_format(cls = None):
        return '<IBB'

    get_format = None(get_format)
    
    def validate_critical_fields(self = None):
        if (self.major_version, self.minor_version) not in ((L2_AD_MAJOR_VERSION_1, L2_AD_MINOR_VERSION_0), (L2_AD_MAJOR_VERSION_1, L2_AD_MINOR_VERSION_1), (L2_AD_MAJOR_VERSION_1, L2_AD_MINOR_VERSION_2), (L2_AD_MAJOR_VERSION_2, L2_AD_MINOR_VERSION_0)):
            raise RuntimeError(f'''Wrapped L2 Associated Data has invalid Version: {self.major_version}.{self.minor_version}''')

    
    def validate(self):
        self.validate_critical_fields()



class L2AssociatedDataLength(StructBase):
    value: int = 'L2AssociatedDataLength'
    
    def get_fields(cls = None):
        return [
            'value']

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        return {
            'value': L2_AD_SIZE }

    get_field_defaults = None(get_field_defaults)
    
    def get_format(cls = None):
        return '>H'

    get_format = None(get_format)
    
    def validate_before_operation(self = None, **_):
        if self.value != L2_AD_SIZE:
            raise RuntimeError(f'''L2 Associated Data Length is invalid: {self.value}.''')


