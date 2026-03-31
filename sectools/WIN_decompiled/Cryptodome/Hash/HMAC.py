
from Cryptodome.Util.py3compat import bord, tobytes
from binascii import unhexlify
from Cryptodome.Hash import MD5
from Cryptodome.Hash import BLAKE2s
from Cryptodome.Util.strxor import strxor
from Cryptodome.Random import get_random_bytes
__all__ = [
    'new',
    'HMAC']

class HMAC(object):
    '''An HMAC hash object.
    Do not instantiate directly. Use the :func:`new` function.

    :ivar digest_size: the size in bytes of the resulting MAC tag
    :vartype digest_size: integer
    '''
    
    def __init__(self, key, msg, digestmod = (b'', None)):
        if digestmod is None:
            digestmod = MD5
        if msg is None:
            msg = b''
        self.digest_size = digestmod.digest_size
        self._digestmod = digestmod
        if isinstance(key, memoryview):
            key = key.tobytes()
    # WARNING: Decompyle incomplete

    
    def update(self, msg):
        '''Authenticate the next chunk of message.

        Args:
            data (byte string/byte array/memoryview): The next chunk of data
        '''
        self._inner.update(msg)
        return self

    
    def _pbkdf2_hmac_assist(self, first_digest, iterations):
        '''Carry out the expensive inner loop for PBKDF2-HMAC'''
        result = self._digestmod._pbkdf2_hmac_assist(self._inner, self._outer, first_digest, iterations)
        return result

    
    def copy(self):
        '''Return a copy ("clone") of the HMAC object.

        The copy will have the same internal state as the original HMAC
        object.
        This can be used to efficiently compute the MAC tag of byte
        strings that share a common initial substring.

        :return: An :class:`HMAC`
        '''
        new_hmac = HMAC(b'fake key', self._digestmod, **('digestmod',))
        new_hmac._inner = self._inner.copy()
        new_hmac._outer = self._outer.copy()
        return new_hmac

    
    def digest(self):
        '''Return the **binary** (non-printable) MAC tag of the message
        authenticated so far.

        :return: The MAC tag digest, computed over the data processed so far.
                 Binary form.
        :rtype: byte string
        '''
        frozen_outer_hash = self._outer.copy()
        frozen_outer_hash.update(self._inner.digest())
        return frozen_outer_hash.digest()

    
    def verify(self, mac_tag):
        '''Verify that a given **binary** MAC (computed by another party)
        is valid.

        Args:
          mac_tag (byte string/byte string/memoryview): the expected MAC of the message.

        Raises:
            ValueError: if the MAC does not match. It means that the message
                has been tampered with or that the MAC key is incorrect.
        '''
        secret = get_random_bytes(16)
        mac1 = BLAKE2s.new(160, secret, mac_tag, **('digest_bits', 'key', 'data'))
        mac2 = BLAKE2s.new(160, secret, self.digest(), **('digest_bits', 'key', 'data'))
        if mac1.digest() != mac2.digest():
            raise ValueError('MAC check failed')

    
    def hexdigest(self):
        '''Return the **printable** MAC tag of the message authenticated so far.

        :return: The MAC tag, computed over the data processed so far.
                 Hexadecimal encoded.
        :rtype: string
        '''
        return ''.join((lambda .0: [ '%02x' % bord(x) for x in .0 ])(tuple(self.digest())))

    
    def hexverify(self, hex_mac_tag):
        '''Verify that a given **printable** MAC (computed by another party)
        is valid.

        Args:
            hex_mac_tag (string): the expected MAC of the message,
                as a hexadecimal string.

        Raises:
            ValueError: if the MAC does not match. It means that the message
                has been tampered with or that the MAC key is incorrect.
        '''
        self.verify(unhexlify(tobytes(hex_mac_tag)))



def new(key, msg, digestmod = (b'', None)):
    '''Create a new MAC object.

    Args:
        key (bytes/bytearray/memoryview):
            key for the MAC object.
            It must be long enough to match the expected security level of the
            MAC.
        msg (bytes/bytearray/memoryview):
            Optional. The very first chunk of the message to authenticate.
            It is equivalent to an early call to :meth:`HMAC.update`.
        digestmod (module):
            The hash to use to implement the HMAC.
            Default is :mod:`Cryptodome.Hash.MD5`.

    Returns:
        An :class:`HMAC` object
    '''
    return HMAC(key, msg, digestmod)

