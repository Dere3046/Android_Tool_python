
from common.data.binary_struct import StructBase
from common.parser.sec_dat.defines import SEC_DAT_FUSE_VERSION_1, SEC_DAT_FUSE_VERSION_2

class FuseHeaderCommon(StructBase):
    version: int = SEC_DAT_FUSE_VERSION_1
    
    def get_fields(cls):
        return [
            'version']

    get_fields = classmethod(get_fields)
    
    def get_field_defaults(cls):
        return {
            'version': cls.VERSION }

    get_field_defaults = classmethod(get_field_defaults)
    
    def get_format(cls):
        return '<I'

    get_format = classmethod(get_format)
    
    def validate_critical_fields(self):
        if self.version not in (SEC_DAT_FUSE_VERSION_1, SEC_DAT_FUSE_VERSION_2):
            raise RuntimeError(f'''Sec Dat contains invalid Fuse Version: {self.version}.''')

    
    def validate(self):
        self.validate_critical_fields()


