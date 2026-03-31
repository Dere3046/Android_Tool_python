
from common.data.binary_struct import StructBase
from common.data.defines import PAD_BYTE_0

class MetadataCommon(StructBase):
    minor_version: int = 'Hash Table Segment Metadata'
    
    def get_fields(cls):
        return [
            'major_version',
            'minor_version']

    get_fields = classmethod(get_fields)
    
    def get_format(cls):
        return '<II'

    get_format = classmethod(get_format)
    
    def all_padding(self):
        return self.pack() == PAD_BYTE_0 * self.get_size()

    
    def is_all_padding(self):
        data = self.data[:self.get_size()] if self.data else self.pack()
        return data == PAD_BYTE_0 * len(data)


