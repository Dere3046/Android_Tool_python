
"""Access to Python's configuration information."""
import os
import sys
from os.path import pardir, realpath
__all__ = [
    'get_config_h_filename',
    'get_config_var',
    'get_config_vars',
    'get_makefile_filename',
    'get_path',
    'get_path_names',
    'get_paths',
    'get_platform',
    'get_python_version',
    'get_scheme_names',
    'parse_config_h']
_ALWAYS_STR = {
    'MACOSX_DEPLOYMENT_TARGET'}
_INSTALL_SCHEMES = {
    'posix_prefix': {
        'stdlib': '{installed_base}/{platlibdir}/python{py_version_short}',
        'platstdlib': '{platbase}/{platlibdir}/python{py_version_short}',
        'purelib': '{base}/lib/python{py_version_short}/site-packages',
        'platlib': '{platbase}/{platlibdir}/python{py_version_short}/site-packages',
        'include': '{installed_base}/include/python{py_version_short}{abiflags}',
        'platinclude': '{installed_platbase}/include/python{py_version_short}{abiflags}',
        'scripts': '{base}/bin',
        'data': '{base}' },
    'posix_home': {
        'stdlib': '{installed_base}/lib/python',
        'platstdlib': '{base}/lib/python',
        'purelib': '{base}/lib/python',
        'platlib': '{base}/lib/python',
        'include': '{installed_base}/include/python',
        'platinclude': '{installed_base}/include/python',
        'scripts': '{base}/bin',
        'data': '{base}' },
    'nt': {
        'stdlib': '{installed_base}/Lib',
        'platstdlib': '{base}/Lib',
        'purelib': '{base}/Lib/site-packages',
        'platlib': '{base}/Lib/site-packages',
        'include': '{installed_base}/Include',
        'platinclude': '{installed_base}/Include',
        'scripts': '{base}/Scripts',
        'data': '{base}' },
    'osx_framework_library': {
        'stdlib': '{installed_base}/{platlibdir}/python{py_version_short}',
        'platstdlib': '{platbase}/{platlibdir}/python{py_version_short}',
        'purelib': '/home/linuxbrew/.linuxbrew/lib/python{py_version_short}/site-packages',
        'platlib': '/home/linuxbrew/.linuxbrew/{platlibdir}/python{py_version_short}/site-packages',
        'include': '{installed_base}/include/python{py_version_short}{abiflags}',
        'platinclude': '{installed_platbase}/include/python{py_version_short}{abiflags}',
        'scripts': '/home/linuxbrew/.linuxbrew/bin',
        'data': '/home/linuxbrew/.linuxbrew' } }
_INSTALL_SCHEMES['venv'] = _INSTALL_SCHEMES['posix_prefix']

def _getuserbase():
    env_base = os.environ.get('PYTHONUSERBASE', None)
    if env_base:
        return env_base
    if None.platform == 'vxworks':
        return None
    