
'''Shared OS X support functions.'''
import os
import re
import sys
__all__ = [
    'compiler_fixup',
    'customize_config_vars',
    'customize_compiler',
    'get_platform_osx']
_UNIVERSAL_CONFIG_VARS = ('CFLAGS', 'LDFLAGS', 'CPPFLAGS', 'BASECFLAGS', 'BLDSHARED', 'LDSHARED', 'CC', 'CXX', 'PY_CFLAGS', 'PY_LDFLAGS', 'PY_CPPFLAGS', 'PY_CORE_CFLAGS', 'PY_CORE_LDFLAGS')
_COMPILER_CONFIG_VARS = ('BLDSHARED', 'LDSHARED', 'CC', 'CXX')
_INITPRE = '_OSX_SUPPORT_INITIAL_'

def _find_executable(executable, path = (None,)):
    """Tries to find 'executable' in the directories listed in 'path'.

    A string listing directories separated by 'os.pathsep'; defaults to
    os.environ['PATH'].  Returns the complete filename or None if not found.
    """
    if path is None:
        path = os.environ['PATH']
    paths = path.split(os.pathsep)
    (base, ext) = os.path.splitext(executable)
    if sys.platform == 'win32' and ext != '.exe':
        executable = executable + '.exe'
    if not os.path.isfile(executable):
        for p in paths:
            f = os.path.join(p, executable)
            if os.path.isfile(f):
                return f
            return None
            return executable


def _read_output(commandstring, capture_stderr = (False,)):
    '''Output from successful command execution or None'''
    import contextlib
# WARNING: Decompyle incomplete


def _find_build_tool(toolname):
    '''Find a build tool on current path or using xcrun'''
    if not _find_executable(toolname) and _read_output('/usr/bin/xcrun -find %s' % (toolname,)):
        pass
    return ''

_SYSTEM_VERSION = None

def _get_system_version():
    '''Return the OS X system version as a string'''
    global _SYSTEM_VERSION
    pass
# WARNING: Decompyle incomplete

_SYSTEM_VERSION_TUPLE = None

def _get_system_version_tuple():
    '''
    Return the macOS system version as a tuple

    The return value is safe to use to compare
    two version numbers.
    '''
    global _SYSTEM_VERSION_TUPLE
    pass
# WARNING: Decompyle incomplete


def _remove_original_values(_config_vars):
    '''Remove original unmodified values for testing'''
    for k in list(_config_vars):
        if k.startswith(_INITPRE):
            del _config_vars[k]


def _save_modified_value(_config_vars, cv, newvalue):
    '''Save modified and original unmodified value of configuration var'''
    oldvalue = _config_vars.get(cv, '')
    if oldvalue != newvalue and _INITPRE + cv not in _config_vars:
        _config_vars[_INITPRE + cv] = oldvalue
    _config_vars[cv] = newvalue

_cache_default_sysroot = None

def _default_sysroot(cc):
    """ Returns the root of the default SDK for this system, or '/' """
    global _cache_default_sysroot, _cache_default_sysroot, _cache_default_sysroot
    if _cache_default_sysroot is not None:
        return _cache_default_sysroot
    contents = None('%s -c -E -v - </dev/null' % (cc,), True)
    in_incdirs = False
    for line in contents.splitlines():
        if line.startswith('#include <...>'):
            in_incdirs = True
            continue
        if line.startswith('End of search list'):
            in_incdirs = False
            continue
        if in_incdirs:
            line = line.strip()
            if line == '/usr/include':
                _cache_default_sysroot = '/'
                continue
            if line.endswith('.sdk/usr/include'):
                _cache_default_sysroot = line[:-12]
    if _cache_default_sysroot is None:
        _cache_default_sysroot = '/'
    return _cache_default_sysroot


def _supports_universal_builds():
    '''Returns True if universal builds are supported on this system'''
    osx_version = _get_system_version_tuple()
    if osx_version:
        return bool(osx_version >= (10, 4))


def _supports_arm64_builds():
    '''Returns True if arm64 builds are supported on this system'''
    osx_version = _get_system_version_tuple()
    if osx_version:
        return osx_version >= (11, 0)


def _find_appropriate_compiler(_config_vars):
    '''Find appropriate C compiler for extension module builds'''
    if 'CC' in os.environ:
        return _config_vars
    cc = oldcc = None['CC'].split()[0]
    if not _find_executable(cc):
        cc = _find_build_tool('clang')
    elif os.path.basename(cc).startswith('gcc'):
        data = _read_output("'%s' --version" % (cc.replace("'", '\'"\'"\''),))
        if data and 'llvm-gcc' in data:
            cc = _find_build_tool('clang')
    if not cc:
        raise SystemError('Cannot locate working compiler')
    if None != oldcc:
        for cv in _COMPILER_CONFIG_VARS:
            if cv in _config_vars and cv not in os.environ:
                cv_split = _config_vars[cv].split()
                cv_split[0] = cc if cv != 'CXX' else cc + '++'
                _save_modified_value(_config_vars, cv, ' '.join(cv_split))
    return _config_vars


def _remove_universal_flags(_config_vars):
    '''Remove all universal build arguments from config vars'''
    for cv in _UNIVERSAL_CONFIG_VARS:
        if cv in _config_vars and cv not in os.environ:
            flags = _config_vars[cv]
            flags = re.sub('-arch\\s+\\w+\\s', ' ', flags, re.ASCII, **('flags',))
            flags = re.sub('-isysroot\\s*\\S+', ' ', flags)
            _save_modified_value(_config_vars, cv, flags)
    return _config_vars


def _remove_unsupported_archs(_config_vars):
    '''Remove any unsupported archs from config vars'''
    if 'CC' in os.environ:
        return _config_vars
    if None.search('-arch\\s+ppc', _config_vars['CFLAGS']) is not None:
        status = os.system("echo 'int main{};' | '%s' -c -arch ppc -x c -o /dev/null /dev/null 2>/dev/null" % (_config_vars['CC'].replace("'", '\'"\'"\''),))
        if status:
            for cv in _UNIVERSAL_CONFIG_VARS:
                if cv in _config_vars and cv not in os.environ:
                    flags = _config_vars[cv]
                    flags = re.sub('-arch\\s+ppc\\w*\\s', ' ', flags)
                    _save_modified_value(_config_vars, cv, flags)
    return _config_vars


def _override_all_archs(_config_vars):
    '''Allow override of all archs with ARCHFLAGS env var'''
    if 'ARCHFLAGS' in os.environ:
        arch = os.environ['ARCHFLAGS']
        for cv in _UNIVERSAL_CONFIG_VARS:
            if cv in _config_vars and '-arch' in _config_vars[cv]:
                flags = _config_vars[cv]
                flags = re.sub('-arch\\s+\\w+\\s', ' ', flags)
                flags = flags + ' ' + arch
                _save_modified_value(_config_vars, cv, flags)
    return _config_vars


def _check_for_unavailable_sdk(_config_vars):
    '''Remove references to any SDKs not available'''
    cflags = _config_vars.get('CFLAGS', '')
    m = re.search('-isysroot\\s*(\\S+)', cflags)
    if m is not None:
        sdk = m.group(1)
        if not os.path.exists(sdk):
            for cv in _UNIVERSAL_CONFIG_VARS:
                if cv in _config_vars and cv not in os.environ:
                    flags = _config_vars[cv]
                    flags = re.sub('-isysroot\\s*\\S+(?:\\s|$)', ' ', flags)
                    _save_modified_value(_config_vars, cv, flags)
    return _config_vars


def compiler_fixup(compiler_so, cc_args):
    """
    This function will strip '-isysroot PATH' and '-arch ARCH' from the
    compile flags if the user has specified one them in extra_compile_flags.

    This is needed because '-arch ARCH' adds another architecture to the
    build, without a way to remove an architecture. Furthermore GCC will
    barf if multiple '-isysroot' arguments are present.
    """
    stripArch = stripSysroot = False
    compiler_so = list(compiler_so)
    if not _supports_universal_builds():
        stripArch = stripSysroot = True
    else:
        stripArch = '-arch' in cc_args
        stripSysroot = any((lambda .0: for arg in .0:
if arg.startswith('-isysroot'):
argcontinueNone)(cc_args))
# WARNING: Decompyle incomplete


def customize_config_vars(_config_vars):
    '''Customize Python build configuration variables.

    Called internally from sysconfig with a mutable mapping
    containing name/value pairs parsed from the configured
    makefile used to build this interpreter.  Returns
    the mapping updated as needed to reflect the environment
    in which the interpreter is running; in the case of
    a Python from a binary installer, the installed
    environment may be very different from the build
    environment, i.e. different OS levels, different
    built tools, different available CPU architectures.

    This customization is performed whenever
    distutils.sysconfig.get_config_vars() is first
    called.  It may be used in environments where no
    compilers are present, i.e. when installing pure
    Python dists.  Customization of compiler paths
    and detection of unavailable archs is deferred
    until the first extension module build is
    requested (in distutils.sysconfig.customize_compiler).

    Currently called from distutils.sysconfig
    '''
    if not _supports_universal_builds():
        _remove_universal_flags(_config_vars)
    _override_all_archs(_config_vars)
    _check_for_unavailable_sdk(_config_vars)
    return _config_vars


def customize_compiler(_config_vars):
    '''Customize compiler path and configuration variables.

    This customization is performed when the first
    extension module build is requested
    in distutils.sysconfig.customize_compiler.
    '''
    _find_appropriate_compiler(_config_vars)
    _remove_unsupported_archs(_config_vars)
    _override_all_archs(_config_vars)
    return _config_vars


def get_platform_osx(_config_vars, osname, release, machine):
    '''Filter values for get_platform()'''
    macver = _config_vars.get('MACOSX_DEPLOYMENT_TARGET', '')
    if not _get_system_version():
        pass
    macrelease = macver
    if not macver:
        pass
    macver = macrelease
# WARNING: Decompyle incomplete

