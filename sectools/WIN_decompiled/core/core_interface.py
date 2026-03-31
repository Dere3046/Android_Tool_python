
from abc import ABC, abstractmethod
from typing import List
from cmd_line_interface.basecmdline import NamespaceWithGet

class CoreInterface(ABC):
    
    def run(self = None, parsed_args = None):
        pass

    run = None(run)


class CoreInterfaceNoNamespace(ABC):
    
    def run(self = None, args = None):
        pass

    run = None(run)

