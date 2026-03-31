
from common.data.defines import PAD_BYTE_0
from common.parser.sec_dat.defines import SEC_DAT_VERSION_2, SEC_DAT_DEFAULT_INFO
from common.parser.sec_dat.sec_dat_footer import SecDatFooter
from common.parser.sec_dat.sec_dat_header import SecDatHeaderCommon

class SecDatSegmentHeaderV2(SecDatHeaderCommon):
    num_segments: int = 'SecDatSegmentHeaderV2'
    
    def get_fields(cls = None):
        return super().get_fields() + [
            'sec_dat_data_size',
            'info',
            'num_segments',
            'reserved']

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        pass
    # WARNING: Decompyle incomplete

    get_field_defaults = None(get_field_defaults)
    
    def get_format(cls = None):
        return super().get_format() + 'I16sI12s'

    get_format = None(get_format)
    
    def get_properties(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def validate_critical_fields(self = None):
        super().validate_critical_fields()
        if self.version != SEC_DAT_VERSION_2:
            raise RuntimeError(f'''Sec Dat Header contains invalid version: {self.version}.''')

    __classcell__ = None

