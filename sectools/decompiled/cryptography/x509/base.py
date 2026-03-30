
from __future__ import annotations
import abc
import datetime
import os
import typing
import warnings
from cryptography import utils
from cryptography.hazmat.bindings._rust import x509 as rust_x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import dsa, ec, ed448, ed25519, padding, rsa, x448, x25519
from cryptography.hazmat.primitives.asymmetric.types import CertificateIssuerPrivateKeyTypes, CertificateIssuerPublicKeyTypes, CertificatePublicKeyTypes
from cryptography.x509.extensions import Extension, Extensions, ExtensionType, _make_sequence_methods
from cryptography.x509.name import Name, _ASN1Type
from cryptography.x509.oid import ObjectIdentifier
_EARLIEST_UTC_TIME = datetime.datetime(1950, 1, 1)
_AllowedHashTypes = typing.Union[(hashes.SHA224, hashes.SHA256, hashes.SHA384, hashes.SHA512, hashes.SHA3_224, hashes.SHA3_256, hashes.SHA3_384, hashes.SHA3_512)]

class AttributeNotFound(Exception):
    
    def __init__(self = None, msg = None, oid = None):
        super().__init__(msg)
        self.oid = oid

    __classcell__ = None


def _reject_duplicate_extension(extension = None, extensions = None):
    for e in extensions:
        if e.oid == extension.oid:
            raise ValueError('This extension has already been set.')
        return None


def _reject_duplicate_attribute(oid = None, attributes = None):
    for attr_oid, _, _ in attributes:
        if attr_oid == oid:
            raise ValueError('This attribute has already been set.')
        return None


def _convert_to_naive_utc_time(time = None):
    '''Normalizes a datetime to a naive datetime in UTC.

    time -- datetime to normalize. Assumed to be in UTC if not timezone
            aware.
    '''
    if time.tzinfo is not None:
        offset = time.utcoffset()
        offset = offset if offset else datetime.timedelta()
        return time.replace(None, **('tzinfo',)) - offset


class Attribute:
    
    def __init__(self = None, oid = None, value = None, _type = (_ASN1Type.UTF8String.value,)):
        self._oid = oid
        self._value = value
        self._type = _type

    
    def oid(self = None):
        return self._oid

    oid = None(oid)
    
    def value(self = None):
        return self._value

    value = None(value)
    
    def __repr__(self = None):
        return f'''<Attribute(oid={self.oid}, value={self.value!r})>'''

    
    def __eq__(self = None, other = None):
        if not isinstance(other, Attribute):
            return NotImplemented
        if None.oid == other.oid and self.value == other.value:
            pass
        return self._type == other._type

    
    def __hash__(self = None):
        return hash((self.oid, self.value, self._type))



class Attributes:
    
    def __init__(self = None, attributes = None):
        self._attributes = list(attributes)

    (__len__, __iter__, __getitem__) = _make_sequence_methods('_attributes')
    
    def __repr__(self = None):
        return f'''<Attributes({self._attributes})>'''

    
    def get_attribute_for_oid(self = None, oid = None):
        for attr in self:
            if attr.oid == oid:
                return attr
            raise AttributeNotFound(f'''No {oid} attribute was found''', oid)



class Version(utils.Enum):
    v1 = 0
    v3 = 2


class InvalidVersion(Exception):
    
    def __init__(self = None, msg = None, parsed_version = None):
        super().__init__(msg)
        self.parsed_version = parsed_version

    __classcell__ = None

Certificate = <NODE:27>((lambda : 
def fingerprint(self = None, algorithm = None):
'''
        Returns bytes using digest passed.
        '''
passfingerprint = None(fingerprint)
def serial_number(self = None):
'''
        Returns certificate serial number
        '''
passserial_number = None(None(serial_number))
def version(self = None):
'''
        Returns the certificate version
        '''
passversion = None(None(version))
def public_key(self = None):
'''
        Returns the public key
        '''
passpublic_key = None(public_key)
def public_key_algorithm_oid(self = None):
'''
        Returns the ObjectIdentifier of the public key.
        '''
passpublic_key_algorithm_oid = None(None(public_key_algorithm_oid))
def not_valid_before(self = None):
'''
        Not before time (represented as UTC datetime)
        '''
passnot_valid_before = None(None(not_valid_before))
def not_valid_before_utc(self = None):
'''
        Not before time (represented as a non-naive UTC datetime)
        '''
passnot_valid_before_utc = None(None(not_valid_before_utc))
def not_valid_after(self = None):
'''
        Not after time (represented as UTC datetime)
        '''
passnot_valid_after = None(None(not_valid_after))
def not_valid_after_utc(self = None):
'''
        Not after time (represented as a non-naive UTC datetime)
        '''
passnot_valid_after_utc = None(None(not_valid_after_utc))
def issuer(self = None):
'''
        Returns the issuer name object.
        '''
passissuer = None(None(issuer))
def subject(self = None):
'''
        Returns the subject name object.
        '''
passsubject = None(None(subject))
def signature_hash_algorithm(self = None):
'''
        Returns a HashAlgorithm corresponding to the type of the digest signed
        in the certificate.
        '''
passsignature_hash_algorithm = None(None(signature_hash_algorithm))
def signature_algorithm_oid(self = None):
'''
        Returns the ObjectIdentifier of the signature algorithm.
        '''
passsignature_algorithm_oid = None(None(signature_algorithm_oid))
def signature_algorithm_parameters(self = None):
'''
        Returns the signature algorithm parameters.
        '''
passsignature_algorithm_parameters = None(None(signature_algorithm_parameters))
def extensions(self = None):
'''
        Returns an Extensions object.
        '''
passextensions = None(None(extensions))
def signature(self = None):
'''
        Returns the signature bytes.
        '''
passsignature = None(None(signature))
def tbs_certificate_bytes(self = None):
'''
        Returns the tbsCertificate payload bytes as defined in RFC 5280.
        '''
passtbs_certificate_bytes = None(None(tbs_certificate_bytes))
def tbs_precertificate_bytes(self = None):
'''
        Returns the tbsCertificate payload bytes with the SCT list extension
        stripped.
        '''
passtbs_precertificate_bytes = None(None(tbs_precertificate_bytes))
def __eq__(self = None, other = None):
'''
        Checks equality.
        '''
pass__eq__ = None(__eq__)
def __hash__(self = None):
'''
        Computes a hash.
        '''
pass__hash__ = None(__hash__)
def public_bytes(self = None, encoding = None):
'''
        Serializes the certificate to PEM or DER format.
        '''
passpublic_bytes = None(public_bytes)
def verify_directly_issued_by(self = None, issuer = None):
"""
        This method verifies that certificate issuer name matches the
        issuer subject name and that the certificate is signed by the
        issuer's private key. No other validation is performed.
        """
passverify_directly_issued_by = None(verify_directly_issued_by)), 'Certificate', abc.ABCMeta, **('metaclass',))
Certificate.register(rust_x509.Certificate)
RevokedCertificate = <NODE:27>((lambda : 
def serial_number(self = None):
'''
        Returns the serial number of the revoked certificate.
        '''
passserial_number = None(None(serial_number))
def revocation_date(self = None):
'''
        Returns the date of when this certificate was revoked.
        '''
passrevocation_date = None(None(revocation_date))
def revocation_date_utc(self = None):
'''
        Returns the date of when this certificate was revoked as a non-naive
        UTC datetime.
        '''
passrevocation_date_utc = None(None(revocation_date_utc))
def extensions(self = None):
'''
        Returns an Extensions object containing a list of Revoked extensions.
        '''
passextensions = None(None(extensions))), 'RevokedCertificate', abc.ABCMeta, **('metaclass',))
RevokedCertificate.register(rust_x509.RevokedCertificate)

class _RawRevokedCertificate(RevokedCertificate):
    
    def __init__(self = None, serial_number = None, revocation_date = None, extensions = ('serial_number', 'int', 'revocation_date', 'datetime.datetime', 'extensions', 'Extensions')):
        self._serial_number = serial_number
        self._revocation_date = revocation_date
        self._extensions = extensions

    
    def serial_number(self = None):
        return self._serial_number

    serial_number = None(serial_number)
    
    def revocation_date(self = None):
        warnings.warn('Properties that return a naïve datetime object have been deprecated. Please switch to revocation_date_utc.', utils.DeprecatedIn42, 2, **('stacklevel',))
        return self._revocation_date

    revocation_date = None(revocation_date)
    
    def revocation_date_utc(self = None):
        return self._revocation_date.replace(datetime.timezone.utc, **('tzinfo',))

    revocation_date_utc = None(revocation_date_utc)
    
    def extensions(self = None):
        return self._extensions

    extensions = None(extensions)

CertificateRevocationList = <NODE:27>((lambda : 
def public_bytes(self = None, encoding = None):
'''
        Serializes the CRL to PEM or DER format.
        '''
passpublic_bytes = None(public_bytes)
def fingerprint(self = None, algorithm = None):
'''
        Returns bytes using digest passed.
        '''
passfingerprint = None(fingerprint)
def get_revoked_certificate_by_serial_number(self = None, serial_number = None):
'''
        Returns an instance of RevokedCertificate or None if the serial_number
        is not in the CRL.
        '''
passget_revoked_certificate_by_serial_number = None(get_revoked_certificate_by_serial_number)
def signature_hash_algorithm(self = None):
'''
        Returns a HashAlgorithm corresponding to the type of the digest signed
        in the certificate.
        '''
passsignature_hash_algorithm = None(None(signature_hash_algorithm))
def signature_algorithm_oid(self = None):
'''
        Returns the ObjectIdentifier of the signature algorithm.
        '''
passsignature_algorithm_oid = None(None(signature_algorithm_oid))
def signature_algorithm_parameters(self = None):
'''
        Returns the signature algorithm parameters.
        '''
passsignature_algorithm_parameters = None(None(signature_algorithm_parameters))
def issuer(self = None):
'''
        Returns the X509Name with the issuer of this CRL.
        '''
passissuer = None(None(issuer))
def next_update(self = None):
'''
        Returns the date of next update for this CRL.
        '''
passnext_update = None(None(next_update))
def next_update_utc(self = None):
'''
        Returns the date of next update for this CRL as a non-naive UTC
        datetime.
        '''
passnext_update_utc = None(None(next_update_utc))
def last_update(self = None):
'''
        Returns the date of last update for this CRL.
        '''
passlast_update = None(None(last_update))
def last_update_utc(self = None):
'''
        Returns the date of last update for this CRL as a non-naive UTC
        datetime.
        '''
passlast_update_utc = None(None(last_update_utc))
def extensions(self = None):
'''
        Returns an Extensions object containing a list of CRL extensions.
        '''
passextensions = None(None(extensions))
def signature(self = None):
'''
        Returns the signature bytes.
        '''
passsignature = None(None(signature))
def tbs_certlist_bytes(self = None):
'''
        Returns the tbsCertList payload bytes as defined in RFC 5280.
        '''
passtbs_certlist_bytes = None(None(tbs_certlist_bytes))
def __eq__(self = None, other = None):
'''
        Checks equality.
        '''
pass__eq__ = None(__eq__)
def __len__(self = None):
'''
        Number of revoked certificates in the CRL.
        '''
pass__len__ = None(__len__)
def __getitem__(self = None, idx = None):
pass__getitem__ = None(__getitem__)
def __getitem__(self = None, idx = None):
pass__getitem__ = None(__getitem__)
def __getitem__(self = None, idx = None):
'''
        Returns a revoked certificate (or slice of revoked certificates).
        '''
pass__getitem__ = None(__getitem__)
def __iter__(self = None):
'''
        Iterator over the revoked certificates
        '''
pass__iter__ = None(__iter__)
def is_signature_valid(self = None, public_key = None):
'''
        Verifies signature of revocation list against given public key.
        '''
passis_signature_valid = None(is_signature_valid)), 'CertificateRevocationList', abc.ABCMeta, **('metaclass',))
CertificateRevocationList.register(rust_x509.CertificateRevocationList)
CertificateSigningRequest = <NODE:27>((lambda : 
def __eq__(self = None, other = None):
'''
        Checks equality.
        '''
pass__eq__ = None(__eq__)
def __hash__(self = None):
'''
        Computes a hash.
        '''
pass__hash__ = None(__hash__)
def public_key(self = None):
'''
        Returns the public key
        '''
passpublic_key = None(public_key)
def subject(self = None):
'''
        Returns the subject name object.
        '''
passsubject = None(None(subject))
def signature_hash_algorithm(self = None):
'''
        Returns a HashAlgorithm corresponding to the type of the digest signed
        in the certificate.
        '''
passsignature_hash_algorithm = None(None(signature_hash_algorithm))
def signature_algorithm_oid(self = None):
'''
        Returns the ObjectIdentifier of the signature algorithm.
        '''
passsignature_algorithm_oid = None(None(signature_algorithm_oid))
def signature_algorithm_parameters(self = None):
'''
        Returns the signature algorithm parameters.
        '''
passsignature_algorithm_parameters = None(None(signature_algorithm_parameters))
def extensions(self = None):
'''
        Returns the extensions in the signing request.
        '''
passextensions = None(None(extensions))
def attributes(self = None):
'''
        Returns an Attributes object.
        '''
passattributes = None(None(attributes))
def public_bytes(self = None, encoding = None):
'''
        Encodes the request to PEM or DER format.
        '''
passpublic_bytes = None(public_bytes)
def signature(self = None):
'''
        Returns the signature bytes.
        '''
passsignature = None(None(signature))
def tbs_certrequest_bytes(self = None):
'''
        Returns the PKCS#10 CertificationRequestInfo bytes as defined in RFC
        2986.
        '''
passtbs_certrequest_bytes = None(None(tbs_certrequest_bytes))
def is_signature_valid(self = None):
'''
        Verifies signature of signing request.
        '''
passis_signature_valid = None(None(is_signature_valid))
def get_attribute_for_oid(self = None, oid = None):
'''
        Get the attribute value for a given OID.
        '''
passget_attribute_for_oid = None(get_attribute_for_oid)), 'CertificateSigningRequest', abc.ABCMeta, **('metaclass',))
CertificateSigningRequest.register(rust_x509.CertificateSigningRequest)
load_pem_x509_certificate = rust_x509.load_pem_x509_certificate
load_der_x509_certificate = rust_x509.load_der_x509_certificate
load_pem_x509_certificates = rust_x509.load_pem_x509_certificates
load_pem_x509_csr = rust_x509.load_pem_x509_csr
load_der_x509_csr = rust_x509.load_der_x509_csr
load_pem_x509_crl = rust_x509.load_pem_x509_crl
load_der_x509_crl = rust_x509.load_der_x509_crl

class CertificateSigningRequestBuilder:
    
    def __init__(self = None, subject_name = None, extensions = None, attributes = (None, [], [])):
        '''
        Creates an empty X.509 certificate request (v1).
        '''
        self._subject_name = subject_name
        self._extensions = extensions
        self._attributes = attributes

    
    def subject_name(self = None, name = None):
        """
        Sets the certificate requestor's distinguished name.
        """
        if not isinstance(name, Name):
            raise TypeError('Expecting x509.Name object.')
        if None._subject_name is not None:
            raise ValueError('The subject name may only be set once.')
        return None(name, self._extensions, self._attributes)

    
    def add_extension(self = None, extval = None, critical = None):
        '''
        Adds an X.509 extension to the certificate request.
        '''
        if not isinstance(extval, ExtensionType):
            raise TypeError('extension must be an ExtensionType')
        extension = None(extval.oid, critical, extval)
        _reject_duplicate_extension(extension, self._extensions)
        return CertificateSigningRequestBuilder(self._subject_name, self._subject_name[extension], self._attributes)

    
    def add_attribute(self = None, oid = None, value = None, *, _tag):
        '''
        Adds an X.509 attribute with an OID and associated value.
        '''
        if not isinstance(oid, ObjectIdentifier):
            raise TypeError('oid must be an ObjectIdentifier')
        if not None(value, bytes):
            raise TypeError('value must be bytes')
        if not None is not None and isinstance(_tag, _ASN1Type):
            raise TypeError('tag must be _ASN1Type')
        None(oid, self._attributes)
        if _tag is not None:
            tag = _tag.value
        else:
            tag = None
        return CertificateSigningRequestBuilder(self._subject_name, self._extensions, self._extensions[(oid, value, tag)])

    
    def sign(self = None, private_key = None, algorithm = None, backend = None, *, rsa_padding):
        """
        Signs the request using the requestor's private key.
        """
        if self._subject_name is None:
            raise ValueError('A CertificateSigningRequest must have a subject')
        if None is not None:
            if not isinstance(rsa_padding, (padding.PSS, padding.PKCS1v15)):
                raise TypeError('Padding must be PSS or PKCS1v15')
            if not None(private_key, rsa.RSAPrivateKey):
                raise TypeError('Padding is only supported for RSA keys')
            return None.create_x509_csr(self, private_key, algorithm, rsa_padding)



class CertificateBuilder:
    _extensions: 'list[Extension[ExtensionType]]' = 'CertificateBuilder'
    
    def __init__(self, issuer_name, subject_name, public_key = None, serial_number = None, not_valid_before = None, not_valid_after = (None, None, None, None, None, None, []), extensions = ('issuer_name', 'Name | None', 'subject_name', 'Name | None', 'public_key', 'CertificatePublicKeyTypes | None', 'serial_number', 'int | None', 'not_valid_before', 'datetime.datetime | None', 'not_valid_after', 'datetime.datetime | None', 'extensions', 'list[Extension[ExtensionType]]', 'return', 'None')):
        self._version = Version.v3
        self._issuer_name = issuer_name
        self._subject_name = subject_name
        self._public_key = public_key
        self._serial_number = serial_number
        self._not_valid_before = not_valid_before
        self._not_valid_after = not_valid_after
        self._extensions = extensions

    
    def issuer_name(self = None, name = None):
        """
        Sets the CA's distinguished name.
        """
        if not isinstance(name, Name):
            raise TypeError('Expecting x509.Name object.')
        if None._issuer_name is not None:
            raise ValueError('The issuer name may only be set once.')
        return None(name, self._subject_name, self._public_key, self._serial_number, self._not_valid_before, self._not_valid_after, self._extensions)

    
    def subject_name(self = None, name = None):
        """
        Sets the requestor's distinguished name.
        """
        if not isinstance(name, Name):
            raise TypeError('Expecting x509.Name object.')
        if None._subject_name is not None:
            raise ValueError('The subject name may only be set once.')
        return None(self._issuer_name, name, self._public_key, self._serial_number, self._not_valid_before, self._not_valid_after, self._extensions)

    
    def public_key(self = None, key = None):
        """
        Sets the requestor's public key (as found in the signing request).
        """
        if not isinstance(key, (dsa.DSAPublicKey, rsa.RSAPublicKey, ec.EllipticCurvePublicKey, ed25519.Ed25519PublicKey, ed448.Ed448PublicKey, x25519.X25519PublicKey, x448.X448PublicKey)):
            raise TypeError('Expecting one of DSAPublicKey, RSAPublicKey, EllipticCurvePublicKey, Ed25519PublicKey, Ed448PublicKey, X25519PublicKey, or X448PublicKey.')
        if None._public_key is not None:
            raise ValueError('The public key may only be set once.')
        return None(self._issuer_name, self._subject_name, key, self._serial_number, self._not_valid_before, self._not_valid_after, self._extensions)

    
    def serial_number(self = None, number = None):
        '''
        Sets the certificate serial number.
        '''
        if not isinstance(number, int):
            raise TypeError('Serial number must be of integral type.')
        if None._serial_number is not None:
            raise ValueError('The serial number may only be set once.')
        if None <= 0:
            raise ValueError('The serial number should be positive.')
        if None.bit_length() >= 160:
            raise ValueError('The serial number should not be more than 159 bits.')
        return None(self._issuer_name, self._subject_name, self._public_key, number, self._not_valid_before, self._not_valid_after, self._extensions)

    
    def not_valid_before(self = None, time = None):
        '''
        Sets the certificate activation time.
        '''
        if not isinstance(time, datetime.datetime):
            raise TypeError('Expecting datetime object.')
        if None._not_valid_before is not None:
            raise ValueError('The not valid before may only be set once.')
        time = None(time)
        if time < _EARLIEST_UTC_TIME:
            raise ValueError('The not valid before date must be on or after 1950 January 1).')
        if None._not_valid_after is not None and time > self._not_valid_after:
            raise ValueError('The not valid before date must be before the not valid after date.')
        return None(self._issuer_name, self._subject_name, self._public_key, self._serial_number, time, self._not_valid_after, self._extensions)

    
    def not_valid_after(self = None, time = None):
        '''
        Sets the certificate expiration time.
        '''
        if not isinstance(time, datetime.datetime):
            raise TypeError('Expecting datetime object.')
        if None._not_valid_after is not None:
            raise ValueError('The not valid after may only be set once.')
        time = None(time)
        if time < _EARLIEST_UTC_TIME:
            raise ValueError('The not valid after date must be on or after 1950 January 1.')
        if None._not_valid_before is not None and time < self._not_valid_before:
            raise ValueError('The not valid after date must be after the not valid before date.')
        return None(self._issuer_name, self._subject_name, self._public_key, self._serial_number, self._not_valid_before, time, self._extensions)

    
    def add_extension(self = None, extval = None, critical = None):
        '''
        Adds an X.509 extension to the certificate.
        '''
        if not isinstance(extval, ExtensionType):
            raise TypeError('extension must be an ExtensionType')
        extension = None(extval.oid, critical, extval)
        _reject_duplicate_extension(extension, self._extensions)
        return CertificateBuilder(self._issuer_name, self._subject_name, self._public_key, self._serial_number, self._not_valid_before, self._not_valid_after, self._not_valid_after[extension])

    
    def sign(self = None, private_key = None, algorithm = None, backend = None, *, rsa_padding):
        """
        Signs the certificate using the CA's private key.
        """
        if self._subject_name is None:
            raise ValueError('A certificate must have a subject name')
        if None._issuer_name is None:
            raise ValueError('A certificate must have an issuer name')
        if None._serial_number is None:
            raise ValueError('A certificate must have a serial number')
        if None._not_valid_before is None:
            raise ValueError('A certificate must have a not valid before time')
        if None._not_valid_after is None:
            raise ValueError('A certificate must have a not valid after time')
        if None._public_key is None:
            raise ValueError('A certificate must have a public key')
        if None is not None:
            if not isinstance(rsa_padding, (padding.PSS, padding.PKCS1v15)):
                raise TypeError('Padding must be PSS or PKCS1v15')
            if not None(private_key, rsa.RSAPrivateKey):
                raise TypeError('Padding is only supported for RSA keys')
            return None.create_x509_certificate(self, private_key, algorithm, rsa_padding)



class CertificateRevocationListBuilder:
    _revoked_certificates: 'list[RevokedCertificate]' = 'CertificateRevocationListBuilder'
    
    def __init__(self, issuer_name = None, last_update = None, next_update = None, extensions = (None, None, None, [], []), revoked_certificates = ('issuer_name', 'Name | None', 'last_update', 'datetime.datetime | None', 'next_update', 'datetime.datetime | None', 'extensions', 'list[Extension[ExtensionType]]', 'revoked_certificates', 'list[RevokedCertificate]')):
        self._issuer_name = issuer_name
        self._last_update = last_update
        self._next_update = next_update
        self._extensions = extensions
        self._revoked_certificates = revoked_certificates

    
    def issuer_name(self = None, issuer_name = None):
        if not isinstance(issuer_name, Name):
            raise TypeError('Expecting x509.Name object.')
        if None._issuer_name is not None:
            raise ValueError('The issuer name may only be set once.')
        return None(issuer_name, self._last_update, self._next_update, self._extensions, self._revoked_certificates)

    
    def last_update(self = None, last_update = None):
        if not isinstance(last_update, datetime.datetime):
            raise TypeError('Expecting datetime object.')
        if None._last_update is not None:
            raise ValueError('Last update may only be set once.')
        last_update = None(last_update)
        if last_update < _EARLIEST_UTC_TIME:
            raise ValueError('The last update date must be on or after 1950 January 1.')
        if None._next_update is not None and last_update > self._next_update:
            raise ValueError('The last update date must be before the next update date.')
        return None(self._issuer_name, last_update, self._next_update, self._extensions, self._revoked_certificates)

    
    def next_update(self = None, next_update = None):
        if not isinstance(next_update, datetime.datetime):
            raise TypeError('Expecting datetime object.')
        if None._next_update is not None:
            raise ValueError('Last update may only be set once.')
        next_update = None(next_update)
        if next_update < _EARLIEST_UTC_TIME:
            raise ValueError('The last update date must be on or after 1950 January 1.')
        if None._last_update is not None and next_update < self._last_update:
            raise ValueError('The next update date must be after the last update date.')
        return None(self._issuer_name, self._last_update, next_update, self._extensions, self._revoked_certificates)

    
    def add_extension(self = None, extval = None, critical = None):
        '''
        Adds an X.509 extension to the certificate revocation list.
        '''
        if not isinstance(extval, ExtensionType):
            raise TypeError('extension must be an ExtensionType')
        extension = None(extval.oid, critical, extval)
        _reject_duplicate_extension(extension, self._extensions)
        return CertificateRevocationListBuilder(self._issuer_name, self._last_update, self._next_update, self._next_update[extension], self._revoked_certificates)

    
    def add_revoked_certificate(self = None, revoked_certificate = None):
        '''
        Adds a revoked certificate to the CRL.
        '''
        if not isinstance(revoked_certificate, RevokedCertificate):
            raise TypeError('Must be an instance of RevokedCertificate')
        return None(self._issuer_name, self._last_update, self._next_update, self._extensions, self._extensions[revoked_certificate])

    
    def sign(self = None, private_key = None, algorithm = None, backend = None, *, rsa_padding):
        if self._issuer_name is None:
            raise ValueError('A CRL must have an issuer name')
        if None._last_update is None:
            raise ValueError('A CRL must have a last update time')
        if None._next_update is None:
            raise ValueError('A CRL must have a next update time')
        if None is not None:
            if not isinstance(rsa_padding, (padding.PSS, padding.PKCS1v15)):
                raise TypeError('Padding must be PSS or PKCS1v15')
            if not None(private_key, rsa.RSAPrivateKey):
                raise TypeError('Padding is only supported for RSA keys')
            return None.create_x509_crl(self, private_key, algorithm, rsa_padding)



class RevokedCertificateBuilder:
    
    def __init__(self = None, serial_number = None, revocation_date = None, extensions = (None, None, [])):
        self._serial_number = serial_number
        self._revocation_date = revocation_date
        self._extensions = extensions

    
    def serial_number(self = None, number = None):
        if not isinstance(number, int):
            raise TypeError('Serial number must be of integral type.')
        if None._serial_number is not None:
            raise ValueError('The serial number may only be set once.')
        if None <= 0:
            raise ValueError('The serial number should be positive')
        if None.bit_length() >= 160:
            raise ValueError('The serial number should not be more than 159 bits.')
        return None(number, self._revocation_date, self._extensions)

    
    def revocation_date(self = None, time = None):
        if not isinstance(time, datetime.datetime):
            raise TypeError('Expecting datetime object.')
        if None._revocation_date is not None:
            raise ValueError('The revocation date may only be set once.')
        time = None(time)
        if time < _EARLIEST_UTC_TIME:
            raise ValueError('The revocation date must be on or after 1950 January 1.')
        return None(self._serial_number, time, self._extensions)

    
    def add_extension(self = None, extval = None, critical = None):
        if not isinstance(extval, ExtensionType):
            raise TypeError('extension must be an ExtensionType')
        extension = None(extval.oid, critical, extval)
        _reject_duplicate_extension(extension, self._extensions)
        return RevokedCertificateBuilder(self._serial_number, self._revocation_date, self._revocation_date[extension])

    
    def build(self = None, backend = None):
        if self._serial_number is None:
            raise ValueError('A revoked certificate must have a serial number')
        if None._revocation_date is None:
            raise ValueError('A revoked certificate must have a revocation date')
        return None(self._serial_number, self._revocation_date, Extensions(self._extensions))



def random_serial_number():
    return int.from_bytes(os.urandom(20), 'big') >> 1

