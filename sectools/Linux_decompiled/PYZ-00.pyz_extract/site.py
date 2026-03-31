
"""
This is a fake 'site' module available in default Python Library.

The real 'site' does some magic to find paths to other possible Python modules. We do not want this behaviour for
frozen applications.

Fake 'site' makes PyInstaller to work with distutils and to work inside virtualenv environment.
"""
__pyinstaller__faked__site__module__ = True
PREFIXES = []
ENABLE_USER_SITE = False
USER_SITE = ''
USER_BASE = ''

class _Helper:
    """
    Define the builtin 'help'. This is a wrapper around pydoc.help (with a twist).
    """
    
    def __repr__(self):
        return 'Type help() for interactive help, or help(object) for help about object.'

    
    def __call__(self, *args, **kwds):
        pydoc = __import__(''.join('pydoc'))
    # WARNING: Decompyle incomplete


