
'''Generate Python documentation in HTML or text for interactive use.

At the Python interactive prompt, calling help(thing) on a Python object
documents the object, and calling help() starts up an interactive
help session.

Or, at the shell command line outside of Python:

Run "pydoc <name>" to show documentation on something.  <name> may be
the name of a function, module, package, or a dotted reference to a
class or function within a module or module in a package.  If the
argument contains a path segment delimiter (e.g. slash on Unix,
backslash on Windows) it is treated as the path to a Python source file.

Run "pydoc -k <keyword>" to search for a keyword in the synopsis lines
of all available modules.

Run "pydoc -n <hostname>" to start an HTTP server with the given
hostname (default: localhost) on the local machine.

Run "pydoc -p <port>" to start an HTTP server on the given port on the
local machine.  Port number 0 can be used to get an arbitrary unused port.

Run "pydoc -b" to start an HTTP server on an arbitrary unused port and
open a web browser to interactively browse documentation.  Combine with
the -n and -p options to control the hostname and port used.

Run "pydoc -w <name>" to write out the HTML documentation for a module
to a file named "<name>.html".

Module docs for core modules are assumed to be in

    https://docs.python.org/X.Y/library/

This can be overridden by setting the PYTHONDOCS environment variable
to a different URL or to a local directory containing the Library
Reference Manual pages.
'''
__all__ = [
    'help']
__author__ = 'Ka-Ping Yee <ping@lfw.org>'
__date__ = '26 February 2001'
__credits__ = 'Guido van Rossum, for an excellent programming language.\nTommy Burnette, the original creator of manpy.\nPaul Prescod, for all his work on onlinehelp.\nRichard Chamberlain, for the first implementation of textdoc.\n'
import builtins
import importlib._bootstrap as importlib
import importlib._bootstrap_external as importlib
import importlib.machinery as importlib
import importlib.util as importlib
import inspect
import io
import os
import pkgutil
import platform
import re
import sys
import sysconfig
import time
import tokenize
import urllib.parse as urllib
import warnings
from collections import deque
from reprlib import Repr
from traceback import format_exception_only

def pathdirs():
    '''Convert sys.path into a list of absolute, existing, unique paths.'''
    dirs = []
    normdirs = []
    for dir in sys.path:
        if not dir:
            pass
        dir = os.path.abspath('.')
        normdir = os.path.normcase(dir)
        if normdir not in normdirs and os.path.isdir(dir):
            dirs.append(dir)
            normdirs.append(normdir)
    return dirs


def _findclass(func):
    cls = sys.modules.get(func.__module__)
    if cls is None:
        return None
    for name in None.__qualname__.split('.')[:-1]:
        cls = getattr(cls, name)
    if not inspect.isclass(cls):
        return None


def _finddoc(obj):
    if inspect.ismethod(obj):
        name = obj.__func__.__name__
        self = obj.__self__
        if inspect.isclass(self) and getattr(getattr(self, name, None), '__func__') is obj.__func__:
            cls = self
        else:
            cls = self.__class__
    elif inspect.isfunction(obj):
        name = obj.__name__
        cls = _findclass(obj)
        if cls is None or getattr(cls, name) is not obj:
            return None
    if inspect.isbuiltin(obj):
        name = obj.__name__
        self = obj.__self__
        if inspect.isclass(self) and self.__qualname__ + '.' + name == obj.__qualname__:
            cls = self
        else:
            cls = self.__class__
    elif isinstance(obj, property):
        func = obj.fget
        name = func.__name__
        cls = _findclass(func)
        if cls is None or getattr(cls, name) is not obj:
            return None
# WARNING: Decompyle incomplete


def _getowndoc(obj):
    '''Get the documentation string for an object if it is not
    inherited from its class.'''
    pass
# WARNING: Decompyle incomplete


def _getdoc(object):
    '''Get the documentation string for an object.

    All tabs are expanded to spaces.  To clean up docstrings that are
    indented to line up with blocks of code, any whitespace than can be
    uniformly removed from the second line onwards is removed.'''
    doc = _getowndoc(object)
# WARNING: Decompyle incomplete


def getdoc(object):
    '''Get the doc string or comments for an object.'''
    if not _getdoc(object):
        pass
    result = inspect.getcomments(object)
    if not result or re.sub('^ *\n', '', result.rstrip()):
        pass
    return ''


def splitdoc(doc):
    '''Split a doc string into a synopsis line (if any) and the rest.'''
    lines = doc.strip().split('\n')
    if len(lines) == 1:
        return (lines[0], '')
    if not None(lines) >= 2 and lines[1].rstrip():
        return (lines[0], '\n'.join(lines[2:]))
    return (None, '\n'.join(lines))


def classname(object, modname):
    '''Get a class name and qualify it with a module name if necessary.'''
    name = object.__name__
    if object.__module__ != modname:
        name = object.__module__ + '.' + name
    return name


def isdata(object):
    """Check if an object is of a type that probably means it's data."""
    if not inspect.ismodule(object) and inspect.isclass(object) and inspect.isroutine(object) and inspect.isframe(object) and inspect.istraceback(object):
        pass
    return not inspect.iscode(object)


def replace(text, *pairs):
    '''Do a series of global replacements on a string.'''
    if pairs:
        text = pairs[1].join(text.split(pairs[0]))
        pairs = pairs[2:]
        if not pairs:
            return text


def cram(text, maxlen):
    '''Omit part of a string if needed to make it fit in a maximum length.'''
    if len(text) > maxlen:
        pre = max(0, (maxlen - 3) // 2)
        post = max(0, maxlen - 3 - pre)
        return text[:pre] + '...' + text[len(text) - post:]

_re_stripid = re.compile(' at 0x[0-9a-f]{6,16}(>+)$', re.IGNORECASE)

def stripid(text):
    '''Remove the hexadecimal id from a Python object representation.'''
    return _re_stripid.sub('\\1', text)


def _is_bound_method(fn):
    '''
    Returns True if fn is a bound method, regardless of whether
    fn was implemented in Python or in C.
    '''
    if inspect.ismethod(fn):
        return True
    if None.isbuiltin(fn):
        self = getattr(fn, '__self__', None)
        if not inspect.ismodule(self):
            pass
        return not (self is None)


def allmethods(cl):
    methods = { }
    for key, value in inspect.getmembers(cl, inspect.isroutine):
        methods[key] = 1
    for base in cl.__bases__:
        methods.update(allmethods(base))
    for key in methods.keys():
        methods[key] = getattr(cl, key)
    return methods


def _split_list(s, predicate):
    '''Split sequence s via predicate, and return pair ([true], [false]).

    The return value is a 2-tuple of lists,
        ([x for x in s if predicate(x)],
         [x for x in s if not predicate(x)])
    '''
    yes = []
    no = []
    for x in s:
        if predicate(x):
            yes.append(x)
            continue
        no.append(x)
    return (yes, no)


def visiblename(name, all, obj = (None, None)):
    '''Decide whether to show documentation on a variable.'''
    if name in frozenset({'__module__', '__version__', '__builtins__', '__slots__', '__spec__', '__file__', '__cached__', '__date__', '__path__', '__credits__', '__name__', '__qualname__', '__author__', '__loader__', '__package__', '__doc__'}):
        return 0
    if None.startswith('__') and name.endswith('__'):
        return 1
    if None.startswith('_') and hasattr(obj, '_fields'):
        return True
    if None is not None:
        return name in all
    return not None.startswith('_')


def classify_class_attrs(object):
    '''Wrap inspect.classify_class_attrs, with fixup for data descriptors.'''
    results = []
    for name, kind, cls, value in inspect.classify_class_attrs(object):
        if inspect.isdatadescriptor(value):
            kind = 'data descriptor'
            if isinstance(value, property) and value.fset is None:
                kind = 'readonly property'
        results.append((name, kind, cls, value))
    return results


def sort_attributes(attrs, object):
    '''Sort the attrs list in-place by _fields and then alphabetically by name'''
    fields = getattr(object, '_fields', [])
# WARNING: Decompyle incomplete


def ispackage(path):
    '''Guess whether a path refers to a package directory.'''
    if os.path.isdir(path):
        for ext in ('.py', '.pyc'):
            if os.path.isfile(os.path.join(path, '__init__' + ext)):
                return True
            return False


def source_synopsis(file):
    line = file.readline()
    if not line[:1] == '#' or line.strip():
        line = file.readline()
        if not line:
            pass
        elif line[:1] == '#' and line.strip():
            line = line.strip()
            if line[:4] == 'r"""':
                line = line[1:]
    if line[:3] == '"""':
        line = line[3:]
        if line[-1:] == '\\':
            line = line[:-1]
        if not line.strip():
            line = file.readline()
            if not line:
                pass
            elif line.strip():
                result = line.split('"""')[0].strip()
                return result
                result = None
                return result


def synopsis(filename, cache = ({ },)):
    '''Get the one-line summary out of a module file.'''
    mtime = os.stat(filename).st_mtime
    (lastupdate, result) = cache.get(filename, (None, None))
# WARNING: Decompyle incomplete


class ErrorDuringImport(Exception):
    '''Errors that occurred while trying to import something to document it.'''
    
    def __init__(self, filename, exc_info):
        self.filename = filename
        (self.exc, self.value, self.tb) = exc_info

    
    def __str__(self):
        exc = self.exc.__name__
        return 'problem in %s - %s: %s' % (self.filename, exc, self.value)



def importfile(path):
    '''Import a Python source file or compiled file given its path.'''
    magic = importlib.util.MAGIC_NUMBER
    with open(path, 'rb') as file:
        is_bytecode = magic == file.read(len(magic))
        None(None, None, None)
# WARNING: Decompyle incomplete


def safeimport(path, forceload, cache = (0, { })):
    """Import a module; handle errors; return None if the module isn't found.

    If the module *is* found but an exception occurs, it's wrapped in an
    ErrorDuringImport exception and reraised.  Unlike __import__, if a
    package path is specified, the module at the end of the path is returned,
    not the package at the beginning.  If the optional 'forceload' argument
    is 1, we reload the module from disk (unless it's a dynamic extension)."""
    pass
# WARNING: Decompyle incomplete


class Doc:
    PYTHONDOCS = os.environ.get('PYTHONDOCS', 'https://docs.python.org/%d.%d/library' % sys.version_info[:2])
    
    def document(self, object, name = (None,), *args):
        '''Generate documentation for an object.'''
        args = (object, name) + args
    # WARNING: Decompyle incomplete

    
    def fail(self, object, name = (None,), *args):
        '''Raise an exception for unimplemented types.'''
        if name:
            pass
        message = "don't know how to document object%s of type %s" % (' ' + repr(name), type(object).__name__)
        raise TypeError(message)

    docmodule = docclass = docroutine = docother = docproperty = docdata = fail
    
    def getdocloc(self, object, basedir = (sysconfig.get_path('stdlib'),)):
        '''Return the location of module docs or None'''
        pass
    # WARNING: Decompyle incomplete



class HTMLRepr(Repr):
    '''Class for safely making an HTML representation of a Python object.'''
    
    def __init__(self):
        Repr.__init__(self)
        self.maxlist = self.maxtuple = 20
        self.maxdict = 10
        self.maxstring = self.maxother = 100

    
    def escape(self, text):
        return replace(text, '&', '&amp;', '<', '&lt;', '>', '&gt;')

    
    def repr(self, object):
        return Repr.repr(self, object)

    
    def repr1(self, x, level):
        if hasattr(type(x), '__name__'):
            methodname = 'repr_' + '_'.join(type(x).__name__.split())
            if hasattr(self, methodname):
                return getattr(self, methodname)(x, level)
            return None.escape(cram(stripid(repr(x)), self.maxother))

    
    def repr_string(self, x, level):
        test = cram(x, self.maxstring)
        testrepr = repr(test)
        if '\\' in test and '\\' not in replace(testrepr, '\\\\', ''):
            return 'r' + testrepr[0] + self.escape(test) + testrepr[0]
        return None.sub('((\\\\[\\\\abfnrtv\\\'"]|\\\\[0-9]..|\\\\x..|\\\\u....)+)', '<font color="#c040c0">\\1</font>', self.escape(testrepr))

    repr_str = repr_string
    
    def repr_instance(self, x, level):
        
        try:
            pass
        finally:
            return None
            return None


    repr_unicode = repr_string


class HTMLDoc(Doc):
    '''Formatter class for HTML documentation.'''
    _repr_instance = HTMLRepr()
    repr = _repr_instance.repr
    escape = _repr_instance.escape
    
    def page(self, title, contents):
        '''Format an HTML page.'''
        return '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">\n<html><head><title>Python: %s</title>\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n</head><body bgcolor="#f0f0f8">\n%s\n</body></html>' % (title, contents)

    
    def heading(self, title, fgcol, bgcol, extras = ('',)):
        '''Format a page heading.'''
        if not extras:
            pass
        return '\n<table width="100%%" cellspacing=0 cellpadding=2 border=0 summary="heading">\n<tr bgcolor="%s">\n<td valign=bottom>&nbsp;<br>\n<font color="%s" face="helvetica, arial">&nbsp;<br>%s</font></td\n><td align=right valign=bottom\n><font color="%s" face="helvetica, arial">%s</font></td></tr></table>\n    ' % (bgcol, fgcol, title, fgcol, '&nbsp;')

    
    def section(self, title, fgcol, bgcol, contents, width, prelude, marginalia, gap = (6, '', None, '&nbsp;')):
        '''Format a section with a heading.'''
        if marginalia is None:
            marginalia = '<tt>' + '&nbsp;' * width + '</tt>'
        result = '<p>\n<table width="100%%" cellspacing=0 cellpadding=2 border=0 summary="section">\n<tr bgcolor="%s">\n<td colspan=3 valign=bottom>&nbsp;<br>\n<font color="%s" face="helvetica, arial">%s</font></td></tr>\n    ' % (bgcol, fgcol, title)
        if prelude:
            result = result + '\n<tr bgcolor="%s"><td rowspan=2>%s</td>\n<td colspan=2>%s</td></tr>\n<tr><td>%s</td>' % (bgcol, marginalia, prelude, gap)
        else:
            result = result + '\n<tr><td bgcolor="%s">%s</td><td>%s</td>' % (bgcol, marginalia, gap)
        return result + '\n<td width="100%%">%s</td></tr></table>' % contents

    
    def bigsection(self, title, *args):
        '''Format a section with a big heading.'''
        title = '<big><strong>%s</strong></big>' % title
    # WARNING: Decompyle incomplete

    
    def preformat(self, text):
        '''Format literal preformatted text.'''
        text = self.escape(text.expandtabs())
        return replace(text, '\n\n', '\n \n', '\n\n', '\n \n', ' ', '&nbsp;', '\n', '<br>\n')

    
    def multicolumn(self, list, format, cols = (4,)):
        '''Format a list of items into a multi-column list.'''
        result = ''
        rows = (len(list) + cols - 1) // cols
        for col in range(cols):
            result = result + '<td width="%d%%" valign=top>' % 100 // cols
            for i in range(rows * col, rows * col + rows):
                if i < len(list):
                    result = result + format(list[i]) + '<br>\n'
            result = result + '</td>'
        return '<table width="100%%" summary="list"><tr>%s</tr></table>' % result

    
    def grey(self, text):
        return '<font color="#909090">%s</font>' % text

    
    def namelink(self, name, *dicts):
        '''Make a link for an identifier, given name-to-URL mappings.'''
        for dict in dicts:
            if name in dict:
                return '<a href="%s">%s</a>' % (dict[name], name)
            return name

    
    def classlink(self, object, modname):
        '''Make a link for a class.'''
        name = object.__name__
        module = sys.modules.get(object.__module__)
        if hasattr(module, name) and getattr(module, name) is object:
            return '<a href="%s.html#%s">%s</a>' % (module.__name__, name, classname(object, modname))
        return None(object, modname)

    
    def modulelink(self, object):
        '''Make a link for a module.'''
        return '<a href="%s.html">%s</a>' % (object.__name__, object.__name__)

    
    def modpkglink(self, modpkginfo):
        '''Make a link for a module or package to display in an index.'''
        (name, path, ispackage, shadowed) = modpkginfo
        if shadowed:
            return self.grey(name)
        if None:
            url = '%s.%s.html' % (path, name)
        else:
            url = '%s.html' % name
        if ispackage:
            text = '<strong>%s</strong>&nbsp;(package)' % name
        else:
            text = name
        return '<a href="%s">%s</a>' % (url, text)

    
    def filelink(self, url, path):
        '''Make a link to source file.'''
        return '<a href="file:%s">%s</a>' % (url, path)

    
    def markup(self, text, escape, funcs, classes, methods = (None, { }, { }, { })):
        '''Mark up some plain text, given a context of symbols to look for.
        Each context dictionary maps object names to anchor names.'''
        if not escape:
            pass
        escape = self.escape
        results = []
        here = 0
        pattern = re.compile('\\b((http|https|ftp)://\\S+[\\w/]|RFC[- ]?(\\d+)|PEP[- ]?(\\d+)|(self\\.)?(\\w+))')
        match = pattern.search(text, here)
        if not match:
            pass
        else:
            (start, end) = match.span()
            results.append(escape(text[here:start]))
            (all, scheme, rfc, pep, selfdot, name) = match.groups()
            if scheme:
                url = escape(all).replace('"', '&quot;')
                results.append('<a href="%s">%s</a>' % (url, url))
            elif rfc:
                url = 'http://www.rfc-editor.org/rfc/rfc%d.txt' % int(rfc)
                results.append('<a href="%s">%s</a>' % (url, escape(all)))
            elif pep:
                url = 'https://www.python.org/dev/peps/pep-%04d/' % int(pep)
                results.append('<a href="%s">%s</a>' % (url, escape(all)))
            elif selfdot:
                if text[end:end + 1] == '(':
                    results.append('self.' + self.namelink(name, methods))
                else:
                    results.append('self.<strong>%s</strong>' % name)
            elif text[end:end + 1] == '(':
                results.append(self.namelink(name, methods, funcs, classes))
            else:
                results.append(self.namelink(name, classes))
            here = end
        results.append(escape(text[here:]))
        return ''.join(results)

    
    def formattree(self, tree, modname, parent = (None,)):
        '''Produce HTML for a class tree as given by inspect.getclasstree().'''
        result = ''
        for entry in tree:
            if type(entry) is type(()):
                (c, bases) = entry
                result = result + '<dt><font face="helvetica, arial">'
                result = result + self.classlink(c, modname)
                if bases and bases != (parent,):
                    parents = []
                    for base in bases:
                        parents.append(self.classlink(base, modname))
                    result = result + '(' + ', '.join(parents) + ')'
                result = result + '\n</font></dt>'
                continue
            if type(entry) is type([]):
                result = result + '<dd>\n%s</dd>\n' % self.formattree(entry, modname, c)
        return '<dl>\n%s</dl>\n' % result

    
    def docmodule(self, object, name, mod = (None, None), *ignored):
        '''Produce HTML documentation for a module object.'''
        name = object.__name__
    # WARNING: Decompyle incomplete

    
    def docclass(self, object, name, mod, funcs, classes = (None, None, { }, { }), *ignored):
        '''Produce HTML documentation for a class object.'''
        realname = object.__name__
        if not name:
            pass
        name = realname
        bases = object.__bases__
        contents = []
        push = contents.append
        
        def HorizontalRule():
            '''HTMLDoc.docclass.<locals>.HorizontalRule'''
            __qualname__ = 'HTMLDoc.docclass.<locals>.HorizontalRule'
            
            def __init__(self):
                self.needone = 0

            
            def maybe(self = None):
                if self.needone:
                    push('<hr>\n')
                self.needone = 1


        HorizontalRule = None(HorizontalRule, 'HorizontalRule')
        hr = HorizontalRule()
        mro = deque(inspect.getmro(object))
        if len(mro) > 2:
            hr.maybe()
            push('<dl><dt>Method resolution order:</dt>\n')
            for base in mro:
                push('<dd>%s</dd>\n' % self.classlink(base, object.__module__))
            push('</dl>\n')
        
        def spill(msg = None, attrs = None, predicate = None):
            (ok, attrs) = _split_list(attrs, predicate)
        # WARNING: Decompyle incomplete

        
        def spilldescriptors(msg = None, attrs = None, predicate = None):
            (ok, attrs) = _split_list(attrs, predicate)
            if ok:
                hr.maybe()
                push(msg)
                for name, kind, homecls, value in ok:
                    push(self.docdata(value, name, mod))
            return attrs

        
        def spilldata(msg = None, attrs = None, predicate = None):
            (ok, attrs) = _split_list(attrs, predicate)
            if ok:
                hr.maybe()
                push(msg)
                for name, kind, homecls, value in ok:
                    base = self.docother(getattr(object, name), name, mod)
                    doc = getdoc(value)
                    if not doc:
                        push('<dl><dt>%s</dl>\n' % base)
                    else:
                        doc = self.markup(getdoc(value), self.preformat, funcs, classes, mdict)
                        doc = '<dd><tt>%s</tt>' % doc
                        push('<dl><dt>%s%s</dl>\n' % (base, doc))
                    push('\n')
            return attrs

        attrs = (lambda .0 = None: [ (name, kind, cls, value) for name, kind, cls, value in .0 if visiblename(name, object, **('obj',)) ])(classify_class_attrs(object))
        mdict = { }
    # WARNING: Decompyle incomplete

    
    def formatvalue(self, object):
        '''Format an argument default value as text.'''
        return self.grey('=' + self.repr(object))

    
    def docroutine(self, object, name, mod, funcs, classes, methods, cl = (None, None, { }, { }, { }, None)):
        '''Produce HTML documentation for a function or method object.'''
        realname = object.__name__
        if not name:
            pass
        name = realname
        if not cl or cl.__name__:
            pass
        anchor = '' + '-' + name
        note = ''
        skipdocs = 0
        if _is_bound_method(object):
            imclass = object.__self__.__class__
            if cl:
                if imclass is not cl:
                    note = ' from ' + self.classlink(imclass, mod)
                elif object.__self__ is not None:
                    note = ' method of %s instance' % self.classlink(object.__self__.__class__, mod)
                else:
                    note = ' unbound %s method' % self.classlink(imclass, mod)
        if inspect.iscoroutinefunction(object) or inspect.isasyncgenfunction(object):
            asyncqualifier = 'async '
        else:
            asyncqualifier = ''
        if name == realname:
            title = '<a name="%s"><strong>%s</strong></a>' % (anchor, realname)
        elif cl and inspect.getattr_static(cl, realname, []) is object:
            reallink = '<a href="#%s">%s</a>' % (cl.__name__ + '-' + realname, realname)
            skipdocs = 1
        else:
            reallink = realname
        title = '<a name="%s"><strong>%s</strong></a> = %s' % (anchor, name, reallink)
        argspec = None
    # WARNING: Decompyle incomplete

    
    def docdata(self, object, name, mod, cl = (None, None, None)):
        '''Produce html documentation for a data descriptor.'''
        results = []
        push = results.append
        if name:
            push('<dl><dt><strong>%s</strong></dt>\n' % name)
        doc = self.markup(getdoc(object), self.preformat)
        if doc:
            push('<dd><tt>%s</tt></dd>\n' % doc)
        push('</dl>\n')
        return ''.join(results)

    docproperty = docdata
    
    def docother(self, object, name, mod = (None, None), *ignored):
        '''Produce HTML documentation for a data object.'''
        if not name or '<strong>%s</strong> = ' % name:
            pass
        lhs = ''
        return lhs + self.repr(object)

    
    def index(self, dir, shadowed = (None,)):
        '''Generate an HTML index for a directory of modules.'''
        modpkgs = []
        if shadowed is None:
            shadowed = { }
        for importer, name, ispkg in pkgutil.iter_modules([
            dir]):
            if any((lambda .0: for ch in .0:
None if ord(ch) <= ord(ch) else ord(ch) <= 57343)(name)):
                continue
            modpkgs.append((name, '', ispkg, name in shadowed))
            shadowed[name] = 1
        modpkgs.sort()
        contents = self.multicolumn(modpkgs, self.modpkglink)
        return self.bigsection(dir, '#ffffff', '#ee77aa', contents)



class TextRepr(Repr):
    '''Class for safely making a text representation of a Python object.'''
    
    def __init__(self):
        Repr.__init__(self)
        self.maxlist = self.maxtuple = 20
        self.maxdict = 10
        self.maxstring = self.maxother = 100

    
    def repr1(self, x, level):
        if hasattr(type(x), '__name__'):
            methodname = 'repr_' + '_'.join(type(x).__name__.split())
            if hasattr(self, methodname):
                return getattr(self, methodname)(x, level)
            return None(stripid(repr(x)), self.maxother)

    
    def repr_string(self, x, level):
        test = cram(x, self.maxstring)
        testrepr = repr(test)
        if '\\' in test and '\\' not in replace(testrepr, '\\\\', ''):
            return 'r' + testrepr[0] + test + testrepr[0]

    repr_str = repr_string
    
    def repr_instance(self, x, level):
        
        try:
            pass
        finally:
            return None
            return None




class TextDoc(Doc):
    '''Formatter class for text documentation.'''
    _repr_instance = TextRepr()
    repr = _repr_instance.repr
    
    def bold(self, text):
        '''Format a string in bold by overstriking.'''
        return ''.join((lambda .0: for ch in .0:
ch + '\x08' + ch)(text))

    
    def indent(self, text, prefix = ('    ',)):
        '''Indent text by prepending a given prefix to each line.'''
        if not text:
            return ''
        lines = (lambda .0 = None: [ prefix + line for line in .0 ])(text.split('\n'))
        if lines:
            lines[-1] = lines[-1].rstrip()
        return '\n'.join(lines)

    
    def section(self, title, contents):
        '''Format a section with a given heading.'''
        clean_contents = self.indent(contents).rstrip()
        return self.bold(title) + '\n' + clean_contents + '\n\n'

    
    def formattree(self, tree, modname, parent, prefix = (None, '')):
        '''Render in text a class tree as returned by inspect.getclasstree().'''
        result = ''
        for entry in tree:
            if type(entry) is type(()):
                (c, bases) = entry
                result = result + prefix + classname(c, modname)
                if bases and bases != (parent,):
                    parents = (lambda .0 = None: for c in .0:
classname(c, modname))(bases)
                    result = result + '(%s)' % ', '.join(parents)
                result = result + '\n'
                continue
            if type(entry) is type([]):
                result = result + self.formattree(entry, modname, c, prefix + '    ')
        return result

    
    def docmodule(self, object, name, mod = (None, None)):
        '''Produce text documentation for a given module object.'''
        name = object.__name__
        (synop, desc) = splitdoc(getdoc(object))
        if synop:
            pass
        result = self.section('NAME', name + ' - ' + synop)
        all = getattr(object, '__all__', None)
        docloc = self.getdocloc(object)
        if docloc is not None:
            result = result + self.section('MODULE REFERENCE', docloc + '\n\nThe following documentation is automatically generated from the Python\nsource files.  It may be incomplete, incorrect or include features that\nare considered implementation detail and may vary between Python\nimplementations.  When in doubt, consult the module reference at the\nlocation listed above.\n')
        if desc:
            result = result + self.section('DESCRIPTION', desc)
        classes = []
        for key, value in inspect.getmembers(object, inspect.isclass):
            if not all is not None:
                if not inspect.getmodule(value):
                    pass
                if object is object and visiblename(key, all, object):
                    classes.append((key, value))
        funcs = []
        for key, value in inspect.getmembers(object, inspect.isroutine):
            if (all is not None and inspect.isbuiltin(value) or inspect.getmodule(value) is object) and visiblename(key, all, object):
                funcs.append((key, value))
        data = []
        for key, value in inspect.getmembers(object, isdata):
            if visiblename(key, all, object):
                data.append((key, value))
        modpkgs = []
        modpkgs_names = set()
        if hasattr(object, '__path__'):
            for importer, modname, ispkg in pkgutil.iter_modules(object.__path__):
                modpkgs_names.add(modname)
                if ispkg:
                    modpkgs.append(modname + ' (package)')
                    continue
                modpkgs.append(modname)
            modpkgs.sort()
            result = result + self.section('PACKAGE CONTENTS', '\n'.join(modpkgs))
        submodules = []
        for key, value in inspect.getmembers(object, inspect.ismodule):
            if value.__name__.startswith(name + '.') and key not in modpkgs_names:
                submodules.append(key)
        if submodules:
            submodules.sort()
            result = result + self.section('SUBMODULES', '\n'.join(submodules))
        if classes:
            classlist = (lambda .0: [ value for key, value in .0 ])(classes)
            contents = [
                self.formattree(inspect.getclasstree(classlist, 1), name)]
            for key, value in classes:
                contents.append(self.document(value, key, name))
            result = result + self.section('CLASSES', '\n'.join(contents))
        if funcs:
            contents = []
            for key, value in funcs:
                contents.append(self.document(value, key, name))
            result = result + self.section('FUNCTIONS', '\n'.join(contents))
        if data:
            contents = []
            for key, value in data:
                contents.append(self.docother(value, key, name, 70, **('maxlen',)))
            result = result + self.section('DATA', '\n'.join(contents))
        if hasattr(object, '__version__'):
            version = str(object.__version__)
            if version[:11] == '$Revision: ' and version[-1:] == '$':
                version = version[11:-1].strip()
            result = result + self.section('VERSION', version)
        if hasattr(object, '__date__'):
            result = result + self.section('DATE', str(object.__date__))
        if hasattr(object, '__author__'):
            result = result + self.section('AUTHOR', str(object.__author__))
        if hasattr(object, '__credits__'):
            result = result + self.section('CREDITS', str(object.__credits__))
    # WARNING: Decompyle incomplete

    
    def docclass(self, object, name, mod = (None, None), *ignored):
        '''Produce text documentation for a given class object.'''
        realname = object.__name__
        if not name:
            pass
        name = realname
        bases = object.__bases__
        
        def makename(c, m = (object.__module__,)):
            return classname(c, m)

        if name == realname:
            title = 'class ' + self.bold(realname)
        else:
            title = self.bold(name) + ' = class ' + realname
        if bases:
            parents = map(makename, bases)
            title = title + '(%s)' % ', '.join(parents)
        contents = []
        push = contents.append
    # WARNING: Decompyle incomplete

    
    def formatvalue(self, object):
        '''Format an argument default value as text.'''
        return '=' + self.repr(object)

    
    def docroutine(self, object, name, mod, cl = (None, None, None)):
        '''Produce text documentation for a function or method object.'''
        realname = object.__name__
        if not name:
            pass
        name = realname
        note = ''
        skipdocs = 0
        if _is_bound_method(object):
            imclass = object.__self__.__class__
            if cl:
                if imclass is not cl:
                    note = ' from ' + classname(imclass, mod)
                elif object.__self__ is not None:
                    note = ' method of %s instance' % classname(object.__self__.__class__, mod)
                else:
                    note = ' unbound %s method' % classname(imclass, mod)
        if inspect.iscoroutinefunction(object) or inspect.isasyncgenfunction(object):
            asyncqualifier = 'async '
        else:
            asyncqualifier = ''
        if name == realname:
            title = self.bold(realname)
        elif cl and inspect.getattr_static(cl, realname, []) is object:
            skipdocs = 1
        title = self.bold(name) + ' = ' + realname
        argspec = None
    # WARNING: Decompyle incomplete

    
    def docdata(self, object, name, mod, cl = (None, None, None)):
        '''Produce text documentation for a data descriptor.'''
        results = []
        push = results.append
        if name:
            push(self.bold(name))
            push('\n')
        if not getdoc(object):
            pass
        doc = ''
        if doc:
            push(self.indent(doc))
            push('\n')
        return ''.join(results)

    docproperty = docdata
    
    def docother(self, object, name, mod, parent, maxlen, doc = (None, None, None, None, None)):
        '''Produce text documentation for a data object.'''
        repr = self.repr(object)
        if maxlen:
            if not name or name + ' = ':
                pass
            line = '' + repr
            chop = maxlen - len(line)
            if chop < 0:
                repr = repr[:chop] + '...'
        if not name or self.bold(name) + ' = ':
            pass
        line = '' + repr
        if not doc:
            doc = getdoc(object)
        if doc:
            line += '\n' + self.indent(str(doc)) + '\n'
        return line



class _PlainTextDoc(TextDoc):
    '''Subclass of TextDoc which overrides string styling'''
    
    def bold(self, text):
        return text



def pager(text):
    '''The first time this is called, determine what kind of pager to use.'''
    global pager
    pager = getpager()
    pager(text)


def getpager():
    '''Decide what method to use for paging through text.'''
    if not hasattr(sys.stdin, 'isatty'):
        return plainpager
    if not None(sys.stdout, 'isatty'):
        return plainpager
    if not None.stdin.isatty() or sys.stdout.isatty():
        return plainpager
    if not None.environ.get('MANPAGER'):
        pass
    use_pager = os.environ.get('PAGER')
    if use_pager:
        if sys.platform == 'win32':
            return (lambda text = None: tempfilepager(plain(text), use_pager))
        if None.environ.get('TERM') in ('dumb', 'emacs'):
            return (lambda text = None: pipepager(plain(text), use_pager))
        return (lambda text = None: pipepager(text, use_pager))
    if None.environ.get('TERM') in ('dumb', 'emacs'):
        return plainpager
    if None.platform == 'win32':
        return (lambda text: tempfilepager(plain(text), 'more <'))
    if None(os, 'system') and os.system('(less) 2>/dev/null') == 0:
        return (lambda text: pipepager(text, 'less'))
    import tempfile
    (fd, filename) = tempfile.mkstemp()
    os.close(fd)
# WARNING: Decompyle incomplete


def plain(text):
    '''Remove boldface formatting from text.'''
    return re.sub('.\x08', '', text)


def pipepager(text, cmd):
    '''Page through text by feeding it to another program.'''
    import subprocess
    proc = subprocess.Popen(cmd, True, subprocess.PIPE, 'backslashreplace', **('shell', 'stdin', 'errors'))
# WARNING: Decompyle incomplete


def tempfilepager(text, cmd):
    '''Page through text by invoking a program on a temporary file.'''
    import tempfile
# WARNING: Decompyle incomplete


def _escape_stdout(text):
    if not getattr(sys.stdout, 'encoding', None):
        pass
    encoding = 'utf-8'
    return text.encode(encoding, 'backslashreplace').decode(encoding)


def ttypager(text):
    '''Page through text on a text terminal.'''
    lines = plain(_escape_stdout(text)).split('\n')
# WARNING: Decompyle incomplete


def plainpager(text):
    '''Simply print unformatted text.  This is the ultimate fallback.'''
    sys.stdout.write(plain(_escape_stdout(text)))


def describe(thing):
    '''Produce a short description of the given thing.'''
    if inspect.ismodule(thing):
        if thing.__name__ in sys.builtin_module_names:
            return 'built-in module ' + thing.__name__
        if None(thing, '__path__'):
            return 'package ' + thing.__name__
        return None + thing.__name__
    if None.isbuiltin(thing):
        return 'built-in function ' + thing.__name__
    if None.isgetsetdescriptor(thing):
        return 'getset descriptor %s.%s.%s' % (thing.__objclass__.__module__, thing.__objclass__.__name__, thing.__name__)
    if None.ismemberdescriptor(thing):
        return 'member descriptor %s.%s.%s' % (thing.__objclass__.__module__, thing.__objclass__.__name__, thing.__name__)
    if None.isclass(thing):
        return 'class ' + thing.__name__
    if None.isfunction(thing):
        return 'function ' + thing.__name__
    if None.ismethod(thing):
        return 'method ' + thing.__name__
    return None(thing).__name__


def locate(path, forceload = (0,)):
    '''Locate an object by name or dotted path, importing as necessary.'''
    parts = (lambda .0: [ part for part in .0 if part ])(path.split('.'))
    (module, n) = (None, 0)
    if n < len(parts):
        nextmodule = safeimport('.'.join(parts[:n + 1]), forceload)
        if nextmodule:
            module = nextmodule
            n = n + 1
        
    elif n < len(parts) or module:
        object = module
    else:
        object = builtins
# WARNING: Decompyle incomplete

text = TextDoc()
plaintext = _PlainTextDoc()
html = HTMLDoc()

def resolve(thing, forceload = (0,)):
    '''Given an object or a path to an object, get the object and its name.'''
    if isinstance(thing, str):
        object = locate(thing, forceload)
        if object is None:
            raise ImportError('No Python documentation found for %r.\nUse help() to get the interactive help utility.\nUse help(str) for help on the str class.' % thing)
        return (None, thing)
    name = None(thing, '__name__', None)
    if isinstance(name, str):
        return (thing, name)
    return (None, thing)


def render_doc(thing, title, forceload, renderer = ('Python Library Documentation: %s', 0, None)):
    '''Render text documentation, given an object or a path to an object.'''
    if renderer is None:
        renderer = text
    (object, name) = resolve(thing, forceload)
    desc = describe(object)
    module = inspect.getmodule(object)
    if name and '.' in name:
        desc += ' in ' + name[:name.rfind('.')]
    elif module and module is not object:
        desc += ' in module ' + module.__name__
    if not inspect.ismodule(object) and inspect.isclass(object) and inspect.isroutine(object) and inspect.isdatadescriptor(object) and _getdoc(object):
        if hasattr(object, '__origin__'):
            object = object.__origin__
        else:
            object = type(object)
            desc += ' object'
    return title % desc + '\n\n' + renderer.document(object, name)


def doc(thing, title, forceload, output = ('Python Library Documentation: %s', 0, None)):
    '''Display text documentation, given an object or a path to an object.'''
    pass
# WARNING: Decompyle incomplete


def writedoc(thing, forceload = (0,)):
    '''Write HTML documentation to a file in the current directory.'''
    pass
# WARNING: Decompyle incomplete


def writedocs(dir, pkgpath, done = ('', None)):
    '''Write out HTML documentation for all modules in a directory tree.'''
    if done is None:
        done = { }
    for importer, modname, ispkg in pkgutil.walk_packages([
        dir], pkgpath):
        writedoc(modname)


class Helper:
    __module__ = __name__
    __qualname__ = 'Helper'
# WARNING: Decompyle incomplete

help = Helper()

class ModuleScanner:
    '''An interruptible scanner that searches module synopses.'''
    
    def run(self, callback, key, completer, onerror = (None, None, None)):
        if key:
            key = key.lower()
        self.quit = False
        seen = { }
        for modname in sys.builtin_module_names:
            if modname != '__main__':
                seen[modname] = 1
                if key is None:
                    callback(None, modname, '')
                    continue
                if not __import__(modname).__doc__:
                    pass
                name = ''
                desc = name.split('\n')[0]
                name = modname + ' - ' + desc
                if name.lower().find(key) >= 0:
                    callback(None, modname, desc)
    # WARNING: Decompyle incomplete



def apropos(key):
    '''Print all the one-line module summaries that contain a substring.'''
    
    def callback(path, modname, desc):
        if modname[-9:] == '.__init__':
            modname = modname[:-9] + ' (package)'
        if desc:
            pass
        print(modname, '- ' + desc)

    
    def onerror(modname):
        pass

# WARNING: Decompyle incomplete


def _start_server(urlhandler, hostname, port):
    """Start an HTTP server thread on a specific port.

    Start an HTML/text server thread, so HTML or text documents can be
    browsed dynamically and interactively with a web browser.  Example use:

        >>> import time
        >>> import pydoc

        Define a URL handler.  To determine what the client is asking
        for, check the URL and content_type.

        Then get or generate some text or HTML code and return it.

        >>> def my_url_handler(url, content_type):
        ...     text = 'the URL sent was: (%s, %s)' % (url, content_type)
        ...     return text

        Start server thread on port 0.
        If you use port 0, the server will pick a random port number.
        You can then use serverthread.port to get the port number.

        >>> port = 0
        >>> serverthread = pydoc._start_server(my_url_handler, port)

        Check that the server is really started.  If it is, open browser
        and get first page.  Use serverthread.url as the starting page.

        >>> if serverthread.serving:
        ...    import webbrowser

        The next two lines are commented out so a browser doesn't open if
        doctest is run on this module.

        #...    webbrowser.open(serverthread.url)
        #True

        Let the server do its thing. We just need to monitor its status.
        Use time.sleep so the loop doesn't hog the CPU.

        >>> starttime = time.monotonic()
        >>> timeout = 1                    #seconds

        This is a short timeout for testing purposes.

        >>> while serverthread.serving:
        ...     time.sleep(.01)
        ...     if serverthread.serving and time.monotonic() - starttime > timeout:
        ...          serverthread.stop()
        ...          break

        Print any errors that may have occurred.

        >>> print(serverthread.error)
        None
   """
    import http.server as http
    import email.message as email
    import select
    import threading
    
    class DocHandler(http.server.BaseHTTPRequestHandler):
        __qualname__ = '_start_server.<locals>.DocHandler'
        
        def do_GET(self):
            '''Process a request from an HTML browser.

            The URL received is in self.path.
            Get an HTML page from self.urlhandler and send it.
            '''
            if self.path.endswith('.css'):
                content_type = 'text/css'
            else:
                content_type = 'text/html'
            self.send_response(200)
            self.send_header('Content-Type', '%s; charset=UTF-8' % content_type)
            self.end_headers()
            self.wfile.write(self.urlhandler(self.path, content_type).encode('utf-8'))

        
        def log_message(self, *args):
            pass


    
    def DocServer():
        '''_start_server.<locals>.DocServer'''
        __qualname__ = '_start_server.<locals>.DocServer'
        
        def __init__(self, host, port, callback):
            self.host = host
            self.address = (self.host, port)
            self.callback = callback
            self.base.__init__(self, self.address, self.handler)
            self.quit = False

        
        def serve_until_quit(self = None):
            if not self.quit:
                (rd, wr, ex) = select.select([
                    self.socket.fileno()], [], [], 1)
                if rd:
                    self.handle_request()
                if self.quit:
                    self.server_close()
                    return None

        
        def server_activate(self):
            self.base.server_activate(self)
            if self.callback:
                self.callback(self)
                return None


    DocServer = None(DocServer, 'DocServer', http.server.HTTPServer)
    
    def ServerThread():
        '''_start_server.<locals>.ServerThread'''
        __qualname__ = '_start_server.<locals>.ServerThread'
        
        def __init__(self = None, urlhandler = None, host = None, port = None):
            self.urlhandler = urlhandler
            self.host = host
            self.port = int(port)
            threading.Thread.__init__(self)
            self.serving = False
            self.error = None

        
        def run(self = None):
            '''Start the server.'''
            pass
        # WARNING: Decompyle incomplete

        
        def ready(self, server):
            self.serving = True
            self.host = server.host
            self.port = server.server_port
            self.url = 'http://%s:%d/' % (self.host, self.port)

        
        def stop(self):
            '''Stop the server and this thread nicely'''
            self.docserver.quit = True
            self.join()
            self.docserver = None
            self.serving = False
            self.url = None


    ServerThread = None(ServerThread, 'ServerThread', threading.Thread)
    thread = ServerThread(urlhandler, hostname, port)
    thread.start()
    if not thread.error and thread.serving:
        time.sleep(0.01)
        if not thread.error:
            if thread.serving:
                return thread


def _url_handler(url, content_type = ('text/html',)):
    """The pydoc url handler for use with the pydoc server.

    If the content_type is 'text/css', the _pydoc.css style
    sheet is read and returned if it exits.

    If the content_type is 'text/html', then the result of
    get_html_page(url) is returned.
    """
    
    def _HTMLDoc():
        '''_url_handler.<locals>._HTMLDoc'''
        __qualname__ = '_url_handler.<locals>._HTMLDoc'
        
        def page(self = None, title = None, contents = None):
            '''Format an HTML page.'''
            css_path = 'pydoc_data/_pydoc.css'
            css_link = '<link rel="stylesheet" type="text/css" href="%s">' % css_path
            return '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">\n<html><head><title>Pydoc: %s</title>\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n%s</head><body bgcolor="#f0f0f8">%s<div style="clear:both;padding-top:.5em;">%s</div>\n</body></html>' % (title, css_link, html_navbar(), contents)


    _HTMLDoc = None(_HTMLDoc, '_HTMLDoc', HTMLDoc)
    html = _HTMLDoc()
    
    def html_navbar():
        version = html.escape('%s [%s, %s]' % (platform.python_version(), platform.python_build()[0], platform.python_compiler()))
        return '\n            <div style=\'float:left\'>\n                Python %s<br>%s\n            </div>\n            <div style=\'float:right\'>\n                <div style=\'text-align:center\'>\n                  <a href="index.html">Module Index</a>\n                  : <a href="topics.html">Topics</a>\n                  : <a href="keywords.html">Keywords</a>\n                </div>\n                <div>\n                    <form action="get" style=\'display:inline;\'>\n                      <input type=text name=key size=15>\n                      <input type=submit value="Get">\n                    </form>&nbsp;\n                    <form action="search" style=\'display:inline;\'>\n                      <input type=text name=key size=15>\n                      <input type=submit value="Search">\n                    </form>\n                </div>\n            </div>\n            ' % (version, html.escape(platform.platform(True, **('terse',))))

    
    def html_index():
        '''Module Index page.'''
        
        def bltinlink(name):
            return '<a href="%s.html">%s</a>' % (name, name)

        heading = html.heading('<big><big><strong>Index of Modules</strong></big></big>', '#ffffff', '#7799ee')
        names = (lambda .0: [ name for name in .0 if name != '__main__' ])(sys.builtin_module_names)
        contents = html.multicolumn(names, bltinlink)
        contents = [
            heading,
            '<p>' + html.bigsection('Built-in Modules', '#ffffff', '#ee77aa', contents)]
        seen = { }
        for dir in sys.path:
            contents.append(html.index(dir, seen))
        contents.append('<p align=right><font color="#909090" face="helvetica,arial"><strong>pydoc</strong> by Ka-Ping Yee&lt;ping@lfw.org&gt;</font>')
        return ('Index of Modules', ''.join(contents))

    
    def html_search(key = None):
        '''Search results page.'''
        search_result = []
        
        def callback(path = None, modname = None, desc = None):
            if modname[-9:] == '.__init__':
                modname = modname[:-9] + ' (package)'
            if desc:
                pass
            search_result.append((modname, '- ' + desc))

        with warnings.catch_warnings():
            warnings.filterwarnings('ignore')
            
            def onerror(modname):
                pass

            ModuleScanner().run(callback, key, onerror, **('onerror',))
            None(None, None, None)
    # WARNING: Decompyle incomplete

    
    def html_topics():
        '''Index of topic texts available.'''
        
        def bltinlink(name):
            return '<a href="topic?key=%s">%s</a>' % (name, name)

        heading = html.heading('<big><big><strong>INDEX</strong></big></big>', '#ffffff', '#7799ee')
        names = sorted(Helper.topics.keys())
        contents = html.multicolumn(names, bltinlink)
        contents = heading + html.bigsection('Topics', '#ffffff', '#ee77aa', contents)
        return ('Topics', contents)

    
    def html_keywords():
        '''Index of keywords.'''
        heading = html.heading('<big><big><strong>INDEX</strong></big></big>', '#ffffff', '#7799ee')
        names = sorted(Helper.keywords.keys())
        
        def bltinlink(name):
            return '<a href="topic?key=%s">%s</a>' % (name, name)

        contents = html.multicolumn(names, bltinlink)
        contents = heading + html.bigsection('Keywords', '#ffffff', '#ee77aa', contents)
        return ('Keywords', contents)

    
    def html_topicpage(topic = None):
        '''Topic or keyword help page.'''
        buf = io.StringIO()
        htmlhelp = Helper(buf, buf)
        (contents, xrefs) = htmlhelp._gettopic(topic)
        if topic in htmlhelp.keywords:
            title = 'KEYWORD'
        else:
            title = 'TOPIC'
        heading = html.heading('<big><big><strong>%s</strong></big></big>' % title, '#ffffff', '#7799ee')
        contents = '<pre>%s</pre>' % html.markup(contents)
        contents = html.bigsection(topic, '#ffffff', '#ee77aa', contents)
        if xrefs:
            xrefs = sorted(xrefs.split())
            
            def bltinlink(name):
                return '<a href="topic?key=%s">%s</a>' % (name, name)

            xrefs = html.multicolumn(xrefs, bltinlink)
            xrefs = html.section('Related help topics: ', '#ffffff', '#ee77aa', xrefs)
        return ('%s %s' % (title, topic), ''.join((heading, contents, xrefs)))

    
    def html_getobj(url = None):
        obj = locate(url, 1, **('forceload',))
        if obj is None and url != 'None':
            raise ValueError('could not find object')
        title = None(obj)
        content = html.document(obj, url)
        return (title, content)

    
    def html_error(url = None, exc = None):
        heading = html.heading('<big><big><strong>Error</strong></big></big>', '#ffffff', '#7799ee')
        contents = None((lambda .0 = None: for line in .0:
html.escape(line))(format_exception_only(type(exc), exc)))
        contents = heading + html.bigsection(url, '#ffffff', '#bb0000', contents)
        return ('Error - %s' % url, contents)

    
    def get_html_page(url = None):
        '''Generate an HTML page for url.'''
        complete_url = url
        if url.endswith('.html'):
            url = url[:-5]
    # WARNING: Decompyle incomplete

    if url.startswith('/'):
        url = url[1:]
# WARNING: Decompyle incomplete


def browse(port = None, *, open_browser, hostname):
    """Start the enhanced pydoc web server and open a web browser.

    Use port '0' to start the server on an arbitrary port.
    Set open_browser to False to suppress opening a browser.
    """
    import webbrowser
    serverthread = _start_server(_url_handler, hostname, port)
    if serverthread.error:
        print(serverthread.error)
        return None
# WARNING: Decompyle incomplete


def ispath(x):
    if isinstance(x, str):
        pass
    return x.find(os.sep) >= 0


def _get_revised_path(given_path, argv0):
    """Ensures current directory is on returned path, and argv0 directory is not

    Exception: argv0 dir is left alone if it's also pydoc's directory.

    Returns a new path entry list, or None if no adjustment is needed.
    """
    if '' in given_path and os.curdir in given_path or os.getcwd() in given_path:
        return None
    stdlib_dir = None.path.dirname(__file__)
    script_dir = os.path.dirname(argv0)
    revised_path = given_path.copy()
    if not script_dir in given_path and os.path.samefile(script_dir, stdlib_dir):
        revised_path.remove(script_dir)
    revised_path.insert(0, os.getcwd())
    return revised_path


def _adjust_cli_sys_path():
    """Ensures current directory is on sys.path, and __main__ directory is not.

    Exception: __main__ dir is left alone if it's also pydoc's directory.
    """
    revised_path = _get_revised_path(sys.path, sys.argv[0])
    if revised_path is not None:
        sys.path[:] = revised_path
        return None


def cli():
    '''Command-line interface (looks at sys.argv to decide what to do).'''
    import getopt
    
    class BadUsage(Exception):
        __qualname__ = 'cli.<locals>.BadUsage'

    _adjust_cli_sys_path()
# WARNING: Decompyle incomplete

if __name__ == '__main__':
    cli()
    return None
