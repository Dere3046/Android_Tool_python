
from common.parser.elf_with_hash_segment.v6.hash_table_segment_header import HashTableSegmentHeaderV6
from common.parser.elf_with_hash_segment.v6.metadata.defines import METADATA_MAJOR_VERSION_0, METADATA_MAJOR_VERSION_1, METADATA_MINOR_VERSION_0
from common.parser.elf_with_hash_segment.v6.metadata.v0_0.metadata_0_0 import MetadataV00
from common.parser.elf_with_hash_segment.v6.metadata.v1_0.metadata_1_0 import MetadataV10
from common.parser.mbn.mbn_header import MBNHeader, MBNMetadata

class MBNMetadataV00(MetadataV00, MBNMetadata):
    pass


class MBNMetadataV10(MetadataV10, MBNMetadata):
    pass


class MBNHeaderV6(HashTableSegmentHeaderV6, MBNHeader):
    METADATA_SIZE_TO_CLASS = {
        MBNMetadataV00.get_size(): MBNMetadataV00 }
    METADATA_CLASSES = {
        (METADATA_MAJOR_VERSION_1, METADATA_MINOR_VERSION_0): MBNMetadataV10,
        (METADATA_MAJOR_VERSION_0, METADATA_MINOR_VERSION_0): MBNMetadataV00 }

