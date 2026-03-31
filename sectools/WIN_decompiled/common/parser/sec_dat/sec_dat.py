
import hashlib
from operator import methodcaller
from typing import Any, Type
import profile
from cmd_line_interface.sectools.cmd_line_common.base_defines import SECURITY_PROFILE
from cmd_line_interface.sectools.cmd_line_common.defines import INSPECT
from cmd_line_interface.sectools.fuseblower.defines import FUSE_BLOWER_NAME
from common.data.base_parser import BaseParserGenerator, DumpDict
from common.data.data import properties_repr
from common.data.defines import PAD_BYTE_0
from common.logging.logger import log_warning
from common.parser.hash_segment.defines import AUTHORITY_OEM
from common.parser.parser_image_info_interface import ImageFormatType, ImageInfoInterface, ImageProperties, SEC_DAT_PROPERTIES
from common.parser.sec_dat.defines import OPERATION_DESCRIPTION_TO_INT_V1, OPERATION_DESCRIPTION_TO_INT_V3, REGION_TYPE_DESCRIPTION_TO_INT_V1, REGION_TYPE_DESCRIPTION_TO_INT_V3, REGION_TYPE_QFPROM_SPREADSHEET_V1, REGION_TYPE_QFPROM_SPREADSHEET_V3, SEC_DAT_VERSION_1, SEC_DAT_VERSION_2, SEC_DAT_VERSION_3, SEGMENT_EFUSE, SEGMENT_TYPE_DESCRIPTION
from common.parser.sec_dat.fuse_entry import FuseEntry, FuseEntryV3
from common.parser.sec_dat.sec_dat_footer import SecDatFooter
from common.parser.sec_dat.sec_dat_header import SecDatHeaderCommon
from common.parser.sec_dat.sec_dat_segment import SecDatSegment
from common.parser.sec_dat.segment_header import SegmentHeader
from common.parser.sec_dat.v1.sec_dat_header import SecDatSegmentHeaderV1
from common.parser.sec_dat.v2.sec_dat_header import SecDatSegmentHeaderV2
from common.parser.sec_dat.v3.sec_dat_header import SecDatSegmentHeaderV3
from core.fuse_blower.augmented_inspect import get_augmented_fuse_entries_table
from profile.schema import FuseBlowing, SecDatProperties
SEC_DAT_HEADER_CLASSES: dict[(int, Type[SecDatSegmentHeaderV1 | SecDatSegmentHeaderV2 | SecDatSegmentHeaderV3])] = {
    SEC_DAT_VERSION_3: SecDatSegmentHeaderV3,
    SEC_DAT_VERSION_2: SecDatSegmentHeaderV2,
    SEC_DAT_VERSION_1: SecDatSegmentHeaderV1 }

class SecDat(ImageInfoInterface, BaseParserGenerator):
    
    def __init__(self = None, data = None, **kwargs):
        ''' Parse the data of a Sec Dat image. '''
        self.header = None
        self.segment_headers = []
        self.segments = []
        self.segments_dict = { }
        self.fuse_entries = []
        self.footer = None
    # WARNING: Decompyle incomplete

    
    def image_type_string(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def create_default(self = None, *, sec_dat_version, **_):
        if not self.header:
            if sec_dat_version in SEC_DAT_HEADER_CLASSES:
                self.header = SEC_DAT_HEADER_CLASSES[sec_dat_version]()
                if sec_dat_version != SEC_DAT_VERSION_3:
                    self.footer = SecDatFooter(hashlib.sha256(self.header.pack()).digest())
                    return None
                return None
            raise None(f'''Creation of v{sec_dat_version} {self.class_type_string()} is not supported.''')

    
    def unpack(self = None, data = None):
        self.header = SEC_DAT_HEADER_CLASSES[SecDatHeaderCommon(data).version](data)
        offset = self.header.get_size()
        if isinstance(self.header, SecDatSegmentHeaderV3):
            for _ in range(self.header.fuse_count):
                self.fuse_entries.append(FuseEntryV3(data[offset:]))
                offset += FuseEntryV3.get_size()
            return None
        if None(self.header, SecDatSegmentHeaderV2):
            for _ in range(self.header.num_segments):
                self.segment_headers.append(SegmentHeader(data[offset:]))
                offset += SegmentHeader.get_size()
            for seg_idx in range(self.header.num_segments):
                segment = SecDatSegment(memoryview(data[self.segment_headers[seg_idx].segment_offset:]))
                self.segments.append(segment)
                self.segments_dict[self.segment_headers[seg_idx]] = segment
                offset = self.segment_headers[seg_idx].segment_offset + segment.get_size()
            self.footer = SecDatFooter(data[offset:])
            return None
        if None.header.sec_dat_data_size != SecDatFooter.get_size():
            segment = SecDatSegment(memoryview(data[offset:]))
            self.segments.append(segment)
            offset += segment.get_size()
        self.footer = SecDatFooter(data[offset:])

    
    def validate_before_operation(self = None, **kwargs):
        pass
    # WARNING: Decompyle incomplete

    
    def add_fuse_entry(self, region_type, address = None, lsb = None, msb = None, operation = (SEGMENT_EFUSE,), segment_type = ('region_type', str, 'address', int, 'lsb', int, 'msb', int, 'operation', str, 'segment_type', int, 'return', None)):
        pass
    # WARNING: Decompyle incomplete

    
    def add_fuse_entries(self = None, fuse_entries = None):
        for segment_type, address in fuse_entries.items():
            fuse_entry = None
            self.add_fuse_entry(fuse_entry.region_type, int(address, 0), fuse_entry.lsb, fuse_entry.msb, fuse_entry.operation, segment_type)

    
    def add_segment_header(self = None, segment_type = None):
        pass
    # WARNING: Decompyle incomplete

    
    def pack(self = None):
        data = bytearray()
        if self.header:
            data += self.header.pack()
        if self.segment_headers:
            for segment_header in self.segment_headers:
                data += segment_header.pack()
        if self.segments:
            for idx, segment in enumerate(self.segments):
                if self.segment_headers:
                    data = data.ljust(self.segment_headers[idx].segment_offset, PAD_BYTE_0)
                data += segment.pack()
        if self.fuse_entries:
            for fuse_entry in self.fuse_entries:
                data += fuse_entry.pack()
        if self.footer:
            data += self.footer.pack()
        return memoryview(data)

    
    def get_size(self = None):
        size = 0
        if self.header:
            size += self.header.get_size()
        if self.segments_dict:
            size = sorted((lambda .0: [ segment_header.segment_offset + segment.get_size() for segment_header, segment in .0 ])(self.segments_dict.items()), True, **('reverse',))[0]
        elif self.segment_headers:
            for segment_header in self.segment_headers:
                size += segment_header.get_size()
        if self.segments:
            for segment in self.segments:
                size += segment.get_size()
        if self.fuse_entries:
            for fuse_entry in self.fuse_entries:
                size += fuse_entry.get_size()
        if self.footer:
            size += self.footer.get_size()
        return size

    
    def get_fuse_entries(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def is_type(cls = None, data = None):
        ''' Detect whether the data is of a sec.dat image. '''
        return SecDatHeaderCommon.is_type(data)

    is_type = None(is_type)
    
    def get_dump_files(self = None, directory = None):
        pass
    # WARNING: Decompyle incomplete

    
    def __repr__(self):
        string = self._repr_compression_format() + f'''{SecDat.class_type_string()} Header:\n''' + properties_repr(self.header.get_properties())
        if self.segment_headers:
            string += '\n\nSegment Headers:\n'
            properties = [
                ('Index', 'Offset', 'Type')]
            for idx, segment_header in enumerate(self.segment_headers):
                properties.append((idx,) + segment_header.get_properties()[0])
            string += properties_repr(properties, [
                0], **('sep_rows',))
        if self.segments:
            for idx, segment in enumerate(self.segments):
                segment_type = SEGMENT_TYPE_DESCRIPTION[self.segment_headers[idx].segment_type if self.segment_headers else SEGMENT_EFUSE]
                string += segment.__repr__().format(segment_type)
        if self.fuse_entries:
            string += '\n\nFuse Entries:\n'
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
            elif not profile.SECURITY_PROFILE:
                log_warning(f'''The image you are inspecting contains fuse information. In order to see more information about the fuses in this image, provide {SECURITY_PROFILE} along with {INSPECT} to the {FUSE_BLOWER_NAME} feature.''')
        if self.footer:
            string += f'''\n\n{SecDat.class_type_string()} Footer:\n''' + properties_repr(self.footer.get_properties())
        return string

    
    def get_image_properties(self = None, _ = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_image_format(self = None, _ = None):
        pass
    # WARNING: Decompyle incomplete

    __classcell__ = None

