
from __future__ import annotations
import typing
from cryptography import utils
from cryptography.hazmat.primitives.asymmetric import dh, dsa, ec, ed448, ed25519, rsa, x448, x25519
PublicKeyTypes = typing.Union[(dh.DHPublicKey, dsa.DSAPublicKey, rsa.RSAPublicKey, ec.EllipticCurvePublicKey, ed25519.Ed25519PublicKey, ed448.Ed448PublicKey, x25519.X25519PublicKey, x448.X448PublicKey)]
PUBLIC_KEY_TYPES = PublicKeyTypes
utils.deprecated(PUBLIC_KEY_TYPES, __name__, 'Use PublicKeyTypes instead', utils.DeprecatedIn40, 'PUBLIC_KEY_TYPES', **('name',))
PrivateKeyTypes = typing.Union[(dh.DHPrivateKey, ed25519.Ed25519PrivateKey, ed448.Ed448PrivateKey, rsa.RSAPrivateKey, dsa.DSAPrivateKey, ec.EllipticCurvePrivateKey, x25519.X25519PrivateKey, x448.X448PrivateKey)]
PRIVATE_KEY_TYPES = PrivateKeyTypes
utils.deprecated(PRIVATE_KEY_TYPES, __name__, 'Use PrivateKeyTypes instead', utils.DeprecatedIn40, 'PRIVATE_KEY_TYPES', **('name',))
CertificateIssuerPrivateKeyTypes = typing.Union[(ed25519.Ed25519PrivateKey, ed448.Ed448PrivateKey, rsa.RSAPrivateKey, dsa.DSAPrivateKey, ec.EllipticCurvePrivateKey)]
CERTIFICATE_PRIVATE_KEY_TYPES = CertificateIssuerPrivateKeyTypes
utils.deprecated(CERTIFICATE_PRIVATE_KEY_TYPES, __name__, 'Use CertificateIssuerPrivateKeyTypes instead', utils.DeprecatedIn40, 'CERTIFICATE_PRIVATE_KEY_TYPES', **('name',))
CertificateIssuerPublicKeyTypes = typing.Union[(dsa.DSAPublicKey, rsa.RSAPublicKey, ec.EllipticCurvePublicKey, ed25519.Ed25519PublicKey, ed448.Ed448PublicKey)]
CERTIFICATE_ISSUER_PUBLIC_KEY_TYPES = CertificateIssuerPublicKeyTypes
utils.deprecated(CERTIFICATE_ISSUER_PUBLIC_KEY_TYPES, __name__, 'Use CertificateIssuerPublicKeyTypes instead', utils.DeprecatedIn40, 'CERTIFICATE_ISSUER_PUBLIC_KEY_TYPES', **('name',))
CertificatePublicKeyTypes = typing.Union[(dsa.DSAPublicKey, rsa.RSAPublicKey, ec.EllipticCurvePublicKey, ed25519.Ed25519PublicKey, ed448.Ed448PublicKey, x25519.X25519PublicKey, x448.X448PublicKey)]
CERTIFICATE_PUBLIC_KEY_TYPES = CertificatePublicKeyTypes
utils.deprecated(CERTIFICATE_PUBLIC_KEY_TYPES, __name__, 'Use CertificatePublicKeyTypes instead', utils.DeprecatedIn40, 'CERTIFICATE_PUBLIC_KEY_TYPES', **('name',))
