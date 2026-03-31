
from abc import ABC, abstractmethod
from typing import Optional, Type, Union
import profile
from cmd_line_interface.basecmdline import NamespaceWithGet
from cmd_line_interface.sectools.cmd_line_common.defines import PLATFORM_BINDING, VARIANT
from core.base_device_restrictions import BaseDeviceRestrictions
from core.platform_binding_utilities import get_security_profile_platform_binding_values
from core.secure_debug.secure_debug_device_restrictions import SecureDebugDeviceRestrictions
from core.secure_image.secure_image_device_restrictions import SecureImageDeviceRestrictions
DeviceRestrictions = Union[(BaseDeviceRestrictions, SecureImageDeviceRestrictions, SecureDebugDeviceRestrictions)]

class DeviceRestrictionsConsumer(ABC):
    
    def __init__(self = None):
        super().__init__()
        self.device_restrictions = None

    
    def device_restrictions_class(self = None):
        pass

    device_restrictions_class = None(None(device_restrictions_class))
    
    def init_device_restrictions(self = None, parsed_args = None):
        security_profile_device_restrictions = get_security_profile_platform_binding_values(parsed_args.get(PLATFORM_BINDING), parsed_args.get(VARIANT), profile.SECURITY_PROFILE)
        self.device_restrictions = self.device_restrictions_class.from_parsed_args(vars(parsed_args), security_profile_device_restrictions)

    __classcell__ = None

