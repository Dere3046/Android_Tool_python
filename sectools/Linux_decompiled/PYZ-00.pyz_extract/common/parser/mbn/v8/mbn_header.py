
from common.parser.elf_with_hash_segment.v7.metadata.defines import COMMON_METADATA_MAJOR_VERSION_0, COMMON_METADATA_MINOR_VERSION_0, COMMON_METADATA_MINOR_VERSION_1
from common.parser.elf_with_hash_segment.v8.hash_table_segment_header import HashTableSegmentHeaderV8
from common.parser.elf_with_hash_segment.v8.metadata.defines import METADATA_MAJOR_VERSION_4, METADATA_MINOR_VERSION_0
from common.parser.elf_with_hash_segment.v8.metadata.v4_0.metadata_4_0 import MetadataV40
from common.parser.mbn.mbn_header import MBNHeader, MBNMetadata
from common.parser.mbn.v7.mbn_header import MBNCommonMetadataV00, MBNCommonMetadataV01

class MBNMetadataV40(MetadataV40, MBNMetadata):
    pass


class MBNHeaderV8(HashTableSegmentHeaderV8, MBNHeader):
    METADATA_SIZE_TO_CLASS = {
        MBNMetadataV40.get_size(): MBNMetadataV40 }
    METADATA_CLASSES = {
        (METADATA_MAJOR_VERSION_4, METADATA_MINOR_VERSION_0): MBNMetadataV40 }
    COMMON_METADATA_CLASSES = {
        (COMMON_METADATA_MAJOR_VERSION_0, COMMON_METADATA_MINOR_VERSION_1): MBNCommonMetadataV01,
        (COMMON_METADATA_MAJOR_VERSION_0, COMMON_METADATA_MINOR_VERSION_0): MBNCommonMetadataV00 }

