
from abc import ABC, abstractmethod
from typing import List, Optional
from cmd_line_interface.basecmdline import NamespaceWithGet
from profile.schema.scale_profile import Profile

class CoreSecurityProfileValidatorInterface(ABC):
    '''
    Basic interface that defines the validation rules between the Security Profile items and a Core object.
    An implementation should check that the parsed profiles contain all members required for the Core to perform
    its operations.
    '''
    
    def validate_mandatory_security_profile_attributes(parsed_profiles = None, parsed_args = staticmethod):
        pass

    validate_mandatory_security_profile_attributes = None(None(validate_mandatory_security_profile_attributes))

