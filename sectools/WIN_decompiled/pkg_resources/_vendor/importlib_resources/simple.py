
'''
Interface adapters for low-level readers.
'''
import abc
import io
import itertools
from typing import BinaryIO, List
from abc import Traversable, TraversableResources

class SimpleReader(abc.ABC):
    '''
    The minimum, low-level interface required from a resource
    provider.
    '''
    
    def package(self):
        '''
        The name of the package for which this reader loads resources.
        '''
        pass

    package = abc.abstractproperty(package)
    
    def children(self):
        '''
        Obtain an iterable of SimpleReader for available
        child containers (e.g. directories).
        '''
        pass

    children = abc.abstractmethod(children)
    
    def resources(self):
        '''
        Obtain available named resources for this virtual package.
        '''
        pass

    resources = abc.abstractmethod(resources)
    
    def open_binary(self, resource):
        '''
        Obtain a File-like for a named resource.
        '''
        pass

    open_binary = abc.abstractmethod(open_binary)
    
    def name(self):
        return self.package.split('.')[-1]

    name = property(name)


class ResourceHandle(Traversable):
    '''
    Handle to a named resource in a ResourceReader.
    '''
    
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name

    
    def is_file(self):
        return True

    
    def is_dir(self):
        return False

    
    def open(self, mode = ('r',), *args, **kwargs):
        stream = self.parent.reader.open_binary(self.name)
    # WARNING: Decompyle incomplete

    
    def joinpath(self, name):
        raise RuntimeError('Cannot traverse into a resource')



class ResourceContainer(Traversable):
    """
    Traversable container for a package's resources via its reader.
    """
    
    def __init__(self, reader):
        self.reader = reader

    
    def is_dir(self):
        return True

    
    def is_file(self):
        return False

    
    def iterdir(self):
        files = (lambda .0 = None: for name in .0:
ResourceHandle(self, name))(self.reader.resources)
        dirs = map(ResourceContainer, self.reader.children())
        return itertools.chain(files, dirs)

    
    def open(self, *args, **kwargs):
        raise IsADirectoryError()

    
    def joinpath(self, name):
        return None((lambda .0 = None: for traversable in .0:
if traversable.name == name:
traversablecontinueNone)(self.iterdir()))



class TraversableReader(SimpleReader, TraversableResources):
    '''
    A TraversableResources based on SimpleReader. Resource providers
    may derive from this class to provide the TraversableResources
    interface by supplying the SimpleReader interface.
    '''
    
    def files(self):
        return ResourceContainer(self)


