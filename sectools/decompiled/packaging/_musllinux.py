
__doc__ = 'PEP 656 support.\n\nThis module implements logic to detect if the currently running Python is\nlinked against musl, and what musl version is used.\n'
from __future__ import annotations
import functools
import re
import subprocess
import sys
from typing import Iterator, NamedTuple, Sequence
from _elffile import ELFFile

class _MuslVersion(NamedTuple):
    minor: 'int' = '_MuslVersion'


def _parse_musl_version(output = None):
    lines = (lambda .0: [ n for n in .0 if n ])((lambda .0: for n in .0:
n.strip())(output.splitlines()))
    if len(lines) < 2 or lines[0][:4] != 'musl':
        return None
    m = None.match('Version (\\d+)\\.(\\d+)', lines[1])
    if not m:
        return None
    return None(int(m.group(1)), int(m.group(2)), **('major', 'minor'))


def _get_musl_version(executable = None):
    """Detect currently-running musl runtime version.

    This is done by checking the specified executable's dynamic linking
    information, and invoking the loader to parse its output for a version
    string. If the loader is musl, the output would be something like::

        musl libc (x86_64)
        Version 1.2.2
        Dynamic Program Loader
    """
    pass
# WARNING: Decompyle incomplete

_get_musl_version = None(_get_musl_version)

def platform_tags(archs = None):
    '''Generate musllinux tags compatible to the current platform.

    :param archs: Sequence of compatible architectures.
        The first one shall be the closest to the actual architecture and be the part of
        platform tag after the ``linux_`` prefix, e.g. ``x86_64``.
        The ``linux_`` prefix is assumed as a prerequisite for the current platform to
        be musllinux-compatible.

    :returns: An iterator of compatible musllinux tags.
    '''
    sys_musl = _get_musl_version(sys.executable)
    if sys_musl is None:
        return None
    for arch in None:
        for minor in range(sys_musl.minor, -1, -1):
            yield f'''musllinux_{sys_musl.major}_{minor}_{arch}'''

# WARNING: Decompyle incomplete
