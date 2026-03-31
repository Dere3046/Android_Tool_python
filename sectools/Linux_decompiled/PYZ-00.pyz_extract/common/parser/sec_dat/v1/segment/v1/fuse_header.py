
from common.data.defines import PAD_BYTE_0
from common.parser.sec_dat.fuse_header import FuseHeaderCommon

class FuseHeaderV1(FuseHeaderCommon):
    fuse_count: int = 'FuseHeaderV1'
    
    def get_fields(cls = None):
        return super().get_fields() + [
            'fuse_entries_size',
            'fuse_count',
            'reserved']

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        pass
    # WARNING: Decompyle incomplete

    get_field_defaults = None(get_field_defaults)
    
    def get_format(cls = None):
        return super().get_format() + 'II16s'

    get_format = None(get_format)
    
    def validate_critical_fields(self):
        if self.version != self.VERSION:
            raise RuntimeError(f'''Sec Dat contains invalid Fuse Version: {self.version}.''')

    
    def get_properties(self):
        return [
            ('Version:', self.version),
            ('Total Fuse Entries Size:', f'''{self.fuse_entries_size} (bytes)'''),
            ('Number of Fuse Entries:', self.fuse_count)]

    __classcell__ = None

