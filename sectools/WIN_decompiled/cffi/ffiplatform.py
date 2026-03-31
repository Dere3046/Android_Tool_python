
import sys
import os
from error import VerificationError
LIST_OF_FILE_NAMES = [
    'sources',
    'include_dirs',
    'library_dirs',
    'extra_objects',
    'depends']

def get_extension(srcfilename, modname, sources = ((),), **kwds):
    _hack_at_distutils()
    Extension = Extension
    import distutils.core
    allsources = [
        srcfilename]
    for src in sources:
        allsources.append(os.path.normpath(src))
# WARNING: Decompyle incomplete


def compile(tmpdir, ext, compiler_verbose, debug = (0, None)):
    '''Compile a C extension module using distutils.'''
    _hack_at_distutils()
    saved_environ = os.environ.copy()
# WARNING: Decompyle incomplete


def _build(tmpdir, ext, compiler_verbose, debug = (0, None)):
    Distribution = Distribution
    import distutils.core
    import distutils.errors as distutils
    import distutils.log as distutils
    dist = Distribution({
        'ext_modules': [
            ext] })
    dist.parse_config_files()
    options = dist.get_option_dict('build_ext')
    if debug is None:
        debug = sys.flags.debug
    options['debug'] = ('ffiplatform', debug)
    options['force'] = ('ffiplatform', True)
    options['build_lib'] = ('ffiplatform', tmpdir)
    options['build_temp'] = ('ffiplatform', tmpdir)
# WARNING: Decompyle incomplete

# WARNING: Decompyle incomplete
