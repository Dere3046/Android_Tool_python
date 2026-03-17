"""Local signer implementation based on decompiled analysis."""

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .base_signer import BaseSigner
from common.crypto.openssl import (
    verify_signature,
    verify_certificate_chain,
    get_signature_information,
    extract_signature_format,
    get_supported_signature_formats,
    load_private_key,
    load_certificate,
    sign_data,
    load_public_key,
)


class LocalSigner(BaseSigner):
    """Local signer using provided certificates and keys."""

    def __init__(
        self,
        parsed_image: Any,
        security_profile: Any,
        device_restrictions: Any,
        authority: str,
        outfile: str,
        root_certificates: Optional[List[str]] = None,
        root_key: Optional[str] = None,
        ca_certificate: Optional[str] = None,
        ca_key: Optional[str] = None,
        subject: Optional[str] = None,
    ) -> None:
        """Initialize local signer.

        Args:
            parsed_image: Parsed image object
            security_profile: Security profile object
            device_restrictions: Device restrictions object
            authority: Authority type (OEM or QTI)
            outfile: Output file path
            root_certificates: List of root certificate file paths
            root_key: Root key file path
            ca_certificate: CA certificate file path
            ca_key: CA key file path
            subject: Attestation certificate subject
        """
        super().__init__(
            parsed_image,
            security_profile,
            device_restrictions,
            authority,
        )

        self.outfile = outfile
        self.root_certificates = root_certificates
        self.root_key = root_key
        self.ca_certificate = ca_certificate
        self.ca_key = ca_key
        self.subject = subject

        self._loaded_root_certs: List[bytes] = []
        self._loaded_ca_cert: Optional[bytes] = None
        self._loaded_root_key = None
        self._loaded_ca_key = None

    def _load_certificates_and_keys(self) -> None:
        """Load certificates and keys from files."""
        if self.root_certificates:
            for cert_path in self.root_certificates:
                with open(cert_path, 'rb') as f:
                    self._loaded_root_certs.append(f.read())

        if self.root_key:
            with open(self.root_key, 'rb') as f:
                self._loaded_root_key = load_private_key(f.read())

        if self.ca_certificate:
            with open(self.ca_certificate, 'rb') as f:
                self._loaded_ca_cert = f.read()

        if self.ca_key:
            with open(self.ca_key, 'rb') as f:
                self._loaded_ca_key = load_private_key(f.read())

    def sign(self, image: Any) -> Tuple[bytes, List[bytes]]:
        """Sign the image using local certificates and keys.

        Args:
            image: Image to sign

        Returns:
            Tuple of (signature, certificate_chain).
        """
        self._load_certificates_and_keys()

        image_hash = self._generate_image_hash(image)
        signature = self._sign_hash(image_hash)
        certificate_chain = self._build_certificate_chain()

        return signature, certificate_chain

    def _generate_image_hash(self, image: Any) -> bytes:
        """Generate hash of image for signing.

        Args:
            image: Image to hash

        Returns:
            Image hash bytes.
        """
        import hashlib
        
        if hasattr(image, 'data'):
            data = image.data
        elif isinstance(image, bytes):
            data = image
        else:
            data = bytes(image)
        
        hash_alg = self._get_hash_algorithm()
        return hashlib.new(hash_alg, data).digest()

    def _get_hash_algorithm(self) -> str:
        """Get hash algorithm from security profile.

        Returns:
            Hash algorithm name.
        """
        if hasattr(self.security_profile, 'signing_features'):
            sig_format = self.security_profile.signing_features.get(
                'signature_format', 'ECDSA-P384'
            )
            if 'P256' in sig_format:
                return 'sha256'
            elif 'P384' in sig_format:
                return 'sha384'
            elif 'P521' in sig_format:
                return 'sha512'
        
        return 'sha384'

    def _sign_hash(self, image_hash: bytes) -> bytes:
        """Sign image hash with private key.

        Args:
            image_hash: Image hash bytes

        Returns:
            Signature bytes.
        """
        if not self._loaded_root_key:
            raise RuntimeError("Root key not loaded")

        algorithm = self.get_signature_algorithm()
        return sign_data(self._loaded_root_key, image_hash, algorithm)

    def _build_certificate_chain(self) -> List[bytes]:
        """Build certificate chain for signature.

        Returns:
            List of certificate bytes (leaf to root).
        """
        chain = []

        if self._loaded_ca_cert:
            chain.append(self._loaded_ca_cert)

        chain.extend(self._loaded_root_certs)

        return chain

    def verify_signature(self, signature: bytes) -> bool:
        """Verify signature using public key.

        Args:
            signature: Signature bytes to verify

        Returns:
            True if signature is valid.
        """
        image_hash = self._generate_image_hash(self.parsed_image)

        if not self._loaded_root_certs:
            return False

        pub_key = load_public_key(self._loaded_root_certs[0])
        pub_key_bytes = pub_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        return verify_signature(signature, pub_key_bytes, image_hash)

    def verify_certificate_chain(self, certificate_chain: List[bytes]) -> bool:
        """Verify certificate chain.

        Args:
            certificate_chain: List of certificate bytes

        Returns:
            True if certificate chain is valid.
        """
        return verify_certificate_chain(certificate_chain, self._loaded_root_certs)

    def get_signature_algorithm(self) -> str:
        """Get signature algorithm.

        Returns:
            Signature algorithm name.
        """
        if hasattr(self.security_profile, 'signing_features'):
            return self.security_profile.signing_features.get('algorithm', 'ECDSA')
        return 'ECDSA'

    def get_signature_information(self, signature: bytes) -> Dict[str, Any]:
        """Get signature information.

        Args:
            signature: Signature bytes

        Returns:
            Dictionary with signature information.
        """
        return get_signature_information(signature)

    def get_signature_format(self) -> str:
        """Get signature format.

        Returns:
            Signature format string.
        """
        return extract_signature_format(b'\x00' * 96)

    def validate_signature_format(self, signature_format: str) -> bool:
        """Validate signature format is supported.

        Args:
            signature_format: Signature format string

        Returns:
            True if format is supported.
        """
        supported_formats = get_supported_signature_formats()
        return signature_format in supported_formats


from cryptography.hazmat.primitives import serialization
