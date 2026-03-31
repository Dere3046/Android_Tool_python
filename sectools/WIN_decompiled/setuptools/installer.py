
import glob
import os
import subprocess
import sys
import tempfile
import warnings
from distutils import log
from distutils.errors import DistutilsError
import pkg_resources
from setuptools.wheel import Wheel
from _deprecation_warning import SetuptoolsDeprecationWarning

def _fixup_find_links(find_links):
    '''Ensure find-links option end-up being a list of strings.'''
    if isinstance(find_links, str):
        return find_links.split()
# WARNING: Decompyle incomplete


def fetch_build_egg(dist, req):
    '''Fetch an egg needed for building.

    Use pip/wheel to fetch/build a wheel.'''
    warnings.warn('setuptools.installer is deprecated. Requirements should be satisfied by a PEP 517 installer.', SetuptoolsDeprecationWarning)
# WARNING: Decompyle incomplete


def strip_marker(req):
    '''
    Return a new requirement without the environment marker to avoid
    calling pip with something like `babel; extra == "i18n"`, which
    would always be ignored.
    '''
    req = pkg_resources.Requirement.parse(str(req))
    req.marker = None
    return req

