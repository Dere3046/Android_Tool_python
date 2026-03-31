
'''asyncio exceptions.'''
__all__ = ('CancelledError', 'InvalidStateError', 'TimeoutError', 'IncompleteReadError', 'LimitOverrunError', 'SendfileNotAvailableError')

class CancelledError(BaseException):
    '''The Future or Task was cancelled.'''
    pass


class TimeoutError(Exception):
    '''The operation exceeded the given deadline.'''
    pass


class InvalidStateError(Exception):
    '''The operation is not allowed in this state.'''
    pass


class SendfileNotAvailableError(RuntimeError):
    '''Sendfile syscall is not available.

    Raised if OS does not support sendfile syscall for given socket or
    file type.
    '''
    pass


class IncompleteReadError(EOFError):
    '''
    Incomplete read error. Attributes:

    - partial: read bytes string before the end of stream was reached
    - expected: total number of expected bytes (or None if unknown)
    '''
    
    def __init__(self = None, partial = None, expected = None):
        r_expected = 'undefined' if expected is None else repr(expected)
        super().__init__(f'''{len(partial)} bytes read on a total of {r_expected} expected bytes''')
        self.partial = partial
        self.expected = expected

    
    def __reduce__(self):
        return (type(self), (self.partial, self.expected))

    __classcell__ = None


class LimitOverrunError(Exception):
    '''Reached the buffer limit while looking for a separator.

    Attributes:
    - consumed: total number of to be consumed bytes.
    '''
    
    def __init__(self = None, message = None, consumed = None):
        super().__init__(message)
        self.consumed = consumed

    
    def __reduce__(self):
        return (type(self), (self.args[0], self.consumed))

    __classcell__ = None

