
from common.parser.sec_dat.defines import SEC_DAT_FUSE_VERSION_2
from common.parser.sec_dat.v1.segment.v1.fuse_header import FuseHeaderV1

class FuseHeaderV2(FuseHeaderV1):
    VERSION = SEC_DAT_FUSE_VERSION_2

