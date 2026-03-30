
from __future__ import annotations
import abc
from cryptography import utils
CipherAlgorithm = <NODE:27>((lambda : 
def name(self = None):
'''
        A string naming this mode (e.g. "AES", "Camellia").
        '''
passname = None(None(name))
def key_sizes(self = None):
'''
        Valid key sizes for this algorithm in bits
        '''
passkey_sizes = None(None(key_sizes))
def key_size(self = None):
'''
        The size of the key being used as an integer in bits (e.g. 128, 256).
        '''
passkey_size = None(None(key_size))), 'CipherAlgorithm', abc.ABCMeta, **('metaclass',))

class BlockCipherAlgorithm(CipherAlgorithm):
    key: 'bytes' = 'BlockCipherAlgorithm'
    
    def block_size(self = None):
        '''
        The size of a block as an integer in bits (e.g. 64, 128).
        '''
        pass

    block_size = None(None(block_size))


def _verify_key_size(algorithm = None, key = None):
    utils._check_byteslike('key', key)
    if len(key) * 8 not in algorithm.key_sizes:
        raise ValueError(f'''Invalid key size ({len(key) * 8}) for {algorithm.name}.''')

