
from typing import Optional, Union
from common.data.base_parser import BaseParser, DumpDict, DumpInterface
from common.parser.elf_preamble.defines import PADDING_SIZE
from common.parser.elf_preamble.preamble_header_start import PreambleHeaderStart

class PreambleHeader(DumpInterface, BaseParser):
    
    def __init__(self = None, data = None):
        self.preamble_header_start = None
        self.preamble_header_padding = b''
        super().__init__(data)

    
    def unpack(self = None, data = None):
        self.preamble_header_start = PreambleHeaderStart(data)
        offset = PreambleHeaderStart.get_size()
        self.preamble_header_padding = data[offset:offset + PADDING_SIZE]

    
    def pack(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_size(self):
        size = 0
        if self.preamble_header_start:
            size += self.preamble_header_start.get_size()
        if self.preamble_header_padding:
            size += len(self.preamble_header_padding)
        return size

    
    def is_type(cls = None, data = None):
        return PreambleHeaderStart.is_type(data)

    is_type = None(is_type)
    
    def get_dump_files(self = None, directory = None):
        return {
            f'''{directory}/preamble_header''': self.pack() }

    
    def get_properties(self):
        return [
            self.preamble_header_start.get_properties()[0] + (f'''{len(self.preamble_header_padding)} (bytes)''',)]

    
    def __repr__(self):
        return ''

    __classcell__ = None

