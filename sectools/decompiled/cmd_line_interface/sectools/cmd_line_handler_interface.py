
from abc import ABC, abstractmethod
from cmd_line_interface.basecmdline import NamespaceWithGet

class CMDLineHandlerInterface(ABC):
    
    def validate_cmd_line_args(cls = None, args = classmethod):
        """Validation function for interdependent command line arguments that can't be expressed via metadata."""
        pass

    validate_cmd_line_args = None(None(validate_cmd_line_args))

