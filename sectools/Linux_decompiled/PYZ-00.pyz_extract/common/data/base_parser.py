
from abc import ABC, abstractmethod
from pathlib import Path
from re import sub
from typing import Any, Type
from cmd_line_interface.sectools.cmd_line_common.defines import DUMP
from common.logging.logger import log_info
from common.utils import write_cmdline_file
DumpDict = dict[(str, bytes | bytearray | memoryview)]

class DumpInterface(ABC):
    
    def get_dump_files(self = None, directory = None):
        pass

    get_dump_files = None(get_dump_files)
    
    def write_dump_files(self = None, directory = None):
        for file, data in self.get_dump_files().items():
            file_path = (directory / file).resolve()
            if data:
                log_info(f'''Writing parser data to {file_path}.''')
                write_cmdline_file(file_path, data, DUMP)
                continue
            log_info(f'''Skipped writing parser data to {file_path} because data is empty.''')



class BaseParser(ABC):
    
    def __init__(self = None, data = None):
        self.compression_format = None
    # WARNING: Decompyle incomplete

    
    def unpack(self = None, data = None):
        pass

    unpack = None(unpack)
    
    def pack(self = None):
        pass

    pack = None(pack)
    
    def validate(self = None):
        """
        Automatically called after data is parsed. Used to determine whether the data violates any of the parser's
        assumptions.
        """
        pass

    
    def validate_before_operation(self = None, **kwargs):
        """
        Must be manually called. Used to determine whether the data violates any of the parser's assumptions which are
        not fatal but must be enforced before the parser is further manipulated, such as when signing an image.
        """
        pass

    
    def is_type(cls = None, data = classmethod):
        pass

    is_type = None(None(is_type))
    
    def __repr__(self = None):
        pass

    __repr__ = None(__repr__)
    
    def _repr_compression_format(self = None):
        if self.compression_format:
            return f'''Image compressed via {self.compression_format}\n\n'''

    
    def class_type_string(cls = None):
        '''Used to display the user-facing name of the parser class.'''
        return sub('((?<=[a-z])[A-Z]|(?<!\\A)[A-Z](?=[a-z]))', ' \\1', cls.__name__).replace('With', 'with a')

    class_type_string = None(class_type_string)
    
    def image_type_string(self = None):
        ''' Used to display the more specific user-facing name of a parser instance, where applicable.'''
        return self.class_type_string()



class BaseParserGenerator(DumpInterface, BaseParser):
    
    def __init__(self = None, data = None, **kwargs):
        self.data = data
    # WARNING: Decompyle incomplete

    
    def create_default(self = None, **kwargs):
        pass

    create_default = None(create_default)
    __classcell__ = None


class BaseParserTransformer(BaseParserGenerator):
    
    class ExceptionNeedsTransform(RuntimeError):
        __qualname__ = 'BaseParserTransformer.ExceptionNeedsTransform'

    
    def __init__(self = None, data = None, transform = None, **kwargs):
        pass
    # WARNING: Decompyle incomplete

    
    def transformable_parsers(cls = None):
        return []

    transformable_parsers = None(transformable_parsers)
    
    def transform(self = None, **kwargs):
        pass

    transform = None(transform)
    __classcell__ = None

