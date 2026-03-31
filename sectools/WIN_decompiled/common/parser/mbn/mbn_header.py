
from typing import Any
from common.data.defines import HASH_TABLE_ALGO_NA_DESCRIPTION

class MBNHeader:
    FIELD_6 = 'code_size'
    FIELD_6_STR = 'Code Size:'
    IMAGE_SIZE_STR = ' (Size of data following MBN Header)'
    code_size: int = 'MBN Header'
    
    def update_defaults(self = None, **_):
        pass

    
    def get_segment_hash_algorithm(self = None, _ = None):
        return [
            HASH_TABLE_ALGO_NA_DESCRIPTION]



class MBNMetadata:
    METADATA_STR = 'MBN Metadata'


class MBNCommonMetadata:
    METADATA_STR = 'MBN Common Metadata'

