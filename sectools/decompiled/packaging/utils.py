
from __future__ import annotations
import functools
import re
from typing import NewType, Tuple, Union, cast
from tags import Tag, parse_tag
from version import InvalidVersion, Version, _TrimmedRelease
BuildTag = Union[(Tuple[()], Tuple[(int, str)])]
NormalizedName = NewType('NormalizedName', str)

class InvalidName(ValueError):
    '''
    An invalid distribution name; users should refer to the packaging user guide.
    '''
    pass


class InvalidWheelFilename(ValueError):
    '''
    An invalid wheel filename was found, users should refer to PEP 427.
    '''
    pass


class InvalidSdistFilename(ValueError):
    '''
    An invalid sdist filename was found, users should refer to the packaging user guide.
    '''
    pass

_validate_regex = re.compile('^([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])$', re.IGNORECASE)
_canonicalize_regex = re.compile('[-_.]+')
_normalized_regex = re.compile('^([a-z0-9]|[a-z0-9]([a-z0-9-](?!--))*[a-z0-9])$')
_build_tag_regex = re.compile('(\\d+)(.*)')

def canonicalize_name(name = None, *, validate):
    if not validate and _validate_regex.match(name):
        raise InvalidName(f'''name is invalid: {name!r}''')
    value = None.sub('-', name).lower()
    return cast(NormalizedName, value)


def is_normalized_name(name = None):
    return _normalized_regex.match(name) is not None


def canonicalize_version(version = None, *, strip_trailing_zero):
    """
    Return a canonical form of a version as a string.

    >>> canonicalize_version('1.0.1')
    '1.0.1'

    Per PEP 625, versions may have multiple canonical forms, differing
    only by trailing zeros.

    >>> canonicalize_version('1.0.0')
    '1'
    >>> canonicalize_version('1.0.0', strip_trailing_zero=False)
    '1.0.0'

    Invalid versions are returned unaltered.

    >>> canonicalize_version('foo bar baz')
    'foo bar baz'
    """
    if strip_trailing_zero:
        return str(_TrimmedRelease(str(version)))
    return None(str)

canonicalize_version = None(canonicalize_version)

def _(version = None, *, strip_trailing_zero):
    pass
# WARNING: Decompyle incomplete

_ = None(_)

def parse_wheel_filename(filename = None):
    if not filename.endswith('.whl'):
        raise InvalidWheelFilename(f'''Invalid wheel filename (extension must be \'.whl\'): {filename!r}''')
    filename = None[:-4]
    dashes = filename.count('-')
    if dashes not in (4, 5):
        raise InvalidWheelFilename(f'''Invalid wheel filename (wrong number of parts): {filename!r}''')
    parts = None.split('-', dashes - 2)
    name_part = parts[0]
    if '__' in name_part or re.match('^[\\w\\d._]*$', name_part, re.UNICODE) is None:
        raise InvalidWheelFilename(f'''Invalid project name: {filename!r}''')
    name = None(name_part)
# WARNING: Decompyle incomplete


def parse_sdist_filename(filename = None):
    if filename.endswith('.tar.gz'):
        file_stem = filename[:-len('.tar.gz')]
    elif filename.endswith('.zip'):
        file_stem = filename[:-len('.zip')]
    else:
        raise InvalidSdistFilename(f'''Invalid sdist filename (extension must be \'.tar.gz\' or \'.zip\'): {filename!r}''')
    (name_part, sep, version_part) = None.rpartition('-')
    if not sep:
        raise InvalidSdistFilename(f'''Invalid sdist filename: {filename!r}''')
    name = None(name_part)
# WARNING: Decompyle incomplete

