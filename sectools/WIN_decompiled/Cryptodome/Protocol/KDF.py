
import re
import struct
from functools import reduce
from Cryptodome.Util.py3compat import tobytes, bord, _copy_bytes, iter_range, tostr, bchr, bstr
from Cryptodome.Hash import SHA1, SHA256, HMAC, CMAC, BLAKE2s
from Cryptodome.Util.strxor import strxor
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.number import size as bit_size, long_to_bytes, bytes_to_long
from Cryptodome.Util._raw_api import load_pycryptodome_raw_lib, create_string_buffer, get_raw_buffer, c_size_t
_raw_salsa20_lib = load_pycryptodome_raw_lib('Cryptodome.Cipher._Salsa20', '\n                    int Salsa20_8_core(const uint8_t *x, const uint8_t *y,\n                                       uint8_t *out);\n                    ')
_raw_scrypt_lib = load_pycryptodome_raw_lib('Cryptodome.Protocol._scrypt', '\n                    typedef int (core_t)(const uint8_t [64], const uint8_t [64], uint8_t [64]);\n                    int scryptROMix(const uint8_t *data_in, uint8_t *data_out,\n                           size_t data_len, unsigned N, core_t *core);\n                    ')

def PBKDF1(password, salt, dkLen, count, hashAlgo = (1000, None)):
    '''Derive one key from a password (or passphrase).

    This function performs key derivation according to an old version of
    the PKCS#5 standard (v1.5) or `RFC2898
    <https://www.ietf.org/rfc/rfc2898.txt>`_.

    Args:
     password (string):
        The secret password to generate the key from.
     salt (byte string):
        An 8 byte string to use for better protection from dictionary attacks.
        This value does not need to be kept secret, but it should be randomly
        chosen for each derivation.
     dkLen (integer):
        The length of the desired key. The default is 16 bytes, suitable for
        instance for :mod:`Cryptodome.Cipher.AES`.
     count (integer):
        The number of iterations to carry out. The recommendation is 1000 or
        more.
     hashAlgo (module):
        The hash algorithm to use, as a module or an object from the :mod:`Cryptodome.Hash` package.
        The digest length must be no shorter than ``dkLen``.
        The default algorithm is :mod:`Cryptodome.Hash.SHA1`.

    Return:
        A byte string of length ``dkLen`` that can be used as key.
    '''
    if not hashAlgo:
        hashAlgo = SHA1
    password = tobytes(password)
    pHash = hashAlgo.new(password + salt)
    digest = pHash.digest_size
    if dkLen > digest:
        raise TypeError('Selected hash algorithm has a too short digest (%d bytes).' % digest)
    if None(salt) != 8:
        raise ValueError('Salt is not 8 bytes long (%d bytes instead).' % len(salt))
    for i in None(count - 1):
        pHash = pHash.new(pHash.digest())
    return pHash.digest()[:dkLen]


def PBKDF2(password, salt, dkLen, count, prf, hmac_hash_module = (16, 1000, None, None)):
    '''Derive one or more keys from a password (or passphrase).

    This function performs key derivation according to the PKCS#5 standard (v2.0).

    Args:
     password (string or byte string):
        The secret password to generate the key from.
     salt (string or byte string):
        A (byte) string to use for better protection from dictionary attacks.
        This value does not need to be kept secret, but it should be randomly
        chosen for each derivation. It is recommended to use at least 16 bytes.
     dkLen (integer):
        The cumulative length of the keys to produce.

        Due to a flaw in the PBKDF2 design, you should not request more bytes
        than the ``prf`` can output. For instance, ``dkLen`` should not exceed
        20 bytes in combination with ``HMAC-SHA1``.
     count (integer):
        The number of iterations to carry out. The higher the value, the slower
        and the more secure the function becomes.

        You should find the maximum number of iterations that keeps the
        key derivation still acceptable on the slowest hardware you must support.

        Although the default value is 1000, **it is recommended to use at least
        1000000 (1 million) iterations**.
     prf (callable):
        A pseudorandom function. It must be a function that returns a
        pseudorandom byte string from two parameters: a secret and a salt.
        The slower the algorithm, the more secure the derivation function.
        If not specified, **HMAC-SHA1** is used.
     hmac_hash_module (module):
        A module from ``Cryptodome.Hash`` implementing a Merkle-Damgard cryptographic
        hash, which PBKDF2 must use in combination with HMAC.
        This parameter is mutually exclusive with ``prf``.

    Return:
        A byte string of length ``dkLen`` that can be used as key material.
        If you want multiple keys, just break up this string into segments of the desired length.
    '''
    password = tobytes(password)
    salt = tobytes(salt)
    if prf and hmac_hash_module:
        raise ValueError("'prf' and 'hmac_hash_module' are mutually exlusive")
    if None is None and hmac_hash_module is None:
        hmac_hash_module = SHA1
    if not prf or hasattr(hmac_hash_module, '_pbkdf2_hmac_assist'):
        if prf is None:
            
            prf = lambda p = None, s = None: HMAC.new(p, s, hmac_hash_module).digest()
        
        def link(s = None):
            s[0] = s[1]
            s[1] = prf(password, s[1])
            return s[0]

        key = b''
        i = 1
        if len(key) < dkLen:
            s = [
                prf(password, salt + struct.pack('>I', i))] * 2
            None += None(None, (lambda .0 = None: for j in .0:
link(s))(range(count)))
            i += 1
            if not len(key) < dkLen:
                pass
            else:
                key = b''
                i = 1
                if len(key) < dkLen:
                    base = HMAC.new(password, b'', hmac_hash_module)
                    first_digest = base.copy().update(salt + struct.pack('>I', i)).digest()
                    key += base._pbkdf2_hmac_assist(first_digest, count)
                    i += 1
                    if not len(key) < dkLen:
                        return key[:dkLen]


class _S2V(object):
    '''String-to-vector PRF as defined in `RFC5297`_.

    This class implements a pseudorandom function family
    based on CMAC that takes as input a vector of strings.

    .. _RFC5297: http://tools.ietf.org/html/rfc5297
    '''
    
    def __init__(self, key, ciphermod, cipher_params = (None,)):
        '''Initialize the S2V PRF.

        :Parameters:
          key : byte string
            A secret that can be used as key for CMACs
            based on ciphers from ``ciphermod``.
          ciphermod : module
            A block cipher module from `Cryptodome.Cipher`.
          cipher_params : dictionary
            A set of extra parameters to use to create a cipher instance.
        '''
        self._key = _copy_bytes(None, None, key)
        self._ciphermod = ciphermod
        self._last_string = self._cache = b'\x00' * ciphermod.block_size
        self._n_updates = ciphermod.block_size * 8 - 1
        if cipher_params is None:
            self._cipher_params = { }
            return None
        self._cipher_params = None(cipher_params)

    
    def new(key, ciphermod):
        '''Create a new S2V PRF.

        :Parameters:
          key : byte string
            A secret that can be used as key for CMACs
            based on ciphers from ``ciphermod``.
          ciphermod : module
            A block cipher module from `Cryptodome.Cipher`.
        '''
        return _S2V(key, ciphermod)

    new = staticmethod(new)
    
    def _double(self, bs):
        doubled = bytes_to_long(bs) << 1
        if bord(bs[0]) & 128:
            doubled ^= 135
        return long_to_bytes(doubled, len(bs))[-len(bs):]

    
    def update(self, item):
        '''Pass the next component of the vector.

        The maximum number of components you can pass is equal to the block
        length of the cipher (in bits) minus 1.

        :Parameters:
          item : byte string
            The next component of the vector.
        :Raise TypeError: when the limit on the number of components has been reached.
        '''
        if self._n_updates == 0:
            raise TypeError('Too many components passed to S2V')
        None._n_updates -= 1
        mac = CMAC.new(self._key, self._last_string, self._ciphermod, self._cipher_params, **('msg', 'ciphermod', 'cipher_params'))
        self._cache = strxor(self._double(self._cache), mac.digest())
        self._last_string = _copy_bytes(None, None, item)

    
    def derive(self):
        '''"Derive a secret from the vector of components.

        :Return: a byte string, as long as the block length of the cipher.
        '''
        if len(self._last_string) >= 16:
            final = self._last_string[:-16] + strxor(self._last_string[-16:], self._cache)
        else:
            padded = self._last_string + b'\x80' + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'[:16]
            final = strxor(padded, self._double(self._cache))
        mac = CMAC.new(self._key, final, self._ciphermod, self._cipher_params, **('msg', 'ciphermod', 'cipher_params'))
        return mac.digest()



def HKDF(master, key_len, salt, hashmod, num_keys, context = (1, None)):
    '''Derive one or more keys from a master secret using
    the HMAC-based KDF defined in RFC5869_.

    Args:
     master (byte string):
        The unguessable value used by the KDF to generate the other keys.
        It must be a high-entropy secret, though not necessarily uniform.
        It must not be a password.
     salt (byte string):
        A non-secret, reusable value that strengthens the randomness
        extraction step.
        Ideally, it is as long as the digest size of the chosen hash.
        If empty, a string of zeroes in used.
     key_len (integer):
        The length in bytes of every derived key.
     hashmod (module):
        A cryptographic hash algorithm from :mod:`Cryptodome.Hash`.
        :mod:`Cryptodome.Hash.SHA512` is a good choice.
     num_keys (integer):
        The number of keys to derive. Every key is :data:`key_len` bytes long.
        The maximum cumulative length of all keys is
        255 times the digest size.
     context (byte string):
        Optional identifier describing what the keys are used for.

    Return:
        A byte string or a tuple of byte strings.

    .. _RFC5869: http://tools.ietf.org/html/rfc5869
    '''
    output_len = key_len * num_keys
    if output_len > 255 * hashmod.digest_size:
        raise ValueError('Too much secret data to derive')
    if not None:
        salt = b'\x00' * hashmod.digest_size
    if context is None:
        context = b''
    hmac = HMAC.new(salt, master, hashmod, **('digestmod',))
    prk = hmac.digest()
    t = [
        b'']
    n = 1
    tlen = 0
    if tlen < output_len:
        hmac = HMAC.new(prk, t[-1] + context + struct.pack('B', n), hashmod, **('digestmod',))
        t.append(hmac.digest())
        tlen += hashmod.digest_size
        n += 1
        if not tlen < output_len:
            derived_output = b''.join(t)
            if num_keys == 1:
                return derived_output[:key_len]
            kol = (lambda .0 = None: [ derived_output[idx:idx + key_len] for idx in .0 ])(iter_range(0, output_len, key_len))
            return list(kol[:num_keys])


def scrypt(password, salt, key_len, N, r, p, num_keys = (1,)):
    '''Derive one or more keys from a passphrase.

    Args:
     password (string):
        The secret pass phrase to generate the keys from.
     salt (string):
        A string to use for better protection from dictionary attacks.
        This value does not need to be kept secret,
        but it should be randomly chosen for each derivation.
        It is recommended to be at least 16 bytes long.
     key_len (integer):
        The length in bytes of every derived key.
     N (integer):
        CPU/Memory cost parameter. It must be a power of 2 and less
        than :math:`2^{32}`.
     r (integer):
        Block size parameter.
     p (integer):
        Parallelization parameter.
        It must be no greater than :math:`(2^{32}-1)/(4r)`.
     num_keys (integer):
        The number of keys to derive. Every key is :data:`key_len` bytes long.
        By default, only 1 key is generated.
        The maximum cumulative length of all keys is :math:`(2^{32}-1)*32`
        (that is, 128TB).

    A good choice of parameters *(N, r , p)* was suggested
    by Colin Percival in his `presentation in 2009`__:

    - *( 2¹⁴, 8, 1 )* for interactive logins (≤100ms)
    - *( 2²⁰, 8, 1 )* for file encryption (≤5s)

    Return:
        A byte string or a tuple of byte strings.

    .. __: http://www.tarsnap.com/scrypt/scrypt-slides.pdf
    '''
    if 2 ** (bit_size(N) - 1) != N:
        raise ValueError('N must be a power of 2')
    if None >= 0x100000000L:
        raise ValueError('N is too big')
    if None > 0x1FFFFFFFE0L // 128 * r:
        raise ValueError('p or r are too big')
    