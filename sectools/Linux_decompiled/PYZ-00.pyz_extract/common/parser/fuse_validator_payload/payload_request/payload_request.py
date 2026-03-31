
from typing import List, Optional, Type, Union
from common.data.base_parser import BaseParserGenerator, DumpDict
from common.data.data import properties_repr
from common.parser.fuse_validator_payload.defines import OFF_TARGET_FEATURE_ID
from common.parser.fuse_validator_payload.fuse_list.fuse_list import FuseList
from common.parser.fuse_validator_payload.payload_request.payload_request_header import FuseValidatorPayloadRequestHeader
from common.parser.fuse_validator_payload.payload_response.payload_response_header import FuseValidatorPayloadResponseHeader
from common.parser.sec_dat.fuse_entry import FuseEntry, FuseEntryV3

class FuseValidatorPayloadRequest(BaseParserGenerator):
    HEADER_CLASS: Union[(Type[FuseValidatorPayloadRequestHeader], Type[FuseValidatorPayloadResponseHeader])] = FuseValidatorPayloadRequestHeader
    
    def __init__(self = None, data = None, **kwargs):
        self.header = None
        self.fuse_list = None
    # WARNING: Decompyle incomplete

    
    def create_default(self = None, feature_id = None, fuses = None, **_):
        self.header = self.HEADER_CLASS()
        self.header.feature_id = feature_id
        self.fuse_list = FuseList(fuses, **('fuses',))
        self.header.total_packet_size = self.get_size()
        if isinstance(self.header, FuseValidatorPayloadRequestHeader):
            self.header.response_payload_size = self.fuse_list.get_size()
            return None

    
    def unpack(self = None, data = None):
        self.header = self.HEADER_CLASS(data)
        self.fuse_list = FuseList(memoryview(data[self.header.get_size():]))

    
    def pack(self = None):
        data = bytearray()
        if self.header:
            data += self.header.pack()
        if self.fuse_list:
            data += self.fuse_list.pack()
        return memoryview(data)

    
    def get_size(self = None):
        size = 0
        if self.header:
            size += self.header.get_size()
        if self.fuse_list:
            size += self.fuse_list.get_size()
        return size

    
    def __repr__(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def is_type(cls = None, data = None):
        if cls.HEADER_CLASS.is_type(memoryview(data)):
            pass
        return FuseList.is_type(memoryview(data[cls.HEADER_CLASS.get_size():]))

    is_type = None(is_type)
    
    def get_dump_files(self = None, directory = None):
        pass
    # WARNING: Decompyle incomplete

    __classcell__ = None

