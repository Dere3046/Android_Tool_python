
from typing import Any, List, Optional, Union
import profile
from cmd_line_interface.sectools.cmd_line_common.base_defines import SECURITY_PROFILE
from cmd_line_interface.sectools.cmd_line_common.defines import INSPECT
from cmd_line_interface.sectools.fuseblower.defines import FUSE_BLOWER_NAME
from common.data.base_parser import BaseParserGenerator, DumpDict
from common.data.data import properties_repr
from common.logging.logger import log_warning
from common.parser.sec_dat.defines import SEC_DAT_FUSE_VERSION_1, SEC_DAT_FUSE_VERSION_2
from common.parser.sec_dat.fuse_entry import FuseEntry
from common.parser.sec_dat.fuse_header import FuseHeaderCommon
from common.parser.sec_dat.v1.segment.v1.fuse_header import FuseHeaderV1
from common.parser.sec_dat.v2.segment.v2.fuse_header import FuseHeaderV2
from core.fuse_blower.augmented_inspect import get_augmented_fuse_entries_table
FUSE_HEADER_CLASSES = {
    SEC_DAT_FUSE_VERSION_2: FuseHeaderV2,
    SEC_DAT_FUSE_VERSION_1: FuseHeaderV1 }

class SecDatSegment(BaseParserGenerator):
    
    def __init__(self = None, data = None, **kwargs):
        ''' Parse the segment data of a Sec Dat image. '''
        self.fuse_header = None
        self.fuse_entries = []
    # WARNING: Decompyle incomplete

    
    def create_default(self = None, *, fuse_version, **_):
        if profile.SECURITY_PROFILE:
            if not getattr(profile.SECURITY_PROFILE.sec_elf_properties, 'fuse_version', None):
                pass
            profile_fuse_version = getattr(profile.SECURITY_PROFILE.sec_dat_properties, 'fuse_version', None)
            if not profile_fuse_version:
                pass
            fuse_version = fuse_version
        if not self.fuse_header:
            self.fuse_header = FUSE_HEADER_CLASSES[fuse_version]()
            return None

    
    def unpack(self = None, data = None):
        self.fuse_header = FUSE_HEADER_CLASSES[FuseHeaderCommon(data).version](data)
        offset = self.fuse_header.get_size()
        for _ in range(self.fuse_header.fuse_count):
            fuse_entry = FuseEntry(data[offset:])
            self.fuse_entries.append(fuse_entry)
            offset += fuse_entry.get_size()

    
    def add_fuse(self, region_type, address = None, lsb = None, msb = None, operation = ('region_type', int, 'address', int, 'lsb', int, 'msb', int, 'operation', int, 'return', None)):
        pass
    # WARNING: Decompyle incomplete

    
    def validate_before_operation(self = None, **kwargs):
        pass
    # WARNING: Decompyle incomplete

    
    def pack(self = None):
        data = bytearray()
        if self.fuse_header:
            data += self.fuse_header.pack()
        for fuse_entry in self.fuse_entries:
            data += fuse_entry.pack()
        return memoryview(data)

    
    def get_size(self = None):
        size = 0
        if self.fuse_header:
            size += self.fuse_header.get_size()
        for fuse_entry in self.fuse_entries:
            size += fuse_entry.get_size()
        return size

    
    def is_type(cls = None, data = None):
        return FuseHeaderCommon.is_type(data)

    is_type = None(is_type)
    
    def get_dump_files(self = None, directory = None):
        pass
    # WARNING: Decompyle incomplete

    
    def __repr__(self):
        string = '\n\n{0} Header:\n' + properties_repr(self.fuse_header.get_properties())
        if self.fuse_entries:
            string += '\n\n{0} Entries:\n'
            properties = [
                ('Index',) + tuple((lambda .0: for desc, _ in .0:
desc)(self.fuse_entries[0].get_properties()))]
            for idx, fuse_entry in enumerate(self.fuse_entries):
                properties.append((idx,) + tuple((lambda .0: for _, prop in .0:
prop)(fuse_entry.get_properties())))
            string += properties_repr(properties, [
                0], **('sep_rows',))
            if profile.SECURITY_PROFILE and profile.SECURITY_PROFILE.fuse_blowing_features:
                string += '\n\n' + get_augmented_fuse_entries_table(self.fuse_entries)
                return string
            if not None.SECURITY_PROFILE:
                log_warning(f'''The image you are inspecting contains fuse information. In order to see more information about the fuses in this image, provide {SECURITY_PROFILE} along with {INSPECT} to the {FUSE_BLOWER_NAME} feature.''')
        return string

    __classcell__ = None

