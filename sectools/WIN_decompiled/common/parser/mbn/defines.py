
from typing import Type
from common.parser.elf_with_hash_segment.v3.hash_table_segment_header import HashTableSegmentHeaderV3
from common.parser.elf_with_hash_segment.v5.hash_table_segment_header import HashTableSegmentHeaderV5
from common.parser.elf_with_hash_segment.v6.hash_table_segment_header import HashTableSegmentHeaderV6
from common.parser.elf_with_hash_segment.v7.hash_table_segment_header import HashTableSegmentHeaderV7
from common.parser.elf_with_hash_segment.v8.hash_table_segment_header import HashTableSegmentHeaderV8
from common.parser.hash_segment.defines import HASH_SEGMENT_V3, HASH_SEGMENT_V5, HASH_SEGMENT_V6, HASH_SEGMENT_V7, HASH_SEGMENT_V8
HASH_TABLE_SEGMENT_HEADER_CLASSES: dict[(int, Type[HashTableSegmentHeaderV3 | HashTableSegmentHeaderV5 | HashTableSegmentHeaderV6 | HashTableSegmentHeaderV7 | HashTableSegmentHeaderV8])] = {
    HASH_SEGMENT_V8: HashTableSegmentHeaderV8,
    HASH_SEGMENT_V7: HashTableSegmentHeaderV7,
    HASH_SEGMENT_V6: HashTableSegmentHeaderV6,
    HASH_SEGMENT_V5: HashTableSegmentHeaderV5,
    HASH_SEGMENT_V3: HashTableSegmentHeaderV3 }
