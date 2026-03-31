
from common.parser.debug_policy_elf.defines import DEBUG_POLICY_V6
from common.parser.debug_policy_elf.v5.debug_policy_segment import DebugPolicySegmentV5
from common.parser.debug_policy_elf.v6.defines import ATB, MODEM_RESTART, MODEM_SSR_DUMP, SILENT_LOGGING, WLAN_RESTART, WLAN_RESTART_DUMP

class DebugPolicySegmentV6(DebugPolicySegmentV5):
    VERSION = DEBUG_POLICY_V6
    FLAGS = DebugPolicySegmentV5.FLAGS | {
        32: (SILENT_LOGGING, 'Enable Silent XPU Error Logging'),
        33: (MODEM_SSR_DUMP, 'Enable RAM Dumps on Modem SSR'),
        34: (MODEM_RESTART, 'Enable Modem SSR'),
        35: (WLAN_RESTART_DUMP, 'Enable RAM Dumps on WLAN Restart'),
        36: (WLAN_RESTART, 'Enable WLAN Restart'),
        37: (ATB, 'Enable QDSS ATB Interface') }

