
from Cryptodome.Util._raw_api import load_pycryptodome_raw_lib, c_size_t, create_string_buffer, get_raw_buffer, c_uint8_ptr, is_writeable_buffer
_raw_strxor = load_pycryptodome_raw_lib('Cryptodome.Util._strxor', '\n                    void strxor(const uint8_t *in1,\n                                const uint8_t *in2,\n                                uint8_t *out, size_t len);\n                    void strxor_c(const uint8_t *in,\n                                  uint8_t c,\n                                  uint8_t *out,\n                                  size_t len);\n                    ')

def strxor(term1, term2, output = (None,)):
    '''XOR two byte strings.
    
    Args:
      term1 (bytes/bytearray/memoryview):
        The first term of the XOR operation.
      term2 (bytes/bytearray/memoryview):
        The second term of the XOR operation.
      output (bytearray/memoryview):
        The location where the result must be written to.
        If ``None``, the result is returned.
    :Return:
        If ``output`` is ``None``, a new ``bytes`` string with the result.
        Otherwise ``None``.
    '''
    if len(term1) != len(term2):
        raise ValueError('Only byte strings of equal length can be xored')
    if None is None:
        result = create_string_buffer(len(term1))
    else:
        result = output
        if not is_writeable_buffer(output):
            raise TypeError('output must be a bytearray or a writeable memoryview')
        if None(term1) != len(output):
            raise ValueError('output must have the same length as the input  (%d bytes)' % len(term1))
        None.strxor(c_uint8_ptr(term1), c_uint8_ptr(term2), c_uint8_ptr(result), c_size_t(len(term1)))
        if output is None:
            return get_raw_buffer(result)
        return None


def strxor_c(term, c, output = (None,)):
    '''XOR a byte string with a repeated sequence of characters.

    Args:
        term(bytes/bytearray/memoryview):
            The first term of the XOR operation.
        c (bytes):
            The byte that makes up the second term of the XOR operation.
        output (None or bytearray/memoryview):
            If not ``None``, the location where the result is stored into.

    Return:
        If ``output`` is ``None``, a new ``bytes`` string with the result.
        Otherwise ``None``.
    '''
    if not c <= c or c < 256:
        raise ValueError('c must be in range(256)')
    raise ValueError('c must be in range(256)')
    if output is None:
        result = create_string_buffer(len(term))
    else:
        result = output
        if not is_writeable_buffer(output):
            raise TypeError('output must be a bytearray or a writeable memoryview')
        if 0(term) != len(output):
            raise ValueError('output must have the same length as the input  (%d bytes)' % len(term))
        None.strxor_c(c_uint8_ptr(term), c, c_uint8_ptr(result), c_size_t(len(term)))
        if output is None:
            return get_raw_buffer(result)
        return None


def _strxor_direct(term1, term2, result):
    '''Very fast XOR - check conditions!'''
    _raw_strxor.strxor(term1, term2, result, c_size_t(len(term1)))

