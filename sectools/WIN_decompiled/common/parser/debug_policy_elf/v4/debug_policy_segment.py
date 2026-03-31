
from common.data.defines import SHA384_SIZE
from common.parser.debug_policy_elf.defines import DEBUG_POLICY_V4
from common.parser.debug_policy_elf.v3.debug_policy_segment import DebugPolicySegmentV3

class DebugPolicySegmentV4(DebugPolicySegmentV3):
    VERSION = DEBUG_POLICY_V4
    
    def hash_size(cls):
        return SHA384_SIZE

    hash_size = classmethod(hash_size)

