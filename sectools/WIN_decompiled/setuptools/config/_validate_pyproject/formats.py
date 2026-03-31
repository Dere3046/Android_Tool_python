
import logging
import os
import re
import string
import typing
from itertools import chain as _chain
_logger = logging.getLogger(__name__)
VERSION_PATTERN = '\n    v?\n    (?:\n        (?:(?P<epoch>[0-9]+)!)?                           # epoch\n        (?P<release>[0-9]+(?:\\.[0-9]+)*)                  # release segment\n        (?P<pre>                                          # pre-release\n            [-_\\.]?\n            (?P<pre_l>(a|b|c|rc|alpha|beta|pre|preview))\n            [-_\\.]?\n            (?P<pre_n>[0-9]+)?\n        )?\n        (?P<post>                                         # post release\n            (?:-(?P<post_n1>[0-9]+))\n            |\n            (?:\n                [-_\\.]?\n                (?P<post_l>post|rev|r)\n                [-_\\.]?\n                (?P<post_n2>[0-9]+)?\n            )\n        )?\n        (?P<dev>                                          # dev release\n            [-_\\.]?\n            (?P<dev_l>dev)\n            [-_\\.]?\n            (?P<dev_n>[0-9]+)?\n        )?\n    )\n    (?:\\+(?P<local>[a-z0-9]+(?:[-_\\.][a-z0-9]+)*))?       # local version\n'
VERSION_REGEX = re.compile('^\\s*' + VERSION_PATTERN + '\\s*$', re.X | re.I)

def pep440(version = None):
    return VERSION_REGEX.match(version) is not None

PEP508_IDENTIFIER_PATTERN = '([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])'
PEP508_IDENTIFIER_REGEX = re.compile(f'''^{PEP508_IDENTIFIER_PATTERN}$''', re.I)

def pep508_identifier(name = None):
    return PEP508_IDENTIFIER_REGEX.match(name) is not None

# WARNING: Decompyle incomplete
