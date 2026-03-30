
from __future__ import annotations
import abc
import typing
from math import gcd
from cryptography.hazmat.bindings._rust import openssl as rust_openssl
from cryptography.hazmat.primitives import _serialization, hashes
from cryptography.hazmat.primitives._asymmetric import AsymmetricPadding
from cryptography.hazmat.primitives.asymmetric import utils as asym_utils
RSAPrivateKey = <NODE:27>((lambda : 
def decrypt(self = None, ciphertext = None, padding = abc.abstractmethod):
'''
        Decrypts the provided ciphertext.
        '''
passdecrypt = None(decrypt)
def key_size(self = None):
'''
        The bit length of the public modulus.
        '''
passkey_size = None(None(key_size))
def public_key(self = None):
'''
        The RSAPublicKey associated with this private key.
        '''
passpublic_key = None(public_key)
def sign(self = None, data = None, padding = abc.abstractmethod, algorithm = ('data', 'bytes', 'padding', 'AsymmetricPadding', 'algorithm', 'asym_utils.Prehashed | hashes.HashAlgorithm', 'return', 'bytes')):
'''
        Signs the data.
        '''
passsign = None(sign)
def private_numbers(self = None):
'''
        Returns an RSAPrivateNumbers.
        '''
passprivate_numbers = None(private_numbers)
def private_bytes(self = None, encoding = None, format = abc.abstractmethod, encryption_algorithm = ('encoding', '_serialization.Encoding', 'format', '_serialization.PrivateFormat', 'encryption_algorithm', '_serialization.KeySerializationEncryption', 'return', 'bytes')):
'''
        Returns the key serialized as bytes.
        '''
passprivate_bytes = None(private_bytes)), 'RSAPrivateKey', abc.ABCMeta, **('metaclass',))
RSAPrivateKeyWithSerialization = RSAPrivateKey
RSAPrivateKey.register(rust_openssl.rsa.RSAPrivateKey)
RSAPublicKey = <NODE:27>((lambda : 
def encrypt(self = None, plaintext = None, padding = abc.abstractmethod):
'''
        Encrypts the given plaintext.
        '''
passencrypt = None(encrypt)
def key_size(self = None):
'''
        The bit length of the public modulus.
        '''
passkey_size = None(None(key_size))
def public_numbers(self = None):
'''
        Returns an RSAPublicNumbers
        '''
passpublic_numbers = None(public_numbers)
def public_bytes(self = None, encoding = None, format = abc.abstractmethod):
'''
        Returns the key serialized as bytes.
        '''
passpublic_bytes = None(public_bytes)
def verify(self, signature = None, data = None, padding = abc.abstractmethod, algorithm = ('signature', 'bytes', 'data', 'bytes', 'padding', 'AsymmetricPadding', 'algorithm', 'asym_utils.Prehashed | hashes.HashAlgorithm', 'return', 'None')):
'''
        Verifies the signature of the data.
        '''
passverify = None(verify)
def recover_data_from_signature(self = None, signature = None, padding = abc.abstractmethod, algorithm = ('signature', 'bytes', 'padding', 'AsymmetricPadding', 'algorithm', 'hashes.HashAlgorithm | None', 'return', 'bytes')):
'''
        Recovers the original data from the signature.
        '''
passrecover_data_from_signature = None(recover_data_from_signature)
def __eq__(self = None, other = None):
'''
        Checks equality.
        '''
pass__eq__ = None(__eq__)), 'RSAPublicKey', abc.ABCMeta, **('metaclass',))
RSAPublicKeyWithSerialization = RSAPublicKey
RSAPublicKey.register(rust_openssl.rsa.RSAPublicKey)
RSAPrivateNumbers = rust_openssl.rsa.RSAPrivateNumbers
RSAPublicNumbers = rust_openssl.rsa.RSAPublicNumbers

def generate_private_key(public_exponent = None, key_size = None, backend = None):
    _verify_rsa_parameters(public_exponent, key_size)
    return rust_openssl.rsa.generate_private_key(public_exponent, key_size)


def _verify_rsa_parameters(public_exponent = None, key_size = None):
    if public_exponent not in (3, 65537):
        raise ValueError('public_exponent must be either 3 (for legacy compatibility) or 65537. Almost everyone should choose 65537 here!')
    if None < 1024:
        raise ValueError('key_size must be at least 1024-bits.')


def _modinv(e = None, m = None):
    '''
    Modular Multiplicative Inverse. Returns x such that: (x*e) mod m == 1
    '''
    (x1, x2) = (1, 0)
    a = e
    b = m
    if b > 0:
        (q, r) = divmod(a, b)
        xn = x1 - q * x2
        (a, b, x1, x2) = (b, r, x2, xn)
        if not b > 0:
            return x1 % m


def rsa_crt_iqmp(p = None, q = None):
    '''
    Compute the CRT (q ** -1) % p value from RSA primes p and q.
    '''
    return _modinv(q, p)


def rsa_crt_dmp1(private_exponent = None, p = None):
    '''
    Compute the CRT private_exponent % (p - 1) value from the RSA
    private_exponent (d) and p.
    '''
    return private_exponent % (p - 1)


def rsa_crt_dmq1(private_exponent = None, q = None):
    '''
    Compute the CRT private_exponent % (q - 1) value from the RSA
    private_exponent (d) and q.
    '''
    return private_exponent % (q - 1)


def rsa_recover_private_exponent(e = None, p = None, q = None):
    '''
    Compute the RSA private_exponent (d) given the public exponent (e)
    and the RSA primes p and q.

    This uses the Carmichael totient function to generate the
    smallest possible working value of the private exponent.
    '''
    lambda_n = (p - 1) * (q - 1) // gcd(p - 1, q - 1)
    return _modinv(e, lambda_n)

_MAX_RECOVERY_ATTEMPTS = 1000

def rsa_recover_prime_factors(n = None, e = None, d = None):
    '''
    Compute factors p and q from the private exponent d. We assume that n has
    no more than two factors. This function is adapted from code in PyCrypto.
    '''
    ktot = d * e - 1
    t = ktot
# WARNING: Decompyle incomplete

