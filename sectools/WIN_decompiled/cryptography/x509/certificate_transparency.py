
from __future__ import annotations
import abc
import datetime
from cryptography import utils
from cryptography.hazmat.bindings._rust import x509 as rust_x509
from cryptography.hazmat.primitives.hashes import HashAlgorithm

class LogEntryType(utils.Enum):
    X509_CERTIFICATE = 0
    PRE_CERTIFICATE = 1


class Version(utils.Enum):
    v1 = 0


class SignatureAlgorithm(utils.Enum):
    '''
    Signature algorithms that are valid for SCTs.

    These are exactly the same as SignatureAlgorithm in RFC 5246 (TLS 1.2).

    See: <https://datatracker.ietf.org/doc/html/rfc5246#section-7.4.1.4.1>
    '''
    ANONYMOUS = 0
    RSA = 1
    DSA = 2
    ECDSA = 3

SignedCertificateTimestamp = <NODE:27>((lambda : 
def version(self = None):
'''
        Returns the SCT version.
        '''
passversion = None(None(version))
def log_id(self = None):
'''
        Returns an identifier indicating which log this SCT is for.
        '''
passlog_id = None(None(log_id))
def timestamp(self = None):
'''
        Returns the timestamp for this SCT.
        '''
passtimestamp = None(None(timestamp))
def entry_type(self = None):
'''
        Returns whether this is an SCT for a certificate or pre-certificate.
        '''
passentry_type = None(None(entry_type))
def signature_hash_algorithm(self = None):
"""
        Returns the hash algorithm used for the SCT's signature.
        """
passsignature_hash_algorithm = None(None(signature_hash_algorithm))
def signature_algorithm(self = None):
"""
        Returns the signing algorithm used for the SCT's signature.
        """
passsignature_algorithm = None(None(signature_algorithm))
def signature(self = None):
'''
        Returns the signature for this SCT.
        '''
passsignature = None(None(signature))
def extension_bytes(self = None):
'''
        Returns the raw bytes of any extensions for this SCT.
        '''
passextension_bytes = None(None(extension_bytes))), 'SignedCertificateTimestamp', abc.ABCMeta, **('metaclass',))
SignedCertificateTimestamp.register(rust_x509.Sct)
