
from binascii import unhexlify
from typing import Any, Iterable
from cmd_line_interface.sectools.cmd_line_common.defines import OEM_TEST_ROOT_CERTIFICATE_HASH
from cmd_line_interface.sectools.secure_debug import defines
from common.data.binary_struct import StructBase
from common.data.defines import SHA256_SIZE, SHA_SIZE_TO_DESCRIPTION
from common.parser.debug_policy_elf.defines import DEBUG_POLICY_MAG, DEBUG_POLICY_V_ABSTRACT, DebugOption, OEM_DESIGNATED_FLAG_INDICES, SUPPORTED_DEBUG_POLICY_VERSIONS
from common.parser.debug_policy_elf.v1.defines import NUM_SOFTWARE_IDS, OFFLINE_CRASH_DUMPS, ONLINE_CRASH_DUMPS

class DebugPolicySegmentCommon(StructBase):
    software_ids: list[int] = DEBUG_POLICY_V_ABSTRACT
    FLAGS = {
        0: (ONLINE_CRASH_DUMPS, 'Enable Online Crash Dumps'),
        1: (OFFLINE_CRASH_DUMPS, 'Enable Offline Crash Dumps') } | (lambda .0: pass# WARNING: Decompyle incomplete
)(OEM_DESIGNATED_FLAG_INDICES)
    
    def __init__(self = None, data = None, check_is_type = None, bypass_validation = None):
        self.root_certificate_hashes = []
        self.root_certificate_hash_count = 0
        self.software_id_count = 0
        self.flags = 0
        super().__init__(data, check_is_type, bypass_validation, **('data', 'check_is_type', 'bypass_validation'))

    
    def get_fields(cls = None):
        return [
            'magic',
            'data_size',
            'version']

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        pass
    # WARNING: Decompyle incomplete

    get_field_defaults = None(get_field_defaults)
    
    def get_format(cls = None):
        return '<4sII'

    get_format = None(get_format)
    
    def validate_critical_fields(self = None):
        ''' The data is not of a Debug Policy Segment if it does not contain the magic '''
        if self.magic != DEBUG_POLICY_MAG:
            raise RuntimeError(f'''Debug Policy Segment contains invalid Magic: {str(self.magic)}.''')
        if None.version not in SUPPORTED_DEBUG_POLICY_VERSIONS:
            raise RuntimeError(f'''Debug Policy Segment has invalid version: {self.version}.''')

    
    def validate(self = None):
        self.validate_critical_fields()

    
    def hash_size(cls = None):
        return SHA256_SIZE

    hash_size = None(hash_size)
    
    def set_all_flags(self = None):
        None((lambda .0 = None: for option in .0:
if any((lambda .0: for flag in .0:
flag in OEM_DESIGNATED_FLAG_INDICES)(option.bits)) and None((lambda .0 = None: for flag in .0:
flag in self.FLAGS)(option.bits)):
                    yield option
                    continue
                    return None
)(defines.security_profile_debug_options))

    
    def set_flags(self = None, debug_options = None):
        for debug_option in debug_options:
            if None((lambda .0 = None: for bit in .0:
bit in self.FLAGS)(debug_option.bits)):
                mask = 0
                for bit in debug_option.bits:
                    mask |= 1 << bit
                    (flag_name, _) = self.FLAGS[bit]
                    setattr(self, flag_name, 1)
                self.flags |= mask
                continue
            raise RuntimeError(f'''Debug Policy v{self.version} images do not support {debug_option.option_id}''')
            return None

    
    def set_oem_root_certificate_hashes(self = None, oem_root_certificate_hashes = None):
        oem_root_certificate_hashes = list(set(oem_root_certificate_hashes))
        for oem_root_certificate_hash in oem_root_certificate_hashes:
            if len(oem_root_certificate_hash[2:]) != self.hash_size() * 2:
                raise RuntimeError(f'''{OEM_TEST_ROOT_CERTIFICATE_HASH} value "{oem_root_certificate_hash}" is not a {SHA_SIZE_TO_DESCRIPTION[self.hash_size()]} hash.''')
            self.root_certificate_hashes = (lambda .0: [ unhexlify(oem_root_certificate_hash[2:]) for oem_root_certificate_hash in .0 ])(oem_root_certificate_hashes)
            self.root_certificate_hash_count = len(oem_root_certificate_hashes)
            if self.root_certificate_hash_count:
                self.software_id_count = NUM_SOFTWARE_IDS
                for i in range(NUM_SOFTWARE_IDS):
                    self.software_ids.append(i)
        return None

    __classcell__ = None

