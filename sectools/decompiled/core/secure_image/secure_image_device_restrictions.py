
from typing import Any, Dict, Optional
import profile
from cmd_line_interface.sectools.cmd_line_common.defines import SECURITY_PROFILE
from cmd_line_interface.sectools.secure_image.defines import CLIENT_ID, CRASH_DUMP, ENABLE, FEATURE_ID, JTAG_DEBUG, LIBRARY_ID, NOP, OEM_ROOT_CERTIFICATE_HASH, SECONDARY_SOFTWARE_ID, TRANSFER_UIE_KEY
from common.data.defines import SHA_SIZE_TO_DESCRIPTION
from core.base_device_restrictions import BaseDeviceRestrictions

class SecureImageDeviceRestrictions(BaseDeviceRestrictions):
    
    def validate_allowed_device_restrictions(self = None, _ = None, independent_platform_binding_non_fatal = None):
        super().validate_allowed_device_restrictions({
            'serial_bind': self.serial_number,
            'root_revoke_activation_enable': self.transfer_root,
            'debug': self.jtag_debug == ENABLE,
            'uie_key_switch_enable': self.transfer_uie_key,
            'crash_dump': self.crash_dump }, independent_platform_binding_non_fatal, **('independent_platform_binding_non_fatal',))
        security_profile = profile.SECURITY_PROFILE
    # WARNING: Decompyle incomplete

    __classcell__ = None

