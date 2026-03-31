
'''Exception Handling

 Exceptions

\t To better support COM exceptions, the framework allows for an instance to be
\t raised.  This instance may have a certain number of known attributes, which are
\t translated into COM exception details.
\t
\t This means, for example, that Python could raise a COM exception that includes details
\t on a Help file and location, and a description for the user.
\t
\t This module provides a class which provides the necessary attributes.

'''
import sys
import pythoncom

class COMException(pythoncom.com_error):
    '''An Exception object that is understood by the framework.

    If the framework is presented with an exception of type class,
    it looks for certain known attributes on this class to provide rich
    error information to the caller.

    It should be noted that the framework supports providing this error
    information via COM Exceptions, or via the ISupportErrorInfo interface.

    By using this class, you automatically provide rich error information to the
    server.
    '''
    
    def __init__(self, description, scode, source, helpfile, helpContext, desc, hresult = (None, None, None, None, None, None, None)):
        '''Initialize an exception
        **Params**

        description -- A string description for the exception.
        scode -- An integer scode to be returned to the server, if necessary.
        The pythoncom framework defaults this to be DISP_E_EXCEPTION if not specified otherwise.
        source -- A string which identifies the source of the error.
        helpfile -- A string which points to a help file which contains details on the error.
        helpContext -- An integer context in the help file.
        desc -- A short-cut for description.
        hresult -- A short-cut for scode.
        '''
        if not scode:
            pass
        scode = hresult
        if scode and scode != 1 and scode >= -32768 and scode < 32768:
            scode = -2147024896 | scode & 65535
        self.scode = scode
        if not description:
            pass
        self.description = desc
        if not scode == 1 and self.description:
            self.description = 'S_FALSE'
        elif not scode and self.description:
            self.description = pythoncom.GetScodeString(scode)
        self.source = source
        self.helpfile = helpfile
        self.helpcontext = helpContext
        pythoncom.com_error.__init__(self, scode, self.description, None, -1)

    
    def __repr__(self):
        return '<COM Exception - scode=%s, desc=%s>' % (self.scode, self.description)


Exception = COMException

def IsCOMException(t = (None,)):
    if t is None:
        t = sys.exc_info()[0]
# WARNING: Decompyle incomplete


def IsCOMServerException(t = (None,)):
    if t is None:
        t = sys.exc_info()[0]
# WARNING: Decompyle incomplete

