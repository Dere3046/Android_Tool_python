
from binascii import Error, unhexlify
from contextlib import suppress
from cmd_line_interface.base_defines import AutoCloseFileType, KWARGS_READ_BINARY

class HexFileToBytes:
    '''
    Generic class for input format conversion.
    This class accepts a file containing data in binary or hex-string representation. If containing hex-string data,
    the data is converted to binary representation.
    '''
    
    def __call__(self = None, path = None):
        file_data = AutoCloseFileType(KWARGS_READ_BINARY, **('mode',))(path)
    # WARNING: Decompyle incomplete


