
from Cryptodome.Util.py3compat import *
from Cryptodome.Util._raw_api import load_pycryptodome_raw_lib, VoidPointer, SmartPointer, create_string_buffer, get_raw_buffer, c_size_t, c_uint8_ptr
_raw_sha1_lib = load_pycryptodome_raw_lib('Cryptodome.Hash._SHA1', '\n                        #define SHA1_DIGEST_SIZE 20\n\n                        int SHA1_init(void **shaState);\n                        int SHA1_destroy(void *shaState);\n                        int SHA1_update(void *hs,\n                                          const uint8_t *buf,\n                                          size_t len);\n                        int SHA1_digest(const void *shaState,\n                                          uint8_t digest[SHA1_DIGEST_SIZE]);\n                        int SHA1_copy(const void *src, void *dst);\n\n                        int SHA1_pbkdf2_hmac_assist(const void *inner,\n                                            const void *outer,\n                                            const uint8_t first_digest[SHA1_DIGEST_SIZE],\n                                            uint8_t final_digest[SHA1_DIGEST_SIZE],\n                                            size_t iterations);\n                        ')

class SHA1Hash(object):
    '''A SHA-1 hash object.
    Do not instantiate directly.
    Use the :func:`new` function.

    :ivar oid: ASN.1 Object ID
    :vartype oid: string

    :ivar block_size: the size in bytes of the internal message block,
                      input to the compression function
    :vartype block_size: integer

    :ivar digest_size: the size in bytes of the resulting hash
    :vartype digest_size: integer
    '''
    digest_size = 20
    block_size = 64
    oid = '1.3.14.3.2.26'
    
    def __init__(self, data = (None,)):
        state = VoidPointer()
        result = _raw_sha1_lib.SHA1_init(state.address_of())
        if result:
            raise ValueError('Error %d while instantiating SHA1' % result)
        self._state = None(state.get(), _raw_sha1_lib.SHA1_destroy)
        if data:
            self.update(data)
            return None

    
    def update(self, data):
        '''Continue hashing of a message by consuming the next chunk of data.

        Args:
            data (byte string/byte array/memoryview): The next chunk of the message being hashed.
        '''
        result = _raw_sha1_lib.SHA1_update(self._state.get(), c_uint8_ptr(data), c_size_t(len(data)))
        if result:
            raise ValueError('Error %d while instantiating SHA1' % result)

    
    def digest(self):
        '''Return the **binary** (non-printable) digest of the message that has been hashed so far.

        :return: The hash digest, computed over the data processed so far.
                 Binary form.
        :rtype: byte string
        '''
        bfr = create_string_buffer(self.digest_size)
        result = _raw_sha1_lib.SHA1_digest(self._state.get(), bfr)
        if result:
            raise ValueError('Error %d while instantiating SHA1' % result)
        return None(bfr)

    
    def hexdigest(self):
        '''Return the **printable** digest of the message that has been hashed so far.

        :return: The hash digest, computed over the data processed so far.
                 Hexadecimal encoded.
        :rtype: string
        '''
        return ''.join((lambda .0: [ '%02x' % bord(x) for x in .0 ])(self.digest()))

    
    def copy(self):
        '''Return a copy ("clone") of the hash object.

        The copy will have the same internal state as the original hash
        object.
        This can be used to efficiently compute the digests of strings that
        share a common initial substring.

        :return: A hash object of the same type
        '''
        clone = SHA1Hash()
        result = _raw_sha1_lib.SHA1_copy(self._state.get(), clone._state.get())
        if result:
            raise ValueError('Error %d while copying SHA1' % result)

    
    def new(self, data = (None,)):
        '''Create a fresh SHA-1 hash object.'''
        return SHA1Hash(data)



def new(data = (None,)):
    '''Create a new hash object.

    :parameter data:
        Optional. The very first chunk of the message to hash.
        It is equivalent to an early call to :meth:`SHA1Hash.update`.
    :type data: byte string/byte array/memoryview

    :Return: A :class:`SHA1Hash` hash object
    '''
    return SHA1Hash().new(data)

digest_size = SHA1Hash.digest_size
block_size = SHA1Hash.block_size

def _pbkdf2_hmac_assist(inner, outer, first_digest, iterations):
    '''Compute the expensive inner loop in PBKDF-HMAC.'''
    pass
# WARNING: Decompyle incomplete

