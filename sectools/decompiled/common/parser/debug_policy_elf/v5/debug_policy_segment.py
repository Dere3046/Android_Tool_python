
from common.parser.debug_policy_elf.defines import DEBUG_POLICY_V5
from common.parser.debug_policy_elf.v4.debug_policy_segment import DebugPolicySegmentV4
from common.parser.debug_policy_elf.v5.defines import DEBUG_LEVEL_0, DEBUG_LEVEL_1, INVASIVE_DEBUG, MODEM_INVASIVE_DEBUG, MODEM_NON_INVASIVE_DEBUG, WLAN_ENCRYPTED_MINI_DUMPS

class DebugPolicySegmentV5(DebugPolicySegmentV4):
    VERSION = DEBUG_POLICY_V5
    FLAGS = DebugPolicySegmentV4.FLAGS | {
        4: (MODEM_INVASIVE_DEBUG, 'Enable Invasive Modem Debug'),
        5: (MODEM_NON_INVASIVE_DEBUG, 'Enable Non-Invasive Modem Debug'),
        6: (INVASIVE_DEBUG, 'Enable Invasive Debug'),
        7: (DEBUG_LEVEL_0, 'Enable Debug Level 0'),
        8: (DEBUG_LEVEL_1, 'Enable Debug Level 1'),
        31: (WLAN_ENCRYPTED_MINI_DUMPS, 'Enable WLAN Encrypted Mini Dumps') }

