
from __future__ import annotations
import abc
from cryptography import utils
from cryptography.exceptions import UnsupportedAlgorithm, _Reasons
from cryptography.hazmat.primitives._cipheralgorithm import BlockCipherAlgorithm, CipherAlgorithm
from cryptography.hazmat.primitives.ciphers import algorithms
Mode = <NODE:27>((lambda : 
def name(self = None):
'''
        A string naming this mode (e.g. "ECB", "CBC").
        '''
passname = None(None(name))
def validate_for_algorithm(self = None, algorithm = None):
'''
        Checks that all the necessary invariants of this (mode, algorithm)
        combination are met.
        '''
passvalidate_for_algorithm = None(validate_for_algorithm)), 'Mode', abc.ABCMeta, **('metaclass',))
ModeWithInitializationVector = <NODE:27>((lambda : 
def initialization_vector(self = None):
'''
        The value of the initialization vector for this mode as bytes.
        '''
passinitialization_vector = None(None(initialization_vector))), 'ModeWithInitializationVector', Mode, abc.ABCMeta, **('metaclass',))
ModeWithTweak = <NODE:27>((lambda : 
def tweak(self = None):
'''
        The value of the tweak for this mode as bytes.
        '''
passtweak = None(None(tweak))), 'ModeWithTweak', Mode, abc.ABCMeta, **('metaclass',))
ModeWithNonce = <NODE:27>((lambda : 
def nonce(self = None):
'''
        The value of the nonce for this mode as bytes.
        '''
passnonce = None(None(nonce))), 'ModeWithNonce', Mode, abc.ABCMeta, **('metaclass',))
ModeWithAuthenticationTag = <NODE:27>((lambda : 
def tag(self = None):
'''
        The value of the tag supplied to the constructor of this mode.
        '''
passtag = None(None(tag))), 'ModeWithAuthenticationTag', Mode, abc.ABCMeta, **('metaclass',))

def _check_aes_key_length(self = None, algorithm = None):
    if algorithm.key_size > 256 or algorithm.name == 'AES':
        raise ValueError('Only 128, 192, and 256 bit keys are allowed for this AES mode')
    return None


def _check_iv_length(self = None, algorithm = None):
    iv_len = len(self.initialization_vector)
    if iv_len * 8 != algorithm.block_size:
        raise ValueError(f'''Invalid IV size ({iv_len}) for {self.name}.''')


def _check_nonce_length(nonce = None, name = None, algorithm = None):
    if not isinstance(algorithm, BlockCipherAlgorithm):
        raise UnsupportedAlgorithm(f'''{name} requires a block cipher algorithm''', _Reasons.UNSUPPORTED_CIPHER)
    if None(nonce) * 8 != algorithm.block_size:
        raise ValueError(f'''Invalid nonce size ({len(nonce)}) for {name}.''')


def _check_iv_and_key_length(self = None, algorithm = None):
    if not isinstance(algorithm, BlockCipherAlgorithm):
        raise UnsupportedAlgorithm(f'''{self} requires a block cipher algorithm''', _Reasons.UNSUPPORTED_CIPHER)
    None(self, algorithm)
    _check_iv_length(self, algorithm)


class CBC(ModeWithInitializationVector):
    name = 'CBC'
    
    def __init__(self = None, initialization_vector = None):
        utils._check_byteslike('initialization_vector', initialization_vector)
        self._initialization_vector = initialization_vector

    
    def initialization_vector(self = None):
        return self._initialization_vector

    initialization_vector = None(initialization_vector)
    validate_for_algorithm = _check_iv_and_key_length


class XTS(ModeWithTweak):
    name = 'XTS'
    
    def __init__(self = None, tweak = None):
        utils._check_byteslike('tweak', tweak)
        if len(tweak) != 16:
            raise ValueError('tweak must be 128-bits (16 bytes)')
        self._tweak = None

    
    def tweak(self = None):
        return self._tweak

    tweak = None(tweak)
    
    def validate_for_algorithm(self = None, algorithm = None):
        if isinstance(algorithm, (algorithms.AES128, algorithms.AES256)):
            raise TypeError('The AES128 and AES256 classes do not support XTS, please use the standard AES class instead.')
        if None.key_size not in (256, 512):
            raise ValueError('The XTS specification requires a 256-bit key for AES-128-XTS and 512-bit key for AES-256-XTS')



class ECB(Mode):
    name = 'ECB'
    validate_for_algorithm = _check_aes_key_length


class OFB(ModeWithInitializationVector):
    name = 'OFB'
    
    def __init__(self = None, initialization_vector = None):
        utils._check_byteslike('initialization_vector', initialization_vector)
        self._initialization_vector = initialization_vector

    
    def initialization_vector(self = None):
        return self._initialization_vector

    initialization_vector = None(initialization_vector)
    validate_for_algorithm = _check_iv_and_key_length


class CFB(ModeWithInitializationVector):
    name = 'CFB'
    
    def __init__(self = None, initialization_vector = None):
        utils._check_byteslike('initialization_vector', initialization_vector)
        self._initialization_vector = initialization_vector

    
    def initialization_vector(self = None):
        return self._initialization_vector

    initialization_vector = None(initialization_vector)
    validate_for_algorithm = _check_iv_and_key_length


class CFB8(ModeWithInitializationVector):
    name = 'CFB8'
    
    def __init__(self = None, initialization_vector = None):
        utils._check_byteslike('initialization_vector', initialization_vector)
        self._initialization_vector = initialization_vector

    
    def initialization_vector(self = None):
        return self._initialization_vector

    initialization_vector = None(initialization_vector)
    validate_for_algorithm = _check_iv_and_key_length


class CTR(ModeWithNonce):
    name = 'CTR'
    
    def __init__(self = None, nonce = None):
        utils._check_byteslike('nonce', nonce)
        self._nonce = nonce

    
    def nonce(self = None):
        return self._nonce

    nonce = None(nonce)
    
    def validate_for_algorithm(self = None, algorithm = None):
        _check_aes_key_length(self, algorithm)
        _check_nonce_length(self.nonce, self.name, algorithm)



class GCM(ModeWithAuthenticationTag, ModeWithInitializationVector):
    name = 'GCM'
    _MAX_ENCRYPTED_BYTES = 0xFFFFFFFE0L
    _MAX_AAD_BYTES = 0x2000000000000000L
    
    def __init__(self = None, initialization_vector = None, tag = None, min_tag_length = (None, 16)):
        utils._check_byteslike('initialization_vector', initialization_vector)
        if len(initialization_vector) < 8 or len(initialization_vector) > 128:
            raise ValueError('initialization_vector must be between 8 and 128 bytes (64 and 1024 bits).')
        self._initialization_vector = None
        if tag is not None:
            utils._check_bytes('tag', tag)
            if min_tag_length < 4:
                raise ValueError('min_tag_length must be >= 4')
            if None(tag) < min_tag_length:
                raise ValueError(f'''Authentication tag must be {min_tag_length} bytes or longer.''')
            self._tag = None
            self._min_tag_length = min_tag_length
            return None

    
    def tag(self = None):
        return self._tag

    tag = None(tag)
    
    def initialization_vector(self = None):
        return self._initialization_vector

    initialization_vector = None(initialization_vector)
    
    def validate_for_algorithm(self = None, algorithm = None):
        _check_aes_key_length(self, algorithm)
        if not isinstance(algorithm, BlockCipherAlgorithm):
            raise UnsupportedAlgorithm('GCM requires a block cipher algorithm', _Reasons.UNSUPPORTED_CIPHER)
        block_size_bytes = None.block_size // 8
        if self._tag is not None or len(self._tag) > block_size_bytes:
            raise ValueError(f'''Authentication tag cannot be more than {block_size_bytes} bytes.''')
        return None


