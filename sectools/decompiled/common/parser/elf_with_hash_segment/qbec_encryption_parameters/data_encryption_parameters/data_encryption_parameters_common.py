
from abc import ABC
from typing import Any, Type
from common.data.base_parser import BaseParser, DumpDict
from common.parser.elf.bit32.program_header import ProgramHeader32
from common.parser.elf.bit64.program_header import ProgramHeader64
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.data_encryption_parameters.defines import DataEncryptionParametersHeader

class DataEncryptionParametersCommon(ABC, BaseParser):
    HEADER_CLASS: Type[DataEncryptionParametersHeader] | None = None
    
    def __init__(self = None, data = None, **_):
        self.header = None
        super().__init__(data, **('data',))

    
    def unpack(self = None, data = None):
        data = memoryview(data)
    # WARNING: Decompyle incomplete

    
    def pack(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def is_type(cls = None, data = None):
        pass
    # WARNING: Decompyle incomplete

    is_type = None(is_type)
    
    def validate(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def validate_before_operation(self = None, **_):
        pass
    # WARNING: Decompyle incomplete

    
    def get_size(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_dump_files(self = None, directory = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_encryption_spec_size(cls = None, _ = None):
        pass
    # WARNING: Decompyle incomplete

    get_encryption_spec_size = None(get_encryption_spec_size)
    __classcell__ = None

