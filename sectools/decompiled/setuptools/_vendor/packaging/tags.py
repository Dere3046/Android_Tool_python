
import logging
import platform
import sys
import sysconfig
from importlib.machinery import EXTENSION_SUFFIXES
from typing import Dict, FrozenSet, Iterable, Iterator, List, Optional, Sequence, Tuple, Union, cast
from  import _manylinux, _musllinux
logger = logging.getLogger(__name__)
PythonVersion = Sequence[int]
MacVersion = Tuple[(int, int)]
INTERPRETER_SHORT_NAMES: Dict[(str, str)] = {
    'python': 'py',
    'cpython': 'cp',
    'pypy': 'pp',
    'ironpython': 'ip',
    'jython': 'jy' }
_32_BIT_INTERPRETER = sys.maxsize <= 0x100000000L

class Tag:
    '''
    A representation of the tag triple for a wheel.

    Instances are considered immutable and thus are hashable. Equality checking
    is also supported.
    '''
    __slots__ = [
        '_interpreter',
        '_abi',
        '_platform',
        '_hash']
    
    def __init__(self = None, interpreter = None, abi = None, platform = ('interpreter', str, 'abi', str, 'platform', str, 'return', None)):
        self._interpreter = interpreter.lower()
        self._abi = abi.lower()
        self._platform = platform.lower()
        self._hash = hash((self._interpreter, self._abi, self._platform))

    
    def interpreter(self = None):
        return self._interpreter

    interpreter = None(interpreter)
    
    def abi(self = None):
        return self._abi

    abi = None(abi)
    
    def platform(self = None):
        return self._platform

    platform = None(platform)
    
    def __eq__(self = None, other = None):
        if not isinstance(other, Tag):
            return NotImplemented
        if None._hash == other._hash and self._platform == other._platform and self._abi == other._abi:
            pass
        return self._interpreter == other._interpreter

    
    def __hash__(self = None):
        return self._hash

    
    def __str__(self = None):
        return f'''{self._interpreter}-{self._abi}-{self._platform}'''

    
    def __repr__(self = None):
        return f'''<{self} @ {id(self)}>'''



def parse_tag(tag = None):
    '''
    Parses the provided tag (e.g. `py3-none-any`) into a frozenset of Tag instances.

    Returning a set is required due to the possibility that the tag is a
    compressed tag set.
    '''
    tags = set()
    (interpreters, abis, platforms) = tag.split('-')
    for interpreter in interpreters.split('.'):
        for abi in abis.split('.'):
            for platform_ in platforms.split('.'):
                tags.add(Tag(interpreter, abi, platform_))
    return frozenset(tags)


def _get_config_var(name = None, warn = None):
    value = sysconfig.get_config_var(name)
    if value is None and warn:
        logger.debug("Config variable '%s' is unset, Python ABI tag may be incorrect", name)
    return value


def _normalize_string(string = None):
    return string.replace('.', '_').replace('-', '_')


def _abi3_applies(python_version = None):
    '''
    Determine if the Python version supports abi3.

    PEP 384 was first implemented in Python 3.2.
    '''
    if len(python_version) > 1:
        pass
    return tuple(python_version) >= (3, 2)


def _cpython_abis(py_version = None, warn = None):
    py_version = tuple(py_version)
    abis = []
    version = _version_nodot(py_version[:2])
    debug = pymalloc = ucs4 = ''
    with_debug = _get_config_var('Py_DEBUG', warn)
    has_refcount = hasattr(sys, 'gettotalrefcount')
    has_ext = '_d.pyd' in EXTENSION_SUFFIXES
    if with_debug or with_debug is None:
        if has_refcount or has_ext:
            debug = 'd'
    if py_version < (3, 8):
        with_pymalloc = _get_config_var('WITH_PYMALLOC', warn)
        if with_pymalloc or with_pymalloc is None:
            pymalloc = 'm'
        if py_version < (3, 3):
            unicode_size = _get_config_var('Py_UNICODE_SIZE', warn)
            if (unicode_size == 4 or unicode_size is None) and sys.maxunicode == 1114111:
                ucs4 = 'u'
            elif debug:
                abis.append(f'''cp{version}''')
    abis.insert(0, 'cp{version}{debug}{pymalloc}{ucs4}'.format(version, debug, pymalloc, ucs4, **('version', 'debug', 'pymalloc', 'ucs4')))
    return abis


def cpython_tags(python_version = None, abis = None, platforms = None, *, warn):
    """
    Yields the tags for a CPython interpreter.

    The tags consist of:
    - cp<python_version>-<abi>-<platform>
    - cp<python_version>-abi3-<platform>
    - cp<python_version>-none-<platform>
    - cp<less than python_version>-abi3-<platform>  # Older Python versions down to 3.2.

    If python_version only specifies a major version then user-provided ABIs and
    the 'none' ABItag will be used.

    If 'abi3' or 'none' are specified in 'abis' then they will be yielded at
    their normal position and not at the beginning.
    """
    if not python_version:
        python_version = sys.version_info[:2]
    interpreter = f'''cp{_version_nodot(python_version[:2])}'''
    if abis is None:
        if len(python_version) > 1:
            abis = _cpython_abis(python_version, warn)
        else:
            abis = []
    abis = list(abis)
# WARNING: Decompyle incomplete


def _generic_abi():
    abi = sysconfig.get_config_var('SOABI')
    if abi:
        yield _normalize_string(abi)
        return None


def generic_tags(interpreter = None, abis = None, platforms = None, *, warn):
    '''
    Yields the tags for a generic interpreter.

    The tags consist of:
    - <interpreter>-<abi>-<platform>

    The "none" ABI will be added if it was not explicitly provided.
    '''
    if not interpreter:
        interp_name = interpreter_name()
        interp_version = interpreter_version(warn, **('warn',))
        interpreter = ''.join([
            interp_name,
            interp_version])
    if abis is None:
        abis = _generic_abi()
    if not platforms:
        pass
    platforms = list(platform_tags())
    abis = list(abis)
    if 'none' not in abis:
        abis.append('none')
    for abi in abis:
        for platform_ in platforms:
            yield Tag(interpreter, abi, platform_)


def _py_interpreter_range(py_version = None):
    '''
    Yields Python versions in descending order.

    After the latest version, the major-only version will be yielded, and then
    all previous versions of that major version.
    '''
    if len(py_version) > 1:
        yield f'''py{_version_nodot(py_version[:2])}'''
    yield f'''py{py_version[0]}'''
    if len(py_version) > 1:
        for minor in range(py_version[1] - 1, -1, -1):
            yield f'''py{_version_nodot((py_version[0], minor))}'''
    return None


def compatible_tags(python_version = None, interpreter = None, platforms = None):
    '''
    Yields the sequence of tags that are compatible with a specific version of Python.

    The tags consist of:
    - py*-none-<platform>
    - <interpreter>-none-any  # ... if `interpreter` is provided.
    - py*-none-any
    '''
    if not python_version:
        python_version = sys.version_info[:2]
    if not platforms:
        pass
    platforms = list(platform_tags())
    for version in _py_interpreter_range(python_version):
        for platform_ in platforms:
            yield Tag(version, 'none', platform_)
    if interpreter:
        yield Tag(interpreter, 'none', 'any')
    for version in _py_interpreter_range(python_version):
        yield Tag(version, 'none', 'any')


def _mac_arch(arch = None, is_32bit = None):
    if not is_32bit:
        return arch
    if None.startswith('ppc'):
        return 'ppc'


def _mac_binary_formats(version = None, cpu_arch = None):
    formats = [
        cpu_arch]
    if cpu_arch == 'x86_64':
        if version < (10, 4):
            return []
        None.extend([
            'intel',
            'fat64',
            'fat32'])
    elif cpu_arch == 'i386':
        if version < (10, 4):
            return []
        None.extend([
            'intel',
            'fat32',
            'fat'])
    elif cpu_arch == 'ppc64':
        if version > (10, 5) or version < (10, 4):
            return []
        None.append('fat64')
    elif cpu_arch == 'ppc':
        if version > (10, 6):
            return []
        None.extend([
            'fat32',
            'fat'])
    if cpu_arch in frozenset({'arm64', 'x86_64'}):
        formats.append('universal2')
    if cpu_arch in frozenset({'ppc', 'i386', 'intel', 'ppc64', 'x86_64'}):
        formats.append('universal')
    return formats


def mac_platforms(version = None, arch = None):
    '''
    Yields the platform tags for a macOS system.

    The `version` parameter is a two-item tuple specifying the macOS version to
    generate platform tags for. The `arch` parameter is the CPU architecture to
    generate platform tags for. Both parameters default to the appropriate value
    for the current system.
    '''
    (version_str, _, cpu_arch) = platform.mac_ver()
    if version is None:
        version = cast('MacVersion', tuple(map(int, version_str.split('.')[:2])))
    else:
        version = version
    if arch is None:
        arch = _mac_arch(cpu_arch)
    else:
        arch = arch
    if (10, 0) <= version and version < (11, 0):
        for minor_version in range(version[1], -1, -1):
            compat_version = (10, minor_version)
            binary_formats = _mac_binary_formats(compat_version, arch)
            for binary_format in binary_formats:
                yield 'macosx_{major}_{minor}_{binary_format}'.format(10, minor_version, binary_format, **('major', 'minor', 'binary_format'))
    if version >= (11, 0):
        for major_version in range(version[0], 10, -1):
            compat_version = (major_version, 0)
            binary_formats = _mac_binary_formats(compat_version, arch)
            for binary_format in binary_formats:
                yield 'macosx_{major}_{minor}_{binary_format}'.format(major_version, 0, binary_format, **('major', 'minor', 'binary_format'))
    if version >= (11, 0):
        if arch == 'x86_64':
            for minor_version in range(16, 3, -1):
                compat_version = (10, minor_version)
                binary_formats = _mac_binary_formats(compat_version, arch)
                for binary_format in binary_formats:
                    yield 'macosx_{major}_{minor}_{binary_format}'.format(compat_version[0], compat_version[1], binary_format, **('major', 'minor', 'binary_format'))
            return None
        for minor_version in None(16, 3, -1):
            compat_version = (10, minor_version)
            binary_format = 'universal2'
            yield 'macosx_{major}_{minor}_{binary_format}'.format(compat_version[0], compat_version[1], binary_format, **('major', 'minor', 'binary_format'))
    return None


def _linux_platforms(is_32bit = None):
    linux = _normalize_string(sysconfig.get_platform())
    if is_32bit:
        if linux == 'linux_x86_64':
            linux = 'linux_i686'
        elif linux == 'linux_aarch64':
            linux = 'linux_armv7l'
    (_, arch) = linux.split('_', 1)
    yield from _manylinux.platform_tags(linux, arch)
    yield from _musllinux.platform_tags(arch)
    yield linux


def _generic_platforms():
    yield _normalize_string(sysconfig.get_platform())


def platform_tags():
    '''
    Provides the platform tags for this installation.
    '''
    if platform.system() == 'Darwin':
        return mac_platforms()
    if None.system() == 'Linux':
        return _linux_platforms()
    return None()


def interpreter_name():
    '''
    Returns the name of the running interpreter.
    '''
    name = sys.implementation.name
    if not INTERPRETER_SHORT_NAMES.get(name):
        pass
    return name


def interpreter_version(*, warn):
    '''
    Returns the version of the running interpreter.
    '''
    version = _get_config_var('py_version_nodot', warn, **('warn',))
    if version:
        version = str(version)
        return version
    version = None(sys.version_info[:2])
    return version


def _version_nodot(version = None):
    return ''.join(map(str, version))


def sys_tags(*, warn):
    '''
    Returns the sequence of tag triples for the running interpreter.

    The order of the sequence corresponds to priority order for the
    interpreter, from most to least important.
    '''
    interp_name = interpreter_name()
    if interp_name == 'cp':
        yield from cpython_tags(warn, **('warn',))
    else:
        yield from generic_tags()
    if interp_name == 'pp':
        yield from compatible_tags('pp3', **('interpreter',))
        return None
    yield from None()

