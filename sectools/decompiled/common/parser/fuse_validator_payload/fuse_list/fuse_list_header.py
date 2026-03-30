
from typing import Any, Dict, List, Tuple
from common.data.binary_struct import StructBase
from common.parser.fuse_validator_payload.fuse_list.defines import FUSE_LIST_VERSION_1, FUSE_LIST_VERSION_2

class FuseListHeader(StructBase):
    fuse_count: int = 'FuseListHeader'
    
    def get_fields(cls = None):
        return [
            'version',
            'fuse_count']

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        return {
            'version': FUSE_LIST_VERSION_2,
            'fuse_count': 0 }

    get_field_defaults = None(get_field_defaults)
    
    def get_format(cls = None):
        return '<II'

    get_format = None(get_format)
    
    def validate_critical_fields(self = None):
        if self.version not in (FUSE_LIST_VERSION_1, FUSE_LIST_VERSION_2):
            raise RuntimeError(f'''Fuse List Header contains invalid Version: {self.version}.''')

    
    def validate(self = None):
        self.validate_critical_fields()

    
    def get_properties(self = None):
        return [
            ('Version:', self.version),
            ('Number of Fuse Entries:', self.fuse_count)]


