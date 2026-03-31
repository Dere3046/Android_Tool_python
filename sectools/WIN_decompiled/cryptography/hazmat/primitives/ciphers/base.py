
from __future__ import annotations
import abc
import typing
from cryptography.hazmat.bindings._rust import openssl as rust_openssl
from cryptography.hazmat.primitives._cipheralgorithm import CipherAlgorithm
from cryptography.hazmat.primitives.ciphers import modes
CipherContext = <NODE:27>((lambda : 
def update(self = None, data = None):
'''
        Processes the provided bytes through the cipher and returns the results
        as bytes.
        '''
passupdate = None(update)
def update_into(self = None, data = None, buf = abc.abstractmethod):
'''
        Processes the provided bytes and writes the resulting data into the
        provided buffer. Returns the number of bytes written.
        '''
passupdate_into = None(update_into)
def finalize(self = None):
'''
        Returns the results of processing the final block as bytes.
        '''
passfinalize = None(finalize)
def reset_nonce(self = None, nonce = None):
'''
        Resets the nonce for the cipher context to the provided value.
        Raises an exception if it does not support reset or if the
        provided nonce does not have a valid length.
        '''
passreset_nonce = None(reset_nonce)), 'CipherContext', abc.ABCMeta, **('metaclass',))
AEADCipherContext = <NODE:27>((lambda : 
def authenticate_additional_data(self = None, data = None):
'''
        Authenticates the provided bytes.
        '''
passauthenticate_additional_data = None(authenticate_additional_data)), 'AEADCipherContext', CipherContext, abc.ABCMeta, **('metaclass',))
AEADDecryptionContext = <NODE:27>((lambda : 
def finalize_with_tag(self = None, tag = None):
'''
        Returns the results of processing the final block as bytes and allows
        delayed passing of the authentication tag.
        '''
passfinalize_with_tag = None(finalize_with_tag)), 'AEADDecryptionContext', AEADCipherContext, abc.ABCMeta, **('metaclass',))
AEADEncryptionContext = <NODE:27>((lambda : 
def tag(self = None):
'''
        Returns tag bytes. This is only available after encryption is
        finalized.
        '''
passtag = None(None(tag))), 'AEADEncryptionContext', AEADCipherContext, abc.ABCMeta, **('metaclass',))
Mode = typing.TypeVar('Mode', typing.Optional[modes.Mode], True, **('bound', 'covariant'))

def Cipher():
    '''Cipher'''
    
    def __init__(self = None, algorithm = None, mode = None, backend = (None,)):
        if not isinstance(algorithm, CipherAlgorithm):
            raise TypeError('Expected interface of CipherAlgorithm.')
    # WARNING: Decompyle incomplete

    
    def encryptor(self = None):
        pass

    encryptor = None(encryptor)
    
    def encryptor(self = None):
        pass

    encryptor = None(encryptor)
    
    def encryptor(self):
        if isinstance(self.mode, modes.ModeWithAuthenticationTag) and self.mode.tag is not None:
            raise ValueError('Authentication tag must be None when encrypting.')
        return None.ciphers.create_encryption_ctx(self.algorithm, self.mode)

    
    def decryptor(self = None):
        pass

    decryptor = None(decryptor)
    
    def decryptor(self = None):
        pass

    decryptor = None(decryptor)
    
    def decryptor(self):
        return rust_openssl.ciphers.create_decryption_ctx(self.algorithm, self.mode)


Cipher = <NODE:27>(Cipher, 'Cipher', typing.Generic[Mode])
_CIPHER_TYPE = Cipher[typing.Union[(modes.ModeWithNonce, modes.ModeWithTweak, None, modes.ECB, modes.ModeWithInitializationVector)]]
CipherContext.register(rust_openssl.ciphers.CipherContext)
AEADEncryptionContext.register(rust_openssl.ciphers.AEADEncryptionContext)
AEADDecryptionContext.register(rust_openssl.ciphers.AEADDecryptionContext)
