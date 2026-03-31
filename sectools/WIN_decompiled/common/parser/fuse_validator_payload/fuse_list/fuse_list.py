
from typing import Any, List, Optional, Union
from common.data.base_parser import BaseParserGenerator, DumpDict
from common.data.data import extract_data_or_fail, properties_repr
from common.parser.fuse_validator_payload.fuse_list.defines import FUSE_LIST_VERSION_1, FUSE_LIST_VERSION_2, FuseEntryUnion
from common.parser.fuse_validator_payload.fuse_list.fuse_list_header import FuseListHeader
from common.parser.sec_dat.fuse_entry import FuseEntry, FuseEntryV3
FUSE_ENTRY_CLASSES = {
    FUSE_LIST_VERSION_2: FuseEntryV3,
    FUSE_LIST_VERSION_1: FuseEntry }
FUSE_ENTRY_CLASSES_TO_VERSION = (lambda .0: pass# WARNING: Decompyle incomplete
)(FUSE_ENTRY_CLASSES.items())

class FuseList(BaseParserGenerator):
    
    def __init__(self = None, data = None, **kwargs):
        self.fuse_list_header = None
        self.fuse_entries = []
    # WARNING: Decompyle incomplete

    
    def create_default(self = None, *, fuses, **_):
        self.fuse_list_header = FuseListHeader()
    # WARNING: Decompyle incomplete

    
    def unpack(self = None, data = None):
        self.fuse_list_header = FuseListHeader(data)
        offset = self.fuse_list_header.get_size()
        fuse_entry_class = FUSE_ENTRY_CLASSES[self.fuse_list_header.version]
        size = fuse_entry_class().get_size()
        for _ in range(self.fuse_list_header.fuse_count):
            fuse_entry = fuse_entry_class(extract_data_or_fail(data, size, offset))
            self.fuse_entries.append(fuse_entry)
            offset += size

    
    def validate_before_operation(self = None, **kwargs):
        for fuse_entry in self.fuse_entries:
            fuse_entry.validate()

    
    def pack(self = None):
        data = bytearray()
        if self.fuse_list_header:
            data += self.fuse_list_header.pack()
        for fuse_entry in self.fuse_entries:
            data += fuse_entry.pack()
        return memoryview(data)

    
    def get_size(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def is_type(cls = None, data = None):
        pass
    # WARNING: Decompyle incomplete

    is_type = None(is_type)
    
    def get_dump_files(self = None, directory = None):
        pass
    # WARNING: Decompyle incomplete

    
    def __repr__(self = None):
        pass
    # WARNING: Decompyle incomplete

    __classcell__ = None

