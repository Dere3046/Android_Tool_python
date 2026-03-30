
from __future__ import annotations
import abc
from cryptography.hazmat.bindings._rust import openssl as rust_openssl
from cryptography.hazmat.primitives import _serialization
generate_parameters = rust_openssl.dh.generate_parameters
DHPrivateNumbers = rust_openssl.dh.DHPrivateNumbers
DHPublicNumbers = rust_openssl.dh.DHPublicNumbers
DHParameterNumbers = rust_openssl.dh.DHParameterNumbers
DHParameters = <NODE:27>((lambda : 
def generate_private_key(self = None):
'''
        Generates and returns a DHPrivateKey.
        '''
passgenerate_private_key = None(generate_private_key)
def parameter_bytes(self = None, encoding = None, format = abc.abstractmethod):
'''
        Returns the parameters serialized as bytes.
        '''
passparameter_bytes = None(parameter_bytes)
def parameter_numbers(self = None):
'''
        Returns a DHParameterNumbers.
        '''
passparameter_numbers = None(parameter_numbers)), 'DHParameters', abc.ABCMeta, **('metaclass',))
DHParametersWithSerialization = DHParameters
DHParameters.register(rust_openssl.dh.DHParameters)
DHPublicKey = <NODE:27>((lambda : 
def key_size(self = None):
'''
        The bit length of the prime modulus.
        '''
passkey_size = None(None(key_size))
def parameters(self = None):
'''
        The DHParameters object associated with this public key.
        '''
passparameters = None(parameters)
def public_numbers(self = None):
'''
        Returns a DHPublicNumbers.
        '''
passpublic_numbers = None(public_numbers)
def public_bytes(self = None, encoding = None, format = abc.abstractmethod):
'''
        Returns the key serialized as bytes.
        '''
passpublic_bytes = None(public_bytes)
def __eq__(self = None, other = None):
'''
        Checks equality.
        '''
pass__eq__ = None(__eq__)), 'DHPublicKey', abc.ABCMeta, **('metaclass',))
DHPublicKeyWithSerialization = DHPublicKey
DHPublicKey.register(rust_openssl.dh.DHPublicKey)
DHPrivateKey = <NODE:27>((lambda : 
def key_size(self = None):
'''
        The bit length of the prime modulus.
        '''
passkey_size = None(None(key_size))
def public_key(self = None):
'''
        The DHPublicKey associated with this private key.
        '''
passpublic_key = None(public_key)
def parameters(self = None):
'''
        The DHParameters object associated with this private key.
        '''
passparameters = None(parameters)
def exchange(self = None, peer_public_key = None):
"""
        Given peer's DHPublicKey, carry out the key exchange and
        return shared key as bytes.
        """
passexchange = None(exchange)
def private_numbers(self = None):
'''
        Returns a DHPrivateNumbers.
        '''
passprivate_numbers = None(private_numbers)
def private_bytes(self = None, encoding = None, format = abc.abstractmethod, encryption_algorithm = ('encoding', '_serialization.Encoding', 'format', '_serialization.PrivateFormat', 'encryption_algorithm', '_serialization.KeySerializationEncryption', 'return', 'bytes')):
'''
        Returns the key serialized as bytes.
        '''
passprivate_bytes = None(private_bytes)), 'DHPrivateKey', abc.ABCMeta, **('metaclass',))
DHPrivateKeyWithSerialization = DHPrivateKey
DHPrivateKey.register(rust_openssl.dh.DHPrivateKey)
