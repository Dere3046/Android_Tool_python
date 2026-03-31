
from typing import Any, Dict, Optional
from cmd_line_interface.base_defines import get_cmd_member
from cmd_line_interface.sectools.cmd_line_common.defines import GENERATE
from core.base_device_restrictions import BaseDeviceRestrictions

class SecureDebugDeviceRestrictions(BaseDeviceRestrictions):
    
    def update(self = None, constructor_args = None, security_profile_args = None):
        super().update(constructor_args, security_profile_args)
        vars(self)['serial_numbers_fatal'] = not bool(constructor_args.get(get_cmd_member(GENERATE), False))

    __classcell__ = None

