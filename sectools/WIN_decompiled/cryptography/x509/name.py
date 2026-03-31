
from __future__ import annotations
import binascii
import re
import sys
import typing
import warnings
from cryptography import utils
from cryptography.hazmat.bindings._rust import x509 as rust_x509
from cryptography.x509.oid import NameOID, ObjectIdentifier

class _ASN1Type(utils.Enum):
    BitString = 3
    OctetString = 4
    UTF8String = 12
    NumericString = 18
    PrintableString = 19
    T61String = 20
    IA5String = 22
    UTCTime = 23
    GeneralizedTime = 24
    VisibleString = 26
    UniversalString = 28
    BMPString = 30

_ASN1_TYPE_TO_ENUM = (lambda .0: pass# WARNING: Decompyle incomplete
)(_ASN1Type)
_NAMEOID_DEFAULT_TYPE: 'dict[ObjectIdentifier, _ASN1Type]' = {
    NameOID.DOMAIN_COMPONENT: _ASN1Type.IA5String,
    NameOID.EMAIL_ADDRESS: _ASN1Type.IA5String,
    NameOID.DN_QUALIFIER: _ASN1Type.PrintableString,
    NameOID.SERIAL_NUMBER: _ASN1Type.PrintableString,
    NameOID.JURISDICTION_COUNTRY_NAME: _ASN1Type.PrintableString,
    NameOID.COUNTRY_NAME: _ASN1Type.PrintableString }
_OidNameMap = typing.Mapping[(ObjectIdentifier, str)]
_NameOidMap = typing.Mapping[(str, ObjectIdentifier)]
_NAMEOID_TO_NAME: '_OidNameMap' = {
    NameOID.USER_ID: 'UID',
    NameOID.DOMAIN_COMPONENT: 'DC',
    NameOID.STREET_ADDRESS: 'STREET',
    NameOID.COUNTRY_NAME: 'C',
    NameOID.ORGANIZATIONAL_UNIT_NAME: 'OU',
    NameOID.ORGANIZATION_NAME: 'O',
    NameOID.STATE_OR_PROVINCE_NAME: 'ST',
    NameOID.LOCALITY_NAME: 'L',
    NameOID.COMMON_NAME: 'CN' }
_NAME_TO_NAMEOID = (lambda .0: pass# WARNING: Decompyle incomplete
)(_NAMEOID_TO_NAME.items())
_NAMEOID_LENGTH_LIMIT = {
    NameOID.COMMON_NAME: (1, 64),
    NameOID.JURISDICTION_COUNTRY_NAME: (2, 2),
    NameOID.COUNTRY_NAME: (2, 2) }

def _escape_dn_value(val = None):
    '''Escape special characters in RFC4514 Distinguished Name value.'''
    if not val:
        return ''
    if None(val, bytes):
        return '#' + binascii.hexlify(val).decode('utf8')
    val = None.replace('\\', '\\\\')
    val = val.replace('"', '\\"')
    val = val.replace('+', '\\+')
    val = val.replace(',', '\\,')
    val = val.replace(';', '\\;')
    val = val.replace('<', '\\<')
    val = val.replace('>', '\\>')
    val = val.replace('\x00', '\\00')
    if val[0] in ('#', ' '):
        val = '\\' + val
    if val[-1] == ' ':
        val = val[:-1] + '\\ '
    return val


def _unescape_dn_value(val = None):
    if not val:
        return ''
    