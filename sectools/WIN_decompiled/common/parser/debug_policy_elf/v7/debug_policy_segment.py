
from common.parser.debug_policy_elf.defines import DEBUG_POLICY_V7
from common.parser.debug_policy_elf.v6.debug_policy_segment import DebugPolicySegmentV6
from common.parser.debug_policy_elf.v7.defines import SAIL_CORE_0_DEBUG, SAIL_CORE_0_NON_INVASIVE_DEBUG, SAIL_CORE_1_DEBUG, SAIL_CORE_1_NON_INVASIVE_DEBUG, SAIL_CORE_2_DEBUG, SAIL_CORE_2_NON_INVASIVE_DEBUG, SAIL_CORE_3_DEBUG, SAIL_CORE_3_NON_INVASIVE_DEBUG, SAIL_CORE_4_DEBUG, SAIL_CORE_4_NON_INVASIVE_DEBUG, SAIL_CORE_5_DEBUG, SAIL_CORE_5_NON_INVASIVE_DEBUG, SAIL_HYPERVISOR_DEBUG, SAIL_HYPERVISOR_NON_INVASIVE_DEBUG

class DebugPolicySegmentV7(DebugPolicySegmentV6):
    VERSION = DEBUG_POLICY_V7
    FLAGS = DebugPolicySegmentV6.FLAGS | {
        9: (SAIL_HYPERVISOR_DEBUG, 'Enable SAIL Hypervisor Debug'),
        10: (SAIL_HYPERVISOR_NON_INVASIVE_DEBUG, 'Enable Non-Invasive SAIL Hypervisor Debug'),
        11: (SAIL_CORE_0_DEBUG, 'Enable Debug of SAIL Core 0'),
        12: (SAIL_CORE_0_NON_INVASIVE_DEBUG, 'Enable Non-Invasive Debug of SAIL Core 0'),
        13: (SAIL_CORE_1_DEBUG, 'Enable Debug of SAIL Core 1'),
        14: (SAIL_CORE_1_NON_INVASIVE_DEBUG, 'Enable Non-Invasive Debug of SAIL Core 1'),
        15: (SAIL_CORE_2_DEBUG, 'Enable Debug of SAIL Core 2'),
        16: (SAIL_CORE_2_NON_INVASIVE_DEBUG, 'Enable Non-Invasive Debug of SAIL Core 2'),
        17: (SAIL_CORE_3_DEBUG, 'Enable Debug of SAIL Core 3'),
        18: (SAIL_CORE_3_NON_INVASIVE_DEBUG, 'Enable Non-Invasive Debug of SAIL Core 3'),
        19: (SAIL_CORE_4_DEBUG, 'Enable Debug of SAIL Core 4'),
        20: (SAIL_CORE_4_NON_INVASIVE_DEBUG, 'Enable Non-Invasive Debug of SAIL Core 4'),
        21: (SAIL_CORE_5_DEBUG, 'Enable Debug of SAIL Core 5'),
        22: (SAIL_CORE_5_NON_INVASIVE_DEBUG, 'Enable Non-Invasive Debug of SAIL Core 5') }

