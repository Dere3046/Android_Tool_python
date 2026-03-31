
from typing import Union
from common.parser.sec_dat.fuse_entry import FuseEntry, FuseEntryV3
FUSE_LIST_VERSION_1 = 1
FUSE_LIST_VERSION_2 = 2
FuseEntryUnion = Union[(FuseEntry, FuseEntryV3)]
