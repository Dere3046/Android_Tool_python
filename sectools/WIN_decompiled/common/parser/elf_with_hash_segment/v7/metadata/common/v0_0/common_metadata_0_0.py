
from typing import Any
from common.data.binary_struct import StructBase
from common.data.data import hex_val
from common.parser.elf_with_hash_segment.v7.defines import HASH_TABLE_ALGO_DESCRIPTION, HASH_TABLE_ALGO_NA, HASH_TABLE_ALGO_SHA256, HASH_TABLE_ALGO_SHA384, HASH_TABLE_ALGO_SHA512
from common.parser.elf_with_hash_segment.v7.metadata.defines import COMMON_METADATA_MAJOR_VERSION_0, COMMON_METADATA_MINOR_VERSION_0, MEASUREMENT_REGISTER_TARGET_DESCRIPTION

class CommonMetadataV00(StructBase):
    METADATA_STR = 'Hash Table Segment Common Metadata'
    MAJOR_VERSION = COMMON_METADATA_MAJOR_VERSION_0
    MINOR_VERSION = COMMON_METADATA_MINOR_VERSION_0
    measurement_register_target: int = [
        HASH_TABLE_ALGO_NA,
        HASH_TABLE_ALGO_SHA256,
        HASH_TABLE_ALGO_SHA384,
        HASH_TABLE_ALGO_SHA512]
    
    def class_type_string(cls = None):
        return f'''{cls.METADATA_STR} v{cls.MAJOR_VERSION}.{cls.MINOR_VERSION}'''

    class_type_string = None(class_type_string)
    
    def get_fields(cls = None):
        return [
            'major_version',
            'minor_version',
            'software_id',
            'secondary_software_id',
            'hash_table_algorithm',
            'measurement_register_target']

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        return {
            'major_version': cls.MAJOR_VERSION,
            'minor_version': cls.MINOR_VERSION,
            'software_id': 0,
            'secondary_software_id': 0,
            'hash_table_algorithm': cls.RECOGNIZED_HASH_TABLE_ALGOS[0],
            'measurement_register_target': 0 }

    get_field_defaults = None(get_field_defaults)
    
    def get_format(cls = None):
        return '<IIIIII'

    get_format = None(get_format)
    
    def validate_critical_fields(self = None):
        if (self.major_version, self.minor_version) != (self.MAJOR_VERSION, self.MINOR_VERSION):
            raise RuntimeError(f'''{self.class_type_string()} has invalid version: {self.major_version}.{self.minor_version}.''')

    
    def validate(self = None):
        self.validate_critical_fields()
        if self.hash_table_algorithm not in self.RECOGNIZED_HASH_TABLE_ALGOS:
            raise RuntimeError(f'''{self.class_type_string()} has invalid Hash Table Algorithm: {self.hash_table_algorithm}.''')

    
    def validate_before_operation(self = None, **_):
        if self.measurement_register_target not in MEASUREMENT_REGISTER_TARGET_DESCRIPTION:
            raise RuntimeError(f'''{self.class_type_string()} has invalid Measurement Register Target: {self.measurement_register_target}.''')

    
    def get_properties(self = None):
        return [
            ('Major Version:', self.major_version),
            ('Minor Version:', self.minor_version),
            ('Software ID:', hex_val(self.software_id, True, **('strip_leading_zeros',))),
            ('Secondary Software ID:', hex_val(self.secondary_software_id, True, **('strip_leading_zeros',))),
            ('Hash Table Algorithm', HASH_TABLE_ALGO_DESCRIPTION.get(self.hash_table_algorithm, self.hash_table_algorithm)),
            ('Measurement Register Target:', MEASUREMENT_REGISTER_TARGET_DESCRIPTION.get(self.measurement_register_target, hex_val(self.measurement_register_target, True, **('strip_leading_zeros',))))]


