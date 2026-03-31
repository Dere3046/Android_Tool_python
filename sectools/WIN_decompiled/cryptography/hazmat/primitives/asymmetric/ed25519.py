
from __future__ import annotations
import abc
from cryptography.exceptions import UnsupportedAlgorithm, _Reasons
from cryptography.hazmat.bindings._rust import openssl as rust_openssl
from cryptography.hazmat.primitives import _serialization
Ed25519PublicKey = <NODE:27>((lambda : 
def from_public_bytes(cls = None, data = None):
backend = backendimport cryptography.hazmat.backends.openssl.backendif not backend.ed25519_supported():
raise UnsupportedAlgorithm('ed25519 is not supported by this version of OpenSSL.', _Reasons.UNSUPPORTED_PUBLIC_KEY_ALGORITHM)None.ed25519.from_public_bytes(data)from_public_bytes = None(from_public_bytes)
def public_bytes(self = None, encoding = None, format = abc.abstractmethod):
'''
        The serialized bytes of the public key.
        '''
passpublic_bytes = None(public_bytes)
def public_bytes_raw(self = None):
'''
        The raw bytes of the public key.
        Equivalent to public_bytes(Raw, Raw).
        '''
passpublic_bytes_raw = None(public_bytes_raw)
def verify(self = None, signature = None, data = abc.abstractmethod):
'''
        Verify the signature.
        '''
passverify = None(verify)
def __eq__(self = None, other = None):
'''
        Checks equality.
        '''
pass__eq__ = None(__eq__)), 'Ed25519PublicKey', abc.ABCMeta, **('metaclass',))
Ed25519PublicKey.register(rust_openssl.ed25519.Ed25519PublicKey)
Ed25519PrivateKey = <NODE:27>((lambda : 
def generate(cls = None):
backend = backendimport cryptography.hazmat.backends.openssl.backendif not backend.ed25519_supported():
raise UnsupportedAlgorithm('ed25519 is not supported by this version of OpenSSL.', _Reasons.UNSUPPORTED_PUBLIC_KEY_ALGORITHM)None.ed25519.generate_key()generate = None(generate)
def from_private_bytes(cls = None, data = None):
backend = backendimport cryptography.hazmat.backends.openssl.backendif not backend.ed25519_supported():
raise UnsupportedAlgorithm('ed25519 is not supported by this version of OpenSSL.', _Reasons.UNSUPPORTED_PUBLIC_KEY_ALGORITHM)None.ed25519.from_private_bytes(data)from_private_bytes = None(from_private_bytes)
def public_key(self = None):
'''
        The Ed25519PublicKey derived from the private key.
        '''
passpublic_key = None(public_key)
def private_bytes(self = None, encoding = None, format = abc.abstractmethod, encryption_algorithm = ('encoding', '_serialization.Encoding', 'format', '_serialization.PrivateFormat', 'encryption_algorithm', '_serialization.KeySerializationEncryption', 'return', 'bytes')):
'''
        The serialized bytes of the private key.
        '''
passprivate_bytes = None(private_bytes)
def private_bytes_raw(self = None):
'''
        The raw bytes of the private key.
        Equivalent to private_bytes(Raw, Raw, NoEncryption()).
        '''
passprivate_bytes_raw = None(private_bytes_raw)
def sign(self = None, data = None):
'''
        Signs the data.
        '''
passsign = None(sign)), 'Ed25519PrivateKey', abc.ABCMeta, **('metaclass',))
Ed25519PrivateKey.register(rust_openssl.ed25519.Ed25519PrivateKey)
