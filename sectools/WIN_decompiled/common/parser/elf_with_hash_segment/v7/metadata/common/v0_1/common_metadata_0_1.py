
from typing import Type, TypeVar
from common.parser.elf_with_hash_segment.v7.defines import HASH_TABLE_ALGO_SHA256_ZI, HASH_TABLE_ALGO_SHA384_ZI, HASH_TABLE_ALGO_SHA512_ZI
from common.parser.elf_with_hash_segment.v7.metadata.common.v0_0.common_metadata_0_0 import CommonMetadataV00
from common.parser.elf_with_hash_segment.v7.metadata.defines import COMMON_METADATA_MINOR_VERSION_1
T = TypeVar('T', 'CommonMetadataV01', **('bound',))

class CommonMetadataV01(CommonMetadataV00):
    MINOR_VERSION = COMMON_METADATA_MINOR_VERSION_1
    RECOGNIZED_HASH_TABLE_ALGOS = CommonMetadataV00.RECOGNIZED_HASH_TABLE_ALGOS + [
        HASH_TABLE_ALGO_SHA256_ZI,
        HASH_TABLE_ALGO_SHA384_ZI,
        HASH_TABLE_ALGO_SHA512_ZI]
    
    def from_common_metadata00(cls = None, metadata00 = None):
        return cls.from_fields(metadata00.software_id, metadata00.secondary_software_id, metadata00.hash_table_algorithm, metadata00.measurement_register_target, **('software_id', 'secondary_software_id', 'hash_table_algorithm', 'measurement_register_target'))

    from_common_metadata00 = None(from_common_metadata00)

