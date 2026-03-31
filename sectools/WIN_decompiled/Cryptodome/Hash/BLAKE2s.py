
from binascii import unhexlify
from Cryptodome.Util.py3compat import bord, tobytes
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util._raw_api import load_pycryptodome_raw_lib, VoidPointer, SmartPointer, create_string_buffer, get_raw_buffer, c_size_t, c_uint8_ptr
_raw_blake2s_lib = load_pycryptodome_raw_lib('Cryptodome.Hash._BLAKE2s', '\n                        int blake2s_init(void **state,\n                                         const uint8_t *key,\n                                         size_t key_size,\n                                         size_t digest_size);\n                        int blake2s_destroy(void *state);\n                        int blake2s_update(void *state,\n                                           const uint8_t *buf,\n                                           size_t len);\n                        int blake2s_digest(const void *state,\n                                           uint8_t digest[32]);\n                        int blake2s_copy(const void *src, void *dst);\n                        ')

class BLAKE2s_Hash(object):
    '''A BLAKE2s hash object.
    Do not instantiate directly. Use the :func:`new` function.

    :ivar oid: ASN.1 Object ID
    :vartype oid: string

    :ivar block_size: the size in bytes of the internal message block,
                      input to the compression function
    :vartype block_size: integer

    :ivar digest_size: the size in bytes of the resulting hash
    :vartype digest_size: integer
    '''
    block_size = 32
    
    def __init__(self, data, key, digest_bytes, update_after_digest):
        self.digest_size = digest_bytes
        self._update_after_digest = update_after_digest
        self._digest_done = False
        if not digest_bytes in (16, 20, 28, 32) and key:
            self.oid = '1.3.6.1.4.1.1722.12.2.2.' + str(digest_bytes)
        state = VoidPointer()
        result = _raw_blake2s_lib.blake2s_init(state.address_of(), c_uint8_ptr(key), c_size_t(len(key)), c_size_t(digest_bytes))
        if result:
            raise ValueError('Error %d while instantiating BLAKE2s' % result)
        self._state = None(state.get(), _raw_blake2s_lib.blake2s_destroy)
        if data:
            self.update(data)
            return None

    
    def update(self, data):
        '''Continue hashing of a message by consuming the next chunk of data.

        Args:
            data (byte string/byte array/memoryview): The next chunk of the message being hashed.
        '''
        if not self._digest_done and self._update_after_digest:
            raise TypeError("You can only call 'digest' or 'hexdigest' on this object")
        result = None.blake2s_update(self._state.get(), c_uint8_ptr(data), c_size_t(len(data)))
        if result:
            raise ValueError('Error %d while hashing BLAKE2s data' % result)

    
    def digest(self):
        '''Return the **binary** (non-printable) digest of the message that has been hashed so far.

        :return: The hash digest, computed over the data processed so far.
                 Binary form.
        :rtype: byte string
        '''
        bfr = create_string_buffer(32)
        result = _raw_blake2s_lib.blake2s_digest(self._state.get(), bfr)
        if result:
            raise ValueError('Error %d while creating BLAKE2s digest' % result)
        self._digest_done = None
        return get_raw_buffer(bfr)[:self.digest_size]

    
    def hexdigest(self):
        '''Return the **printable** digest of the message that has been hashed so far.

        :return: The hash digest, computed over the data processed so far.
                 Hexadecimal encoded.
        :rtype: string
        '''
        return ''.join((lambda .0: [ '%02x' % bord(x) for x in .0 ])(tuple(self.digest())))

    
    def verify(self, mac_tag):
        '''Verify that a given **binary** MAC (computed by another party)
        is valid.

        Args:
          mac_tag (byte string/byte array/memoryview): the expected MAC of the message.

        Raises:
            ValueError: if the MAC does not match. It means that the message
                has been tampered with or that the MAC key is incorrect.
        '''
        secret = get_random_bytes(16)
        mac1 = new(160, secret, mac_tag, **('digest_bits', 'key', 'data'))
        mac2 = new(160, secret, self.digest(), **('digest_bits', 'key', 'data'))
        if mac1.digest() != mac2.digest():
            raise ValueError('MAC check failed')

    
    def hexverify(self, hex_mac_tag):
        '''Verify that a given **printable** MAC (computed by another party)
        is valid.

        Args:
            hex_mac_tag (string): the expected MAC of the message, as a hexadecimal string.

        Raises:
            ValueError: if the MAC does not match. It means that the message
                has been tampered with or that the MAC key is incorrect.
        '''
        self.verify(unhexlify(tobytes(hex_mac_tag)))

    
    def new(self, **kwargs):
        '''Return a new instance of a BLAKE2s hash object.
        See :func:`new`.
        '''
        if 'digest_bytes' not in kwargs and 'digest_bits' not in kwargs:
            kwargs['digest_bytes'] = self.digest_size
    # WARNING: Decompyle incomplete



def new(**kwargs):
    '''Create a new hash object.

    Args:
        data (byte string/byte array/memoryview):
            Optional. The very first chunk of the message to hash.
            It is equivalent to an early call to :meth:`BLAKE2s_Hash.update`.
        digest_bytes (integer):
            Optional. The size of the digest, in bytes (1 to 32). Default is 32.
        digest_bits (integer):
            Optional and alternative to ``digest_bytes``.
            The size of the digest, in bits (8 to 256, in steps of 8).
            Default is 256.
        key (byte string):
            Optional. The key to use to compute the MAC (1 to 64 bytes).
            If not specified, no key will be used.
        update_after_digest (boolean):
            Optional. By default, a hash object cannot be updated anymore after
            the digest is computed. When this flag is ``True``, such check
            is no longer enforced.

    Returns:
        A :class:`BLAKE2s_Hash` hash object
    '''
    data = kwargs.pop('data', None)
    update_after_digest = kwargs.pop('update_after_digest', False)
    digest_bytes = kwargs.pop('digest_bytes', None)
    digest_bits = kwargs.pop('digest_bits', None)
    if None not in (digest_bytes, digest_bits):
        raise TypeError('Only one digest parameter must be provided')
    if None == (digest_bytes, digest_bits):
        digest_bytes = 32
    if digest_bytes is not None:
        if not digest_bytes <= digest_bytes or digest_bytes <= 32:
            raise ValueError("'digest_bytes' not in range 1..32")
        raise ValueError("'digest_bytes' not in range 1..32")
    if digest_bits <= digest_bits or digest_bits <= 256:
        pass
    else:
        8
        raise ValueError("'digest_bytes' not in range 8..256, with steps of 8")
    if 8 % 8:
        raise ValueError("'digest_bytes' not in range 8..256, with steps of 8")
    digest_bytes = None // 8
    key = kwargs.pop('key', b'')
    if len(key) > 32:
        raise ValueError('BLAKE2s key cannot exceed 32 bytes')
    if None:
        raise TypeError('Unknown parameters: ' + str(kwargs))
    return None(data, key, digest_bytes, update_after_digest)

