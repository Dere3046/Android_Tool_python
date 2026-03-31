
from common.data.base_parser import BaseParser, DumpDict, DumpInterface
from common.data.data import properties_repr
from common.parser.elf_preamble.defines import PREAMBLE_HEADER_SIZE
from common.parser.elf_preamble.preamble_header import PreambleHeader

class Preamble(DumpInterface, BaseParser):
    
    def __init__(self = None, data = None):
        self.preamble_headers = []
        super().__init__(data)
    # WARNING: Decompyle incomplete

    
    def unpack(self = None, data = None):
        offset = 0
        if PreambleHeader.is_type(data[offset:]):
            preamble_header = PreambleHeader(memoryview(data[offset:]))
            self.preamble_headers.append(preamble_header)
            offset += preamble_header.get_size()
        else:
            end = offset + PREAMBLE_HEADER_SIZE
            if self.preamble_headers and end < len(data):
                self.preamble_headers[-1].preamble_header_padding = memoryview(b''.join([
                    self.preamble_headers[-1].preamble_header_padding,
                    data[offset:end]]))
            return None

    
    def get_size(self):
        size = 0
        for header in self.preamble_headers:
            size += header.preamble_header_start.get_size() + len(header.preamble_header_padding)
        return size

    
    def pack(self = None):
        data = bytearray()
        for preamble_header in self.preamble_headers:
            data += preamble_header.pack()
        return memoryview(data)

    
    def is_type(cls = None, data = None):
        return PreambleHeader.is_type(data)

    is_type = None(is_type)
    
    def get_dump_files(self = None, directory = None):
        return (lambda .0 = None: pass# WARNING: Decompyle incomplete
)(enumerate(self.preamble_headers))

    
    def __repr__(self):
        properties = [
            ('Header Index', 'Flash Code Word', 'Magic', 'Magic Number', 'Padding')]
        for idx, header in enumerate(self.preamble_headers):
            properties.append((idx,) + header.get_properties()[0])
        return properties_repr(properties, [
            0], **('sep_rows',))

    __classcell__ = None

