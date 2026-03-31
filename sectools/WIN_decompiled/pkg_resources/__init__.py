
__doc__ = '\nPackage resource API\n--------------------\n\nA resource is a logical file contained within a package, or a logical\nsubdirectory thereof.  The package resource API expects resource names\nto have their path parts separated with ``/``, *not* whatever the local\npath separator is.  Do not use os.path operations to manipulate resource\nnames being passed into the API.\n\nThe package resource API is designed to work with normal filesystem packages,\n.egg files, and unpacked .egg files.  It can also work in a limited way with\n.zip files and with custom PEP 302 loaders that support the ``get_data()``\nmethod.\n'
import sys
import os
import io
import time
import re
import types
import zipfile
import zipimport
import warnings
import stat
import functools
import pkgutil
import operator
import platform
import collections
import plistlib
import email.parser as email
import errno
import tempfile
import textwrap
import itertools
import inspect
import ntpath
import posixpath
import importlib
from pkgutil import get_importer
# WARNING: Decompyle incomplete
