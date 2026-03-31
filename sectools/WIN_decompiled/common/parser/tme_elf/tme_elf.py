
from contextlib import suppress
from functools import partial
from operator import attrgetter, eq, methodcaller
from typing import Any
import profile
from common.data.base_parser import DumpDict
from common.data.data import comma_separated_string, plural_s, properties_repr, tuple_to_version_string, version_string_to_tuple
from common.parser.elf.bit32.program_header import ProgramHeader32
from common.parser.elf.bit64.program_header import ProgramHeader64
from common.parser.elf.defines import ELFCLASS32, ELFCLASS_TO_INT, INT_TO_ELFCLASS, PT_LOAD
from common.parser.elf.elf import ELF
from common.parser.elf.program_header import PROGRAM_HEADER_CLASSES
from common.parser.parser_security_profile_validator_interface import ParserSecurityProfileValidatorInterface
from common.parser.tme.dpr.dpr import DPR
from common.parser.tme.dpr.validations import DPRValidationOptions
from common.parser.tme.tme_parser.tme import TME
from core.tme_secure_debug.augmented_inspect import DESCRIBE_DPR, TME_DEBUG_POLICY_IMAGE, augmented_inspect, describe
from profile.defines import ANY
from profile.profile_core import SecurityProfile

class TMEELF(ParserSecurityProfileValidatorInterface, ELF):
    
    def __init__(self = None, data = None, **kwargs):
        ''' Parse the data of an image containing a TME segment. '''
        self.tme_objects = []
        self.tme_segment_phdr = None
    # WARNING: Decompyle incomplete

    
    def class_type_string(cls = None):
        return f'''TME {ELF.class_type_string()}'''

    class_type_string = None(class_type_string)
    
    def validate_against_security_profile(self = None, security_profile = None, _ = None):
        profile_tme = security_profile.tme_debugging_features
        if not profile_tme:
            return None
        if None.oem_debug_policy_format != 'ELF':
            raise RuntimeError(f'''Security Profile requires {profile_tme.oem_debug_policy_format} format, however {TME_DEBUG_POLICY_IMAGE} provided.''')
        tme_version = None.tme_version
        if not None(None((lambda x = None: x.version == tme_version), self.tme_objects)):
            identified_versions = set(map(attrgetter('version'), self.tme_objects))
            raise RuntimeError(f'''Security Profile requires version {tme_version} for all TME objects, however version{plural_s(identified_versions)} {comma_separated_string(identified_versions, 'and')} identified.''')
        expected_version = None(profile_tme.command_version)
        major_getter = methodcaller('get_item', 'SvcDebugPolicy/CmdMajorVersion')
        minor_getter = methodcaller('get_item', 'SvcDebugPolicy/CmdMinorVersion')
        identified_command_versions = None(None((lambda x = None: (int(major_getter(x), 0), int(minor_getter(x), 0))), filter((lambda x: DESCRIBE_DPR in describe(x)), self.tme_objects)))
        if not None(None((lambda x = None: x == expected_version), identified_command_versions)):
            tmp = comma_separated_string(map(tuple_to_version_string, identified_command_versions), 'and')
            raise RuntimeError(f'''Security Profile requires command version {profile_tme.command_version} for all TME objects, however version{plural_s(identified_command_versions)} {tmp} identified.''')
        phy_addr = None(profile_tme.tme_elf_properties.phy_addr, 0, **('base',))
    # WARNING: Decompyle incomplete

    
    def create_default(self = None, *, elf_class, tme_segment_address, tme_objects, **_):
        '''The TME ELF contains TME DPR segment.'''
        if tme_objects:
            self.tme_objects = tme_objects
        dpr_segment_alignment = 4096
        if profile.SECURITY_PROFILE and hasattr(profile.SECURITY_PROFILE.tme_debugging_features, 'tme_elf_properties'):
            tme_elf_properties = profile.SECURITY_PROFILE.tme_debugging_features.tme_elf_properties
            if tme_elf_properties.dpr_segment_alignment != ANY:
                dpr_segment_alignment = int(tme_elf_properties.dpr_segment_alignment, 16)
            if not tme_segment_address:
                tme_segment_address = int(tme_elf_properties.phy_addr, 16)
            if elf_class is None:
                elf_class = INT_TO_ELFCLASS[tme_elf_properties.elf_classes.default_elf_class]
        if not elf_class:
            pass
        super().create_default(ELFCLASS32, **('elf_class',))
    # WARNING: Decompyle incomplete

    
    def unpack(self = None, data = None):
        super().unpack(data)
        phdrs = list(filter((lambda x: x.p_type == PT_LOAD), self.phdrs))
        if len(phdrs) > 1:
            raise RuntimeError('The ELF contains multiple LOAD segments. TME Debug Policy images must only contain single LOAD segment.')
        if not None:
            raise RuntimeError('The ELF does not contain a TME Debug Policy Segment.')
        self.tme_segment_phdr = None(iter(phdrs))
        tme_data = self.segments[self.tme_segment_phdr]
        if tme_data:
            tme = TME(tme_data)
            if not tme.is_cmd_svc():
                raise RuntimeError(f'''TME object of type {tme.get_root_tag().tag_name} was identified in the TME Debug Policy Segment. Only CMD-SVC TME objects are supported in TME Debug Policy Segments.''')
            None.tme_objects.append(tme)
            tme_data = tme_data[len(tme.pack()):]
            if not tme_data:
                return None
            return None

    
    def pack_dpr_segment(self = None):
        tme_objects_data = b''.join(map(methodcaller('pack'), self.tme_objects))
        if len(tme_objects_data) > 4096:
            raise RuntimeError(f'''The TME Segment containing {len(self.tme_objects)} TME objects is {len(tme_objects_data)} bytes in size which exceeds the allowed maximum of 4K bytes. Reduce the number of included DPRs, SLCs, and/or IARs.''')
        return None(tme_objects_data)

    
    def get_size(self):
        return len(self.pack_dpr_segment())

    
    def is_type(cls = None, data = None):
        pass
    # WARNING: Decompyle incomplete

    is_type = None(is_type)
    
    def get_dump_files(self = None, directory = None):
        dump_files = super().get_dump_files(directory)
        subdir = f'''{directory}/tme_segment'''
        for idx, tme in enumerate(self.tme_objects):
            prefix = f'''tme_structure_{idx}_''' if len(self.tme_objects) > 1 else ''
            dump_files[f'''{subdir}/{prefix}{describe(tme).lower().replace(' ', '_')}.bin'''] = tme.pack()
        return dump_files

    
    def __repr__(self = None):
        string = super().__repr__()
        table = [
            ('Number of TME Objects:', str(len(self.tme_objects)))]
        tme_details = ''
        for i, tme in enumerate(self.tme_objects, 1, **('start',)):
            table.append((f'''#{i}. {describe(tme)} size:''', str(len(tme.pack()))))
            tme_details += f'''\n\n#{i}. {describe(tme)} Details:\n{tme}'''
            if augmented_info = augmented_inspect(tme):
                tme_details += f'''\n{augmented_info}'''
        return string + f'''\n\nTME Segment Properties:\n{properties_repr(table)}''' + tme_details

    __classcell__ = None

