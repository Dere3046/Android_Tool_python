
from cmd_line_interface.basecmdline import NamespaceWithGet
from cmd_line_interface.sectools.cmd_line_common.defines import SUBFEATURE
from cmd_line_interface.sectools.tme_command.soc_terminate.defines import SOC_TERMINATE
from core.core_interface import CoreInterface
from core.tme_command.soc_terminate.soc_terminate_core import SocTerminateCore
from core.hash_sign_core import log_info_wrap

class TMECommandCore(CoreInterface):
    
    def run(self = None, parsed_args = None):
        subfeatures = {
            SOC_TERMINATE: SocTerminateCore() }
    # WARNING: Decompyle incomplete


