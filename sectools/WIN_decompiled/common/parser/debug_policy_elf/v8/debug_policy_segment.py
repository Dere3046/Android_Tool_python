
from common.parser.debug_policy_elf.defines import DEBUG_POLICY_V8
from common.parser.debug_policy_elf.v7.debug_policy_segment import DebugPolicySegmentV7
from common.parser.debug_policy_elf.v8.defines import CDSP1_ENCRYPTED_MINI_DUMPS, GPDSP0_ENCRYPTED_MINI_DUMPS, GPSDP1_ENCRYPTED_MINI_DUMPS

class DebugPolicySegmentV8(DebugPolicySegmentV7):
    VERSION = DEBUG_POLICY_V8
    FLAGS = DebugPolicySegmentV7.FLAGS | {
        38: (CDSP1_ENCRYPTED_MINI_DUMPS, 'Enable CDSP1 Encrypted Mini Dumps'),
        39: (GPDSP0_ENCRYPTED_MINI_DUMPS, 'Enable GPDSP0 Encrypted Mini Dumps'),
        40: (GPSDP1_ENCRYPTED_MINI_DUMPS, 'Enable GPDSP1 Encrypted Mini Dumps') }

