
from typing import Any
from common.parser.elf_with_hash_segment.v7.metadata.v3_0.metadata_3_0 import MetadataV30
from common.parser.elf_with_hash_segment.v8.metadata.defines import METADATA_MAJOR_VERSION_4

class MetadataV40(MetadataV30):
    MAJOR_VERSION: int = METADATA_MAJOR_VERSION_4
    
    def get_fields(cls = None):
        fields = super().get_fields()
        fields[fields.index('mrc_index')] = 'reserved'
        return fields

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        pass
    # WARNING: Decompyle incomplete

    get_field_defaults = None(get_field_defaults)
    
    def get_properties(self = None):
        properties = list(filter((lambda prop: prop[0] != 'Root Certificate Index:'), super().get_properties()))
        return properties

    __classcell__ = None

