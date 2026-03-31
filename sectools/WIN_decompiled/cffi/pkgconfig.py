
import sys
import os
import subprocess
from error import PkgConfigError

def merge_flags(cfg1, cfg2):
    '''Merge values from cffi config flags cfg2 to cf1

    Example:
        merge_flags({"libraries": ["one"]}, {"libraries": ["two"]})
        {"libraries": ["one", "two"]}
    '''
    for key, value in cfg2.items():
        if key not in cfg1:
            cfg1[key] = value
            continue
        if not isinstance(cfg1[key], list):
            raise TypeError('cfg1[%r] should be a list of strings' % (key,))
        if not None(value, list):
            raise TypeError('cfg2[%r] should be a list of strings' % (key,))
        None[key].extend(value)
    return cfg1


def call(libname, flag, encoding = (sys.getfilesystemencoding(),)):
    '''Calls pkg-config and returns the output if found
    '''
    a = [
        'pkg-config',
        '--print-errors']
    a.append(flag)
    a.append(libname)
# WARNING: Decompyle incomplete


def flags_from_pkgconfig(libs):
    '''Return compiler line flags for FFI.set_source based on pkg-config output

    Usage
        ...
        ffibuilder.set_source("_foo", pkgconfig = ["libfoo", "libbar >= 1.8.3"])

    If pkg-config is installed on build machine, then arguments include_dirs,
    library_dirs, libraries, define_macros, extra_compile_args and
    extra_link_args are extended with an output of pkg-config for libfoo and
    libbar.

    Raises PkgConfigError in case the pkg-config call fails.
    '''
    
    def get_include_dirs(string):
        return (lambda .0: [ x[2:] for x in .0 if x.startswith('-I') ])(string.split())

    
    def get_library_dirs(string):
        return (lambda .0: [ x[2:] for x in .0 if x.startswith('-L') ])(string.split())

    
    def get_libraries(string):
        return (lambda .0: [ x[2:] for x in .0 if x.startswith('-l') ])(string.split())

    
    def get_macros(string):
        
        def _macro(x):
            x = x[2:]
            if '=' in x:
                return tuple(x.split('=', 1))
            return (None, None)

        return (lambda .0 = None: [ _macro(x) for x in .0 if x.startswith('-D') ])(string.split())

    
    def get_other_cflags(string):
        return (lambda .0: [ x for x in .0 if x.startswith('-D') ])(string.split())

    
    def get_other_libs(string):
        return (lambda .0: [ x for x in .0 if x.startswith('-l') ])(string.split())

    
    def kwargs(libname = None):
        fse = sys.getfilesystemencoding()
        all_cflags = call(libname, '--cflags')
        all_libs = call(libname, '--libs')
        return {
            'include_dirs': get_include_dirs(all_cflags),
            'library_dirs': get_library_dirs(all_libs),
            'libraries': get_libraries(all_libs),
            'define_macros': get_macros(all_cflags),
            'extra_compile_args': get_other_cflags(all_cflags),
            'extra_link_args': get_other_libs(all_libs) }

    ret = { }
    for libname in libs:
        lib_flags = kwargs(libname)
        merge_flags(ret, lib_flags)
    return ret

