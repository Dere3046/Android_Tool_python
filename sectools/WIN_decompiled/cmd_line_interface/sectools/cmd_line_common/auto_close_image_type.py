
from argparse import ArgumentTypeError
from dataclasses import dataclass
from operator import methodcaller
from textwrap import indent
from typing import Generic, Tuple, Type, TypeVar, Union
from cmd_line_interface.base_defines import AutoCloseFileType, KWARGS_READ_BINARY
from common.data.base_parser import BaseParser
from common.data.data import a_or_an, and_separated
from common.parser.utils import get_parsed_image
GenericBaseParser = TypeVar('GenericBaseParser', BaseParser, **('bound',))

def ImageWithPath():
    '''ImageWithPath'''
    path: str = 'ImageWithPath'
    
    def as_tuple(self = None):
        return (self.image, self.path)


ImageWithPath = dataclass(<NODE:27>(ImageWithPath, 'ImageWithPath', Generic[GenericBaseParser]))

class AutoCloseImageType:
    '''Generic class for image type validation.'''
    
    def __init__(self = None, image_types = None, return_path = None):
        self.image_types = image_types
        self.return_path = return_path

    
    def __call__(self = None, path = None):
        file_info = AutoCloseFileType(KWARGS_READ_BINARY, True, **('mode', 'return_path'))(path)
    # WARNING: Decompyle incomplete


