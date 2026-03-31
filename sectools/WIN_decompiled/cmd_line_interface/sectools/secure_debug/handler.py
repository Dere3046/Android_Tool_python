
from argparse import SUPPRESS
from typing import Any
from cmd_line_interface.base_defines import XMLInfo, get_cmd_member
from cmd_line_interface.basecmdline import BaseCMDLine
from cmd_line_interface.sectools.cmd_line_common.base_defines import SECURITY_PROFILE
from cmd_line_interface.sectools.cmd_line_common.handler import CommonCMDLineHandler
from cmd_line_interface.sectools.dynamic_arguments_interface import DynamicArgumentsInterface
from cmd_line_interface.sectools.secure_debug.defines import SECURE_DEBUG_DEVICE_RESTRICTIONS, SECURE_DEBUG_SIGNING
from cmd_line_interface.sectools.secure_debug.dynamic_arguments import update_secure_debug_profile_arguments

class SecureDebugSigningOptionsCMDLine(BaseCMDLine):
    
    def __init__(self = None):
        super().__init__(SECURE_DEBUG_SIGNING, SUPPRESS, **('usage',))

    __classcell__ = None


class SecureDebugDeviceRestrictionsCMDLine(BaseCMDLine):
    
    def __init__(self = None):
        super().__init__(SECURE_DEBUG_DEVICE_RESTRICTIONS, SUPPRESS, **('usage',))

    __classcell__ = None


class SecureDebugCMDLineHandler(DynamicArgumentsInterface, CommonCMDLineHandler):
    
    def show_signing_options_help():
        SecureDebugSigningOptionsCMDLine().print_help()

    show_signing_options_help = staticmethod(show_signing_options_help)
    
    def show_available_device_restrictions():
        SecureDebugDeviceRestrictionsCMDLine().print_help()

    show_available_device_restrictions = staticmethod(show_available_device_restrictions)
    
    def add_dynamic_arguments(parsed_args = None):
        security_profile = parsed_args[get_cmd_member(SECURITY_PROFILE)]
    # WARNING: Decompyle incomplete

    add_dynamic_arguments = None(add_dynamic_arguments)

