
'''
.. testsetup::

    from packaging.version import parse, Version
'''
from __future__ import annotations
import itertools
import re
from typing import Any, Callable, NamedTuple, SupportsInt, Tuple, Union
from _structures import Infinity, InfinityType, NegativeInfinity, NegativeInfinityType
__all__ = [
    'VERSION_PATTERN',
    'InvalidVersion',
    'Version',
    'parse']
LocalType = Tuple[(Union[(int, str)], ...)]
CmpPrePostDevType = Union[(InfinityType, NegativeInfinityType, Tuple[(str, int)])]
CmpLocalType = Union[(NegativeInfinityType, Tuple[(Union[(Tuple[(int, str)], Tuple[(NegativeInfinityType, Union[(int, str)])])], ...)])]
CmpKey = Tuple[(int, Tuple[(int, ...)], CmpPrePostDevType, CmpPrePostDevType, CmpPrePostDevType, CmpLocalType)]
VersionComparisonMethod = Callable[([
    CmpKey,
    CmpKey], bool)]

class _Version(NamedTuple):
    local: 'LocalType | None' = '_Version'


def parse(version = None):
    """Parse the given version string.

    >>> parse('1.0.dev1')
    <Version('1.0.dev1')>

    :param version: The version string to parse.
    :raises InvalidVersion: When the version string is not a valid version.
    """
    return Version(version)


class InvalidVersion(ValueError):
    '''Raised when a version string is not a valid version.

    >>> Version("invalid")
    Traceback (most recent call last):
        ...
    packaging.version.InvalidVersion: Invalid version: \'invalid\'
    '''
    pass


class _BaseVersion:
    _key: 'tuple[Any, ...]' = '_BaseVersion'
    
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


_VERSION_PATTERN = '\n    v?\n    (?:\n        (?:(?P<epoch>[0-9]+)!)?                           # epoch\n        (?P<release>[0-9]+(?:\\.[0-9]+)*)                  # release segment\n        (?P<pre>                                          # pre-release\n            [-_\\.]?\n            (?P<pre_l>alpha|a|beta|b|preview|pre|c|rc)\n            [-_\\.]?\n            (?P<pre_n>[0-9]+)?\n        )?\n        (?P<post>                                         # post release\n            (?:-(?P<post_n1>[0-9]+))\n            |\n            (?:\n                [-_\\.]?\n                (?P<post_l>post|rev|r)\n                [-_\\.]?\n                (?P<post_n2>[0-9]+)?\n            )\n        )?\n        (?P<dev>                                          # dev release\n            [-_\\.]?\n            (?P<dev_l>dev)\n            [-_\\.]?\n            (?P<dev_n>[0-9]+)?\n        )?\n    )\n    (?:\\+(?P<local>[a-z0-9]+(?:[-_\\.][a-z0-9]+)*))?       # local version\n'
VERSION_PATTERN = _VERSION_PATTERN

class Version(_BaseVersion):
    '''This class abstracts handling of a project\'s versions.

    A :class:`Version` instance is comparison aware and can be compared and
    sorted using the standard Python interfaces.

    >>> v1 = Version("1.0a5")
    >>> v2 = Version("1.0")
    >>> v1
    <Version(\'1.0a5\')>
    >>> v2
    <Version(\'1.0\')>
    >>> v1 < v2
    True
    >>> v1 == v2
    False
    >>> v1 > v2
    False
    >>> v1 >= v2
    False
    >>> v1 <= v2
    True
    '''
    _key: 'CmpKey' = re.compile('^\\s*' + VERSION_PATTERN + '\\s*$', re.VERBOSE | re.IGNORECASE)
    
    def __init__(self = None, version = None):
        '''Initialize a Version object.

        :param version:
            The string representation of a version which will be parsed and normalized
            before use.
        :raises InvalidVersion:
            If the ``version`` does not conform to PEP 440 in any way then this
            exception will be raised.
        '''
        match = self._regex.search(version)
        if not match:
            raise InvalidVersion(f'''Invalid version: {version!r}''')
        if not match.group('post_n1'):
            pass
        self._version = None(int(match.group('epoch')) if match.group('epoch') else 0, tuple((lambda .0: for i in .0:
int(i))(match.group('release').split('.'))), _parse_letter_version(match.group('pre_l'), match.group('pre_n')), _parse_letter_version(match.group('post_l'), match.group('post_n2')), _parse_letter_version(match.group('dev_l'), match.group('dev_n')), _parse_local_version(match.group('local')), **('epoch', 'release', 'pre', 'post', 'dev', 'local'))
        self._key = _cmpkey(self._version.epoch, self._version.release, self._version.pre, self._version.post, self._version.dev, self._version.local)

    
    def __repr__(self = None):
        """A representation of the Version that shows all internal state.

        >>> Version('1.0.0')
        <Version('1.0.0')>
        """
        return f'''<Version(\'{self}\')>'''

    
    def __str__(self = None):
        '''A string representation of the version that can be round-tripped.

        >>> str(Version("1.0a5"))
        \'1.0a5\'
        '''
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
        '''The epoch of the version.

        >>> Version("2.0.0").epoch
        0
        >>> Version("1!2.0.0").epoch
        1
        '''
        return self._version.epoch

    epoch = None(epoch)
    
    def release(self = None):
        '''The components of the "release" segment of the version.

        >>> Version("1.2.3").release
        (1, 2, 3)
        >>> Version("2.0.0").release
        (2, 0, 0)
        >>> Version("1!2.0.0.post0").release
        (2, 0, 0)

        Includes trailing zeroes but not the epoch or any pre-release / development /
        post-release suffixes.
        '''
        return self._version.release

    release = None(release)
    
    def pre(self = None):
        '''The pre-release segment of the version.

        >>> print(Version("1.2.3").pre)
        None
        >>> Version("1.2.3a1").pre
        (\'a\', 1)
        >>> Version("1.2.3b1").pre
        (\'b\', 1)
        >>> Version("1.2.3rc1").pre
        (\'rc\', 1)
        '''
        return self._version.pre

    pre = None(pre)
    
    def post(self = None):
        '''The post-release number of the version.

        >>> print(Version("1.2.3").post)
        None
        >>> Version("1.2.3.post1").post
        1
        '''
        if self._version.post:
            return self._version.post[1]

    post = None(post)
    
    def dev(self = None):
        '''The development number of the version.

        >>> print(Version("1.2.3").dev)
        None
        >>> Version("1.2.3.dev1").dev
        1
        '''
        if self._version.dev:
            return self._version.dev[1]

    dev = None(dev)
    
    def local(self = None):
        '''The local version segment of the version.

        >>> print(Version("1.2.3").local)
        None
        >>> Version("1.2.3+abc").local
        \'abc\'
        '''
        if self._version.local:
            return '.'.join((lambda .0: for x in .0:
str(x))(self._version.local))

    local = None(local)
    
    def public(self = None):
        '''The public portion of the version.

        >>> Version("1.2.3").public
        \'1.2.3\'
        >>> Version("1.2.3+abc").public
        \'1.2.3\'
        >>> Version("1!1.2.3dev1+abc").public
        \'1!1.2.3.dev1\'
        '''
        return str(self).split('+', 1)[0]

    public = None(public)
    
    def base_version(self = None):
        '''The "base version" of the version.

        >>> Version("1.2.3").base_version
        \'1.2.3\'
        >>> Version("1.2.3+abc").base_version
        \'1.2.3\'
        >>> Version("1!1.2.3dev1+abc").base_version
        \'1!1.2.3\'

        The "base version" is the public version of the project without any pre or post
        release markers.
        '''
        parts = []
        if self.epoch != 0:
            parts.append(f'''{self.epoch}!''')
        parts.append('.'.join((lambda .0: for x in .0:
str(x))(self.release)))
        return ''.join(parts)

    base_version = None(base_version)
    
    def is_prerelease(self = None):
        '''Whether this version is a pre-release.

        >>> Version("1.2.3").is_prerelease
        False
        >>> Version("1.2.3a1").is_prerelease
        True
        >>> Version("1.2.3b1").is_prerelease
        True
        >>> Version("1.2.3rc1").is_prerelease
        True
        >>> Version("1.2.3dev1").is_prerelease
        True
        '''
        if not self.dev is not None:
            pass
        return self.pre is not None

    is_prerelease = None(is_prerelease)
    
    def is_postrelease(self = None):
        '''Whether this version is a post-release.

        >>> Version("1.2.3").is_postrelease
        False
        >>> Version("1.2.3.post1").is_postrelease
        True
        '''
        return self.post is not None

    is_postrelease = None(is_postrelease)
    
    def is_devrelease(self = None):
        '''Whether this version is a development release.

        >>> Version("1.2.3").is_devrelease
        False
        >>> Version("1.2.3.dev1").is_devrelease
        True
        '''
        return self.dev is not None

    is_devrelease = None(is_devrelease)
    
    def major(self = None):
        '''The first item of :attr:`release` or ``0`` if unavailable.

        >>> Version("1.2.3").major
        1
        '''
        if len(self.release) >= 1:
            return self.release[0]

    major = None(major)
    
    def minor(self = None):
        '''The second item of :attr:`release` or ``0`` if unavailable.

        >>> Version("1.2.3").minor
        2
        >>> Version("1").minor
        0
        '''
        if len(self.release) >= 2:
            return self.release[1]

    minor = None(minor)
    
    def micro(self = None):
        '''The third item of :attr:`release` or ``0`` if unavailable.

        >>> Version("1.2.3").micro
        3
        >>> Version("1").micro
        0
        '''
        if len(self.release) >= 3:
            return self.release[2]

    micro = None(micro)


class _TrimmedRelease(Version):
    
    def release(self = None):
        """
        Release segment without any trailing zeros.

        >>> _TrimmedRelease('1.0.0').release
        (1,)
        >>> _TrimmedRelease('0.0').release
        (0,)
        """
        rel = super().release
        nonzeros = (lambda .0: for index, val in .0:
if val:
indexcontinueNone)(enumerate(rel))
        last_nonzero = max(nonzeros, 0, **('default',))
        return rel[:last_nonzero + 1]

    release = None(release)
    __classcell__ = None


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
# WARNING: Decompyle incomplete

_local_version_separators = re.compile('[\\._-]')

def _parse_local_version(local = None):
    '''
    Takes a string like abc.1.twelve and turns it into ("abc", 1, "twelve").
    '''
    if local is not None:
        return tuple((lambda .0: for part in .0:
part.lower() if not part.isdigit() else int(part))(_local_version_separators.split(local)))


def _cmpkey(epoch, release, pre = None, post = None, dev = None, local = ('epoch', 'int', 'release', 'tuple[int, ...]', 'pre', 'tuple[str, int] | None', 'post', 'tuple[str, int] | None', 'dev', 'tuple[str, int] | None', 'local', 'LocalType | None', 'return', 'CmpKey')):
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

