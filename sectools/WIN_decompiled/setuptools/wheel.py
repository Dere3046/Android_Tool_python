
'''Wheels support.'''
import email
import itertools
import os
import posixpath
import re
import zipfile
import contextlib
from distutils.util import get_platform
import pkg_resources
import setuptools
from pkg_resources import parse_version
from setuptools.extern.packaging.tags import sys_tags
from setuptools.extern.packaging.utils import canonicalize_name
from setuptools.command.egg_info import write_requirements
from setuptools.archive_util import _unpack_zipfile_obj
WHEEL_NAME = re.compile('^(?P<project_name>.+?)-(?P<version>\\d.*?)\n    ((-(?P<build>\\d.*?))?-(?P<py_version>.+?)-(?P<abi>.+?)-(?P<platform>.+?)\n    )\\.whl$', re.VERBOSE).match
NAMESPACE_PACKAGE_INIT = "__import__('pkg_resources').declare_namespace(__name__)\n"

def unpack(src_dir, dst_dir):
    '''Move everything under `src_dir` to `dst_dir`, and delete the former.'''
    for dirpath, dirnames, filenames in os.walk(src_dir):
        subdir = os.path.relpath(dirpath, src_dir)
        for f in filenames:
            src = os.path.join(dirpath, f)
            dst = os.path.join(dst_dir, subdir, f)
            os.renames(src, dst)
        for n, d in reversed(list(enumerate(dirnames))):
            src = os.path.join(dirpath, d)
            dst = os.path.join(dst_dir, subdir, d)
            if not os.path.exists(dst):
                os.renames(src, dst)
                del dirnames[n]
# WARNING: Decompyle incomplete


def disable_info_traces():
    '''
    Temporarily disable info traces.
    '''
    log = log
    import distutils
    saved = log.set_threshold(log.WARN)
# WARNING: Decompyle incomplete

disable_info_traces = contextlib.contextmanager(disable_info_traces)

class Wheel:
    
    def __init__(self, filename):
        match = WHEEL_NAME(os.path.basename(filename))
        if match is None:
            raise ValueError('invalid wheel name: %r' % filename)
        self.filename = None
        for k, v in match.groupdict().items():
            setattr(self, k, v)

    
    def tags(self):
        '''List tags (py_version, abi, platform) supported by this wheel.'''
        return itertools.product(self.py_version.split('.'), self.abi.split('.'), self.platform.split('.'))

    
    def is_compatible(self):
        '''Is the wheel is compatible with the current platform?'''
        supported_tags = set((lambda .0: for t in .0:
(t.interpreter, t.abi, t.platform))(sys_tags()))
        return None((lambda .0 = None: for t in .0:
if t in supported_tags:
TruecontinueNone)(self.tags()), False)

    
    def egg_name(self):
        return pkg_resources.Distribution(self.project_name, self.version, None if self.platform == 'any' else get_platform(), **('project_name', 'version', 'platform')).egg_name() + '.egg'

    
    def get_dist_info(self, zf):
        for member in zf.namelist():
            dirname = posixpath.dirname(member)
            if dirname.endswith('.dist-info') and canonicalize_name(dirname).startswith(canonicalize_name(self.project_name)):
                return dirname
            raise ValueError('unsupported wheel format. .dist-info not found')

    
    def install_as_egg(self, destination_eggdir):
        '''Install wheel as an egg directory.'''
        pass
    # WARNING: Decompyle incomplete

    
    def _install_as_egg(self, destination_eggdir, zf):
        dist_basename = '%s-%s' % (self.project_name, self.version)
        dist_info = self.get_dist_info(zf)
        dist_data = '%s.data' % dist_basename
        egg_info = os.path.join(destination_eggdir, 'EGG-INFO')
        self._convert_metadata(zf, destination_eggdir, dist_info, egg_info)
        self._move_data_entries(destination_eggdir, dist_data)
        self._fix_namespace_packages(egg_info, destination_eggdir)

    
    def _convert_metadata(zf, destination_eggdir, dist_info, egg_info):
        
        def get_metadata(name = None):
            pass
        # WARNING: Decompyle incomplete

        wheel_metadata = get_metadata('WHEEL')
        wheel_version = parse_version(wheel_metadata.get('Wheel-Version'))
        wheel_v1 = None if wheel_version <= wheel_version else wheel_version < parse_version('2.0dev0')
        if not wheel_v1:
            raise ValueError('unsupported wheel format version: %s' % wheel_version)
        None(zf, destination_eggdir)
        dist_info = os.path.join(destination_eggdir, dist_info)
        dist = pkg_resources.Distribution.from_location(destination_eggdir, dist_info, pkg_resources.PathMetadata(destination_eggdir, dist_info), **('metadata',))
        
        def raw_req(req):
            req.marker = None
            return str(req)

        install_requires = list(map(raw_req, dist.requires()))
        extras_require = (lambda .0 = None: pass# WARNING: Decompyle incomplete
)(dist.extras)
        os.rename(dist_info, egg_info)
        os.rename(os.path.join(egg_info, 'METADATA'), os.path.join(egg_info, 'PKG-INFO'))
        setup_dist = setuptools.Distribution(dict(install_requires, extras_require, **('install_requires', 'extras_require')), **('attrs',))
    # WARNING: Decompyle incomplete

    _convert_metadata = staticmethod(_convert_metadata)
    
    def _move_data_entries(destination_eggdir, dist_data):
        '''Move data entries to their correct location.'''
        dist_data = os.path.join(destination_eggdir, dist_data)
        dist_data_scripts = os.path.join(dist_data, 'scripts')
        if os.path.exists(dist_data_scripts):
            egg_info_scripts = os.path.join(destination_eggdir, 'EGG-INFO', 'scripts')
            os.mkdir(egg_info_scripts)
            for entry in os.listdir(dist_data_scripts):
                if entry.endswith('.pyc'):
                    os.unlink(os.path.join(dist_data_scripts, entry))
                    continue
                os.rename(os.path.join(dist_data_scripts, entry), os.path.join(egg_info_scripts, entry))
            os.rmdir(dist_data_scripts)
        for subdir in None(None, (lambda .0 = None: for d in .0:
os.path.join(dist_data, d))(('data', 'headers', 'purelib', 'platlib'))):
            unpack(subdir, destination_eggdir)
        if os.path.exists(dist_data):
            os.rmdir(dist_data)
            return None

    _move_data_entries = staticmethod(_move_data_entries)
    
    def _fix_namespace_packages(egg_info, destination_eggdir):
        namespace_packages = os.path.join(egg_info, 'namespace_packages.txt')
    # WARNING: Decompyle incomplete

    _fix_namespace_packages = staticmethod(_fix_namespace_packages)

