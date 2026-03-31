
from __future__ import annotations
import abc
from cryptography import utils
from cryptography.hazmat.primitives.hashes import HashAlgorithm

class PBES(utils.Enum):
    PBESv1SHA1And3KeyTripleDESCBC = 'PBESv1 using SHA1 and 3-Key TripleDES'
    PBESv2SHA256AndAES256CBC = 'PBESv2 using SHA256 PBKDF2 and AES256 CBC'


class Encoding(utils.Enum):
    PEM = 'PEM'
    DER = 'DER'
    OpenSSH = 'OpenSSH'
    Raw = 'Raw'
    X962 = 'ANSI X9.62'
    SMIME = 'S/MIME'


class PrivateFormat(utils.Enum):
    PKCS8 = 'PKCS8'
    TraditionalOpenSSL = 'TraditionalOpenSSL'
    Raw = 'Raw'
    OpenSSH = 'OpenSSH'
    PKCS12 = 'PKCS12'
    
    def encryption_builder(self = None):
        if self not in (PrivateFormat.OpenSSH, PrivateFormat.PKCS12):
            raise ValueError('encryption_builder only supported with PrivateFormat.OpenSSH and PrivateFormat.PKCS12')
        return None(self)



class PublicFormat(utils.Enum):
    SubjectPublicKeyInfo = 'X.509 subjectPublicKeyInfo with PKCS#1'
    PKCS1 = 'Raw PKCS#1'
    OpenSSH = 'OpenSSH'
    Raw = 'Raw'
    CompressedPoint = 'X9.62 Compressed Point'
    UncompressedPoint = 'X9.62 Uncompressed Point'


class ParameterFormat(utils.Enum):
    PKCS3 = 'PKCS3'

KeySerializationEncryption = <NODE:27>((lambda : pass), 'KeySerializationEncryption', abc.ABCMeta, **('metaclass',))

class BestAvailableEncryption(KeySerializationEncryption):
    
    def __init__(self = None, password = None):
        if isinstance(password, bytes) or len(password) == 0:
            raise ValueError('Password must be 1 or more bytes.')
        self.password = None



class NoEncryption(KeySerializationEncryption):
    pass


class KeySerializationEncryptionBuilder:
    
    def __init__(self = None, format = None, *, _kdf_rounds, _hmac_hash, _key_cert_algorithm):
        self._format = format
        self._kdf_rounds = _kdf_rounds
        self._hmac_hash = _hmac_hash
        self._key_cert_algorithm = _key_cert_algorithm

    
    def kdf_rounds(self = None, rounds = None):
        if self._kdf_rounds is not None:
            raise ValueError('kdf_rounds already set')
        if not None(rounds, int):
            raise TypeError('kdf_rounds must be an integer')
        if None < 1:
            raise ValueError('kdf_rounds must be a positive integer')
        return None(self._format, rounds, self._hmac_hash, self._key_cert_algorithm, **('_kdf_rounds', '_hmac_hash', '_key_cert_algorithm'))

    
    def hmac_hash(self = None, algorithm = None):
        if self._format is not PrivateFormat.PKCS12:
            raise TypeError('hmac_hash only supported with PrivateFormat.PKCS12')
        if None._hmac_hash is not None:
            raise ValueError('hmac_hash already set')
        return None(self._format, self._kdf_rounds, algorithm, self._key_cert_algorithm, **('_kdf_rounds', '_hmac_hash', '_key_cert_algorithm'))

    
    def key_cert_algorithm(self = None, algorithm = None):
        if self._format is not PrivateFormat.PKCS12:
            raise TypeError('key_cert_algorithm only supported with PrivateFormat.PKCS12')
        if None._key_cert_algorithm is not None:
            raise ValueError('key_cert_algorithm already set')
        return None(self._format, self._kdf_rounds, self._hmac_hash, algorithm, **('_kdf_rounds', '_hmac_hash', '_key_cert_algorithm'))

    
    def build(self = None, password = None):
        if isinstance(password, bytes) or len(password) == 0:
            raise ValueError('Password must be 1 or more bytes.')
        return None(self._format, password, self._kdf_rounds, self._hmac_hash, self._key_cert_algorithm, **('kdf_rounds', 'hmac_hash', 'key_cert_algorithm'))



class _KeySerializationEncryption(KeySerializationEncryption):
    
    def __init__(self = None, format = None, password = None, *, kdf_rounds, hmac_hash, key_cert_algorithm):
        self._format = format
        self.password = password
        self._kdf_rounds = kdf_rounds
        self._hmac_hash = hmac_hash
        self._key_cert_algorithm = key_cert_algorithm


