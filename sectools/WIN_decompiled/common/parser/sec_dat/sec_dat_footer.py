
from binascii import hexlify
from common.data.binary_struct import StructBase

class SecDatFooter(StructBase):
    footer: bytes = 'SecDatFooter'
    
    def get_fields(cls):
        return [
            'footer']

    get_fields = classmethod(get_fields)
    
    def get_format(cls):
        return '<32s'

    get_format = classmethod(get_format)
    
    def get_properties(self):
        return [
            ('Footer:', hexlify(self.footer).decode())]


