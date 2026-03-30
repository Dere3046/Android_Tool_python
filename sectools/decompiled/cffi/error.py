

class FFIError(Exception):
    __module__ = 'cffi'


class CDefError(Exception):
    __module__ = 'cffi'
    
    def __str__(self):
        pass
    # WARNING: Decompyle incomplete



class VerificationError(Exception):
    ''' An error raised when verification fails
    '''
    __module__ = 'cffi'


class VerificationMissing(Exception):
    ''' An error raised when incomplete structures are passed into
    cdef, but no verification has been done
    '''
    __module__ = 'cffi'


class PkgConfigError(Exception):
    ''' An error raised for missing modules in pkg-config
    '''
    __module__ = 'cffi'

