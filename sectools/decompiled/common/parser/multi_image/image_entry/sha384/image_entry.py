
from common.data.defines import SHA384_DESCRIPTION, SHA_DESCRIPTION_TO_FUNCTION
from common.parser.multi_image.image_entry.image_entry_base import MultiImageSegmentEntryBase

class MultiImageSegmentEntrySHA384(MultiImageSegmentEntryBase):
    IMAGE_HASH_FUNCTION = SHA_DESCRIPTION_TO_FUNCTION[SHA384_DESCRIPTION]
    
    def get_format(cls):
        return '<II48s'

    get_format = classmethod(get_format)

