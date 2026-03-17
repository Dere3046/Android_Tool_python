"""Base signer implementation based on decompiled analysis."""

from typing import Any, Dict, List, Optional, Tuple


class BaseSigner:
    """Base class for all signers.
    
    Based on decompiled analysis of sectools.exe signer classes.
    Provides common interface for LOCAL, TEST, and PLUGIN signing modes.
    """

    def __init__(
        self,
        parsed_image: Any,
        security_profile: Any,
        device_restrictions: Any,
        authority: str,
    ) -> None:
        """Initialize base signer.
        
        Args:
            parsed_image: Parsed image object
            security_profile: Security profile object
            device_restrictions: Device restrictions object
            authority: Authority type (OEM or QTI)
        """
        self.parsed_image = parsed_image
        self.security_profile = security_profile
        self.device_restrictions = device_restrictions
        self.authority = authority

    def sign(self, image: Any) -> Tuple[bytes, List[bytes]]:
        """Sign the image.
        
        Args:
            image: Image to sign
            
        Returns:
            Tuple of (signature, certificate_chain)
        """
        raise NotImplementedError("Subclasses must implement sign")

    def verify_signature(self, signature: bytes) -> bool:
        """Verify signature.
        
        Args:
            signature: Signature bytes to verify
            
        Returns:
            True if signature is valid
        """
        raise NotImplementedError("Subclasses must implement verify_signature")

    def verify_certificate_chain(self, certificate_chain: List[bytes]) -> bool:
        """Verify certificate chain.
        
        Args:
            certificate_chain: List of certificate bytes
            
        Returns:
            True if certificate chain is valid
        """
        raise NotImplementedError("Subclasses must implement verify_certificate_chain")

    def get_signature_algorithm(self) -> str:
        """Get signature algorithm.
        
        Returns:
            Signature algorithm name
        """
        raise NotImplementedError("Subclasses must implement get_signature_algorithm")

    def get_signature_information(self, signature: bytes) -> Dict[str, Any]:
        """Get signature information.
        
        Args:
            signature: Signature bytes
            
        Returns:
            Dictionary with signature information
        """
        raise NotImplementedError("Subclasses must implement get_signature_information")
