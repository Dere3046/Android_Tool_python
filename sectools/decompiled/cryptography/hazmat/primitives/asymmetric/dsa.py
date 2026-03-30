
from __future__ import annotations
import abc
import typing
from cryptography.hazmat.bindings._rust import openssl as rust_openssl
from cryptography.hazmat.primitives import _serialization, hashes
from cryptography.hazmat.primitives.asymmetric import utils as asym_utils
DSAParameters = <NODE:27>((lambda : 
def generate_private_key(self = None):
'''
        Generates and returns a DSAPrivateKey.
        '''
passgenerate_private_key = None(generate_private_key)
def parameter_numbers(self = None):
'''
        Returns a DSAParameterNumbers.
        '''
passparameter_numbers = None(parameter_numbers)), 'DSAParameters', abc.ABCMeta, **('metaclass',))
DSAParametersWithNumbers = DSAParameters
DSAParameters.register(rust_openssl.dsa.DSAParameters)
DSAPrivateKey = <NODE:27>((lambda : 
def key_size(self = None):
'''
        The bit length of the prime modulus.
        '''
passkey_size = None(None(key_size))
def public_key(self = None):
'''
        The DSAPublicKey associated with this private key.
        '''
passpublic_key = None(public_key)
def parameters(self = None):
'''
        The DSAParameters object associated with this private key.
        '''
passparameters = None(parameters)
def sign(self = None, data = None, algorithm = abc.abstractmethod):
'''
        Signs the data
        '''
passsign = None(sign)
def private_numbers(self = None):
'''
        Returns a DSAPrivateNumbers.
        '''
passprivate_numbers = None(private_numbers)
def private_bytes(self = None, encoding = None, format = abc.abstractmethod, encryption_algorithm = ('encoding', '_serialization.Encoding', 'format', '_serialization.PrivateFormat', 'encryption_algorithm', '_serialization.KeySerializationEncryption', 'return', 'bytes')):
'''
        Returns the key serialized as bytes.
        '''
passprivate_bytes = None(private_bytes)), 'DSAPrivateKey', abc.ABCMeta, **('metaclass',))
DSAPrivateKeyWithSerialization = DSAPrivateKey
DSAPrivateKey.register(rust_openssl.dsa.DSAPrivateKey)
DSAPublicKey = <NODE:27>((lambda : 
def key_size(self = None):
'''
        The bit length of the prime modulus.
        '''
passkey_size = None(None(key_size))
def parameters(self = None):
'''
        The DSAParameters object associated with this public key.
        '''
passparameters = None(parameters)
def public_numbers(self = None):
'''
        Returns a DSAPublicNumbers.
        '''
passpublic_numbers = None(public_numbers)
def public_bytes(self = None, encoding = None, format = abc.abstractmethod):
'''
        Returns the key serialized as bytes.
        '''
passpublic_bytes = None(public_bytes)
def verify(self = None, signature = None, data = abc.abstractmethod, algorithm = ('signature', 'bytes', 'data', 'bytes', 'algorithm', 'asym_utils.Prehashed | hashes.HashAlgorithm', 'return', 'None')):
'''
        Verifies the signature of the data.
        '''
passverify = None(verify)
def __eq__(self = None, other = None):
'''
        Checks equality.
        '''
pass__eq__ = None(__eq__)), 'DSAPublicKey', abc.ABCMeta, **('metaclass',))
DSAPublicKeyWithSerialization = DSAPublicKey
DSAPublicKey.register(rust_openssl.dsa.DSAPublicKey)
DSAPrivateNumbers = rust_openssl.dsa.DSAPrivateNumbers
DSAPublicNumbers = rust_openssl.dsa.DSAPublicNumbers
DSAParameterNumbers = rust_openssl.dsa.DSAParameterNumbers

def generate_parameters(key_size = None, backend = None):
    if key_size not in (1024, 2048, 3072, 4096):
        raise ValueError('Key size must be 1024, 2048, 3072, or 4096 bits.')
    return None.dsa.generate_parameters(key_size)


def generate_private_key(key_size = None, backend = None):
    parameters = generate_parameters(key_size)
    return parameters.generate_private_key()

