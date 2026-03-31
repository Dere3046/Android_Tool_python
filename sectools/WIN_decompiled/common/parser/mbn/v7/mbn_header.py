
from common.parser.elf_with_hash_segment.v7.hash_table_segment_header import HashTableSegmentHeaderV7
from common.parser.elf_with_hash_segment.v7.metadata.common.v0_0.common_metadata_0_0 import CommonMetadataV00
from common.parser.elf_with_hash_segment.v7.metadata.common.v0_1.common_metadata_0_1 import CommonMetadataV01
from common.parser.elf_with_hash_segment.v7.metadata.defines import COMMON_METADATA_MAJOR_VERSION_0, COMMON_METADATA_MINOR_VERSION_0, COMMON_METADATA_MINOR_VERSION_1, METADATA_MAJOR_VERSION_2, METADATA_MAJOR_VERSION_3, METADATA_MINOR_VERSION_0, METADATA_MINOR_VERSION_1
from common.parser.elf_with_hash_segment.v7.metadata.v2_0.metadata_2_0 import MetadataV20
from common.parser.elf_with_hash_segment.v7.metadata.v3_0.metadata_3_0 import MetadataV30
from common.parser.elf_with_hash_segment.v7.metadata.v3_1.metadata_3_1 import MetadataV31
from common.parser.mbn.mbn_header import MBNCommonMetadata, MBNHeader, MBNMetadata

class MBNCommonMetadataV00(CommonMetadataV00, MBNCommonMetadata):
    pass


class MBNCommonMetadataV01(CommonMetadataV01, MBNCommonMetadata):
    pass


class MBNMetadataV20(MetadataV20, MBNMetadata):
    pass


class MBNMetadataV30(MetadataV30, MBNMetadata):
    pass


class MBNMetadataV31(MetadataV31, MBNMetadata):
    pass


class MBNHeaderV7(HashTableSegmentHeaderV7, MBNHeader):
    METADATA_SIZE_TO_CLASS = {
        MBNMetadataV20.get_size(): MBNMetadataV20 }
    METADATA_CLASSES = {
        (METADATA_MAJOR_VERSION_3, METADATA_MINOR_VERSION_1): MBNMetadataV31,
        (METADATA_MAJOR_VERSION_3, METADATA_MINOR_VERSION_0): MBNMetadataV30,
        (METADATA_MAJOR_VERSION_2, METADATA_MINOR_VERSION_0): MBNMetadataV20 }
    COMMON_METADATA_CLASSES = {
        (COMMON_METADATA_MAJOR_VERSION_0, COMMON_METADATA_MINOR_VERSION_1): MBNCommonMetadataV01,
        (COMMON_METADATA_MAJOR_VERSION_0, COMMON_METADATA_MINOR_VERSION_0): MBNCommonMetadataV00 }

