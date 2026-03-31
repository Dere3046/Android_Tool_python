
"""
Set up 'os' and 'os.path' module replacement functions for use during import bootstrap.
"""
import sys
_builtin_names = sys.builtin_module_names
_mindirlen = 0
if 'posix' in _builtin_names:
    from posix import environ as os_environ
    from posix import listdir as os_listdir
    os_sep = '/'
    _mindirlen = 1
elif 'nt' in _builtin_names:
    from nt import environ as os_environ
    from nt import listdir as os_listdir
    os_sep = '\\'
    _mindirlen = 3
else:
    raise ImportError('No OS-specific module found!')

def os_path_join(a, b, sep = (None,)):
    if a == '':
        return b
    lastchar = None[-1:]
    if lastchar == '/' or lastchar == sep:
        return a + b
    return None + sep + b


def os_path_dirname(a, sep, mindirlen = (os_sep, _mindirlen)):
    for i in range(len(a) - 1, -1, -1):
        c = a[i]
        if c == '/' or c == sep:
            if i < mindirlen:
                return a[:i + 1]
            return None[:i]
        return ''

if sys.platform.startswith('win'):
    
    def os_path_basename(pth):
        if pth[1:2] == ':':
            p = pth[2:]
        else:
            p = pth
        i = len(p)
        if i and p[i - 1] not in '/\\':
            i = i - 1
            if i:
                if not p[i - 1] not in '/\\':
                    return p[i:]

else:
    
    def os_path_basename(pth):
        i = pth.rfind('/') + 1
        return pth[i:]

if 'PYTHONCASEOK' not in os_environ:
    
    def caseOk(filename):
        files = os_listdir(os_path_dirname(filename))
        return os_path_basename(filename) in files

    return None
