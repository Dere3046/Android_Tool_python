
from common.parser.sec_dat.defines import SEC_DAT_VERSION_3
from common.parser.sec_dat.sec_dat_header import SecDatHeaderCommon

class SecDatSegmentHeaderV3(SecDatHeaderCommon):
    fuse_count: int = 'SecDatSegmentHeaderV3'
    
    def get_fields(cls = None):
        return super().get_fields() + [
            'fuse_count']

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        pass
    # WARNING: Decompyle incomplete

    get_field_defaults = None(get_field_defaults)
    
    def get_format(cls = None):
        return super().get_format() + 'I'

    get_format = None(get_format)
    
    def get_properties(self = None):
        return super().get_properties() + [
            ('Number of Fuse Entries:', self.fuse_count)]

    
    def validate_critical_fields(self = None):
        super().validate_critical_fields()
        if self.version != SEC_DAT_VERSION_3:
            raise RuntimeError(f'''Sec Dat Header contains invalid version: {self.version}.''')

    __classcell__ = None

