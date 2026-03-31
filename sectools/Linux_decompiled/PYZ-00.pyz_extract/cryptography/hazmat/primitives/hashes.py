
from __future__ import annotations
import abc
from cryptography.hazmat.bindings._rust import openssl as rust_openssl
__all__ = [
    'MD5',
    'SHA1',
    'SHA3_224',
    'SHA3_256',
    'SHA3_384',
    'SHA3_512',
    'SHA224',
    'SHA256',
    'SHA384',
    'SHA512',
    'SHA512_224',
    'SHA512_256',
    'SHAKE128',
    'SHAKE256',
    'SM3',
    'BLAKE2b',
    'BLAKE2s',
    'ExtendableOutputFunction',
    'Hash',
    'HashAlgorithm',
    'HashContext']
HashAlgorithm = <NODE:27>((lambda : 
def name(self = None):
'''
        A string naming this algorithm (e.g. "sha256", "md5").
        '''
passname = None(None(name))
def digest_size(self = None):
'''
        The size of the resulting digest in bytes.
        '''
passdigest_size = None(None(digest_size))
def block_size(self = None):
'''
        The internal block size of the hash function, or None if the hash
        function does not use blocks internally (e.g. SHA3).
        '''
passblock_size = None(None(block_size))), 'HashAlgorithm', abc.ABCMeta, **('metaclass',))
HashContext = <NODE:27>((lambda : 
def algorithm(self = None):
'''
        A HashAlgorithm that will be used by this context.
        '''
passalgorithm = None(None(algorithm))
def update(self = None, data = None):
'''
        Processes the provided bytes through the hash.
        '''
passupdate = None(update)
def finalize(self = None):
'''
        Finalizes the hash context and returns the hash digest as bytes.
        '''
passfinalize = None(finalize)
def copy(self = None):
'''
        Return a HashContext that is a copy of the current context.
        '''
passcopy = None(copy)), 'HashContext', abc.ABCMeta, **('metaclass',))
Hash = rust_openssl.hashes.Hash
HashContext.register(Hash)
ExtendableOutputFunction = <NODE:27>((lambda : __doc__ = '\n    An interface for extendable output functions.\n    '), 'ExtendableOutputFunction', abc.ABCMeta, **('metaclass',))

class SHA1(HashAlgorithm):
    name = 'sha1'
    digest_size = 20
    block_size = 64


class SHA512_224(HashAlgorithm):
    name = 'sha512-224'
    digest_size = 28
    block_size = 128


class SHA512_256(HashAlgorithm):
    name = 'sha512-256'
    digest_size = 32
    block_size = 128


class SHA224(HashAlgorithm):
    name = 'sha224'
    digest_size = 28
    block_size = 64


class SHA256(HashAlgorithm):
    name = 'sha256'
    digest_size = 32
    block_size = 64


class SHA384(HashAlgorithm):
    name = 'sha384'
    digest_size = 48
    block_size = 128


class SHA512(HashAlgorithm):
    name = 'sha512'
    digest_size = 64
    block_size = 128


class SHA3_224(HashAlgorithm):
    name = 'sha3-224'
    digest_size = 28
    block_size = None


class SHA3_256(HashAlgorithm):
    name = 'sha3-256'
    digest_size = 32
    block_size = None


class SHA3_384(HashAlgorithm):
    name = 'sha3-384'
    digest_size = 48
    block_size = None


class SHA3_512(HashAlgorithm):
    name = 'sha3-512'
    digest_size = 64
    block_size = None


class SHAKE128(ExtendableOutputFunction, HashAlgorithm):
    name = 'shake128'
    block_size = None
    
    def __init__(self = None, digest_size = None):
        if not isinstance(digest_size, int):
            raise TypeError('digest_size must be an integer')
        if None < 1:
            raise ValueError('digest_size must be a positive integer')
        self._digest_size = None

    
    def digest_size(self = None):
        return self._digest_size

    digest_size = None(digest_size)


class SHAKE256(ExtendableOutputFunction, HashAlgorithm):
    name = 'shake256'
    block_size = None
    
    def __init__(self = None, digest_size = None):
        if not isinstance(digest_size, int):
            raise TypeError('digest_size must be an integer')
        if None < 1:
            raise ValueError('digest_size must be a positive integer')
        self._digest_size = None

    
    def digest_size(self = None):
        return self._digest_size

    digest_size = None(digest_size)


class MD5(HashAlgorithm):
    name = 'md5'
    digest_size = 16
    block_size = 64


class BLAKE2b(HashAlgorithm):
    name = 'blake2b'
    _max_digest_size = 64
    _min_digest_size = 1
    block_size = 128
    
    def __init__(self = None, digest_size = None):
        if digest_size != 64:
            raise ValueError('Digest size must be 64')
        self._digest_size = None

    
    def digest_size(self = None):
        return self._digest_size

    digest_size = None(digest_size)


class BLAKE2s(HashAlgorithm):
    name = 'blake2s'
    block_size = 64
    _max_digest_size = 32
    _min_digest_size = 1
    
    def __init__(self = None, digest_size = None):
        if digest_size != 32:
            raise ValueError('Digest size must be 32')
        self._digest_size = None

    
    def digest_size(self = None):
        return self._digest_size

    digest_size = None(digest_size)


class SM3(HashAlgorithm):
    name = 'sm3'
    digest_size = 32
    block_size = 64

