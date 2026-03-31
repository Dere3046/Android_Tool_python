
from contextlib import suppress
from typing import Any, Type
import profile
from common.data.base_parser import DumpDict
from common.data.data import ceil_to_multiple
from common.parser.debug_policy_elf.debug_policy_segment import DebugPolicySegmentCommon
from common.parser.debug_policy_elf.defines import DEBUG_POLICY_V1, DEBUG_POLICY_V2, DEBUG_POLICY_V3, DEBUG_POLICY_V4, DEBUG_POLICY_V5, DEBUG_POLICY_V6, DEBUG_POLICY_V7, DEBUG_POLICY_V8, DebugOption
from common.parser.debug_policy_elf.v1.debug_policy_segment import DebugPolicySegmentV1
from common.parser.debug_policy_elf.v2.debug_policy_segment import DebugPolicySegmentV2
from common.parser.debug_policy_elf.v3.debug_policy_segment import DebugPolicySegmentV3
from common.parser.debug_policy_elf.v4.debug_policy_segment import DebugPolicySegmentV4
from common.parser.debug_policy_elf.v5.debug_policy_segment import DebugPolicySegmentV5
from common.parser.debug_policy_elf.v6.debug_policy_segment import DebugPolicySegmentV6
from common.parser.debug_policy_elf.v7.debug_policy_segment import DebugPolicySegmentV7
from common.parser.debug_policy_elf.v8.debug_policy_segment import DebugPolicySegmentV8
from common.parser.elf.bit32.program_header import ProgramHeader32
from common.parser.elf.bit64.program_header import ProgramHeader64
from common.parser.elf.defines import ELFCLASS32, PT_LOAD
from common.parser.elf.elf import ELF
from common.parser.elf.program_header import PROGRAM_HEADER_CLASSES
from common.parser.hash_segment.defines import AUTHORITY_OEM
from common.parser.parser_image_info_interface import ImageFormatType
from profile.defines import ANY, END, START
from profile.schema import LegacyDebugging
DebugPolicySegment = DebugPolicySegmentV1 | DebugPolicySegmentV2 | DebugPolicySegmentV3 | DebugPolicySegmentV4 | DebugPolicySegmentV5 | DebugPolicySegmentV6 | DebugPolicySegmentV7 | DebugPolicySegmentV8
DEBUG_POLICY_SEGMENT_CLASSES: dict[(int, Type[DebugPolicySegment])] = {
    DEBUG_POLICY_V8: DebugPolicySegmentV8,
    DEBUG_POLICY_V7: DebugPolicySegmentV7,
    DEBUG_POLICY_V6: DebugPolicySegmentV6,
    DEBUG_POLICY_V5: DebugPolicySegmentV5,
    DEBUG_POLICY_V4: DebugPolicySegmentV4,
    DEBUG_POLICY_V3: DebugPolicySegmentV3,
    DEBUG_POLICY_V2: DebugPolicySegmentV2,
    DEBUG_POLICY_V1: DebugPolicySegmentV1 }

class DebugPolicyELF(ELF):
    
    def __init__(self = None, data = None, **kwargs):
        ''' Parse the data of an image containing a Debug Policy segment. '''
        self.debug_policy_segment_phdr = None
        self.debug_policy_segment_idx = 0
        self.debug_policy_segment = None
    # WARNING: Decompyle incomplete

    
    def image_type_string(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def unpack(self = None, data = None):
        super().unpack(data)
        load_phdr = None
        for phdr in self.phdrs:
            if phdr.p_type == PT_LOAD:
                if not load_phdr:
                    load_phdr = phdr
                    continue
                raise RuntimeError(f'''ELF contains multiple LOAD segments. {DebugPolicyELF.class_type_string()} images must only contain 1 LOAD segment.''')
            if load_phdr:
                self.debug_policy_segment_phdr = load_phdr
                debug_policy_segment_data = self.segments[load_phdr]
            else:
                raise RuntimeError('ELF does not contain a Debug Policy Segment.')
            version = None(debug_policy_segment_data).version
            self.debug_policy_segment = DEBUG_POLICY_SEGMENT_CLASSES[version](debug_policy_segment_data)
            return None

    
    def create_default(self = None, *, elf_class, debug_policy_version, debug_policy_segment_address, **_):
        super().create_default(elf_class, **('elf_class',))
    # WARNING: Decompyle incomplete

    
    def pack_debug_policy_segment(self = None):
        if self.debug_policy_segment:
            return memoryview(self.debug_policy_segment.pack())
        return None(memoryview)

    
    def pack(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_size(self = None):
        size = 0
        if self.debug_policy_segment:
            size += self.debug_policy_segment.get_size()
        return size

    
    def set_serial_numbers(self = None, serial_numbers = None):
        pass
    # WARNING: Decompyle incomplete

    
    def set_oem_root_certificate_hashes(self = None, oem_root_certificate_hashes = None):
        pass
    # WARNING: Decompyle incomplete

    
    def set_qti_root_certificate_hashes(self = None, qti_root_certificate_hashes = None):
        pass
    # WARNING: Decompyle incomplete

    
    def set_flags(self = None, debug_options = None):
        pass
    # WARNING: Decompyle incomplete

    
    def set_all_flags(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def is_type(cls = None, data = None):
        ''' Detect whether the data is of an ELF MBN image containing a Debug Policy segment. '''
        match = False
        if super().is_type(data):
            with suppress(Exception):
                elf = ELF(memoryview(data))
                load_phdr_lst = (lambda .0: [ phdr for phdr in .0 if phdr.p_type == PT_LOAD ])(elf.phdrs)
                if len(load_phdr_lst) == 1:
                    pass
            match = DebugPolicySegmentCommon.is_type(elf.segments[load_phdr_lst[0]])
        None(None, None, None)
        return match
    # WARNING: Decompyle incomplete

    is_type = None(is_type)
    
    def get_dump_files(self = None, directory = None):
        dump_files = super().get_dump_files(directory)
        if self.debug_policy_segment:
            dump_files['debug_policy_segment.bin'] = self.debug_policy_segment.pack()
        return dump_files

    
    def __repr__(self = None):
        string = super().__repr__()
        if self.debug_policy_segment:
            string += '\n\n' + str(self.debug_policy_segment)
        return string

    
    def get_segment_placement(self = None, phdr = None):
        if (self.phdrs[0] == phdr or self.phdrs[0].is_os_segment_phdr()) and self.phdrs[1] == phdr:
            return [
                START]
        return [
            None]

    
    def get_image_format(self = None, _ = None):
        pass
    # WARNING: Decompyle incomplete

    __classcell__ = None

