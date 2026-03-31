
import abc
from typing import BinaryIO, Iterable, Text
from _compat import runtime_checkable, Protocol
ResourceReader = <NODE:27>((lambda : __doc__ = 'Abstract base class for loaders to provide resource reading support.'
def open_resource(self = None, resource = None):
"""Return an opened, file-like object for binary reading.

        The 'resource' argument is expected to represent only a file name.
        If the resource cannot be found, FileNotFoundError is raised.
        """
raise FileNotFoundErroropen_resource = None(open_resource)
def resource_path(self = None, resource = None):
"""Return the file system path to the specified resource.

        The 'resource' argument is expected to represent only a file name.
        If the resource does not exist on the file system, raise
        FileNotFoundError.
        """
raise FileNotFoundErrorresource_path = None(resource_path)
def is_resource(self = None, path = None):
"""Return True if the named 'path' is a resource.

        Files are resources, directories are not.
        """
raise FileNotFoundErroris_resource = None(is_resource)
def contents(self = None):
'''Return an iterable of entries in `package`.'''
raise FileNotFoundErrorcontents = None(contents)), 'ResourceReader', abc.ABCMeta, **('metaclass',))
Traversable = runtime_checkable(<NODE:12>)

class TraversableResources(ResourceReader):
    '''
    The required interface for providing traversable
    resources.
    '''
    
    def files(self):
        '''Return a Traversable object for the loaded package.'''
        pass

    files = abc.abstractmethod(files)
    
    def open_resource(self, resource):
        return self.files().joinpath(resource).open('rb')

    
    def resource_path(self, resource):
        raise FileNotFoundError(resource)

    
    def is_resource(self, path):
        return self.files().joinpath(path).is_file()

    
    def contents(self):
        return (lambda .0: for item in .0:
item.name)(self.files().iterdir())


