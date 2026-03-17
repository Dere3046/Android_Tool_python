"""Test signer implementation based on decompiled analysis."""

from typing import Any, Dict, List, Optional, Tuple

from .base_signer import BaseSigner
from common.crypto.openssl import (
    verify_signature,
    verify_certificate_chain,
    get_signature_information,
    get_default_certificate_chain_depth,
    get_default_root_certificate_count,
    generate_key_pair,
    sign_data,
    load_public_key,
)
from cryptography.hazmat.primitives import serialization


class TestSigner(BaseSigner):
    """Test signer using test certificates."""

    def __init__(
        self,
        parsed_image: Any,
        security_profile: Any,
        device_restrictions: Any,
        authority: str,
        outfile: str,
        certificate_chain_depth: Optional[int] = None,
        root_certificate_count: Optional[int] = None,
        root_certificate_index: Optional[int] = None,
        subject: Optional[str] = None,
        signature_format: Optional[str] = None,
    ) -> None:
        """Initialize test signer.

        Args:
            parsed_image: Parsed image object
            security_profile: Security profile object
            device_restrictions: Device restrictions object
            authority: Authority type (OEM or QTI)
            outfile: Output file path
            certificate_chain_depth: Certificate chain depth
            root_certificate_count: Number of root certificates
            root_certificate_index: Root certificate index
            subject: Attestation certificate subject
            signature_format: Signature format
        """
        super().__init__(
            parsed_image,
            security_profile,
            device_restrictions,
            authority,
        )

        self.outfile = outfile
        self.certificate_chain_depth = (
            certificate_chain_depth or get_default_certificate_chain_depth()
        )
        self.root_certificate_count = (
            root_certificate_count or get_default_root_certificate_count()
        )
        self.root_certificate_index = root_certificate_index
        self.subject = subject
        self.signature_format = signature_format or 'ECDSA-P384'

        self._test_certificates: List[bytes] = []
        self._test_key = None
        self._test_public_key_bytes: Optional[bytes] = None

    def _load_test_certificates(self) -> None:
        """Load test certificates."""
        if self._test_key is not None:
            return

        curve = 'P-384'
        if self.signature_format and 'P256' in self.signature_format:
            curve = 'P-256'

        self._test_key, pub_key = generate_key_pair(curve)
        
        self._test_public_key_bytes = pub_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def sign(self, image: Any) -> Tuple[bytes, List[bytes]]:
        """Sign the image using test certificates.

        Args:
            image: Image to sign

        Returns:
            Tuple of (signature, certificate_chain).
        """
        self._load_test_certificates()

        image_hash = self._generate_image_hash(image)
        signature = self._sign_hash(image_hash)
        certificate_chain = self._build_test_certificate_chain()

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

        if self.signature_format and 'P256' in self.signature_format:
            return hashlib.sha256(data).digest()
        return hashlib.sha384(data).digest()

    def _sign_hash(self, image_hash: bytes) -> bytes:
        """Sign image hash with test key.

        Args:
            image_hash: Image hash bytes

        Returns:
            Signature bytes.
        """
        return sign_data(self._test_key, image_hash, 'ECDSA')

    def _build_test_certificate_chain(self) -> List[bytes]:
        """Build test certificate chain.

        Returns:
            List of test certificate bytes.
        """
        return self._test_certificates

    def verify_signature(self, signature: bytes) -> bool:
        """Verify test signature.

        Args:
            signature: Signature bytes to verify

        Returns:
            True if signature is valid.
        """
        self._load_test_certificates()
        
        image_hash = self._generate_image_hash(self.parsed_image)

        return verify_signature(
            signature,
            self._test_public_key_bytes,
            image_hash,
            'ECDSA'
        )

    def verify_certificate_chain(self, certificate_chain: List[bytes]) -> bool:
        """Verify test certificate chain.

        Args:
            certificate_chain: List of certificate bytes

        Returns:
            True if certificate chain is valid.
        """
        return verify_certificate_chain(certificate_chain, self._test_certificates)

    def get_signature_algorithm(self) -> str:
        """Get signature algorithm.

        Returns:
            Signature algorithm name.
        """
        return 'ECDSA'

    def get_signature_information(self, signature: bytes) -> Dict[str, Any]:
        """Get signature information.

        Args:
            signature: Signature bytes

        Returns:
            Dictionary with signature information.
        """
        info = get_signature_information(signature)
        info['format'] = self.signature_format
        info['test_mode'] = True
        return info

    def get_certificate_chain_depth(self) -> int:
        """Get certificate chain depth.

        Returns:
            Chain depth.
        """
        return self.certificate_chain_depth

    def get_root_certificate_count(self) -> int:
        """Get root certificate count.

        Returns:
            Root certificate count.
        """
        return self.root_certificate_count
