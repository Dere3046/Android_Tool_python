
import importlib.util as importlib
import importlib.machinery as importlib
import sys
import os

def __import_pywin32_system_module__(modname, globs):
    suffix = '_d' if '_d.pyd' in importlib.machinery.EXTENSION_SUFFIXES else ''
    filename = '%s%d%d%s.dll' % (modname, sys.version_info[0], sys.version_info[1], suffix)
    if hasattr(sys, 'frozen'):
        for look in sys.path:
            if os.path.isfile(look):
                look = os.path.dirname(look)
            found = os.path.join(look, filename)
            if os.path.isfile(found):
                pass
            
            raise ImportError("Module '%s' isn't in frozen sys.path %s" % (modname, sys.path))
            import _win32sysloader
            found = _win32sysloader.GetModuleFilename(filename)
            if found is None:
                found = _win32sysloader.LoadModule(filename)
    if found is None and os.path.isfile(os.path.join(sys.prefix, filename)):
        found = os.path.join(sys.prefix, filename)
    if found is None and os.path.isfile(os.path.join(os.path.dirname(__file__), filename)):
        found = os.path.join(os.path.dirname(__file__), filename)
    if found is None:
        import site
        maybe = os.path.join(site.USER_SITE, 'pywin32_system32', filename)
        if os.path.isfile(maybe):
            found = maybe
    if found is None:
        import sysconfig
        maybe = os.path.join(sysconfig.get_paths()['platlib'], 'pywin32_system32', filename)
        if os.path.isfile(maybe):
            found = maybe
    if found is None:
        raise ImportError("No system module '%s' (%s)" % (modname, filename))
    old_mod = None.modules[modname]
    loader = importlib.machinery.ExtensionFileLoader(modname, found)
    spec = importlib.machinery.ModuleSpec(modname, loader, found, **('name', 'loader', 'origin'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
# WARNING: Decompyle incomplete

__import_pywin32_system_module__('pywintypes', globals())
