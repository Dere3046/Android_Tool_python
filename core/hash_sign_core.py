"""Hash and sign core implementation based on decompiled analysis.

This module implements the HashSignCore class based on sectools.exe
decompiled analysis from hash_sign_core.pyc.
"""

from typing import Any, Dict, List, Optional

from common.logging.logger import log_debug, log_info, log_warning
from common.parser.hash_segment.hash_segment_common import HashTableSegmentCommon
from common.parser.parser_image_info_interface import ImageProperties
from core.core_interface import CoreInterface
from core.hash_sign_core import log_info_wrap


# Operation constants
HASH = 'hash'
SIGN = 'sign'
ENCRYPT = 'encrypt'
INFILE = 'infile'
OUTFILE = 'outfile'
SECURITY_PROFILE = 'security-profile'
SIGNING_MODE = 'signing-mode'
LOCAL = 'LOCAL'
TEST = 'TEST'
PLUGIN = 'PLUGIN'
ROOT_CERTIFICATE = 'root-certificate'
ROOT_KEY = 'root-key'
CA_CERTIFICATE = 'ca-certificate'
CA_KEY = 'ca-key'
ATTEST_CERTIFICATE_SUBJECT = 'attest-certificate-subject'
CERTIFICATE_CHAIN_DEPTH = 'certificate-chain-depth'
ROOT_CERTIFICATE_COUNT = 'root-certificate-count'
ROOT_CERTIFICATE_INDEX = 'root-certificate-index'
SIGNATURE_FORMAT = 'signature-format'
PLUGIN_SIGNER = 'plugin-signer'
PLUGIN_SIGNER_ARGS = 'plugin-signer-args'
AUTHORITY_OEM = 'OEM'
AUTHORITY_QTI = 'QTI'
MAX_RETRY_SIGN_ATTEMPTS = 3


class HashSignCore(CoreInterface):
    """Hash and sign core class.
    
    Based on decompiled analysis of hash_sign_core.pyc from sectools.exe.
    Implements hash and sign operations for ELF/MBN images.
    """

    def __init__(self) -> None:
        """Initialize hash and sign core."""
        self.parsed_image = None
        self.authority = AUTHORITY_OEM
        self.operations: List[str] = []
        self.device_restrictions = None

    def run(self, parsed_args: Dict[str, Any]) -> None:
        """Run hash and sign operations.
        
        Args:
            parsed_args: Parsed command line arguments
        """
        log_debug("Entering hash_sign core.")
        
        # Handle hash operation
        if parsed_args.get(HASH):
            with log_info_wrap(HASH):
                self.hash_operation(parsed_args)
        
        # Handle sign operation
        if parsed_args.get(SIGN):
            with log_info_wrap(SIGN):
                self.sign_operation(parsed_args)

    def hash_operation(self, parsed_args: Dict[str, Any]) -> None:
        """Perform hash operation on image.
        
        Prepares the image for hash table generation based on security profile
        and device restrictions.
        
        Args:
            parsed_args: Parsed command line arguments
        """
        log_debug("Preparing image for hash operation.")
        
        if self.parsed_image is None:
            raise AssertionError("parsed_image is not set")
        
        # Check if image supports hash table segment
        if isinstance(self.parsed_image, HashTableSegmentCommon):
            # Get preexisting hash table segment
            preexisting_hash_table_segment = parsed_args.get(INFILE)
            
            # Transform parser for operation
            self.transform_parser(parsed_args)
            
            # Prepare for operation
            if self.device_restrictions:
                self.parsed_image.prep_for_operation(
                    self.authority,
                    HASH,
                    self.operations,
                    self.device_restrictions,
                    preexisting_hash_table_segment
                )
        else:
            raise AssertionError("Image does not support hash table segment")

    def sign_operation(self, parsed_args: Dict[str, Any]) -> None:
        """Perform sign operation on image.
        
        Signs the image using the specified signing mode (LOCAL, TEST, or PLUGIN)
        with provided certificates and keys.
        
        Args:
            parsed_args: Parsed command line arguments
            
        Raises:
            AssertionError: If parsed_image is not set or security profile missing
            RuntimeError: If signing fails
        """
        log_debug("Preparing image for sign operation.")
        
        if self.parsed_image is None:
            raise AssertionError("parsed_image is not set")
        
        # Check if image supports hash table segment
        if isinstance(self.parsed_image, HashTableSegmentCommon):
            # Get preexisting hash table segment
            preexisting_hash_table_segment = parsed_args.get(INFILE)
            
            # Check if hash operation was performed first
            if HASH not in self.operations:
                self.transform_parser(parsed_args)
            
            # Get security profile
            security_profile = parsed_args.get(SECURITY_PROFILE)
            if security_profile is None:
                raise AssertionError("SECURITY_PROFILE is not set")
            
            # Prepare for operation
            if self.device_restrictions:
                self.parsed_image.prep_for_operation(
                    self.authority,
                    SIGN,
                    self.operations,
                    self.device_restrictions,
                    preexisting_hash_table_segment
                )
            
            # Perform signing
            self._perform_signing(parsed_args, security_profile)
        else:
            raise AssertionError("Image does not support hash table segment")

    def _perform_signing(
        self,
        parsed_args: Dict[str, Any],
        security_profile: Any
    ) -> None:
        """Perform actual signing operation.
        
        Creates appropriate signer based on signing mode and signs the image.
        Supports LOCAL, TEST, and PLUGIN signing modes.
        
        Args:
            parsed_args: Parsed command line arguments
            security_profile: Security profile object
            
        Raises:
            RuntimeError: If signing fails or signature verification fails
        """
        # Get signing mode
        signing_mode = parsed_args.get(SIGNING_MODE, LOCAL)
        
        log_debug(f"Constructing {signing_mode} Signer.")
        
        # Create signer based on mode
        signer = None
        
        if signing_mode == LOCAL:
            # Local signing using provided certificates
            signer = self._create_local_signer(parsed_args, security_profile)
        elif signing_mode == TEST:
            # Test signing with test certificates
            signer = self._create_test_signer(parsed_args, security_profile)
        elif signing_mode == PLUGIN:
            # Plugin signing
            signer = self._create_plugin_signer(parsed_args, security_profile)
        
        if signer is None:
            raise RuntimeError(f"Failed to create {signing_mode} signer")
        
        # Sign the image
        log_debug(f"Invoking {signing_mode} Signer's sign function.")
        
        # Get signature and certificate chain
        signature, certificate_chain = signer.sign(self.parsed_image)
        
        # Validate signature
        self._validate_signature(
            signature,
            certificate_chain,
            signer,
            parsed_args
        )
        
        # Inject into image
        log_debug("Injecting returned signature and certificate chain into image.")
        self._inject_signature(signature, certificate_chain)

    def _create_local_signer(
        self,
        parsed_args: Dict[str, Any],
        security_profile: Any
    ) -> Any:
        """Create local signer.
        
        Args:
            parsed_args: Parsed command line arguments
            security_profile: Security profile object
            
        Returns:
            LocalSigner instance
        """
        # Import here to avoid circular dependency
        from core.secure_image.signer.local.local_signer import LocalSigner
        
        return LocalSigner(
            parsed_image=self.parsed_image,
            security_profile=security_profile,
            device_restrictions=self.device_restrictions,
            authority=self.authority,
            outfile=parsed_args.get(OUTFILE),
            root_certificates=parsed_args.get(ROOT_CERTIFICATE),
            root_key=parsed_args.get(ROOT_KEY),
            ca_certificate=parsed_args.get(CA_CERTIFICATE),
            ca_key=parsed_args.get(CA_KEY),
            subject=parsed_args.get(ATTEST_CERTIFICATE_SUBJECT),
        )

    def _create_test_signer(
        self,
        parsed_args: Dict[str, Any],
        security_profile: Any
    ) -> Any:
        """Create test signer.
        
        Args:
            parsed_args: Parsed command line arguments
            security_profile: Security profile object
            
        Returns:
            TestSigner instance
        """
        from core.secure_image.signer.test.test_signer import TestSigner
        
        return TestSigner(
            parsed_image=self.parsed_image,
            security_profile=security_profile,
            device_restrictions=self.device_restrictions,
            authority=self.authority,
            certificate_chain_depth=parsed_args.get(CERTIFICATE_CHAIN_DEPTH),
            root_certificate_count=parsed_args.get(ROOT_CERTIFICATE_COUNT),
            root_certificate_index=parsed_args.get(ROOT_CERTIFICATE_INDEX),
            subject=parsed_args.get(ATTEST_CERTIFICATE_SUBJECT),
            signature_format=parsed_args.get(SIGNATURE_FORMAT),
        )

    def _create_plugin_signer(
        self,
        parsed_args: Dict[str, Any],
        security_profile: Any
    ) -> Any:
        """Create plugin signer.
        
        Args:
            parsed_args: Parsed command line arguments
            security_profile: Security profile object
            
        Returns:
            PluginSigner instance
        """
        from core.secure_image.signer.plugin.plugin_signer import PluginSigner
        
        return PluginSigner(
            parsed_image=self.parsed_image,
            security_profile=security_profile,
            device_restrictions=self.device_restrictions,
            authority=self.authority,
            plugin_signer=parsed_args.get(PLUGIN_SIGNER),
            plugin_signer_args=parsed_args.get(PLUGIN_SIGNER_ARGS),
            subject=parsed_args.get(ATTEST_CERTIFICATE_SUBJECT),
        )

    def _validate_signature(
        self,
        signature: bytes,
        certificate_chain: List[bytes],
        signer: Any,
        parsed_args: Dict[str, Any]
    ) -> None:
        """Validate signature and certificate chain.
        
        Args:
            signature: Signature bytes
            certificate_chain: List of certificate bytes
            signer: Signer instance
            parsed_args: Parsed command line arguments
            
        Raises:
            RuntimeError: If validation fails
        """
        # Verify signature
        if not signer.verify_signature(signature):
            raise RuntimeError(f"{signer.__class__.__name__} signature failed verification.")
        
        # Verify certificate chain
        if not signer.verify_certificate_chain(certificate_chain):
            raise RuntimeError(f"{signer.__class__.__name__} certificate chain failed verification.")

    def _inject_signature(
        self,
        signature: bytes,
        certificate_chain: List[bytes]
    ) -> None:
        """Inject signature and certificate chain into image.
        
        Args:
            signature: Signature bytes
            certificate_chain: List of certificate bytes
        """
        if self.parsed_image and hasattr(self.parsed_image, 'set_signature'):
            self.parsed_image.set_signature(signature, certificate_chain)

    def transform_parser(self, parsed_args: Dict[str, Any]) -> None:
        """Transform parser for operation.
        
        Prepares the parser for hash or sign operation by setting up
        necessary data structures and validating the image.
        
        Args:
            parsed_args: Parsed command line arguments
        """
        # Transform parser based on parsed image type
        # Update image format and properties based on authority
        if self.parsed_image:
            # Validate image before operation
            self.parsed_image.validate_before_operation()
            
            # Update image properties
            image_props = self.parsed_image.get_image_properties(self.authority)
            
            # Log transformation
            log_debug(f"Parser transformed for {self.authority} authority")

    def get_image_properties(self, authority: str = AUTHORITY_OEM) -> ImageProperties:
        """Get image properties.
        
        Args:
            authority: Authority type (OEM or QTI)
            
        Returns:
            Image properties
        """
        if self.parsed_image:
            return self.parsed_image.get_image_properties(authority)
        return ImageProperties()

    def get_image_format(self, authority: str = AUTHORITY_OEM) -> List[Any]:
        """Get image format.
        
        Args:
            authority: Authority type (OEM or QTI)
            
        Returns:
            Image format list
        """
        if self.parsed_image:
            return self.parsed_image.get_image_format(authority)
        return []
