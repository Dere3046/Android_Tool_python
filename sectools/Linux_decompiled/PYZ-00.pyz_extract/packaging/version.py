
import collections
import itertools
import re
import warnings
from typing import Callable, Iterator, List, Optional, SupportsInt, Tuple, Union
from _structures import Infinity, InfinityType, NegativeInfinity, NegativeInfinityType
__all__ = [
    'parse',
    'Version',
    'LegacyVersion',
    'InvalidVersion',
    'VERSION_PATTERN']
InfiniteTypes = Union[(InfinityType, NegativeInfinityType)]
PrePostDevType = Union[(InfiniteTypes, Tuple[(str, int)])]
SubLocalType = Union[(InfiniteTypes, int, str)]
LocalType = Union[(NegativeInfinityType, Tuple[(Union[(SubLocalType, Tuple[(SubLocalType, str)], Tuple[(NegativeInfinityType, SubLocalType)])], ...)])]
CmpKey = Tuple[(int, Tuple[(int, ...)], PrePostDevType, PrePostDevType, PrePostDevType, LocalType)]
LegacyCmpKey = Tuple[(int, Tuple[(str, ...)])]
VersionComparisonMethod = Callable[([
    Union[(CmpKey, LegacyCmpKey)],
    Union[(CmpKey, LegacyCmpKey)]], bool)]
_Version = collections.namedtuple('_Version', [
    'epoch',
    'release',
    'dev',
    'pre',
    'post',
    'local'])

def parse(version = None):
    '''
    Parse the given version string and return either a :class:`Version` object
    or a :class:`LegacyVersion` object depending on if the given version is
    a valid PEP 440 version or a legacy version.
    '''
    pass
# WARNING: Decompyle incomplete


class InvalidVersion(ValueError):
    '''
    An invalid version was found, users should refer to PEP 440.
    '''
    pass


class _BaseVersion:
    _key: Union[(CmpKey, LegacyCmpKey)] = '_BaseVersion'
    
    def __hash__(self = None):
        return hash(self._key)

    
    def __lt__(self = None, other = None):
        if not isinstance(other, _BaseVersion):
            return NotImplemented
        return None._key < other._key

    
    def __le__(self = None, other = None):
        if not isinstance(other, _BaseVersion):
            return NotImplemented
        return None._key <= other._key

    
    def __eq__(self = None, other = None):
        if not isinstance(other, _BaseVersion):
            return NotImplemented
        return None._key == other._key

    
    def __ge__(self = None, other = None):
        if not isinstance(other, _BaseVersion):
            return NotImplemented
        return None._key >= other._key

    
    def __gt__(self = None, other = None):
        if not isinstance(other, _BaseVersion):
            return NotImplemented
        return None._key > other._key

    
    def __ne__(self = None, other = None):
        if not isinstance(other, _BaseVersion):
            return NotImplemented
        return None._key != other._key



class LegacyVersion(_BaseVersion):
    
    def __init__(self = None, version = None):
        self._version = str(version)
        self._key = _legacy_cmpkey(self._version)
        warnings.warn('Creating a LegacyVersion has been deprecated and will be removed in the next major release', DeprecationWarning)

    
    def __str__(self = None):
        return self._version

    
    def __repr__(self = None):
        return f'''<LegacyVersion(\'{self}\')>'''

    
    def public(self = None):
        return self._version

    public = None(public)
    
    def base_version(self = None):
        return self._version

    base_version = None(base_version)
    
    def epoch(self = None):
        return -1

    epoch = None(epoch)
    
    def release(self = None):
        pass

    release = None(release)
    
    def pre(self = None):
        pass

    pre = None(pre)
    
    def post(self = None):
        pass

    post = None(post)
    
    def dev(self = None):
        pass

    dev = None(dev)
    
    def local(self = None):
        pass

    local = None(local)
    
    def is_prerelease(self = None):
        return False

    is_prerelease = None(is_prerelease)
    
    def is_postrelease(self = None):
        return False

    is_postrelease = None(is_postrelease)
    
    def is_devrelease(self = None):
        return False

    is_devrelease = None(is_devrelease)

_legacy_version_component_re = re.compile('(\\d+ | [a-z]+ | \\.| -)', re.VERBOSE)
_legacy_version_replacement_map = {
    'pre': 'c',
    'preview': 'c',
    '-': 'final-',
    'rc': 'c',
    'dev': '@' }

def _parse_version_parts(s = None):
    for part in _legacy_version_component_re.split(s):
        part = _legacy_version_replacement_map.get(part, part)
        if part or part == '.':
            continue
        if part[:1] in '0123456789':
            yield part.zfill(8)
            continue
        yield '*' + part
    yield '*final'


def _legacy_cmpkey(version = None):
    epoch = -1
    parts = []
    for part in _parse_version_parts(version.lower()):
        if part.startswith('*'):
            if part < '*final' and parts and parts[-1] == '*final-':
                parts.pop()
                if parts:
                    if (parts[-1] == '*final-' or parts) and parts[-1] == '00000000':
                        parts.pop()
                        if parts:
                            if not parts[-1] == '00000000':
                                parts.append(part)
                                continue
                                return (epoch, tuple(parts))

VERSION_PATTERN = '\n    v?\n    (?:\n        (?:(?P<epoch>[0-9]+)!)?                           # epoch\n        (?P<release>[0-9]+(?:\\.[0-9]+)*)                  # release segment\n        (?P<pre>                                          # pre-release\n            [-_\\.]?\n            (?P<pre_l>(a|b|c|rc|alpha|beta|pre|preview))\n            [-_\\.]?\n            (?P<pre_n>[0-9]+)?\n        )?\n        (?P<post>                                         # post release\n            (?:-(?P<post_n1>[0-9]+))\n            |\n            (?:\n                [-_\\.]?\n                (?P<post_l>post|rev|r)\n                [-_\\.]?\n                (?P<post_n2>[0-9]+)?\n            )\n        )?\n        (?P<dev>                                          # dev release\n            [-_\\.]?\n            (?P<dev_l>dev)\n            [-_\\.]?\n            (?P<dev_n>[0-9]+)?\n        )?\n    )\n    (?:\\+(?P<local>[a-z0-9]+(?:[-_\\.][a-z0-9]+)*))?       # local version\n'

class Version(_BaseVersion):
    _regex = re.compile('^\\s*' + VERSION_PATTERN + '\\s*$', re.VERBOSE | re.IGNORECASE)
    
    def __init__(self = None, version = None):
        match = self._regex.search(version)
        if not match:
            raise InvalidVersion(f'''Invalid version: \'{version}\'''')
        if not match.group('post_n1'):
            pass
        self._version = None(int(match.group('epoch')) if match.group('epoch') else 0, tuple((lambda .0: for i in .0:
int(i))(match.group('release').split('.'))), _parse_letter_version(match.group('pre_l'), match.group('pre_n')), _parse_letter_version(match.group('post_l'), match.group('post_n2')), _parse_letter_version(match.group('dev_l'), match.group('dev_n')), _parse_local_version(match.group('local')), **('epoch', 'release', 'pre', 'post', 'dev', 'local'))
        self._key = _cmpkey(self._version.epoch, self._version.release, self._version.pre, self._version.post, self._version.dev, self._version.local)

    
    def __repr__(self = None):
        return f'''<Version(\'{self}\')>'''

    
    def __str__(self = None):
        parts = []
        if self.epoch != 0:
            parts.append(f'''{self.epoch}!''')
        parts.append('.'.join((lambda .0: for x in .0:
str(x))(self.release)))
        if self.pre is not None:
            parts.append(''.join((lambda .0: for x in .0:
str(x))(self.pre)))
        if self.post is not None:
            parts.append(f'''.post{self.post}''')
        if self.dev is not None:
            parts.append(f'''.dev{self.dev}''')
        if self.local is not None:
            parts.append(f'''+{self.local}''')
        return ''.join(parts)

    
    def epoch(self = None):
        _epoch = self._version.epoch
        return _epoch

    epoch = None(epoch)
    
    def release(self = None):
        _release = self._version.release
        return _release

    release = None(release)
    
    def pre(self = None):
        _pre = self._version.pre
        return _pre

    pre = None(pre)
    
    def post(self = None):
        if self._version.post:
            return self._version.post[1]

    post = None(post)
    
    def dev(self = None):
        if self._version.dev:
            return self._version.dev[1]

    dev = None(dev)
    
    def local(self = None):
        if self._version.local:
            return '.'.join((lambda .0: for x in .0:
str(x))(self._version.local))

    local = None(local)
    
    def public(self = None):
        return str(self).split('+', 1)[0]

    public = None(public)
    
    def base_version(self = None):
        parts = []
        if self.epoch != 0:
            parts.append(f'''{self.epoch}!''')
        parts.append('.'.join((lambda .0: for x in .0:
str(x))(self.release)))
        return ''.join(parts)

    base_version = None(base_version)
    
    def is_prerelease(self = None):
        if not self.dev is not None:
            pass
        return self.pre is not None

    is_prerelease = None(is_prerelease)
    
    def is_postrelease(self = None):
        return self.post is not None

    is_postrelease = None(is_postrelease)
    
    def is_devrelease(self = None):
        return self.dev is not None

    is_devrelease = None(is_devrelease)
    
    def major(self = None):
        if len(self.release) >= 1:
            return self.release[0]

    major = None(major)
    
    def minor(self = None):
        if len(self.release) >= 2:
            return self.release[1]

    minor = None(minor)
    
    def micro(self = None):
        if len(self.release) >= 3:
            return self.release[2]

    micro = None(micro)


def _parse_letter_version(letter = None, number = None):
    if letter:
        if number is None:
            number = 0
        letter = letter.lower()
        if letter == 'alpha':
            letter = 'a'
        elif letter == 'beta':
            letter = 'b'
        elif letter in ('c', 'pre', 'preview'):
            letter = 'rc'
        elif letter in ('rev', 'r'):
            letter = 'post'
        return (letter, int(number))
    if None and number:
        letter = 'post'
        return (letter, int(number))

_local_version_separators = re.compile('[\\._-]')

def _parse_local_version(local = None):
    '''
    Takes a string like abc.1.twelve and turns it into ("abc", 1, "twelve").
    '''
    if local is not None:
        return tuple((lambda .0: for part in .0:
part.lower() if not part.isdigit() else int(part))(_local_version_separators.split(local)))


def _cmpkey(epoch, release, pre = None, post = None, dev = None, local = ('epoch', int, 'release', Tuple[(int, ...)], 'pre', Optional[Tuple[(str, int)]], 'post', Optional[Tuple[(str, int)]], 'dev', Optional[Tuple[(str, int)]], 'local', Optional[Tuple[SubLocalType]], 'return', CmpKey)):
    _release = tuple(reversed(list(itertools.dropwhile((lambda x: x == 0), reversed(release)))))
    if pre is None and post is None and dev is not None:
        _pre = NegativeInfinity
    elif pre is None:
        _pre = Infinity
    else:
        _pre = pre
    if post is None:
        _post = NegativeInfinity
    else:
        _post = post
    if dev is None:
        _dev = Infinity
    else:
        _dev = dev
    if local is None:
        _local = NegativeInfinity
    else:
        _local = tuple((lambda .0: for i in .0:
(i, '') if isinstance(i, int) else (NegativeInfinity, i))(local))
    return (epoch, _release, _pre, _post, _dev, _local)

