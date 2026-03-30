
from typing import List, Union

class ProtocolError(RuntimeError):
    '''The custom exception for protocol validation errors.'''
    pass


class ProtocolParsingError(ProtocolError):
    '''Parsing error with key stack.'''
    
    def __init__(self = None, tag_id_stack = None, *args):
        self.tag_id_stack = tag_id_stack
        self.version_info = None
    # WARNING: Decompyle incomplete

    
    def add_version_info(self = None, version_info = None):
        if self.version_info is None:
            self.version_info = version_info
            return None

    
    def stack_str(self = None):
        return '->'.join(list(reversed(self.tag_id_stack)))

    
    def __str__(self = None):
        version_info = f'''[TME v{self.version_info}]''' if self.version_info is not None else ''
        tag_id_stack_info = f''' ({self.stack_str()}) ''' if self.stack_str() else ''
        return super().__str__() + tag_id_stack_info + version_info

    __classcell__ = None


class ProtocolErrorTagUnknown(ProtocolParsingError):
    '''Parsing error with key stack.'''
    
    def __init__(self = None, tag = None, tag_id_stack = None, *args):
        self.tag = tag
    # WARNING: Decompyle incomplete

    __classcell__ = None


class ProtocolVersionError(ProtocolParsingError):
    '''Version mismatch error.'''
    
    def __init__(self = None, actual_version = None, *args):
        pass
    # WARNING: Decompyle incomplete

    __classcell__ = None


class NormalizationNotImplemented(ProtocolParsingError):
    '''Normalization not implemented for tag parser.'''
    
    def __init__(self = None, *args):
        pass
    # WARNING: Decompyle incomplete

    __classcell__ = None

