
from common.data.defines import SHA256_DESCRIPTION, SHA_DESCRIPTION_TO_FUNCTION
from common.parser.multi_image.image_entry.image_entry_base import MultiImageSegmentEntryBase

class MultiImageSegmentEntrySHA256(MultiImageSegmentEntryBase):
    IMAGE_HASH_FUNCTION = SHA_DESCRIPTION_TO_FUNCTION[SHA256_DESCRIPTION]
    
    def get_format(cls):
        return '<II32s'

    get_format = classmethod(get_format)

