
from abc import ABC, abstractmethod
from cmd_line_interface.basecmdline import NamespaceWithGet
from profile.profile_core import SecurityProfile

class CoreSpecificProfileConsumerInterface(ABC):
    '''
    Basic interface for Core objects that instantiates members of the SecurityProfile object which will be necessary
    for the Core to perform its operations.
    '''
    
    def set_core_specific_profile_attributes(cls = None, security_profile = classmethod, parsed_args = abstractmethod):
        pass

    set_core_specific_profile_attributes = None(None(set_core_specific_profile_attributes))

