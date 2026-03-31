
from __future__ import annotations
import abc
import typing
from cryptography import utils
from cryptography.exceptions import UnsupportedAlgorithm, _Reasons
from cryptography.hazmat._oid import ObjectIdentifier
from cryptography.hazmat.bindings._rust import openssl as rust_openssl
from cryptography.hazmat.primitives import _serialization, hashes
from cryptography.hazmat.primitives.asymmetric import utils as asym_utils

class EllipticCurveOID:
    SECP192R1 = ObjectIdentifier('1.2.840.10045.3.1.1')
    SECP224R1 = ObjectIdentifier('1.3.132.0.33')
    SECP256K1 = ObjectIdentifier('1.3.132.0.10')
    SECP256R1 = ObjectIdentifier('1.2.840.10045.3.1.7')
    SECP384R1 = ObjectIdentifier('1.3.132.0.34')
    SECP521R1 = ObjectIdentifier('1.3.132.0.35')
    BRAINPOOLP256R1 = ObjectIdentifier('1.3.36.3.3.2.8.1.1.7')
    BRAINPOOLP384R1 = ObjectIdentifier('1.3.36.3.3.2.8.1.1.11')
    BRAINPOOLP512R1 = ObjectIdentifier('1.3.36.3.3.2.8.1.1.13')
    SECT163K1 = ObjectIdentifier('1.3.132.0.1')
    SECT163R2 = ObjectIdentifier('1.3.132.0.15')
    SECT233K1 = ObjectIdentifier('1.3.132.0.26')
    SECT233R1 = ObjectIdentifier('1.3.132.0.27')
    SECT283K1 = ObjectIdentifier('1.3.132.0.16')
    SECT283R1 = ObjectIdentifier('1.3.132.0.17')
    SECT409K1 = ObjectIdentifier('1.3.132.0.36')
    SECT409R1 = ObjectIdentifier('1.3.132.0.37')
    SECT571K1 = ObjectIdentifier('1.3.132.0.38')
    SECT571R1 = ObjectIdentifier('1.3.132.0.39')

EllipticCurve = <NODE:27>((lambda : 
def name(self = None):
'''
        The name of the curve. e.g. secp256r1.
        '''
passname = None(None(name))
def key_size(self = None):
'''
        Bit size of a secret scalar for the curve.
        '''
passkey_size = None(None(key_size))), 'EllipticCurve', abc.ABCMeta, **('metaclass',))
EllipticCurveSignatureAlgorithm = <NODE:27>((lambda : 
def algorithm(self = None):
'''
        The digest algorithm used with this signature.
        '''
passalgorithm = None(None(algorithm))), 'EllipticCurveSignatureAlgorithm', abc.ABCMeta, **('metaclass',))
EllipticCurvePrivateKey = <NODE:27>((lambda : 
def exchange(self = None, algorithm = None, peer_public_key = abc.abstractmethod):
"""
        Performs a key exchange operation using the provided algorithm with the
        provided peer's public key.
        """
passexchange = None(exchange)
def public_key(self = None):
'''
        The EllipticCurvePublicKey for this private key.
        '''
passpublic_key = None(public_key)
def curve(self = None):
'''
        The EllipticCurve that this key is on.
        '''
passcurve = None(None(curve))
def key_size(self = None):
'''
        Bit size of a secret scalar for the curve.
        '''
passkey_size = None(None(key_size))
def sign(self = None, data = None, signature_algorithm = abc.abstractmethod):
'''
        Signs the data
        '''
passsign = None(sign)
def private_numbers(self = None):
'''
        Returns an EllipticCurvePrivateNumbers.
        '''
passprivate_numbers = None(private_numbers)
def private_bytes(self = None, encoding = None, format = abc.abstractmethod, encryption_algorithm = ('encoding', '_serialization.Encoding', 'format', '_serialization.PrivateFormat', 'encryption_algorithm', '_serialization.KeySerializationEncryption', 'return', 'bytes')):
'''
        Returns the key serialized as bytes.
        '''
passprivate_bytes = None(private_bytes)), 'EllipticCurvePrivateKey', abc.ABCMeta, **('metaclass',))
EllipticCurvePrivateKeyWithSerialization = EllipticCurvePrivateKey
EllipticCurvePrivateKey.register(rust_openssl.ec.ECPrivateKey)
EllipticCurvePublicKey = <NODE:27>((lambda : 
def curve(self = None):
'''
        The EllipticCurve that this key is on.
        '''
passcurve = None(None(curve))
def key_size(self = None):
'''
        Bit size of a secret scalar for the curve.
        '''
passkey_size = None(None(key_size))
def public_numbers(self = None):
'''
        Returns an EllipticCurvePublicNumbers.
        '''
passpublic_numbers = None(public_numbers)
def public_bytes(self = None, encoding = None, format = abc.abstractmethod):
'''
        Returns the key serialized as bytes.
        '''
passpublic_bytes = None(public_bytes)
def verify(self = None, signature = None, data = abc.abstractmethod, signature_algorithm = ('signature', 'bytes', 'data', 'bytes', 'signature_algorithm', 'EllipticCurveSignatureAlgorithm', 'return', 'None')):
'''
        Verifies the signature of the data.
        '''
passverify = None(verify)
def from_encoded_point(cls = None, curve = None, data = classmethod):
utils._check_bytes('data', data)if len(data) == 0:
raise ValueError('data must not be an empty byte string')if None[0] not in (2, 3, 4):
raise ValueError('Unsupported elliptic curve point type')None.ec.from_public_bytes(curve, data)from_encoded_point = None(from_encoded_point)
def __eq__(self = None, other = None):
'''
        Checks equality.
        '''
pass__eq__ = None(__eq__)), 'EllipticCurvePublicKey', abc.ABCMeta, **('metaclass',))
EllipticCurvePublicKeyWithSerialization = EllipticCurvePublicKey
EllipticCurvePublicKey.register(rust_openssl.ec.ECPublicKey)
EllipticCurvePrivateNumbers = rust_openssl.ec.EllipticCurvePrivateNumbers
EllipticCurvePublicNumbers = rust_openssl.ec.EllipticCurvePublicNumbers

class SECT571R1(EllipticCurve):
    name = 'sect571r1'
    key_size = 570


class SECT409R1(EllipticCurve):
    name = 'sect409r1'
    key_size = 409


class SECT283R1(EllipticCurve):
    name = 'sect283r1'
    key_size = 283


class SECT233R1(EllipticCurve):
    name = 'sect233r1'
    key_size = 233


class SECT163R2(EllipticCurve):
    name = 'sect163r2'
    key_size = 163


class SECT571K1(EllipticCurve):
    name = 'sect571k1'
    key_size = 571


class SECT409K1(EllipticCurve):
    name = 'sect409k1'
    key_size = 409


class SECT283K1(EllipticCurve):
    name = 'sect283k1'
    key_size = 283


class SECT233K1(EllipticCurve):
    name = 'sect233k1'
    key_size = 233


class SECT163K1(EllipticCurve):
    name = 'sect163k1'
    key_size = 163


class SECP521R1(EllipticCurve):
    name = 'secp521r1'
    key_size = 521


class SECP384R1(EllipticCurve):
    name = 'secp384r1'
    key_size = 384


class SECP256R1(EllipticCurve):
    name = 'secp256r1'
    key_size = 256


class SECP256K1(EllipticCurve):
    name = 'secp256k1'
    key_size = 256


class SECP224R1(EllipticCurve):
    name = 'secp224r1'
    key_size = 224


class SECP192R1(EllipticCurve):
    name = 'secp192r1'
    key_size = 192


class BrainpoolP256R1(EllipticCurve):
    name = 'brainpoolP256r1'
    key_size = 256


class BrainpoolP384R1(EllipticCurve):
    name = 'brainpoolP384r1'
    key_size = 384


class BrainpoolP512R1(EllipticCurve):
    name = 'brainpoolP512r1'
    key_size = 512

# WARNING: Decompyle incomplete
