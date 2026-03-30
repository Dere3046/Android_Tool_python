
from abc import ABC, abstractmethod
from typing import Any

class DynamicArgumentsInterface(ABC):
    
    def add_dynamic_arguments(parsed_args = None):
        '''
        Will be called before parsing command line arguments and allows updating/adding dynamic arguments.
        '''
        pass

    add_dynamic_arguments = None(None(add_dynamic_arguments))

