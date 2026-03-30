
from contextlib import suppress
from io import TextIOWrapper
from  import abc

class SpecLoaderAdapter:
    '''
    Adapt a package spec to adapt the underlying loader.
    '''
    
    def __init__(self, spec, adapter = ((lambda spec: spec.loader),)):
        self.spec = spec
        self.loader = adapter(spec)

    
    def __getattr__(self, name):
        return getattr(self.spec, name)



class TraversableResourcesLoader:
    '''
    Adapt a loader to provide TraversableResources.
    '''
    
    def __init__(self, spec):
        self.spec = spec

    
    def get_resource_reader(self, name):
        return CompatibilityFiles(self.spec)._native()



def _io_wrapper(file, mode = ('r',), *args, **kwargs):
    pass
# WARNING: Decompyle incomplete


class CompatibilityFiles:
    '''
    Adapter for an existing or non-existent resource reader
    to provide a compatibility .files().
    '''
    
    class SpecPath(abc.Traversable):
        __qualname__ = 'CompatibilityFiles.SpecPath'
        __doc__ = '\n        Path tied to a module spec.\n        Can be read and exposes the resource reader children.\n        '
        
        def __init__(self, spec, reader):
            self._spec = spec
            self._reader = reader

        
        def iterdir(self):
            if not self._reader:
                return iter(())
            return None((lambda .0 = None: for path in .0:
CompatibilityFiles.ChildPath(self._reader, path))(self._reader.contents()))

        
        def is_file(self):
            return False

        is_dir = is_file
        
        def joinpath(self, other):
            if not self._reader:
                return CompatibilityFiles.OrphanPath(other)
            return None.ChildPath(self._reader, other)

        
        def name(self):
            return self._spec.name

        name = property(name)
        
        def open(self, mode = ('r',), *args, **kwargs):
            pass
        # WARNING: Decompyle incomplete


    
    class ChildPath(abc.Traversable):
        __qualname__ = 'CompatibilityFiles.ChildPath'
        __doc__ = "\n        Path tied to a resource reader child.\n        Can be read but doesn't expose any meaningful children.\n        "
        
        def __init__(self, reader, name):
            self._reader = reader
            self._name = name

        
        def iterdir(self):
            return iter(())

        
        def is_file(self):
            return self._reader.is_resource(self.name)

        
        def is_dir(self):
            return not self.is_file()

        
        def joinpath(self, other):
            return CompatibilityFiles.OrphanPath(self.name, other)

        
        def name(self):
            return self._name

        name = property(name)
        
        def open(self, mode = ('r',), *args, **kwargs):
            pass
        # WARNING: Decompyle incomplete


    
    class OrphanPath(abc.Traversable):
        __qualname__ = 'CompatibilityFiles.OrphanPath'
        __doc__ = "\n        Orphan path, not tied to a module spec or resource reader.\n        Can't be read and doesn't expose any meaningful children.\n        "
        
        def __init__(self, *path_parts):
            if len(path_parts) < 1:
                raise ValueError('Need at least one path part to construct a path')
            self._path = None

        
        def iterdir(self):
            return iter(())

        
        def is_file(self):
            return False

        is_dir = is_file
        
        def joinpath(self, other):
            pass
        # WARNING: Decompyle incomplete

        
        def name(self):
            return self._path[-1]

        name = property(name)
        
        def open(self, mode = ('r',), *args, **kwargs):
            raise FileNotFoundError("Can't open orphan path")


    
    def __init__(self, spec):
        self.spec = spec

    
    def _reader(self):
        pass
    # WARNING: Decompyle incomplete

    _reader = property(_reader)
    
    def _native(self):
        '''
        Return the native reader if it supports files().
        '''
        reader = self._reader
        if hasattr(reader, 'files'):
            return reader

    
    def __getattr__(self, attr):
        return getattr(self._reader, attr)

    
    def files(self):
        return CompatibilityFiles.SpecPath(self.spec, self._reader)



def wrap_spec(package):
    '''
    Construct a package spec with traversable compatibility
    on the spec/loader/reader.
    '''
    return SpecLoaderAdapter(package.__spec__, TraversableResourcesLoader)

