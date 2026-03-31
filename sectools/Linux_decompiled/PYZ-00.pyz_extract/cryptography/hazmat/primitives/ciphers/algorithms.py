
from __future__ import annotations
from cryptography import utils
from cryptography.hazmat.decrepit.ciphers.algorithms import ARC4
from cryptography.hazmat.decrepit.ciphers.algorithms import CAST5
from cryptography.hazmat.decrepit.ciphers.algorithms import IDEA
from cryptography.hazmat.decrepit.ciphers.algorithms import SEED
from cryptography.hazmat.decrepit.ciphers.algorithms import Blowfish
from cryptography.hazmat.decrepit.ciphers.algorithms import TripleDES
from cryptography.hazmat.primitives._cipheralgorithm import _verify_key_size
from cryptography.hazmat.primitives.ciphers import BlockCipherAlgorithm, CipherAlgorithm

class AES(BlockCipherAlgorithm):
    name = 'AES'
    block_size = 128
    key_sizes = frozenset([
        128,
        192,
        256,
        512])
    
    def __init__(self = None, key = None):
        self.key = _verify_key_size(self, key)

    
    def key_size(self = None):
        return len(self.key) * 8

    key_size = None(key_size)


class AES128(BlockCipherAlgorithm):
    name = 'AES'
    block_size = 128
    key_sizes = frozenset([
        128])
    key_size = 128
    
    def __init__(self = None, key = None):
        self.key = _verify_key_size(self, key)



class AES256(BlockCipherAlgorithm):
    name = 'AES'
    block_size = 128
    key_sizes = frozenset([
        256])
    key_size = 256
    
    def __init__(self = None, key = None):
        self.key = _verify_key_size(self, key)



class Camellia(BlockCipherAlgorithm):
    name = 'camellia'
    block_size = 128
    key_sizes = frozenset([
        128,
        192,
        256])
    
    def __init__(self = None, key = None):
        self.key = _verify_key_size(self, key)

    
    def key_size(self = None):
        return len(self.key) * 8

    key_size = None(key_size)

utils.deprecated(ARC4, __name__, 'ARC4 has been moved to cryptography.hazmat.decrepit.ciphers.algorithms.ARC4 and will be removed from this module in 48.0.0.', utils.DeprecatedIn43, 'ARC4', **('name',))
utils.deprecated(TripleDES, __name__, 'TripleDES has been moved to cryptography.hazmat.decrepit.ciphers.algorithms.TripleDES and will be removed from this module in 48.0.0.', utils.DeprecatedIn43, 'TripleDES', **('name',))
utils.deprecated(Blowfish, __name__, 'Blowfish has been moved to cryptography.hazmat.decrepit.ciphers.algorithms.Blowfish and will be removed from this module in 45.0.0.', utils.DeprecatedIn37, 'Blowfish', **('name',))
utils.deprecated(CAST5, __name__, 'CAST5 has been moved to cryptography.hazmat.decrepit.ciphers.algorithms.CAST5 and will be removed from this module in 45.0.0.', utils.DeprecatedIn37, 'CAST5', **('name',))
utils.deprecated(IDEA, __name__, 'IDEA has been moved to cryptography.hazmat.decrepit.ciphers.algorithms.IDEA and will be removed from this module in 45.0.0.', utils.DeprecatedIn37, 'IDEA', **('name',))
utils.deprecated(SEED, __name__, 'SEED has been moved to cryptography.hazmat.decrepit.ciphers.algorithms.SEED and will be removed from this module in 45.0.0.', utils.DeprecatedIn37, 'SEED', **('name',))

class ChaCha20(CipherAlgorithm):
    name = 'ChaCha20'
    key_sizes = frozenset([
        256])
    
    def __init__(self = None, key = None, nonce = None):
        self.key = _verify_key_size(self, key)
        utils._check_byteslike('nonce', nonce)
        if len(nonce) != 16:
            raise ValueError('nonce must be 128-bits (16 bytes)')
        self._nonce = None

    
    def nonce(self = None):
        return self._nonce

    nonce = None(nonce)
    
    def key_size(self = None):
        return len(self.key) * 8

    key_size = None(key_size)


class SM4(BlockCipherAlgorithm):
    name = 'SM4'
    block_size = 128
    key_sizes = frozenset([
        128])
    
    def __init__(self = None, key = None):
        self.key = _verify_key_size(self, key)

    
    def key_size(self = None):
        return len(self.key) * 8

    key_size = None(key_size)

