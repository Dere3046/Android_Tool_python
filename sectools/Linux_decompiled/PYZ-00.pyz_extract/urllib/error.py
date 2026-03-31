
"""Exception classes raised by urllib.

The base exception class is URLError, which inherits from OSError.  It
doesn't define any behavior of its own, but is the base class for all
exceptions defined in this package.

HTTPError is an exception class that is also a valid HTTP response
instance.  It behaves this way because HTTP protocol errors are valid
responses, with a status code, headers, and a body.  In some contexts,
an application may want to handle an exception like a regular
response.
"""
import urllib.response as urllib
__all__ = [
    'URLError',
    'HTTPError',
    'ContentTooShortError']

class URLError(OSError):
    
    def __init__(self, reason, filename = (None,)):
        self.args = (reason,)
        self.reason = reason
        if filename is not None:
            self.filename = filename
            return None

    
    def __str__(self):
        return '<urlopen error %s>' % self.reason



class HTTPError(urllib.response.addinfourl, URLError):
    '''Raised when HTTP error occurs, but also acts like non-error return'''
    __super_init = urllib.response.addinfourl.__init__
    
    def __init__(self, url, code, msg, hdrs, fp):
        self.code = code
        self.msg = msg
        self.hdrs = hdrs
        self.fp = fp
        self.filename = url
        if fp is not None:
            self.__super_init(fp, hdrs, url, code)
            return None

    
    def __str__(self):
        return 'HTTP Error %s: %s' % (self.code, self.msg)

    
    def __repr__(self):
        return '<HTTPError %s: %r>' % (self.code, self.msg)

    
    def reason(self):
        return self.msg

    reason = property(reason)
    
    def headers(self):
        return self.hdrs

    headers = property(headers)
    
    def headers(self, headers):
        self.hdrs = headers

    headers = headers.setter(headers)


class ContentTooShortError(URLError):
    '''Exception raised when downloaded size does not match content-length.'''
    
    def __init__(self, message, content):
        URLError.__init__(self, message)
        self.content = content


