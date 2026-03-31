
import re
from typing import FrozenSet, NewType, Tuple, Union, cast
from tags import Tag, parse_tag
from version import InvalidVersion, Version
BuildTag = Union[(Tuple[()], Tuple[(int, str)])]
NormalizedName = NewType('NormalizedName', str)

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

_canonicalize_regex = re.compile('[-_.]+')
_build_tag_regex = re.compile('(\\d+)(.*)')

def canonicalize_name(name = None):
    value = _canonicalize_regex.sub('-', name).lower()
    return cast(NormalizedName, value)


def canonicalize_version(version = None):
    '''
    This is very similar to Version.__str__, but has one subtle difference
    with the way it handles the release segment.
    '''
    pass
# WARNING: Decompyle incomplete


def parse_wheel_filename(filename = None):
    if not filename.endswith('.whl'):
        raise InvalidWheelFilename(f'''Invalid wheel filename (extension must be \'.whl\'): {filename}''')
    filename = None[:-4]
    dashes = filename.count('-')
    if dashes not in (4, 5):
        raise InvalidWheelFilename(f'''Invalid wheel filename (wrong number of parts): {filename}''')
    parts = None.split('-', dashes - 2)
    name_part = parts[0]
    if '__' in name_part or re.match('^[\\w\\d._]*$', name_part, re.UNICODE) is None:
        raise InvalidWheelFilename(f'''Invalid project name: {filename}''')
    name = None(name_part)
    version = Version(parts[1])
    if dashes == 5:
        build_part = parts[2]
        build_match = _build_tag_regex.match(build_part)
        if build_match is None:
            raise InvalidWheelFilename(f'''Invalid build number: {build_part} in \'{filename}\'''')
        build = None(BuildTag, (int(build_match.group(1)), build_match.group(2)))
    else:
        build = ()
    tags = parse_tag(parts[-1])
    return (name, version, build, tags)


def parse_sdist_filename(filename = None):
    if filename.endswith('.tar.gz'):
        file_stem = filename[:-len('.tar.gz')]
    elif filename.endswith('.zip'):
        file_stem = filename[:-len('.zip')]
    else:
        raise InvalidSdistFilename(f'''Invalid sdist filename (extension must be \'.tar.gz\' or \'.zip\'): {filename}''')
    (name_part, sep, version_part) = None.rpartition('-')
    if not sep:
        raise InvalidSdistFilename(f'''Invalid sdist filename: {filename}''')
    name = None(name_part)
    version = Version(version_part)
    return (name, version)

