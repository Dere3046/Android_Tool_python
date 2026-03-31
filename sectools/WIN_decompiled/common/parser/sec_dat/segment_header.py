
from common.data.binary_struct import StructBase
from common.parser.sec_dat.defines import SEGMENT_TYPE_DESCRIPTION

class SegmentHeader(StructBase):
    attribute: int = 'SegmentHeader'
    
    def get_fields(cls):
        return [
            'segment_offset',
            'segment_type',
            'attribute']

    get_fields = classmethod(get_fields)
    
    def get_format(cls):
        return '<IHH'

    get_format = classmethod(get_format)
    
    def validate(self):
        if self.segment_type not in SEGMENT_TYPE_DESCRIPTION:
            raise RuntimeError(f'''Sec Dat Segment Header contains invalid Segment type: {self.segment_type}.''')

    
    def get_properties(self):
        return [
            (self.segment_offset, SEGMENT_TYPE_DESCRIPTION.get(self.segment_type, self.segment_type))]


