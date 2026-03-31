
import importlib.util as importlib
import sys

class VendorImporter:
    '''
    A PEP 302 meta path importer for finding optionally-vendored
    or otherwise naturally-installed packages from root_name.
    '''
    
    def __init__(self, root_name, vendored_names, vendor_pkg = ((), None)):
        self.root_name = root_name
        self.vendored_names = set(vendored_names)
        if not vendor_pkg:
            pass
        self.vendor_pkg = root_name.replace('extern', '_vendor')

    
    def search_path(self):
        '''
        Search first the vendor package then as a natural package.
        '''
        yield self.vendor_pkg + '.'
        yield ''

    search_path = property(search_path)
    
    def _module_matches_namespace(self, fullname):
        '''Figure out if the target module is vendored.'''
        (root, base, target) = fullname.partition(self.root_name + '.')
        if not root:
            pass
        return any(map(target.startswith, self.vendored_names))

    
    def load_module(self, fullname):
        '''
        Iterate over the search path to locate and load fullname.
        '''
        (root, base, target) = fullname.partition(self.root_name + '.')
    # WARNING: Decompyle incomplete

    
    def create_module(self, spec):
        return self.load_module(spec.name)

    
    def exec_module(self, module):
        pass

    
    def find_spec(self, fullname, path, target = (None, None)):
        '''Return a module spec for vendored names.'''
        if self._module_matches_namespace(fullname):
            return importlib.util.spec_from_loader(fullname, self)

    
    def install(self):
        '''
        Install this importer into sys.meta_path if not already present.
        '''
        if self not in sys.meta_path:
            sys.meta_path.append(self)
            return None


names = ('packaging', 'pyparsing', 'ordered_set', 'more_itertools', 'importlib_metadata', 'zipp', 'importlib_resources', 'jaraco', 'typing_extensions', 'tomli')
VendorImporter(__name__, names, 'setuptools._vendor').install()
