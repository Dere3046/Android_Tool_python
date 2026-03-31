
'''Response classes used by urllib.

The base class, addbase, defines a minimal file-like interface,
including read() and readline().  The typical response object is an
addinfourl instance, which defines an info() method that returns
headers and a geturl() method that returns the url.
'''
import tempfile
__all__ = [
    'addbase',
    'addclosehook',
    'addinfo',
    'addinfourl']

class addbase(tempfile._TemporaryFileWrapper):
    '''Base class for addinfo and addclosehook. Is a good idea for garbage collection.'''
    
    def __init__(self = None, fp = None):
        super(addbase, self).__init__(fp, '<urllib response>', False, **('delete',))
        self.fp = fp

    
    def __repr__(self):
        return '<%s at %r whose fp = %r>' % (self.__class__.__name__, id(self), self.file)

    
    def __enter__(self):
        if self.fp.closed:
            raise ValueError('I/O operation on closed file')

    
    def __exit__(self, type, value, traceback):
        self.close()

    __classcell__ = None


class addclosehook(addbase):
    '''Class to add a close hook to an open file.'''
    
    def __init__(self = None, fp = None, closehook = None, *hookargs):
        super(addclosehook, self).__init__(fp)
        self.closehook = closehook
        self.hookargs = hookargs

    
    def close(self = None):
        pass
    # WARNING: Decompyle incomplete

    __classcell__ = None


class addinfo(addbase):
    '''class to add an info() method to an open file.'''
    
    def __init__(self = None, fp = None, headers = None):
        super(addinfo, self).__init__(fp)
        self.headers = headers

    
    def info(self):
        return self.headers

    __classcell__ = None


class addinfourl(addinfo):
    '''class to add info() and geturl() methods to an open file.'''
    
    def __init__(self = None, fp = None, headers = None, url = None, code = None):
        super(addinfourl, self).__init__(fp, headers)
        self.url = url
        self.code = code

    
    def status(self):
        return self.code

    status = property(status)
    
    def getcode(self):
        return self.code

    
    def geturl(self):
        return self.url

    __classcell__ = None

