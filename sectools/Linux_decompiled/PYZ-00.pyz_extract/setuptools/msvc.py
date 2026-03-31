
__doc__ = '\nImproved support for Microsoft Visual C++ compilers.\n\nKnown supported compilers:\n--------------------------\nMicrosoft Visual C++ 9.0:\n    Microsoft Visual C++ Compiler for Python 2.7 (x86, amd64)\n    Microsoft Windows SDK 6.1 (x86, x64, ia64)\n    Microsoft Windows SDK 7.0 (x86, x64, ia64)\n\nMicrosoft Visual C++ 10.0:\n    Microsoft Windows SDK 7.1 (x86, x64, ia64)\n\nMicrosoft Visual C++ 14.X:\n    Microsoft Visual C++ Build Tools 2015 (x86, x64, arm)\n    Microsoft Visual Studio Build Tools 2017 (x86, x64, arm, arm64)\n    Microsoft Visual Studio Build Tools 2019 (x86, x64, arm, arm64)\n\nThis may also support compilers shipped with compatible Visual Studio versions.\n'
import json
from io import open
from os import listdir, pathsep
from os.path import join, isfile, isdir, dirname
import sys
import contextlib
import platform
import itertools
import subprocess
import distutils.errors as distutils
from setuptools.extern.packaging.version import LegacyVersion
from setuptools.extern.more_itertools import unique_everseen
from monkey import get_unpatched
if platform.system() == 'Windows':
    import winreg
    from os import environ
else:
    
    class winreg:
        HKEY_USERS = None
        HKEY_CURRENT_USER = None
        HKEY_LOCAL_MACHINE = None
        HKEY_CLASSES_ROOT = None

    environ = dict()
_msvc9_suppress_errors = (ImportError, distutils.errors.DistutilsPlatformError)
# WARNING: Decompyle incomplete
