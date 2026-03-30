
from common.data.binary_struct import StructBase
from common.parser.sec_dat.defines import SEC_DAT_MAGIC1, SEC_DAT_MAGIC2, SEC_DAT_SUPPORTED_VERSIONS, SEC_DAT_VERSION_1

class SecDatHeaderCommon(StructBase):
    version: int = 'SecDatHeaderCommon'
    
    def get_fields(cls):
        return [
            'magic1',
            'magic2',
            'version']

    get_fields = classmethod(get_fields)
    
    def get_field_defaults(cls):
        return {
            'magic1': SEC_DAT_MAGIC1,
            'magic2': SEC_DAT_MAGIC2,
            'version': SEC_DAT_VERSION_1 }

    get_field_defaults = classmethod(get_field_defaults)
    
    def get_format(cls):
        return '<III'

    get_format = classmethod(get_format)
    
    def validate_critical_fields(self):
        ''' The data is not of a Sec Dat Segment if it does not contain the magic1 and magic2 '''
        if self.magic1 != SEC_DAT_MAGIC1:
            raise RuntimeError(f'''Sec Dat Header contains invalid Magic 1: {self.magic1}.''')
        if None.magic2 != SEC_DAT_MAGIC2:
            raise RuntimeError(f'''Sec Dat Header contains invalid Magic 2: {self.magic1}.''')
        if None.version not in SEC_DAT_SUPPORTED_VERSIONS:
            raise RuntimeError(f'''Sec Dat Header contains invalid version: {self.version}.''')

    
    def validate(self):
        self.validate_critical_fields()

    
    def get_properties(self):
        return [
            ('Magic 1:', hex(self.magic1)),
            ('Magic 2:', hex(self.magic2)),
            ('Version:', self.version)]


