
from binascii import hexlify, unhexlify
from typing import List, Optional, Union
from cmd_line_interface.sectools.secure_debug.defines import QTI_TEST_ROOT_CERTIFICATE_HASH
from common.data.data import properties_repr
from common.data.defines import PAD_BYTE_0, SHA_SIZE_TO_DESCRIPTION
from common.parser.debug_policy_elf.defines import DEBUG_POLICY_V3
from common.parser.debug_policy_elf.v1.defines import NUM_SOFTWARE_IDS
from common.parser.debug_policy_elf.v2.debug_policy_segment import DebugPolicySegmentV2
from common.parser.debug_policy_elf.v2.defines import NUM_ROOT_CERTIFICATE_HASHES
from common.parser.debug_policy_elf.v3.defines import ADSP_ENCRYPTED_MINI_DUMPS, APPS_ENCRYPTED_MINI_DUMPS, CDSP_ENCRYPTED_MINI_DUMPS, CSS_ENCRYPTED_MINI_DUMPS, LPASS_ENCRYPTED_MINI_DUMPS, MPSS_ENCRYPTED_MINI_DUMPS, NONSECURE_CRASH_DUMPS

class DebugPolicySegmentV3(DebugPolicySegmentV2):
    VERSION = DEBUG_POLICY_V3
    FLAGS = DebugPolicySegmentV2.FLAGS | {
        24: (NONSECURE_CRASH_DUMPS, 'Enable Non-secure Crash Dumps'),
        25: (APPS_ENCRYPTED_MINI_DUMPS, 'Enable APPS Encrypted Mini Dumps'),
        26: (MPSS_ENCRYPTED_MINI_DUMPS, 'Enable MPSS Encrypted Mini Dumps'),
        27: (LPASS_ENCRYPTED_MINI_DUMPS, 'Enable LPSS Encrypted Mini Dumps'),
        28: (CSS_ENCRYPTED_MINI_DUMPS, 'Enable CSS Encrypted Mini Dumps'),
        29: (ADSP_ENCRYPTED_MINI_DUMPS, 'Enable ADSP Encrypted Mini Dumps'),
        30: (CDSP_ENCRYPTED_MINI_DUMPS, 'Enable CDSP Encrypted Mini Dumps') }
    
    def __init__(self = None, data = None, check_is_type = None, bypass_validation = None):
        self.qti_root_certificate_hash_count = 0
        self.qti_root_certificate_hashes = []
        super().__init__(data, check_is_type, bypass_validation, **('data', 'check_is_type', 'bypass_validation'))

    
    def get_fields(cls = None):
        fields = super().get_fields()
        fields.append('qti_root_certificate_hash_count')
        for i in range(NUM_ROOT_CERTIFICATE_HASHES):
            fields.append('qti_root_certificate_hash_' + str(i))
        return fields

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        pass
    # WARNING: Decompyle incomplete

    get_field_defaults = None(get_field_defaults)
    
    def get_format(cls = None):
        return f'''{super().get_format()}I{f'''{cls.hash_size()}s''' * NUM_ROOT_CERTIFICATE_HASHES}'''

    get_format = None(get_format)
    
    def unpack_post_process(self = None):
        super().unpack_post_process()
        for i in range(NUM_ROOT_CERTIFICATE_HASHES):
            if i < self.qti_root_certificate_hash_count:
                self.qti_root_certificate_hashes.append(getattr(self, 'qti_root_certificate_hash_' + str(i)))

    
    def pack_pre_process(self = None):
        super().pack_pre_process()
        self.qti_root_certificate_hash_count = len(self.qti_root_certificate_hashes)
        for i in range(NUM_ROOT_CERTIFICATE_HASHES):
            if self.qti_root_certificate_hashes and i < len(self.qti_root_certificate_hashes):
                setattr(self, 'qti_root_certificate_hash_' + str(i), self.qti_root_certificate_hashes[i])
                continue
            setattr(self, 'qti_root_certificate_hash_' + str(i), PAD_BYTE_0 * self.hash_size())

    
    def get_header_properties(self = None):
        return super().get_header_properties() + [
            ('Number of QTI Root Certificate Hashes:', self.qti_root_certificate_hash_count)]

    
    def __repr__(self = None):
        string = super().__repr__()
        if self.qti_root_certificate_hashes:
            string += '\n\nDebug Policy Enabled QTI Root Certificate Hashes:\n' + properties_repr((lambda .0: [ ('0x' + hexlify(root_certificate_hash).decode(),) for root_certificate_hash in .0 ])(self.qti_root_certificate_hashes))
        return string

    
    def set_qti_root_certificate_hashes(self, qti_root_certificate_hashes):
        qti_root_certificate_hashes = list(set(qti_root_certificate_hashes))
        if len(qti_root_certificate_hashes) > NUM_ROOT_CERTIFICATE_HASHES:
            raise RuntimeError(f'''Debug Policy v{self.version} images support a maximum of {NUM_ROOT_CERTIFICATE_HASHES} QTI Root Certificate Hashes.''')
        for qti_root_certificate_hash in None:
            if len(qti_root_certificate_hash[2:]) != self.hash_size() * 2:
                raise RuntimeError(f'''{QTI_TEST_ROOT_CERTIFICATE_HASH} value "{qti_root_certificate_hash}" is not a {SHA_SIZE_TO_DESCRIPTION[self.hash_size()]} hash.''')
            self.qti_root_certificate_hashes = (lambda .0: [ unhexlify(qti_root_certificate_hash[2:]) for qti_root_certificate_hash in .0 ])(qti_root_certificate_hashes)
            self.qti_root_certificate_hash_count = len(qti_root_certificate_hashes)
            if self.qti_root_certificate_hash_count:
                for i in range(NUM_SOFTWARE_IDS):
                    self.software_ids.append(i)
        return None

    __classcell__ = None

