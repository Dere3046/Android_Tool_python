
from abc import ABC, abstractmethod
from profile.profile_core import SecurityProfile

class ParserSecurityProfileValidatorInterface(ABC):
    """
    The basic interface that defines the validation rules between the Security Profile items and the object.
    This interface does not care if the object's internal state is valid (hopefully it is) but only that the
    object is compliant with Security Profile. Validation of the Security Profile schema is also outside the
    scope of this interface.
    """
    
    def validate_against_security_profile(self = None, security_profile = None, path = abstractmethod):
        pass

    validate_against_security_profile = None(validate_against_security_profile)

