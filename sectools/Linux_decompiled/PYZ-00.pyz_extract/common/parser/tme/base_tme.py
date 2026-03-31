
from pathlib import Path
from typing import Any, Union
from common.data.base_parser import BaseParser
from common.logging.logger import log_debug
from common.parser.tme.tme_parser.tme import TME
from core.tme_secure_debug.augmented_inspect import augmented_inspect, describe

class BaseTME(BaseParser):
    tme: TME = 'Basic TME parser useful for TME image inspection only.'
    
    def __init__(self = None, data = None):
        if isinstance(data, Path):
            data = memoryview(data.read_bytes())
        if isinstance(data, (BaseTME, TME)):
            data = memoryview(data.pack())
        super().__init__(data, **('data',))

    
    def class_type_string(cls = None):
        return 'TME'

    class_type_string = None(class_type_string)
    
    def pack(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def unpack(self = None, data = None):
        self.tme = TME(data)

    
    def validate(self = None):
        super().validate()
    # WARNING: Decompyle incomplete

    
    def is_type(cls = None, data = None):
        pass
    # WARNING: Decompyle incomplete

    is_type = None(is_type)
    
    def describe(self = None):
        '''Returns a string describing the TME object.'''
        return describe(self.tme)

    
    def __repr__(self = None):
        '''The object is printable.'''
        pass
    # WARNING: Decompyle incomplete

    
    def get_item(self = None, json_pointer = None):
        '''
        Convenience function. Returns a TME item from object using JSON pointer string.
        Example: dpr.get_item("SvcDebugPolicy/DebugPolicyData/DebugOptions")
        '''
        return self.tme.get_item(json_pointer)

    
    def set_item(self = None, json_pointer = None, value = None):
        self.tme.set_item(json_pointer, value)

    __classcell__ = None

