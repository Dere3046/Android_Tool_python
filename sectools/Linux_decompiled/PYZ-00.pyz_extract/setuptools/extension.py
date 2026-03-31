
import re
import functools
import distutils.core as distutils
import distutils.errors as distutils
import distutils.extension as distutils
from monkey import get_unpatched

def _have_cython():
    '''
    Return True if Cython can be imported.
    '''
    cython_impl = 'Cython.Distutils.build_ext'
# WARNING: Decompyle incomplete

have_pyrex = _have_cython
_Extension = get_unpatched(distutils.core.Extension)

class Extension(_Extension):
    """Extension that uses '.c' files in place of '.pyx' files"""
    
    def __init__(self = None, name = None, sources = None, *args, **kw):
        self.py_limited_api = kw.pop('py_limited_api', False)
    # WARNING: Decompyle incomplete

    
    def _convert_pyx_sources_to_lang(self):
        '''
        Replace sources with .pyx extensions to sources with the target
        language extension. This mechanism allows language authors to supply
        pre-converted sources but to prefer the .pyx sources.
        '''
        if _have_cython():
            return None
        if not None.language:
            pass
        lang = ''
        target_ext = '.cpp' if lang.lower() == 'c++' else '.c'
        sub = functools.partial(re.sub, '.pyx$', target_ext)
        self.sources = list(map(sub, self.sources))

    __classcell__ = None


class Library(Extension):
    '''Just like a regular Extension, but built as a library instead'''
    pass

