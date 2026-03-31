
from __future__ import annotations
import abc
import datetime
import hashlib
import ipaddress
import typing
from cryptography import utils
from cryptography.hazmat.bindings._rust import asn1
from cryptography.hazmat.bindings._rust import x509 as rust_x509
from cryptography.hazmat.primitives import constant_time, serialization
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptography.hazmat.primitives.asymmetric.types import CertificateIssuerPublicKeyTypes, CertificatePublicKeyTypes
from cryptography.x509.certificate_transparency import SignedCertificateTimestamp
from cryptography.x509.general_name import DirectoryName, DNSName, GeneralName, IPAddress, OtherName, RegisteredID, RFC822Name, UniformResourceIdentifier, _IPAddressTypes
from cryptography.x509.name import Name, RelativeDistinguishedName
from cryptography.x509.oid import CRLEntryExtensionOID, ExtensionOID, ObjectIdentifier, OCSPExtensionOID
ExtensionTypeVar = typing.TypeVar('ExtensionTypeVar', 'ExtensionType', True, **('bound', 'covariant'))

def _key_identifier_from_public_key(public_key = None):
    if isinstance(public_key, RSAPublicKey):
        data = public_key.public_bytes(serialization.Encoding.DER, serialization.PublicFormat.PKCS1)
    elif isinstance(public_key, EllipticCurvePublicKey):
        data = public_key.public_bytes(serialization.Encoding.X962, serialization.PublicFormat.UncompressedPoint)
    else:
        serialized = public_key.public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
        data = asn1.parse_spki_for_data(serialized)
    return hashlib.sha1(data).digest()


def _make_sequence_methods(field_name = None):
    
    def len_method(self = None):
        return len(getattr(self, field_name))

    
    def iter_method(self = None):
        return iter(getattr(self, field_name))

    
    def getitem_method(self = None, idx = None):
        return getattr(self, field_name)[idx]

    return (len_method, iter_method, getitem_method)


class DuplicateExtension(Exception):
    
    def __init__(self = None, msg = None, oid = None):
        super().__init__(msg)
        self.oid = oid

    __classcell__ = None


class ExtensionNotFound(Exception):
    
    def __init__(self = None, msg = None, oid = None):
        super().__init__(msg)
        self.oid = oid

    __classcell__ = None

ExtensionType = <NODE:27>((lambda : oid: 'typing.ClassVar[ObjectIdentifier]' = 'ExtensionType'
def public_bytes(self = None):
'''
        Serializes the extension type to DER.
        '''
raise NotImplementedError(f'''public_bytes is not implemented for extension type {self!r}''')), 'ExtensionType', abc.ABCMeta, **('metaclass',))

class Extensions:
    
    def __init__(self = None, extensions = None):
        self._extensions = list(extensions)

    
    def get_extension_for_oid(self = None, oid = None):
        for ext in self:
            if ext.oid == oid:
                return ext
            raise ExtensionNotFound(f'''No {oid} extension was found''', oid)

    
    def get_extension_for_class(self = None, extclass = None):
        if extclass is UnrecognizedExtension:
            raise TypeError("UnrecognizedExtension can't be used with get_extension_for_class because more than one instance of the class may be present.")
        for ext in None:
            if isinstance(ext.value, extclass):
                return ext
            raise ExtensionNotFound(f'''No {extclass} extension was found''', extclass.oid)

    (__len__, __iter__, __getitem__) = _make_sequence_methods('_extensions')
    
    def __repr__(self = None):
        return f'''<Extensions({self._extensions})>'''



class CRLNumber(ExtensionType):
    oid = ExtensionOID.CRL_NUMBER
    
    def __init__(self = None, crl_number = None):
        if not isinstance(crl_number, int):
            raise TypeError('crl_number must be an integer')
        self._crl_number = None

    
    def __eq__(self = None, other = None):
        if not isinstance(other, CRLNumber):
            return NotImplemented
        return None.crl_number == other.crl_number

    
    def __hash__(self = None):
        return hash(self.crl_number)

    
    def __repr__(self = None):
        return f'''<CRLNumber({self.crl_number})>'''

    
    def crl_number(self = None):
        return self._crl_number

    crl_number = None(crl_number)
    
    def public_bytes(self = None):
        return rust_x509.encode_extension_value(self)



class AuthorityKeyIdentifier(ExtensionType):
    oid = ExtensionOID.AUTHORITY_KEY_IDENTIFIER
    
    def __init__(self = None, key_identifier = None, authority_cert_issuer = None, authority_cert_serial_number = ('key_identifier', 'bytes | None', 'authority_cert_issuer', 'typing.Iterable[GeneralName] | None', 'authority_cert_serial_number', 'int | None', 'return', 'None')):
        if (authority_cert_issuer is None) != (authority_cert_serial_number is None):
            raise ValueError('authority_cert_issuer and authority_cert_serial_number must both be present or both None')
        if None is not None:
            authority_cert_issuer = list(authority_cert_issuer)
            if not all((lambda .0: for x in .0:
isinstance(x, GeneralName))(authority_cert_issuer)):
                raise TypeError('authority_cert_issuer must be a list of GeneralName objects')
            if not None is not None and isinstance(authority_cert_serial_number, int):
                raise TypeError('authority_cert_serial_number must be an integer')
            self._key_identifier = None
            self._authority_cert_issuer = authority_cert_issuer
            self._authority_cert_serial_number = authority_cert_serial_number
            return None

    
    def from_issuer_public_key(cls = None, public_key = None):
        digest = _key_identifier_from_public_key(public_key)
        return cls(digest, None, None, **('key_identifier', 'authority_cert_issuer', 'authority_cert_serial_number'))

    from_issuer_public_key = None(from_issuer_public_key)
    
    def from_issuer_subject_key_identifier(cls = None, ski = None):
        return cls(ski.digest, None, None, **('key_identifier', 'authority_cert_issuer', 'authority_cert_serial_number'))

    from_issuer_subject_key_identifier = None(from_issuer_subject_key_identifier)
    
    def __repr__(self = None):
        return f'''<AuthorityKeyIdentifier(key_identifier={self.key_identifier!r}, authority_cert_issuer={self.authority_cert_issuer}, authority_cert_serial_number={self.authority_cert_serial_number})>'''

    
    def __eq__(self = None, other = None):
        if not isinstance(other, AuthorityKeyIdentifier):
            return NotImplemented
        if None.key_identifier == other.key_identifier and self.authority_cert_issuer == other.authority_cert_issuer:
            pass
        return self.authority_cert_serial_number == other.authority_cert_serial_number

    
    def __hash__(self = None):
        if self.authority_cert_issuer is None:
            aci = None
        else:
            aci = tuple(self.authority_cert_issuer)
        return hash((self.key_identifier, aci, self.authority_cert_serial_number))

    
    def key_identifier(self = None):
        return self._key_identifier

    key_identifier = None(key_identifier)
    
    def authority_cert_issuer(self = None):
        return self._authority_cert_issuer

    authority_cert_issuer = None(authority_cert_issuer)
    
    def authority_cert_serial_number(self = None):
        return self._authority_cert_serial_number

    authority_cert_serial_number = None(authority_cert_serial_number)
    
    def public_bytes(self = None):
        return rust_x509.encode_extension_value(self)



class SubjectKeyIdentifier(ExtensionType):
    oid = ExtensionOID.SUBJECT_KEY_IDENTIFIER
    
    def __init__(self = None, digest = None):
        self._digest = digest

    
    def from_public_key(cls = None, public_key = None):
        return cls(_key_identifier_from_public_key(public_key))

    from_public_key = None(from_public_key)
    
    def digest(self = None):
        return self._digest

    digest = None(digest)
    
    def key_identifier(self = None):
        return self._digest

    key_identifier = None(key_identifier)
    
    def __repr__(self = None):
        return f'''<SubjectKeyIdentifier(digest={self.digest!r})>'''

    
    def __eq__(self = None, other = None):
        if not isinstance(other, SubjectKeyIdentifier):
            return NotImplemented
        return None.bytes_eq(self.digest, other.digest)

    
    def __hash__(self = None):
        return hash(self.digest)

    
    def public_bytes(self = None):
        return rust_x509.encode_extension_value(self)



class AuthorityInformationAccess(ExtensionType):
    oid = ExtensionOID.AUTHORITY_INFORMATION_ACCESS
    
    def __init__(self = None, descriptions = None):
        descriptions = list(descriptions)
        if not all((lambda .0: for x in .0:
isinstance(x, AccessDescription))(descriptions)):
            raise TypeError('Every item in the descriptions list must be an AccessDescription')
        self._descriptions = None

    (__len__, __iter__, __getitem__) = _make_sequence_methods('_descriptions')
    
    def __repr__(self = None):
        return f'''<AuthorityInformationAccess({self._descriptions})>'''

    
    def __eq__(self = None, other = None):
        if not isinstance(other, AuthorityInformationAccess):
            return NotImplemented
        return None._descriptions == other._descriptions

    
    def __hash__(self = None):
        return hash(tuple(self._descriptions))

    
    def public_bytes(self = None):
        return rust_x509.encode_extension_value(self)



class SubjectInformationAccess(ExtensionType):
    oid = ExtensionOID.SUBJECT_INFORMATION_ACCESS
    
    def __init__(self = None, descriptions = None):
        descriptions = list(descriptions)
        if not all((lambda .0: for x in .0:
isinstance(x, AccessDescription))(descriptions)):
            raise TypeError('Every item in the descriptions list must be an AccessDescription')
        self._descriptions = None

    (__len__, __iter__, __getitem__) = _make_sequence_methods('_descriptions')
    
    def __repr__(self = None):
        return f'''<SubjectInformationAccess({self._descriptions})>'''

    
    def __eq__(self = None, other = None):
        if not isinstance(other, SubjectInformationAccess):
            return NotImplemented
        return None._descriptions == other._descriptions

    
    def __hash__(self = None):
        return hash(tuple(self._descriptions))

    
    def public_bytes(self = None):
        return rust_x509.encode_extension_value(self)



class AccessDescription:
    
    def __init__(self = None, access_method = None, access_location = None):
        if not isinstance(access_method, ObjectIdentifier):
            raise TypeError('access_method must be an ObjectIdentifier')
        if not None(access_location, GeneralName):
            raise TypeError('access_location must be a GeneralName')
        self._access_method = None
        self._access_location = access_location

    
    def __repr__(self = None):
        return f'''<AccessDescription(access_method={self.access_method}, access_location={self.access_location})>'''

    
    def __eq__(self = None, other = None):
        if not isinstance(other, AccessDescription):
            return NotImplemented
        if None.access_method == other.access_method:
            pass
        return self.access_location == other.access_location

    
    def __hash__(self = None):
        return hash((self.access_method, self.access_location))

    
    def access_method(self = None):
        return self._access_method

    access_method = None(access_method)
    
    def access_location(self = None):
        return self._access_location

    access_location = None(access_location)


class BasicConstraints(ExtensionType):
    oid = ExtensionOID.BASIC_CONSTRAINTS
    
    def __init__(self = None, ca = None, path_length = None):
        if not isinstance(ca, bool):
            raise TypeError('ca must be a boolean value')
        if not None is not None and ca:
            raise ValueError('path_length must be None when ca is False')
        if None is not None:
            if isinstance(path_length, int) or path_length < 0:
                raise TypeError('path_length must be a non-negative integer or None')
            self._ca = None
            self._path_length = path_length
            return None

    
    def ca(self = None):
        return self._ca

    ca = None(ca)
    
    def path_length(self = None):
        return self._path_length

    path_length = None(path_length)
    
    def __repr__(self = None):
        return f'''<BasicConstraints(ca={self.ca}, path_length={self.path_length})>'''

    
    def __eq__(self = None, other = None):
        if not isinstance(other, BasicConstraints):
            return NotImplemented
        if None.ca == other.ca:
            pass
        return self.path_length == other.path_length

    
    def __hash__(self = None):
        return hash((self.ca, self.path_length))

    
    def public_bytes(self = None):
        return rust_x509.encode_extension_value(self)



class DeltaCRLIndicator(ExtensionType):
    oid = ExtensionOID.DELTA_CRL_INDICATOR
    
    def __init__(self = None, crl_number = None):
        if not isinstance(crl_number, int):
            raise TypeError('crl_number must be an integer')
        self._crl_number = None

    
    def crl_number(self = None):
        return self._crl_number

    crl_number = None(crl_number)
    
    def __eq__(self = None, other = None):
        if not isinstance(other, DeltaCRLIndicator):
            return NotImplemented
        return None.crl_number == other.crl_number

    
    def __hash__(self = None):
        return hash(self.crl_number)

    
    def __repr__(self = None):
        return f'''<DeltaCRLIndicator(crl_number={self.crl_number})>'''

    
    def public_bytes(self = None):
        return rust_x509.encode_extension_value(self)



class CRLDistributionPoints(ExtensionType):
    oid = ExtensionOID.CRL_DISTRIBUTION_POINTS
    
    def __init__(self = None, distribution_points = None):
        distribution_points = list(distribution_points)
        if not all((lambda .0: for x in .0:
isinstance(x, DistributionPoint))(distribution_points)):
            raise TypeError('distribution_points must be a list of DistributionPoint objects')
        self._distribution_points = None

    (__len__, __iter__, __getitem__) = _make_sequence_methods('_distribution_points')
    
    def __repr__(self = None):
        return f'''<CRLDistributionPoints({self._distribution_points})>'''

    
    def __eq__(self = None, other = None):
        if not isinstance(other, CRLDistributionPoints):
            return NotImplemented
        return None._distribution_points == other._distribution_points

    
    def __hash__(self = None):
        return hash(tuple(self._distribution_points))

    
    def public_bytes(self = None):
        return rust_x509.encode_extension_value(self)



class FreshestCRL(ExtensionType):
    oid = ExtensionOID.FRESHEST_CRL
    
    def __init__(self = None, distribution_points = None):
        distribution_points = list(distribution_points)
        if not all((lambda .0: for x in .0:
isinstance(x, DistributionPoint))(distribution_points)):
            raise TypeError('distribution_points must be a list of DistributionPoint objects')
        self._distribution_points = None

    (__len__, __iter__, __getitem__) = _make_sequence_methods('_distribution_points')
    
    def __repr__(self = None):
        return f'''<FreshestCRL({self._distribution_points})>'''

    
    def __eq__(self = None, other = None):
        if not isinstance(other, FreshestCRL):
            return NotImplemented
        return None._distribution_points == other._distribution_points

    
    def __hash__(self = None):
        return hash(tuple(self._distribution_points))

    
    def public_bytes(self = None):
        return rust_x509.encode_extension_value(self)



class DistributionPoint:
    
    def __init__(self, full_name = None, relative_name = None, reasons = None, crl_issuer = ('full_name', 'typing.Iterable[GeneralName] | None', 'relative_name', 'RelativeDistinguishedName | None', 'reasons', 'frozenset[ReasonFlags] | None', 'crl_issuer', 'typing.Iterable[GeneralName] | None', 'return', 'None')):
        if full_name and relative_name:
            raise ValueError('You cannot provide both full_name and relative_name, at least one must be None.')
        if not None and relative_name and crl_issuer:
            raise ValueError('Either full_name, relative_name or crl_issuer must be provided.')
        if None is not None:
            full_name = list(full_name)
            if not all((lambda .0: for x in .0:
isinstance(x, GeneralName))(full_name)):
                raise TypeError('full_name must be a list of GeneralName objects')
            if not None and isinstance(relative_name, RelativeDistinguishedName):
                raise TypeError('relative_name must be a RelativeDistinguishedName')
            if None is not None:
                crl_issuer = list(crl_issuer)
                if not all((lambda .0: for x in .0:
isinstance(x, GeneralName))(crl_issuer)):
                    raise TypeError('crl_issuer must be None or a list of general names')
                if None:
                    if not isinstance(reasons, frozenset) or all((lambda .0: for x in .0:
isinstance(x, ReasonFlags))(reasons)):
                        raise TypeError('reasons must be None or frozenset of ReasonFlags')
                    if None:
                        if ReasonFlags.unspecified in reasons or ReasonFlags.remove_from_crl in reasons:
                            raise ValueError('unspecified and remove_from_crl are not valid reasons in a DistributionPoint')
                        self._full_name = None
                        self._relative_name = relative_name
                        self._reasons = reasons
                        self._crl_issuer = crl_issuer
                        return None

    
    def __repr__(self = None):
        return '<DistributionPoint(full_name={0.full_name}, relative_name={0.relative_name}, reasons={0.reasons}, crl_issuer={0.crl_issuer})>'.format(self)

    
    def __eq__(self = None, other = None):
        if not isinstance(other, DistributionPoint):
            return NotImplemented
        if None.full_name == other.full_name and self.relative_name == other.relative_name and self.reasons == other.reasons:
            pass
        return self.crl_issuer == other.crl_issuer

    
    def __hash__(self = None):
        if self.full_name is not None:
            fn = tuple(self.full_name)
        else:
            fn = None
        if self.crl_issuer is not None:
            crl_issuer = tuple(self.crl_issuer)
        else:
            crl_issuer = None
        return hash((fn, self.relative_name, self.reasons, crl_issuer))

    
    def full_name(self = None):
        return self._full_name

    full_name = None(full_name)
    
    def relative_name(self = None):
        return self._relative_name

    relative_name = None(relative_name)
    
    def reasons(self = None):
        return self._reasons

    reasons = None(reasons)
    
    def crl_issuer(self = None):
        return self._crl_issuer

    crl_issuer = None(crl_issuer)


class ReasonFlags(utils.Enum):
    unspecified = 'unspecified'
    key_compromise = 'keyCompromise'
    ca_compromise = 'cACompromise'
    affiliation_changed = 'affiliationChanged'
    superseded = 'superseded'
    cessation_of_operation = 'cessationOfOperation'
    certificate_hold = 'certificateHold'
    privilege_withdrawn = 'privilegeWithdrawn'
    aa_compromise = 'aACompromise'
    remove_from_crl = 'removeFromCRL'

_REASON_BIT_MAPPING = {
    1: ReasonFlags.key_compromise,
    2: ReasonFlags.ca_compromise,
    3: ReasonFlags.affiliation_changed,
    4: ReasonFlags.superseded,
    5: ReasonFlags.cessation_of_operation,
    6: ReasonFlags.certificate_hold,
    7: ReasonFlags.privilege_withdrawn,
    8: ReasonFlags.aa_compromise }
_CRLREASONFLAGS = {
    ReasonFlags.aa_compromise: 8,
    ReasonFlags.privilege_withdrawn: 7,
    ReasonFlags.certificate_hold: 6,
    ReasonFlags.cessation_of_operation: 5,
    ReasonFlags.superseded: 4,
    ReasonFlags.affiliation_changed: 3,
    ReasonFlags.ca_compromise: 2,
    ReasonFlags.key_compromise: 1 }
_CRL_ENTRY_REASON_ENUM_TO_CODE = {
    ReasonFlags.aa_compromise: 10,
    ReasonFlags.privilege_withdrawn: 9,
    ReasonFlags.remove_from_crl: 8,
    ReasonFlags.certificate_hold: 6,
    ReasonFlags.cessation_of_operation: 5,
    ReasonFlags.superseded: 4,
    ReasonFlags.affiliation_changed: 3,
    ReasonFlags.ca_compromise: 2,
    ReasonFlags.key_compromise: 1,
    ReasonFlags.unspecified: 0 }

class PolicyConstraints(ExtensionType):
    oid = ExtensionOID.POLICY_CONSTRAINTS
    
    def __init__(self = None, require_explicit_policy = None, inhibit_policy_mapping = None):
        if not require_explicit_policy is not None and isinstance(require_explicit_policy, int):
            raise TypeError('require_explicit_policy must be a non-negative integer or None')
        if not None is not None and isinstance(inhibit_policy_mapping, int):
            raise TypeError('inhibit_policy_mapping must be a non-negative integer or None')
        if None is None and require_explicit_policy is None:
            raise ValueError('At least one of require_explicit_policy and inhibit_policy_mapping must not be None')
        self._require_explicit_policy = None
        self._inhibit_policy_mapping = inhibit_policy_mapping

    
    def __repr__(self = None):
        return '<PolicyConstraints(require_explicit_policy={0.require_explicit_policy}, inhibit_policy_mapping={0.inhibit_policy_mapping})>'.format(self)

    
    def __eq__(self = None, other = None):
        if not isinstance(other, PolicyConstraints):
            return NotImplemented
        if None.require_explicit_policy == other.require_explicit_policy:
            pass
        return self.inhibit_policy_mapping == other.inhibit_policy_mapping

    
    def __hash__(self = None):
        return hash((self.require_explicit_policy, self.inhibit_policy_mapping))

    
    def require_explicit_policy(self = None):
        return self._require_explicit_policy

    require_explicit_policy = None(require_explicit_policy)
    
    def inhibit_policy_mapping(self = None):
        return self._inhibit_policy_mapping

    inhibit_policy_mapping = None(inhibit_policy_mapping)
    
    def public_bytes(self = None):
        return rust_x509.encode_extension_value(self)



class CertificatePolicies(ExtensionType):
    oid = ExtensionOID.CERTIFICATE_POLICIES
    
    def __init__(self = None, policies = None):
        policies = list(policies)
        if not all((lambda .0: for x in .0:
isinstance(x, PolicyInformation))(policies)):
            raise TypeError('Every item in the policies list must be a PolicyInformation')
        self._policies = None

    (__len__, __iter__, __getitem__) = _make_sequence_methods('_policies')
    
    def __repr__(self = None):
        return f'''<CertificatePolicies({self._policies})>'''

    
    def __eq__(self = None, other = None):
        if not isinstance(other, CertificatePolicies):
            return NotImplemented
        return None._policies == other._policies

    
    def __hash__(self = None):
        return hash(tuple(self._policies))

    
    def public_bytes(self = None):
        return rust_x509.encode_extension_value(self)



class PolicyInformation:
    
    def __init__(self = None, policy_identifier = None, policy_qualifiers = None):
        if not isinstance(policy_identifier, ObjectIdentifier):
            raise TypeError('policy_identifier must be an ObjectIdentifier')
        self._policy_identifier = None
        if policy_qualifiers is not None:
            policy_qualifiers = list(policy_qualifiers)
            if not all((lambda .0: for x in .0:
isinstance(x, (str, UserNotice)))(policy_qualifiers)):
                raise TypeError('policy_qualifiers must be a list of strings and/or UserNotice objects or None')
            self._policy_qualifiers = None
            return None

    
    def __repr__(self = None):
        return f'''<PolicyInformation(policy_identifier={self.policy_identifier}, policy_qualifiers={self.policy_qualifiers})>'''

    
    def __eq__(self = None, other = None):
        if not isinstance(other, PolicyInformation):
            return NotImplemented
        if None.policy_identifier == other.policy_identifier:
            pass
        return self.policy_qualifiers == other.policy_qualifiers

    
    def __hash__(self = None):
        if self.policy_qualifiers is not None:
            pq = tuple(self.policy_qualifiers)
        else:
            pq = None
        return hash((self.policy_identifier, pq))

    
    def policy_identifier(self = None):
        return self._policy_identifier

    policy_identifier = None(policy_identifier)
    
    def policy_qualifiers(self = None):
        return self._policy_qualifiers

    policy_qualifiers = None(policy_qualifiers)


class UserNotice:
    
    def __init__(self = None, notice_reference = None, explicit_text = None):
        if not notice_reference and isinstance(notice_reference, NoticeReference):
            raise TypeError('notice_reference must be None or a NoticeReference')
        self._notice_reference = None
        self._explicit_text = explicit_text

    
    def __repr__(self = None):
        return f'''<UserNotice(notice_reference={self.notice_reference}, explicit_text={self.explicit_text!r})>'''

    
    def __eq__(self = None, other = None):
        if not isinstance(other, UserNotice):
            return NotImplemented
        if None.notice_reference == other.notice_reference:
            pass
        return self.explicit_text == other.explicit_text

    
    def __hash__(self = None):
        return hash((self.notice_reference, self.explicit_text))

    
    def notice_reference(self = None):
        return self._notice_reference

    notice_reference = None(notice_reference)
    
    def explicit_text(self = None):
        return self._explicit_text

    explicit_text = None(explicit_text)


class NoticeReference:
    
    def __init__(self = None, organization = None, notice_numbers = None):
        self._organization = organization
        notice_numbers = list(notice_numbers)
        if not all((lambda .0: for x in .0:
isinstance(x, int))(notice_numbers)):
            raise TypeError('notice_numbers must be a list of integers')
        self._notice_numbers = None

    
    def __repr__(self = None):
        return f'''<NoticeReference(organization={self.organization!r}, notice_numbers={self.notice_numbers})>'''

    
    def __eq__(self = None, other = None):
        if not isinstance(other, NoticeReference):
            return NotImplemented
        if None.organization == other.organization:
            pass
        return self.notice_numbers == other.notice_numbers

    
    def __hash__(self = None):
        return hash((self.organization, tuple(self.notice_numbers)))

    
    def organization(self = None):
        return self._organization

    organization = None(organization)
    
    def notice_numbers(self = None):
        return self._notice_numbers

    notice_numbers = None(notice_numbers)


class ExtendedKeyUsage(ExtensionType):
    oid = ExtensionOID.EXTENDED_KEY_USAGE
    
    def __init__(self = None, usages = None):
        usages = list(usages)
        if not all((lambda .0: for x in .0:
isinstance(x, ObjectIdentifier))(usages)):
            raise TypeError('Every item in the usages list must be an ObjectIdentifier')
        self._usages = None

    (__len__, __iter__, __getitem__) = _make_sequence_methods('_usages')
    
    def __repr__(self = None):
        return f'''<ExtendedKeyUsage({self._usages})>'''

    
    def __eq__(self = None, other = None):
        if not isinstance(other, ExtendedKeyUsage):
            return NotImplemented
        return None._usages == other._usages

    
    def __hash__(self = None):
        return hash(tuple(self._usages))

    
    def public_bytes(self = None):
        return rust_x509.encode_extension_value(self)



class OCSPNoCheck(ExtensionType):
    oid = ExtensionOID.OCSP_NO_CHECK
    
    def __eq__(self = None, other = None):
        if not isinstance(other, OCSPNoCheck):
            return NotImplemented

    
    def __hash__(self = None):
        return hash(OCSPNoCheck)

    
    def __repr__(self = None):
        return '<OCSPNoCheck()>'

    
    def public_bytes(self = None):
        return rust_x509.encode_extension_value(self)



class PrecertPoison(ExtensionType):
    oid = ExtensionOID.PRECERT_POISON
    
    def __eq__(self = None, other = None):
        if not isinstance(other, PrecertPoison):
            return NotImplemented

    
    def __hash__(self = None):
        return hash(PrecertPoison)

    
    def __repr__(self = None):
        return '<PrecertPoison()>'

    
    def public_bytes(self = None):
        return rust_x509.encode_extension_value(self)



class TLSFeature(ExtensionType):
    oid = ExtensionOID.TLS_FEATURE
    
    def __init__(self = None, features = None):
        features = list(features)
        if all((lambda .0: for x in .0:
isinstance(x, TLSFeatureType))(features)) or len(features) == 0:
            raise TypeError('features must be a list of elements from the TLSFeatureType enum')
        self._features = None

    (__len__, __iter__, __getitem__) = _make_sequence_methods('_features')
    
    def __repr__(self = None):
        return f'''<TLSFeature(features={self._features})>'''

    
    def __eq__(self = None, other = None):
        if not isinstance(other, TLSFeature):
            return NotImplemented
        return None._features == other._features

    
    def __hash__(self = None):
        return hash(tuple(self._features))

    
    def public_bytes(self = None):
        return rust_x509.encode_extension_value(self)



class TLSFeatureType(utils.Enum):
    status_request = 5
    status_request_v2 = 17

_TLS_FEATURE_TYPE_TO_ENUM = (lambda .0: pass# WARNING: Decompyle incomplete
)(TLSFeatureType)

class InhibitAnyPolicy(ExtensionType):
    oid = ExtensionOID.INHIBIT_ANY_POLICY
    
    def __init__(self = None, skip_certs = None):
        if not isinstance(skip_certs, int):
            raise TypeError('skip_certs must be an integer')
        if None < 0:
            raise ValueError('skip_certs must be a non-negative integer')
        self._skip_certs = None

    
    def __repr__(self = None):
        return f'''<InhibitAnyPolicy(skip_certs={self.skip_certs})>'''

    
    def __eq__(self = None, other = None):
        if not isinstance(other, InhibitAnyPolicy):
            return NotImplemented
        return None.skip_certs == other.skip_certs

    
    def __hash__(self = None):
        return hash(self.skip_certs)

    
    def skip_certs(self = None):
        return self._skip_certs

    skip_certs = None(skip_certs)
    
    def public_bytes(self = None):
        return rust_x509.encode_extension_value(self)



class KeyUsage(ExtensionType):
    oid = ExtensionOID.KEY_USAGE
    
    def __init__(self, digital_signature, content_commitment, key_encipherment, data_encipherment, key_agreement, key_cert_sign = None, crl_sign = None, encipher_only = None, decipher_only = ('digital_signature', 'bool', 'content_commitment', 'bool', 'key_encipherment', 'bool', 'data_encipherment', 'bool', 'key_agreement', 'bool', 'key_cert_sign', 'bool', 'crl_sign', 'bool', 'encipher_only', 'bool', 'decipher_only', 'bool', 'return', 'None')):
        if not key_agreement:
            if encipher_only or decipher_only:
                raise ValueError('encipher_only and decipher_only can only be true when key_agreement is true')
            self._digital_signature = None
            self._content_commitment = content_commitment
            self._key_encipherment = key_encipherment
            self._data_encipherment = data_encipherment
            self._key_agreement = key_agreement
            self._key_cert_sign = key_cert_sign
            self._crl_sign = crl_sign
            self._encipher_only = encipher_only
            self._decipher_only = decipher_only
            return None

    
    def digital_signature(self = None):
        return self._digital_signature

    digital_signature = None(digital_signature)
    
    def content_commitment(self = None):
        return self._content_commitment

    content_commitment = None(content_commitment)
    
    def key_encipherment(self = None):
        return self._key_encipherment

    key_encipherment = None(key_encipherment)
    
    def data_encipherment(self = None):
        return self._data_encipherment

    data_encipherment = None(data_encipherment)
    
    def key_agreement(self = None):
        return self._key_agreement

    key_agreement = None(key_agreement)
    
    def key_cert_sign(self = None):
        return self._key_cert_sign

    key_cert_sign = None(key_cert_sign)
    
    def crl_sign(self = None):
        return self._crl_sign

    crl_sign = None(crl_sign)
    
    def encipher_only(self = None):
        if not self.key_agreement:
            raise ValueError('encipher_only is undefined unless key_agreement is true')
        return None._encipher_only

    encipher_only = None(encipher_only)
    
    def decipher_only(self = None):
        if not self.key_agreement:
            raise ValueError('decipher_only is undefined unless key_agreement is true')
        return None._decipher_only

    decipher_only = None(decipher_only)
    
    def __repr__(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def __eq__(self = None, other = None):
        if not isinstance(other, KeyUsage):
            return NotImplemented
        if None.digital_signature == other.digital_signature and self.content_commitment == other.content_commitment and self.key_encipherment == other.key_encipherment and self.data_encipherment == other.data_encipherment and self.key_agreement == other.key_agreement and self.key_cert_sign == other.key_cert_sign and self.crl_sign == other.crl_sign and self._encipher_only == other._encipher_only:
            pass
        return self._decipher_only == other._decipher_only

    
    def __hash__(self = None):
        return hash((self.digital_signature, self.content_commitment, self.key_encipherment, self.data_encipherment, self.key_agreement, self.key_cert_sign, self.crl_sign, self._encipher_only, self._decipher_only))

    
    def public_bytes(self = None):
        return rust_x509.encode_extension_value(self)



class NameConstraints(ExtensionType):
    oid = ExtensionOID.NAME_CONSTRAINTS
    
    def __init__(self = None, permitted_subtrees = None, excluded_subtrees = None):
        if permitted_subtrees is not None:
            permitted_subtrees = list(permitted_subtrees)
            if not permitted_subtrees:
                raise ValueError('permitted_subtrees must be a non-empty list or None')
            if not None((lambda .0: for x in .0:
isinstance(x, GeneralName))(permitted_subtrees)):
                raise TypeError('permitted_subtrees must be a list of GeneralName objects or None')
            None._validate_tree(permitted_subtrees)
        if excluded_subtrees is not None:
            excluded_subtrees = list(excluded_subtrees)
            if not excluded_subtrees:
                raise ValueError('excluded_subtrees must be a non-empty list or None')
            if not None((lambda .0: for x in .0:
isinstance(x, GeneralName))(excluded_subtrees)):
                raise TypeError('excluded_subtrees must be a list of GeneralName objects or None')
            None._validate_tree(excluded_subtrees)
        if permitted_subtrees is None and excluded_subtrees is None:
            raise ValueError('At least one of permitted_subtrees and excluded_subtrees must not be None')
        self._permitted_subtrees = None
        self._excluded_subtrees = excluded_subtrees

    
    def __eq__(self = None, other = None):
        if not isinstance(other, NameConstraints):
            return NotImplemented
        if None.excluded_subtrees == other.excluded_subtrees:
            pass
        return self.permitted_subtrees == other.permitted_subtrees

    
    def _validate_tree(self = None, tree = None):
        self._validate_ip_name(tree)
        self._validate_dns_name(tree)

    
    def _validate_ip_name(self = None, tree = None):
        if any((lambda .0: for name in .0:
if isinstance(name, IPAddress):
passnot isinstance(name.value, (ipaddress.IPv4Network, ipaddress.IPv6Network)))(tree)):
            raise TypeError('IPAddress name constraints must be an IPv4Network or IPv6Network object')

    
    def _validate_dns_name(self = None, tree = None):
        if any((lambda .0: for name in .0:
if isinstance(name, DNSName):
pass'*' in name.value)(tree)):
            raise ValueError("DNSName name constraints must not contain the '*' wildcard character")

    
    def __repr__(self = None):
        return f'''<NameConstraints(permitted_subtrees={self.permitted_subtrees}, excluded_subtrees={self.excluded_subtrees})>'''

    
    def __hash__(self = None):
        if self.permitted_subtrees is not None:
            ps = tuple(self.permitted_subtrees)
        else:
            ps = None
        if self.excluded_subtrees is not None:
            es = tuple(self.excluded_subtrees)
        else:
            es = None
        return hash((ps, es))

    
    def permitted_subtrees(self = None):
        return self._permitted_subtrees

    permitted_subtrees = None(permitted_subtrees)
    
    def excluded_subtrees(self = None):
        return self._excluded_subtrees

    excluded_subtrees = None(excluded_subtrees)
    
    def public_bytes(self = None):
        return rust_x509.encode_extension_value(self)



def Extension():
    '''Extension'''
    
    def __init__(self = None, oid = None, critical = None, value = ('oid', 'ObjectIdentifier', 'critical', 'bool', 'value', 'ExtensionTypeVar', 'return', 'None')):
        if not isinstance(oid, ObjectIdentifier):
            raise TypeError('oid argument must be an ObjectIdentifier instance.')
        if not None(critical, bool):
            raise TypeError('critical must be a boolean value')
        self._oid = None
        self._critical = critical
        self._value = value

    
    def oid(self = None):
        return self._oid

    oid = None(oid)
    
    def critical(self = None):
        return self._critical

    critical = None(critical)
    
    def value(self = None):
        return self._value

    value = None(value)
    
    def __repr__(self = None):
        return f'''<Extension(oid={self.oid}, critical={self.critical}, value={self.value})>'''

    
    def __eq__(self = None, other = None):
        if not isinstance(other, Extension):
            return NotImplemented
        if None.oid == other.oid and self.critical == other.critical:
            pass
        return self.value == other.value

    
    def __hash__(self = None):
        return hash((self.oid, self.critical, self.value))


Extension = <NODE:27>(Extension, 'Extension', typing.Generic[ExtensionTypeVar])

class GeneralNames:
    
    def __init__(self = None, general_names = None):
        general_names = list(general_names)
        if not all((lambda .0: for x in .0:
isinstance(x, GeneralName))(general_names)):
            raise TypeError('Every item in the general_names list must be an object conforming to the GeneralName interface')
        self._general_names = None

    (__len__, __iter__, __getitem__) = _make_sequence_methods('_general_names')
    
    def get_values_for_type(self = None, type = None):
        pass

    get_values_for_type = None(get_values_for_type)
    
    def get_values_for_type(self = None, type = None):
        pass

    get_values_for_type = None(get_values_for_type)
    
    def get_values_for_type(self = None, type = None):
        pass

    get_values_for_type = None(get_values_for_type)
    
    def get_values_for_type(self = None, type = None):
        pass

    get_values_for_type = None(get_values_for_type)
    
    def get_values_for_type(self = None, type = None):
        pass

    get_values_for_type = None(get_values_for_type)
    
    def get_values_for_type(self = None, type = None):
        objs = (lambda .0 = None: for i in .0:
if isinstance(i, type):
icontinueNone)(self)
        if type != OtherName:
            return (lambda .0: [ i.value for i in .0 ])(objs)
        return None(objs)

    
    def __repr__(self = None):
        return f'''<GeneralNames({self._general_names})>'''

    
    def __eq__(self = None, other = None):
        if not isinstance(other, GeneralNames):
            return NotImplemented
        return None._general_names == other._general_names

    
    def __hash__(self = None):
        return hash(tuple(self._general_names))



class SubjectAlternativeName(ExtensionType):
    oid = ExtensionOID.SUBJECT_ALTERNATIVE_NAME
    
    def __init__(self = None, general_names = None):
        self._general_names = GeneralNames(general_names)

    (__len__, __iter__, __getitem__) = _make_sequence_methods('_general_names')
    
    def get_values_for_type(self = None, type = None):
        pass

    get_values_for_type = None(get_values_for_type)
    
    def get_values_for_type(self = None, type = None):
        pass

    get_values_for_type = None(get_values_for_type)
    
    def get_values_for_type(self = None, type = None):
        pass

    get_values_for_type = None(get_values_for_type)
    
    def get_values_for_type(self = None, type = None):
        pass

    get_values_for_type = None(get_values_for_type)
    
    def get_values_for_type(self = None, type = None):
        pass

    get_values_for_type = None(get_values_for_type)
    
    def get_values_for_type(self = None, type = None):
        return self._general_names.get_values_for_type(type)

    
    def __repr__(self = None):
        return f'''<SubjectAlternativeName({self._general_names})>'''

    
    def __eq__(self = None, other = None):
        if not isinstance(other, SubjectAlternativeName):
            return NotImplemented
        return None._general_names == other._general_names

    
    def __hash__(self = None):
        return hash(self._general_names)

    
    def public_bytes(self = None):
        return rust_x509.encode_extension_value(self)



class IssuerAlternativeName(ExtensionType):
    oid = ExtensionOID.ISSUER_ALTERNATIVE_NAME
    
    def __init__(self = None, general_names = None):
        self._general_names = GeneralNames(general_names)

    (__len__, __iter__, __getitem__) = _make_sequence_methods('_general_names')
    
    def get_values_for_type(self = None, type = None):
        pass

    get_values_for_type = None(get_values_for_type)
    
    def get_values_for_type(self = None, type = None):
        pass

    get_values_for_type = None(get_values_for_type)
    
    def get_values_for_type(self = None, type = None):
        pass

    get_values_for_type = None(get_values_for_type)
    
    def get_values_for_type(self = None, type = None):
        pass

    get_values_for_type = None(get_values_for_type)
    
    def get_values_for_type(self = None, type = None):
        pass

    get_values_for_type = None(get_values_for_type)
    
    def get_values_for_type(self = None, type = None):
        return self._general_names.get_values_for_type(type)

    
    def __repr__(self = None):
        return f'''<IssuerAlternativeName({self._general_names})>'''

    
    def __eq__(self = None, other = None):
        if not isinstance(other, IssuerAlternativeName):
            return NotImplemented
        return None._general_names == other._general_names

    
    def __hash__(self = None):
        return hash(self._general_names)

    
    def public_bytes(self = None):
        return rust_x509.encode_extension_value(self)



class CertificateIssuer(ExtensionType):
    oid = CRLEntryExtensionOID.CERTIFICATE_ISSUER
    
    def __init__(self = None, general_names = None):
        self._general_names = GeneralNames(general_names)

    (__len__, __iter__, __getitem__) = _make_sequence_methods('_general_names')
    
    def get_values_for_type(self = None, type = None):
        pass

    get_values_for_type = None(get_values_for_type)
    
    def get_values_for_type(self = None, type = None):
        pass

    get_values_for_type = None(get_values_for_type)
    
    def get_values_for_type(self = None, type = None):
        pass

    get_values_for_type = None(get_values_for_type)
    
    def get_values_for_type(self = None, type = None):
        pass

    get_values_for_type = None(get_values_for_type)
    
    def get_values_for_type(self = None, type = None):
        pass

    get_values_for_type = None(get_values_for_type)
    
    def get_values_for_type(self = None, type = None):
        return self._general_names.get_values_for_type(type)

    
    def __repr__(self = None):
        return f'''<CertificateIssuer({self._general_names})>'''

    
    def __eq__(self = None, other = None):
        if not isinstance(other, CertificateIssuer):
            return NotImplemented
        return None._general_names == other._general_names

    
    def __hash__(self = None):
        return hash(self._general_names)

    
    def public_bytes(self = None):
        return rust_x509.encode_extension_value(self)



class CRLReason(ExtensionType):
    oid = CRLEntryExtensionOID.CRL_REASON
    
    def __init__(self = None, reason = None):
        if not isinstance(reason, ReasonFlags):
            raise TypeError('reason must be an element from ReasonFlags')
        self._reason = None

    
    def __repr__(self = None):
        return f'''<CRLReason(reason={self._reason})>'''

    
    def __eq__(self = None, other = None):
        if not isinstance(other, CRLReason):
            return NotImplemented
        return None.reason == other.reason

    
    def __hash__(self = None):
        return hash(self.reason)

    
    def reason(self = None):
        return self._reason

    reason = None(reason)
    
    def public_bytes(self = None):
        return rust_x509.encode_extension_value(self)



class InvalidityDate(ExtensionType):
    oid = CRLEntryExtensionOID.INVALIDITY_DATE
    
    def __init__(self = None, invalidity_date = None):
        if not isinstance(invalidity_date, datetime.datetime):
            raise TypeError('invalidity_date must be a datetime.datetime')
        self._invalidity_date = None

    
    def __repr__(self = None):
        return f'''<InvalidityDate(invalidity_date={self._invalidity_date})>'''

    
    def __eq__(self = None, other = None):
        if not isinstance(other, InvalidityDate):
            return NotImplemented
        return None.invalidity_date == other.invalidity_date

    
    def __hash__(self = None):
        return hash(self.invalidity_date)

    
    def invalidity_date(self = None):
        return self._invalidity_date

    invalidity_date = None(invalidity_date)
    
    def invalidity_date_utc(self = None):
        if self._invalidity_date.tzinfo is None:
            return self._invalidity_date.replace(datetime.timezone.utc, **('tzinfo',))
        return None._invalidity_date.astimezone(datetime.timezone.utc, **('tz',))

    invalidity_date_utc = None(invalidity_date_utc)
    
    def public_bytes(self = None):
        return rust_x509.encode_extension_value(self)



class PrecertificateSignedCertificateTimestamps(ExtensionType):
    oid = ExtensionOID.PRECERT_SIGNED_CERTIFICATE_TIMESTAMPS
    
    def __init__(self = None, signed_certificate_timestamps = None):
        signed_certificate_timestamps = list(signed_certificate_timestamps)
        if not all((lambda .0: for sct in .0:
isinstance(sct, SignedCertificateTimestamp))(signed_certificate_timestamps)):
            raise TypeError('Every item in the signed_certificate_timestamps list must be a SignedCertificateTimestamp')
        self._signed_certificate_timestamps = None

    (__len__, __iter__, __getitem__) = _make_sequence_methods('_signed_certificate_timestamps')
    
    def __repr__(self = None):
        return f'''<PrecertificateSignedCertificateTimestamps({list(self)})>'''

    
    def __hash__(self = None):
        return hash(tuple(self._signed_certificate_timestamps))

    
    def __eq__(self = None, other = None):
        if not isinstance(other, PrecertificateSignedCertificateTimestamps):
            return NotImplemented
        return None._signed_certificate_timestamps == other._signed_certificate_timestamps

    
    def public_bytes(self = None):
        return rust_x509.encode_extension_value(self)



class SignedCertificateTimestamps(ExtensionType):
    oid = ExtensionOID.SIGNED_CERTIFICATE_TIMESTAMPS
    
    def __init__(self = None, signed_certificate_timestamps = None):
        signed_certificate_timestamps = list(signed_certificate_timestamps)
        if not all((lambda .0: for sct in .0:
isinstance(sct, SignedCertificateTimestamp))(signed_certificate_timestamps)):
            raise TypeError('Every item in the signed_certificate_timestamps list must be a SignedCertificateTimestamp')
        self._signed_certificate_timestamps = None

    (__len__, __iter__, __getitem__) = _make_sequence_methods('_signed_certificate_timestamps')
    
    def __repr__(self = None):
        return f'''<SignedCertificateTimestamps({list(self)})>'''

    
    def __hash__(self = None):
        return hash(tuple(self._signed_certificate_timestamps))

    
    def __eq__(self = None, other = None):
        if not isinstance(other, SignedCertificateTimestamps):
            return NotImplemented
        return None._signed_certificate_timestamps == other._signed_certificate_timestamps

    
    def public_bytes(self = None):
        return rust_x509.encode_extension_value(self)



class OCSPNonce(ExtensionType):
    oid = OCSPExtensionOID.NONCE
    
    def __init__(self = None, nonce = None):
        if not isinstance(nonce, bytes):
            raise TypeError('nonce must be bytes')
        self._nonce = None

    
    def __eq__(self = None, other = None):
        if not isinstance(other, OCSPNonce):
            return NotImplemented
        return None.nonce == other.nonce

    
    def __hash__(self = None):
        return hash(self.nonce)

    
    def __repr__(self = None):
        return f'''<OCSPNonce(nonce={self.nonce!r})>'''

    
    def nonce(self = None):
        return self._nonce

    nonce = None(nonce)
    
    def public_bytes(self = None):
        return rust_x509.encode_extension_value(self)



class OCSPAcceptableResponses(ExtensionType):
    oid = OCSPExtensionOID.ACCEPTABLE_RESPONSES
    
    def __init__(self = None, responses = None):
        responses = list(responses)
        if any((lambda .0: for r in .0:
not isinstance(r, ObjectIdentifier))(responses)):
            raise TypeError('All responses must be ObjectIdentifiers')
        self._responses = None

    
    def __eq__(self = None, other = None):
        if not isinstance(other, OCSPAcceptableResponses):
            return NotImplemented
        return None._responses == other._responses

    
    def __hash__(self = None):
        return hash(tuple(self._responses))

    
    def __repr__(self = None):
        return f'''<OCSPAcceptableResponses(responses={self._responses})>'''

    
    def __iter__(self = None):
        return iter(self._responses)

    
    def public_bytes(self = None):
        return rust_x509.encode_extension_value(self)



class IssuingDistributionPoint(ExtensionType):
    oid = ExtensionOID.ISSUING_DISTRIBUTION_POINT
    
    def __init__(self, full_name, relative_name, only_contains_user_certs, only_contains_ca_certs = None, only_some_reasons = None, indirect_crl = None, only_contains_attribute_certs = ('full_name', 'typing.Iterable[GeneralName] | None', 'relative_name', 'RelativeDistinguishedName | None', 'only_contains_user_certs', 'bool', 'only_contains_ca_certs', 'bool', 'only_some_reasons', 'frozenset[ReasonFlags] | None', 'indirect_crl', 'bool', 'only_contains_attribute_certs', 'bool', 'return', 'None')):
        if full_name is not None:
            full_name = list(full_name)
        if only_some_reasons:
            if not isinstance(only_some_reasons, frozenset) or all((lambda .0: for x in .0:
isinstance(x, ReasonFlags))(only_some_reasons)):
                raise TypeError('only_some_reasons must be None or frozenset of ReasonFlags')
            if None:
                if ReasonFlags.unspecified in only_some_reasons or ReasonFlags.remove_from_crl in only_some_reasons:
                    raise ValueError('unspecified and remove_from_crl are not valid reasons in an IssuingDistributionPoint')
                if not None(only_contains_user_certs, bool) and isinstance(only_contains_ca_certs, bool) and isinstance(indirect_crl, bool) or isinstance(only_contains_attribute_certs, bool):
                    raise TypeError('only_contains_user_certs, only_contains_ca_certs, indirect_crl and only_contains_attribute_certs must all be boolean.')
                crl_constraints = [
                    None,
                    only_contains_ca_certs,
                    indirect_crl,
                    only_contains_attribute_certs]
                if len((lambda .0: [ x for x in .0 if x ])(crl_constraints)) > 1:
                    raise ValueError('Only one of the following can be set to True: only_contains_user_certs, only_contains_ca_certs, indirect_crl, only_contains_attribute_certs')
                if not None([
                    only_contains_user_certs,
                    only_contains_ca_certs,
                    indirect_crl,
                    only_contains_attribute_certs,
                    full_name,
                    relative_name,
                    only_some_reasons]):
                    raise ValueError('Cannot create empty extension: if only_contains_user_certs, only_contains_ca_certs, indirect_crl, and only_contains_attribute_certs are all False, then either full_name, relative_name, or only_some_reasons must have a value.')
                self._only_contains_user_certs = None
                self._only_contains_ca_certs = only_contains_ca_certs
                self._indirect_crl = indirect_crl
                self._only_contains_attribute_certs = only_contains_attribute_certs
                self._only_some_reasons = only_some_reasons
                self._full_name = full_name
                self._relative_name = relative_name
                return None

    
    def __repr__(self = None):
        return f'''<IssuingDistributionPoint(full_name={self.full_name}, relative_name={self.relative_name}, only_contains_user_certs={self.only_contains_user_certs}, only_contains_ca_certs={self.only_contains_ca_certs}, only_some_reasons={self.only_some_reasons}, indirect_crl={self.indirect_crl}, only_contains_attribute_certs={self.only_contains_attribute_certs})>'''

    
    def __eq__(self = None, other = None):
        if not isinstance(other, IssuingDistributionPoint):
            return NotImplemented
        if None.full_name == other.full_name and self.relative_name == other.relative_name and self.only_contains_user_certs == other.only_contains_user_certs and self.only_contains_ca_certs == other.only_contains_ca_certs and self.only_some_reasons == other.only_some_reasons and self.indirect_crl == other.indirect_crl:
            pass
        return self.only_contains_attribute_certs == other.only_contains_attribute_certs

    
    def __hash__(self = None):
        return hash((self.full_name, self.relative_name, self.only_contains_user_certs, self.only_contains_ca_certs, self.only_some_reasons, self.indirect_crl, self.only_contains_attribute_certs))

    
    def full_name(self = None):
        return self._full_name

    full_name = None(full_name)
    
    def relative_name(self = None):
        return self._relative_name

    relative_name = None(relative_name)
    
    def only_contains_user_certs(self = None):
        return self._only_contains_user_certs

    only_contains_user_certs = None(only_contains_user_certs)
    
    def only_contains_ca_certs(self = None):
        return self._only_contains_ca_certs

    only_contains_ca_certs = None(only_contains_ca_certs)
    
    def only_some_reasons(self = None):
        return self._only_some_reasons

    only_some_reasons = None(only_some_reasons)
    
    def indirect_crl(self = None):
        return self._indirect_crl

    indirect_crl = None(indirect_crl)
    
    def only_contains_attribute_certs(self = None):
        return self._only_contains_attribute_certs

    only_contains_attribute_certs = None(only_contains_attribute_certs)
    
    def public_bytes(self = None):
        return rust_x509.encode_extension_value(self)



class MSCertificateTemplate(ExtensionType):
    oid = ExtensionOID.MS_CERTIFICATE_TEMPLATE
    
    def __init__(self = None, template_id = None, major_version = None, minor_version = ('template_id', 'ObjectIdentifier', 'major_version', 'int | None', 'minor_version', 'int | None', 'return', 'None')):
        if not isinstance(template_id, ObjectIdentifier):
            raise TypeError('oid must be an ObjectIdentifier')
        self._template_id = None
        if not (major_version is not None or isinstance(major_version, int) or minor_version is not None) and isinstance(minor_version, int):
            raise TypeError('major_version and minor_version must be integers or None')
        self._major_version = None
        self._minor_version = minor_version

    
    def template_id(self = None):
        return self._template_id

    template_id = None(template_id)
    
    def major_version(self = None):
        return self._major_version

    major_version = None(major_version)
    
    def minor_version(self = None):
        return self._minor_version

    minor_version = None(minor_version)
    
    def __repr__(self = None):
        return f'''<MSCertificateTemplate(template_id={self.template_id}, major_version={self.major_version}, minor_version={self.minor_version})>'''

    
    def __eq__(self = None, other = None):
        if not isinstance(other, MSCertificateTemplate):
            return NotImplemented
        if None.template_id == other.template_id and self.major_version == other.major_version:
            pass
        return self.minor_version == other.minor_version

    
    def __hash__(self = None):
        return hash((self.template_id, self.major_version, self.minor_version))

    
    def public_bytes(self = None):
        return rust_x509.encode_extension_value(self)



class UnrecognizedExtension(ExtensionType):
    
    def __init__(self = None, oid = None, value = None):
        if not isinstance(oid, ObjectIdentifier):
            raise TypeError('oid must be an ObjectIdentifier')
        self._oid = None
        self._value = value

    
    def oid(self = None):
        return self._oid

    oid = None(oid)
    
    def value(self = None):
        return self._value

    value = None(value)
    
    def __repr__(self = None):
        return f'''<UnrecognizedExtension(oid={self.oid}, value={self.value!r})>'''

    
    def __eq__(self = None, other = None):
        if not isinstance(other, UnrecognizedExtension):
            return NotImplemented
        if None.oid == other.oid:
            pass
        return self.value == other.value

    
    def __hash__(self = None):
        return hash((self.oid, self.value))

    
    def public_bytes(self = None):
        return self.value


