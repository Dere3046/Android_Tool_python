
from cmd_line_interface.sectools.secure_image.defines import DISABLE, ENABLE
from common.parser.elf_with_hash_segment.v6.metadata.v0_0.metadata_0_0 import MetadataV00
from common.parser.elf_with_hash_segment.v7.metadata.defines import DEBUG_DESCRIPTION_3_1, DEBUG_DISABLE, DEBUG_ENABLE, DEBUG_NOP, METADATA_MINOR_VERSION_1
from common.parser.elf_with_hash_segment.v7.metadata.v3_0.metadata_3_0 import MetadataV30

class MetadataV31(MetadataV30):
    MINOR_VERSION: int = METADATA_MINOR_VERSION_1
    DEBUG_FLAG: str = MetadataV00.DEBUG_FLAG
    DEBUG_DESCRIPTION_DICT: dict[(int, str)] = DEBUG_DESCRIPTION_3_1
    FLAGS: list[tuple[(int, str, str)]] = list(MetadataV30.FLAGS)
    FLAGS[9] = (786432, DEBUG_FLAG, MetadataV30.DEBUG_FLAG_DESCRIPTION)
    tuple[(int, str, str)]
    
    def set_jtag_debug(self = None, jtag_debug = None):
        if jtag_debug == DISABLE:
            self.debug = DEBUG_DISABLE
            return None
        if None == ENABLE:
            self.debug = DEBUG_ENABLE
            return None
        self.debug = None


