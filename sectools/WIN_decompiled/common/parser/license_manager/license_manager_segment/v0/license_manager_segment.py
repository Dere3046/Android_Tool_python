
from common.data.binary_struct import StructBase
from common.data.data import hex_val
from common.parser.license_manager.license_manager_segment.v0.defines import LM_DESCSZ, LM_MAG, LM_NAMESZ, LM_TYPE

class LicenseManagerSegmentV0(StructBase):
    library_id: int = 'LicenseManagerSegmentV0'
    
    def get_fields(cls):
        return [
            'namesz',
            'descsz',
            'type',
            'magic',
            'version',
            'client_id',
            'library_id',
            'reserved']

    get_fields = classmethod(get_fields)
    
    def get_field_defaults(cls):
        return {
            'namesz': LM_NAMESZ,
            'descsz': LM_DESCSZ,
            'type': LM_TYPE,
            'magic': LM_MAG,
            'version': 0,
            'client_id': 0,
            'library_id': 0,
            'reserved': 0 }

    get_field_defaults = classmethod(get_field_defaults)
    
    def get_format(cls):
        return '<III8sIIII'

    get_format = classmethod(get_format)
    
    def validate_critical_fields(self):
        ''' The data is not of a License Manager Segment if it does not contain the magic '''
        if self.magic != LM_MAG:
            raise RuntimeError(f'''License Manager Segment contains invalid Magic: {self.magic}.''')
        if None.version != 0:
            raise RuntimeError(f'''License Manager Segment contains invalid version: {self.version}.''')

    
    def validate(self):
        self.validate_critical_fields()
        if self.namesz != LM_NAMESZ:
            raise RuntimeError(f'''License Manager Segment contains invalid Name Size: {self.namesz}.''')
        if None.descsz != LM_DESCSZ:
            raise RuntimeError(f'''License Manager Segment contains invalid Description Size: {self.descsz}.''')
        if None.type != LM_TYPE:
            raise RuntimeError(f'''License Manager Segment contains invalid Type: {self.type}.''')

    
    def get_properties(self):
        pass
    # WARNING: Decompyle incomplete


