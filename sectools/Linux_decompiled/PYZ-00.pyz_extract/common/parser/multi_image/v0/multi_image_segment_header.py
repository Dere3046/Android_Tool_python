
from common.data.binary_struct import StructBase
from common.parser.multi_image.defines import MULTI_IMAGE, MULTI_IMAGE_HASH_ALGO_DESCRIPTION, MULTI_IMAGE_HASH_ALGO_SHA384, MULTI_IMAGE_MAG
from common.parser.multi_image.v0.defines import NUM_RESERVED

class MultiImageSegmentHeaderV0(StructBase):
    hash_algorithm: int = 'MultiImageSegmentHeaderV0'
    
    def get_fields(cls):
        fields = [
            'magic',
            'version']
        for i in range(NUM_RESERVED):
            fields.append('reserved_' + str(i))
        fields += [
            'num_entries',
            'hash_algorithm']
        return fields

    get_fields = classmethod(get_fields)
    
    def get_field_defaults(cls):
        fields = {
            'magic': MULTI_IMAGE_MAG,
            'version': 0 }
        for i in range(NUM_RESERVED):
            fields['reserved_' + str(i)] = 0
        fields.update({
            'num_entries': 0,
            'hash_algorithm': MULTI_IMAGE_HASH_ALGO_SHA384 })
        return fields

    get_field_defaults = classmethod(get_field_defaults)
    
    def get_format(cls):
        return f'''<4sI{'Q' * NUM_RESERVED}II'''

    get_format = classmethod(get_format)
    
    def validate_critical_fields(self):
        ''' The data is not of a Multi-Image Segment if it does not contain the magic '''
        if self.magic != MULTI_IMAGE_MAG:
            raise RuntimeError(f'''{MULTI_IMAGE} Segment Header contains invalid Magic: {self.magic}.''')
        if None.version != 0:
            raise RuntimeError(f'''{MULTI_IMAGE} Segment Header contains invalid version: {self.version}.''')

    
    def validate(self):
        self.validate_critical_fields()
        if self.hash_algorithm not in MULTI_IMAGE_HASH_ALGO_DESCRIPTION:
            raise RuntimeError(f'''{MULTI_IMAGE} Segment Header specifies invalid Hash Algorithm: {self.hash_algorithm}.''')

    
    def get_properties(self):
        pass
    # WARNING: Decompyle incomplete


