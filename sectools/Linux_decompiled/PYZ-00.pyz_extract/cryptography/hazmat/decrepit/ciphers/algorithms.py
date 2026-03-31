
from __future__ import annotations
from cryptography.hazmat.primitives._cipheralgorithm import BlockCipherAlgorithm, CipherAlgorithm, _verify_key_size

class ARC4(CipherAlgorithm):
    name = 'RC4'
    key_sizes = frozenset([
        40,
        56,
        64,
        80,
        128,
        160,
        192,
        256])
    
    def __init__(self = None, key = None):
        self.key = _verify_key_size(self, key)

    
    def key_size(self = None):
        return len(self.key) * 8

    key_size = None(key_size)


class TripleDES(BlockCipherAlgorithm):
    name = '3DES'
    block_size = 64
    key_sizes = frozenset([
        64,
        128,
        192])
    
    def __init__(self = None, key = None):
        if len(key) == 8:
            key += key + key
        elif len(key) == 16:
            key += key[:8]
        self.key = _verify_key_size(self, key)

    
    def key_size(self = None):
        return len(self.key) * 8

    key_size = None(key_size)


class Blowfish(BlockCipherAlgorithm):
    name = 'Blowfish'
    block_size = 64
    key_sizes = frozenset(range(32, 449, 8))
    
    def __init__(self = None, key = None):
        self.key = _verify_key_size(self, key)

    
    def key_size(self = None):
        return len(self.key) * 8

    key_size = None(key_size)


class CAST5(BlockCipherAlgorithm):
    name = 'CAST5'
    block_size = 64
    key_sizes = frozenset(range(40, 129, 8))
    
    def __init__(self = None, key = None):
        self.key = _verify_key_size(self, key)

    
    def key_size(self = None):
        return len(self.key) * 8

    key_size = None(key_size)


class SEED(BlockCipherAlgorithm):
    name = 'SEED'
    block_size = 128
    key_sizes = frozenset([
        128])
    
    def __init__(self = None, key = None):
        self.key = _verify_key_size(self, key)

    
    def key_size(self = None):
        return len(self.key) * 8

    key_size = None(key_size)


class IDEA(BlockCipherAlgorithm):
    name = 'IDEA'
    block_size = 64
    key_sizes = frozenset([
        128])
    
    def __init__(self = None, key = None):
        self.key = _verify_key_size(self, key)

    
    def key_size(self = None):
        return len(self.key) * 8

    key_size = None(key_size)


class RC2(BlockCipherAlgorithm):
    name = 'RC2'
    block_size = 64
    key_sizes = frozenset([
        128])
    
    def __init__(self = None, key = None):
        self.key = _verify_key_size(self, key)

    
    def key_size(self = None):
        return len(self.key) * 8

    key_size = None(key_size)

