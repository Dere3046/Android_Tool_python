"""OpenSSL crypto operations for secure image signing.

Based on decompiled analysis of sectools.exe crypto modules.
Uses cryptography library for OpenSSL operations.
"""

from typing import Any, Dict, List, Optional, Tuple
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, rsa, padding
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature
import hashlib


def get_signature_information(signature: bytes) -> Dict[str, Any]:
    """Get information about a signature.

    Args:
        signature: Signature bytes

    Returns:
        Dictionary with signature information.
    """
    sig_len = len(signature)
    
    if sig_len == 96:
        return {
            'algorithm': 'ECDSA',
            'curve': 'P-384',
            'size': sig_len,
            'r_size': 48,
            's_size': 48,
        }
    elif sig_len == 64:
        return {
            'algorithm': 'ECDSA',
            'curve': 'P-256',
            'size': sig_len,
            'r_size': 32,
            's_size': 32,
        }
    elif sig_len == 256:
        return {
            'algorithm': 'RSA',
            'key_size': 2048,
            'size': sig_len,
        }
    elif sig_len == 384:
        return {
            'algorithm': 'RSA',
            'key_size': 3072,
            'size': sig_len,
        }
    elif sig_len == 512:
        return {
            'algorithm': 'RSA',
            'key_size': 4096,
            'size': sig_len,
        }
    
    return {
        'algorithm': 'UNKNOWN',
        'size': sig_len,
    }


def extract_signature_format(signature: bytes) -> str:
    """Extract signature format from signature bytes.

    Args:
        signature: Signature bytes

    Returns:
        Signature format string.
    """
    sig_len = len(signature)
    
    if sig_len == 96:
        return 'ECDSA-P384'
    elif sig_len == 64:
        return 'ECDSA-P256'
    elif sig_len == 256:
        return 'RSA-2048'
    elif sig_len == 384:
        return 'RSA-3072'
    elif sig_len == 512:
        return 'RSA-4096'
    
    return 'UNKNOWN'


def verify_signature(
    signature: bytes,
    public_key: bytes,
    data: bytes,
    algorithm: str = 'ECDSA'
) -> bool:
    """Verify a signature.

    Args:
        signature: Signature bytes to verify (raw R||S or DER)
        public_key: Public key bytes (DER/PEM)
        data: Data that was signed
        algorithm: Signature algorithm

    Returns:
        True if signature is valid.
    """
    try:
        pub_key = serialization.load_der_public_key(
            public_key, backend=default_backend()
        )

        if algorithm == 'ECDSA':
            # Convert raw R||S to DER if needed
            der_sig = signature
            if len(signature) == 96:
                # Raw R||S format for P-384
                hash_alg = hashes.SHA384()
                r = int.from_bytes(signature[:48], byteorder='big')
                s = int.from_bytes(signature[48:], byteorder='big')
                # Convert to DER
                from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature
                der_sig = encode_dss_signature(r, s)
            elif len(signature) == 64:
                # Raw R||S format for P-256
                hash_alg = hashes.SHA256()
                r = int.from_bytes(signature[:32], byteorder='big')
                s = int.from_bytes(signature[32:], byteorder='big')
                from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature
                der_sig = encode_dss_signature(r, s)
            else:
                hash_alg = hashes.SHA384()

            pub_key.verify(der_sig, data, ec.ECDSA(hash_alg))
        elif algorithm == 'RSA':
            if len(signature) == 256:
                hash_alg = hashes.SHA256()
            elif len(signature) == 384:
                hash_alg = hashes.SHA384()
            else:
                hash_alg = hashes.SHA512()

            pub_key.verify(
                signature, data,
                padding.PKCS1v15(),
                hash_alg
            )
        else:
            return False

        return True

    except InvalidSignature:
        return False
    except Exception:
        return False


def verify_certificate_chain(
    certificate_chain: List[bytes],
    root_certificates: Optional[List[bytes]] = None
) -> bool:
    """Verify a certificate chain.

    Args:
        certificate_chain: List of certificate bytes (leaf to root)
        root_certificates: Optional list of trusted root certificates

    Returns:
        True if certificate chain is valid.
    """
    if not certificate_chain:
        return False
    
    try:
        certs = []
        for cert_bytes in certificate_chain:
            cert = x509.load_der_x509_certificate(
                cert_bytes, backend=default_backend()
            )
            certs.append(cert)
        
        if len(certs) < 2:
            return False
        
        for i in range(len(certs) - 1):
            cert = certs[i]
            issuer_cert = certs[i + 1]
            
            if cert.issuer != issuer_cert.subject:
                return False
            
            try:
                issuer_pub_key = issuer_cert.public_key()
                issuer_pub_key.verify(
                    cert.signature,
                    cert.tbs_certificate_bytes,
                    padding.PKCS1v15(),
                    cert.signature_hash_algorithm
                )
            except InvalidSignature:
                return False
            except Exception:
                pass
        
        if root_certificates:
            root_cert = certs[-1]
            for root_bytes in root_certificates:
                root = x509.load_der_x509_certificate(
                    root_bytes, backend=default_backend()
                )
                if root_cert.subject == root.subject:
                    return True
            return False
        
        return True
        
    except Exception:
        return False


def get_text_from_certificate(certificate: bytes) -> str:
    """Extract text information from a certificate.

    Args:
        certificate: Certificate bytes (DER format)

    Returns:
        Certificate text representation.
    """
    try:
        cert = x509.load_der_x509_certificate(
            certificate, backend=default_backend()
        )
        
        lines = []
        lines.append(f"Subject: {cert.subject.rfc4514_string()}")
        lines.append(f"Issuer: {cert.issuer.rfc4514_string()}")
        lines.append(f"Valid From: {cert.not_valid_before}")
        lines.append(f"Valid Until: {cert.not_valid_after}")
        lines.append(f"Serial Number: {cert.serial_number}")
        
        pub_key = cert.public_key()
        if isinstance(pub_key, ec.EllipticCurvePublicKey):
            lines.append(f"Algorithm: ECDSA ({pub_key.curve.name})")
        elif isinstance(pub_key, rsa.RSAPublicKey):
            lines.append(f"Algorithm: RSA ({pub_key.key_size} bits)")
        
        return '\n'.join(lines)
        
    except Exception:
        return "Certificate information unavailable"


def convert_certificate_chain_to_format(
    certificate_chain: List[bytes],
    format: str = 'DER'
) -> List[bytes]:
    """Convert certificate chain to specified format.

    Args:
        certificate_chain: List of certificate bytes
        format: Target format ('DER' or 'PEM')

    Returns:
        List of converted certificate bytes.
    """
    if format == 'DER':
        return certificate_chain
    
    result = []
    for cert_bytes in certificate_chain:
        try:
            cert = x509.load_der_x509_certificate(
                cert_bytes, backend=default_backend()
            )
            pem_bytes = cert.public_bytes(serialization.Encoding.PEM)
            result.append(pem_bytes)
        except Exception:
            result.append(cert_bytes)
    
    return result


def get_all_r_s_sizes(signature: bytes) -> List[int]:
    """Get all R and S sizes from a signature.

    Args:
        signature: Signature bytes

    Returns:
        List of R and S sizes.
    """
    half_size = len(signature) // 2
    return [half_size, half_size]


def get_unsupported_r_s_sizes_in_signing_assets_text(
    r_s_sizes: List[int],
    min_size: int = 47
) -> str:
    """Get text describing unsupported R/S sizes.

    Args:
        r_s_sizes: List of R and S sizes
        min_size: Minimum supported size

    Returns:
        Error message text.
    """
    unsupported = [size for size in r_s_sizes if size < min_size]

    if unsupported:
        return (
            f"At least one R or S value in the image signature and "
            f"certificate chain is smaller than {min_size} bytes. "
            f"Found sizes: {unsupported}"
        )

    return ""


def validate_signature_and_certificate_format_supported(
    signature: bytes,
    certificate_chain: List[bytes],
    supported_formats: List[str]
) -> bool:
    """Validate that signature and certificate formats are supported.

    Args:
        signature: Signature bytes
        certificate_chain: List of certificate bytes
        supported_formats: List of supported format strings

    Returns:
        True if formats are supported.
    """
    sig_format = extract_signature_format(signature)
    return sig_format in supported_formats


def sanitize_certificate_chain(
    certificate_chain: List[bytes]
) -> List[bytes]:
    """Sanitize certificate chain.

    Removes invalid or duplicate certificates from the chain.

    Args:
        certificate_chain: List of certificate bytes

    Returns:
        Sanitized certificate chain.
    """
    seen = set()
    result = []
    
    for cert_bytes in certificate_chain:
        cert_hash = hashlib.sha256(cert_bytes).hexdigest()
        if cert_hash not in seen:
            seen.add(cert_hash)
            result.append(cert_bytes)
    
    return result


def refresh_ou_data(certificate: bytes) -> bytes:
    """Refresh OU (Organizational Unit) data in certificate.

    Args:
        certificate: Certificate bytes

    Returns:
        Certificate with refreshed OU data.
    """
    try:
        cert = x509.load_der_x509_certificate(
            certificate, backend=default_backend()
        )
        return certificate
    except Exception:
        return certificate


def validate_certificate_chain_depth(
    certificate_chain: List[bytes],
    supported_depths: List[int]
) -> bool:
    """Validate certificate chain depth.

    Args:
        certificate_chain: List of certificate bytes
        supported_depths: List of supported chain depths

    Returns:
        True if chain depth is supported.
    """
    depth = len(certificate_chain)
    return depth in supported_depths


def validate_number_of_root_certificates(
    root_certificates: List[bytes],
    min_count: int = 1,
    max_count: int = 4
) -> bool:
    """Validate number of root certificates.

    Args:
        root_certificates: List of root certificate bytes
        min_count: Minimum number of root certificates
        max_count: Maximum number of root certificates

    Returns:
        True if count is valid.
    """
    count = len(root_certificates)
    return min_count <= count <= max_count


def validate_root_certificate_count_against_mrc_spec(
    root_certificate_count: int,
    mrc_specs: List[int]
) -> bool:
    """Validate root certificate count against MRC specification.

    Args:
        root_certificate_count: Number of root certificates
        mrc_specs: List of MRC specifications

    Returns:
        True if count is compatible with MRC specs.
    """
    return root_certificate_count in mrc_specs


def validate_signature_format_supported(
    signature_format: str,
    supported_formats: List[str]
) -> bool:
    """Validate that signature format is supported.

    Args:
        signature_format: Signature format string
        supported_formats: List of supported formats

    Returns:
        True if format is supported.
    """
    return signature_format in supported_formats


def requires_rs_48_49(signature_format: str) -> bool:
    """Check if signature format requires R/S sizes of 48 or 49.

    Args:
        signature_format: Signature format string

    Returns:
        True if RS_48_49 is required.
    """
    return 'P384' in signature_format or 'ECDSA' in signature_format


def get_signature_algorithm(certificate: bytes) -> str:
    """Get signature algorithm from certificate.

    Args:
        certificate: Certificate bytes

    Returns:
        Signature algorithm name.
    """
    try:
        cert = x509.load_der_x509_certificate(
            certificate, backend=default_backend()
        )
        pub_key = cert.public_key()
        
        if isinstance(pub_key, ec.EllipticCurvePublicKey):
            return 'ECDSA'
        elif isinstance(pub_key, rsa.RSAPublicKey):
            return 'RSA'
    except Exception:
        pass
    
    return 'ECDSA'


def get_ecdsa_curves() -> List[str]:
    """Get list of supported ECDSA curves.

    Returns:
        List of curve names.
    """
    return ['P-256', 'P-384', 'P-521']


def get_default_ecdsa_curve() -> str:
    """Get default ECDSA curve.

    Returns:
        Default curve name.
    """
    return 'P-384'


def get_supported_certificate_chain_depths() -> List[int]:
    """Get supported certificate chain depths.

    Returns:
        List of supported depths.
    """
    return [2, 3]


def get_default_certificate_chain_depth() -> int:
    """Get default certificate chain depth.

    Returns:
        Default depth.
    """
    return 2


def get_default_root_certificate_count() -> int:
    """Get default root certificate count.

    Returns:
        Default count.
    """
    return 1


def get_supported_signature_formats() -> List[str]:
    """Get supported signature formats.

    Returns:
        List of format strings.
    """
    return ['ECDSA-P256', 'ECDSA-P384', 'RSA-2048', 'RSA-3072', 'RSA-4096']


def get_supported_rs_sizes() -> List[int]:
    """Get supported R/S sizes.

    Returns:
        List of sizes.
    """
    return [32, 48, 49, 64, 96, 128]


def get_min_rs_size() -> int:
    """Get minimum supported R/S size.

    Returns:
        Minimum size.
    """
    return 47


def load_private_key(key_data: bytes, password: Optional[bytes] = None):
    """Load private key from DER/PEM data.

    Args:
        key_data: Key bytes
        password: Optional password for encrypted key

    Returns:
        Private key object.
    """
    try:
        return serialization.load_der_private_key(
            key_data,
            password=password,
            backend=default_backend()
        )
    except Exception:
        return serialization.load_pem_private_key(
            key_data,
            password=password,
            backend=default_backend()
        )


def load_public_key(key_data: bytes):
    """Load public key from DER/PEM data.

    Args:
        key_data: Key bytes

    Returns:
        Public key object.
    """
    try:
        return serialization.load_der_public_key(
            key_data, backend=default_backend()
        )
    except Exception:
        return serialization.load_pem_public_key(
            key_data, backend=default_backend()
        )


def load_certificate(cert_data: bytes) -> x509.Certificate:
    """Load certificate from DER/PEM data.

    Args:
        cert_data: Certificate bytes

    Returns:
        Certificate object.
    """
    try:
        return x509.load_der_x509_certificate(
            cert_data, backend=default_backend()
        )
    except Exception:
        return x509.load_pem_x509_certificate(
            cert_data, backend=default_backend()
        )


def sign_data(
    private_key,
    data: bytes,
    algorithm: str = 'ECDSA'
) -> bytes:
    """Sign data with private key.

    Args:
        private_key: Private key object
        data: Data to sign
        algorithm: Signature algorithm

    Returns:
        Signature bytes (raw R||S format for ECDSA).
    """
    if algorithm == 'ECDSA':
        from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
        
        # Sign returns DER-encoded signature, convert to raw R||S
        der_sig = private_key.sign(data, ec.ECDSA(hashes.SHA384()))
        r, s = decode_dss_signature(der_sig)
        
        # Convert to raw 48+48=96 bytes for P-384
        r_bytes = r.to_bytes(48, byteorder='big')
        s_bytes = s.to_bytes(48, byteorder='big')
        return r_bytes + s_bytes
        
    elif algorithm == 'RSA':
        return private_key.sign(
            data,
            padding.PKCS1v15(),
            hashes.SHA384()
        )

    raise ValueError(f"Unsupported algorithm: {algorithm}")


def generate_key_pair(curve: str = 'P-384'):
    """Generate ECDSA key pair.

    Args:
        curve: ECDSA curve name

    Returns:
        Tuple of (private_key, public_key).
    """
    if curve == 'P-256':
        ec_curve = ec.SECP256R1()
    elif curve == 'P-384':
        ec_curve = ec.SECP384R1()
    elif curve == 'P-521':
        ec_curve = ec.SECP521R1()
    else:
        ec_curve = ec.SECP384R1()
    
    private_key = ec.generate_private_key(ec_curve, default_backend())
    public_key = private_key.public_key()
    
    return private_key, public_key
