
'''distutils.filelist

Provides the FileList class, used for poking about the filesystem
and building lists of files.
'''
import os
import re
import fnmatch
import functools
from distutils.util import convert_path
from distutils.errors import DistutilsTemplateError, DistutilsInternalError
from distutils import log

class FileList:
    """A list of files built by on exploring the filesystem and filtered by
    applying various patterns to what we find there.

    Instance attributes:
      dir
        directory from which files will be taken -- only used if
        'allfiles' not supplied to constructor
      files
        list of filenames currently being built/filtered/manipulated
      allfiles
        complete list of files under consideration (ie. without any
        filtering applied)
    """
    
    def __init__(self, warn, debug_print = (None, None)):
        self.allfiles = None
        self.files = []

    
    def set_allfiles(self, allfiles):
        self.allfiles = allfiles

    
    def findall(self, dir = (os.curdir,)):
        self.allfiles = findall(dir)

    
    def debug_print(self, msg):
        """Print 'msg' to stdout if the global DEBUG (taken from the
        DISTUTILS_DEBUG environment variable) flag is true.
        """
        DEBUG = DEBUG
        import distutils.debug
        if DEBUG:
            print(msg)
            return None

    
    def append(self, item):
        self.files.append(item)

    
    def extend(self, items):
        self.files.extend(items)

    
    def sort(self):
        sortable_files = sorted(map(os.path.split, self.files))
        self.files = []
    # WARNING: Decompyle incomplete

    
    def remove_duplicates(self):
        for i in range(len(self.files) - 1, 0, -1):
            if self.files[i] == self.files[i - 1]:
                del self.files[i]

    
    def _parse_template_line(self, line):
        words = line.split()
        action = words[0]
        patterns = None
        dir = None
        dir_pattern = None
        if action in ('include', 'exclude', 'global-include', 'global-exclude'):
            if len(words) < 2:
                raise DistutilsTemplateError("'%s' expects <pattern1> <pattern2> ..." % action)
            patterns = (lambda 