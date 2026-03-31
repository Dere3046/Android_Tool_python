
"""zipimport provides support for importing Python modules from Zip archives.

This module exports three objects:
- zipimporter: a class; its constructor takes a path to a Zip archive.
- ZipImportError: exception raised by zipimporter objects. It's a
  subclass of ImportError, so it can be caught as ImportError, too.
- _zip_directory_cache: a dict, mapping archive paths to zip directory
  info dicts, as used in zipimporter._files.

It is usually not needed to use the zipimport module explicitly; it is
used by the builtin import mechanism for sys.path items that are paths
to Zip archives.
"""
import _frozen_importlib_external as _bootstrap_external
from _frozen_importlib_external import _unpack_uint16, _unpack_uint32
import _frozen_importlib as _bootstrap
import _imp
import _io
import marshal
import sys
import time
import _warnings
__all__ = [
    'ZipImportError',
    'zipimporter']
path_sep = _bootstrap_external.path_sep
alt_path_sep = _bootstrap_external.path_separators[1:]

class ZipImportError(ImportError):
    pass

_zip_directory_cache = { }
_module_type = type(sys)
END_CENTRAL_DIR_SIZE = 22
STRING_END_ARCHIVE = b'PK\x05\x06'
MAX_COMMENT_LEN = 65535

class zipimporter(_bootstrap_external._LoaderBasics):
    """zipimporter(archivepath) -> zipimporter object

    Create a new zipimporter instance. 'archivepath' must be a path to
    a zipfile, or to a specific path inside a zipfile. For example, it can be
    '/tmp/myimport.zip', or '/tmp/myimport.zip/mydirectory', if mydirectory is a
    valid directory inside the archive.

    'ZipImportError is raised if 'archivepath' doesn't point to a valid Zip
    archive.

    The 'archive' attribute of zipimporter objects contains the name of the
    zipfile targeted.
    """
    
    def __init__(self, path):
        if not isinstance(path, str):
            import os
            path = os.fsdecode(path)
        if not path:
            raise ZipImportError('archive path is empty', path, **('path',))
        if None:
            path = path.replace(alt_path_sep, path_sep)
        prefix = []
    # WARNING: Decompyle incomplete

    
    def find_loader(self, fullname, path = (None,)):
        """find_loader(fullname, path=None) -> self, str or None.

        Search for a module specified by 'fullname'. 'fullname' must be the
        fully qualified (dotted) module name. It returns the zipimporter
        instance itself if the module was found, a string containing the
        full path name if it's possibly a portion of a namespace package,
        or None otherwise. The optional 'path' argument is ignored -- it's
        there for compatibility with the importer protocol.

        Deprecated since Python 3.10. Use find_spec() instead.
        """
        _warnings.warn('zipimporter.find_loader() is deprecated and slated for removal in Python 3.12; use find_spec() instead', DeprecationWarning)
        mi = _get_module_info(self, fullname)
        if mi is not None:
            return (self, [])
        modpath = None(self, fullname)
        if _is_dir(self, modpath):
            return (None, [
                f'''{self.archive}{path_sep}{modpath}'''])
        return (None, [])

    
    def find_module(self, fullname, path = (None,)):
        """find_module(fullname, path=None) -> self or None.

        Search for a module specified by 'fullname'. 'fullname' must be the
        fully qualified (dotted) module name. It returns the zipimporter
        instance itself if the module was found, or None if it wasn't.
        The optional 'path' argument is ignored -- it's there for compatibility
        with the importer protocol.

        Deprecated since Python 3.10. Use find_spec() instead.
        """
        _warnings.warn('zipimporter.find_module() is deprecated and slated for removal in Python 3.12; use find_spec() instead', DeprecationWarning)
        return self.find_loader(fullname, path)[0]

    
    def find_spec(self, fullname, target = (None,)):
        '''Create a ModuleSpec for the specified module.

        Returns None if the module cannot be found.
        '''
        module_info = _get_module_info(self, fullname)
        if module_info is not None:
            return _bootstrap.spec_from_loader(fullname, self, module_info, **('is_package',))
        modpath = None(self, fullname)
        if _is_dir(self, modpath):
            path = f'''{self.archive}{path_sep}{modpath}'''
            spec = _bootstrap.ModuleSpec(fullname, None, True, **('name', 'loader', 'is_package'))
            spec.submodule_search_locations.append(path)
            return spec

    
    def get_code(self, fullname):
        """get_code(fullname) -> code object.

        Return the code object for the specified module. Raise ZipImportError
        if the module couldn't be imported.
        """
        (code, ispackage, modpath) = _get_module_code(self, fullname)
        return code

    
    def get_data(self, pathname):
        """get_data(pathname) -> string with file data.

        Return the data associated with 'pathname'. Raise OSError if
        the file wasn't found.
        """
        if alt_path_sep:
            pathname = pathname.replace(alt_path_sep, path_sep)
        key = pathname
        if pathname.startswith(self.archive + path_sep):
            key = pathname[len(self.archive + path_sep):]
    # WARNING: Decompyle incomplete

    
    def get_filename(self, fullname):
        """get_filename(fullname) -> filename string.

        Return the filename for the specified module or raise ZipImportError
        if it couldn't be imported.
        """
        (code, ispackage, modpath) = _get_module_code(self, fullname)
        return modpath

    
    def get_source(self, fullname):
        """get_source(fullname) -> source string.

        Return the source code for the specified module. Raise ZipImportError
        if the module couldn't be found, return None if the archive does
        contain the module, but has no source for it.
        """
        mi = _get_module_info(self, fullname)
        if mi is None:
            raise ZipImportError(f'''can\'t find module {fullname!r}''', fullname, **('name',))
        path = None(self, fullname)
        if mi:
            fullpath = _bootstrap_external._path_join(path, '__init__.py')
        else:
            fullpath = f'''{path}.py'''
    # WARNING: Decompyle incomplete

    
    def is_package(self, fullname):
        """is_package(fullname) -> bool.

        Return True if the module specified by fullname is a package.
        Raise ZipImportError if the module couldn't be found.
        """
        mi = _get_module_info(self, fullname)
        if mi is None:
            raise ZipImportError(f'''can\'t find module {fullname!r}''', fullname, **('name',))

    
    def load_module(self, fullname):
        """load_module(fullname) -> module.

        Load the module specified by 'fullname'. 'fullname' must be the
        fully qualified (dotted) module name. It returns the imported
        module, or raises ZipImportError if it could not be imported.

        Deprecated since Python 3.10. Use exec_module() instead.
        """
        msg = 'zipimport.zipimporter.load_module() is deprecated and slated for removal in Python 3.12; use exec_module() instead'
        _warnings.warn(msg, DeprecationWarning)
        (code, ispackage, modpath) = _get_module_code(self, fullname)
        mod = sys.modules.get(fullname)
        if not mod is None or isinstance(mod, _module_type):
            mod = _module_type(fullname)
            sys.modules[fullname] = mod
        mod.__loader__ = self
    # WARNING: Decompyle incomplete

    
    def get_resource_reader(self, fullname):
        """Return the ResourceReader for a package in a zip file.

        If 'fullname' is a package within the zip file, return the
        'ResourceReader' object for the package.  Otherwise return None.
        """
        pass
    # WARNING: Decompyle incomplete

    
    def invalidate_caches(self):
        '''Reload the file data of the archive path.'''
        pass
    # WARNING: Decompyle incomplete

    
    def __repr__(self):
        return f'''<zipimporter object "{self.archive}{path_sep}{self.prefix}">'''


_zip_searchorder = ((path_sep + '__init__.pyc', True, True), (path_sep + '__init__.py', False, True), ('.pyc', True, False), ('.py', False, False))

def _get_module_path(self, fullname):
    return self.prefix + fullname.rpartition('.')[2]


def _is_dir(self, path):
    dirpath = path + path_sep
    return dirpath in self._files


def _get_module_info(self, fullname):
    path = _get_module_path(self, fullname)
    for suffix, isbytecode, ispackage in _zip_searchorder:
        fullpath = path + suffix
        if fullpath in self._files:
            return ispackage
        return None


def _read_directory(archive):
    pass
# WARNING: Decompyle incomplete

cp437_table = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7fÇüéâäàåçêëèïîìÄÅÉæÆôöòûùÿÖÜ¢£¥₧ƒáíóúñÑªº¿⌐¬½¼¡«»░▒▓│┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌█▄▌▐▀αßΓπΣσµτΦΘΩδ∞φε∩≡±≥≤⌠⌡÷≈°∙·√ⁿ²■ '
_importing_zlib = False

def _get_decompress_func():
    global _importing_zlib
    if _importing_zlib:
        _bootstrap._verbose_message('zipimport: zlib UNAVAILABLE')
        raise ZipImportError("can't decompress data; zlib not available")
    _importing_zlib = None
# WARNING: Decompyle incomplete


def _get_data(archive, toc_entry):
    (datapath, compress, data_size, file_size, file_offset, time, date, crc) = toc_entry
    if data_size < 0:
        raise ZipImportError('negative data size')
# WARNING: Decompyle incomplete


def _eq_mtime(t1, t2):
    return abs(t1 - t2) <= 1


def _unmarshal_code(self, pathname, fullpath, fullname, data):
    exc_details = {
        'name': fullname,
        'path': fullpath }
    flags = _bootstrap_external._classify_pyc(data, fullname, exc_details)
    hash_based = flags & 1 != 0
    if hash_based:
        check_source = flags & 2 != 0
        if _imp.check_hash_based_pycs != 'never':
            if check_source or _imp.check_hash_based_pycs == 'always':
                source_bytes = _get_pyc_source(self, fullpath)
                if source_bytes is not None:
                    source_hash = _imp.source_hash(_bootstrap_external._RAW_MAGIC_NUMBER, source_bytes)
                    _bootstrap_external._validate_hash_pyc(data, source_hash, fullname, exc_details)
                else:
                    (source_mtime, source_size) = _get_mtime_and_size_of_source(self, fullpath)
                    if source_mtime:
                        if _eq_mtime(_unpack_uint32(data[8:12]), source_mtime) or _unpack_uint32(data[12:16]) != source_size:
                            _bootstrap._verbose_message(f'''bytecode is stale for {fullname!r}''')
                            return None
                        code = None.loads(data[16:])
                        if not isinstance(code, _code_type):
                            raise TypeError(f'''compiled module {pathname!r} is not a code object''')
                        return None

_code_type = type(_unmarshal_code.__code__)

def _normalize_line_endings(source):
    source = source.replace(b'\r\n', b'\n')
    source = source.replace(b'\r', b'\n')
    return source


def _compile_source(pathname, source):
    source = _normalize_line_endings(source)
    return compile(source, pathname, 'exec', True, **('dont_inherit',))


def _parse_dostime(d, t):
    return time.mktime(((d >> 9) + 1980, d >> 5 & 15, d & 31, t >> 11, t >> 5 & 63, (t & 31) * 2, -1, -1, -1))


def _get_mtime_and_size_of_source(self, path):
    pass
# WARNING: Decompyle incomplete


def _get_pyc_source(self, path):
    pass
# WARNING: Decompyle incomplete


def _get_module_code(self, fullname):
    path = _get_module_path(self, fullname)
    import_error = None
# WARNING: Decompyle incomplete

