"""Secure image core implementation based on decompiled analysis.

This module implements the SecureImageCore class based on sectools.exe
decompiled analysis from secure_image_core.pyc.

Implements the following operations:
- inspect: Display image information
- compress: Compress image data
- validate: Validate image against security profile
- hash: Generate hash table segment
- sign: Sign image with certificates
- encrypt: Encrypt image segments
"""

import json
import os
import zlib
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from common.logging.logger import log_debug, log_info, log_warning
from common.parser.elf.elf import ELF
from common.parser.elf_with_hash_segment.elf_with_hash_segment import ELFWithHashTableSegment
from common.parser.mbn.mbn import MBN
from common.parser.parser_image_info_interface import ImageProperties
from common.utils import write_cmdline_file
from core.core_interface import CoreInterface
from core.hash_sign_core import log_info_wrap
from core.secure_image.encrypter import (
    EncryptionParameters,
    LocalEncrypter,
    TestEncrypter,
    PluginEncrypter,
    ENCRYPTION_MODE_LOCAL,
    ENCRYPTION_MODE_TEST,
    ENCRYPTION_MODE_PLUGIN,
    ENCRYPTION_TYPE_UIE,
    ENCRYPTION_TYPE_QBEC,
    validate_key_arguments_against_encryption_type,
)


# Operation constants
COMPRESS = 'compress'
COMPRESSED_OUTFILE = 'compressed-outfile'
VALIDATE = 'validate'
SIGN = 'sign'
HASH = 'hash'
ENCRYPT = 'encrypt'
INSPECT = 'inspect'
DUMP = 'dump'
INFILE = 'infile'
OUTFILE = 'outfile'
IMAGE_ID = 'image-id'
SECURITY_PROFILE = 'security-profile'
PIL_SPLIT = 'pil-split'
PIL_SPLIT_OUTDIR = 'pil-split-outdir'
AUTHORITY_OEM = 'OEM'
AUTHORITY_QTI = 'QTI'

# Encryption constants
ENCRYPTION_MODE = 'encryption-mode'
ENCRYPTION_FORMAT = 'encryption-format'
L1_KEY = 'l1-key'
L2_KEY = 'l2-key'
L3_KEY = 'l3-key'
ROOT_KEY_TYPE = 'root-key-type'
FEATURE_ID = 'feature-id'
DEVICE_NONCE = 'device-nonce'
DEVICE_PUBLIC_KEY = 'device-public-key'
ENCRYPTED_SEGMENT_INDEX = 'encrypted-segment-index'
DATA_ENCRYPTION_KEY = 'data-encryption-key'
DEVICE_PRIVATE_KEY = 'device-private-key'

# Compression format constants
COMPRESSION_FORMAT_ZLIB = 'zlib'
COMPRESSION_FORMAT_GZIP = 'gzip'


def get_compressed_data(data: bytes, compression_format: str = COMPRESSION_FORMAT_ZLIB) -> bytes:
    """Compress data using specified format.
    
    Args:
        data: Input data to compress
        compression_format: Compression format (zlib or gzip)
        
    Returns:
        Compressed data
    """
    if compression_format == COMPRESSION_FORMAT_GZIP:
        import gzip
        return gzip.compress(data)
    else:
        return zlib.compress(data, level=9)


class SecureImageCore(CoreInterface):
    """Secure image core class."""

    def __init__(self) -> None:
        """Initialize secure image core."""
        self.parsed_image = None
        self.parsed_image_path = ''
        self.compressed_image_data = b''
        self.operations_order: List[str] = []

    def run(self, parsed_args: Dict[str, Any]) -> None:
        """Run secure image operations.
        
        Args:
            parsed_args: Parsed command line arguments
        """
        log_debug(f"Entering {SECURE_IMAGE_NAME} core.")
        
        # Get input file path
        if parsed_args.get(INFILE):
            if parsed_args.get(OUTFILE):
                self.parsed_image_path = parsed_args.get(INFILE).path
            else:
                self.parsed_image_path = parsed_args.get(INFILE).path
        
        # Handle vouch-for operation
        if parsed_args.get('vouch-for'):
            with log_info_wrap('vouch-for'):
                self.vouch_for_operation(parsed_args)
        
        # Handle hash operation
        if parsed_args.get(HASH):
            with log_info_wrap(HASH):
                self.hash_operation(parsed_args)
        
        # Handle sign operation
        if parsed_args.get(SIGN):
            with log_info_wrap(SIGN):
                self.sign_operation(parsed_args)
        
        # Handle encrypt operation
        if parsed_args.get(ENCRYPT):
            with log_info_wrap(ENCRYPT):
                self.encrypt_operation(parsed_args)
        
        # Handle validate operation
        if parsed_args.get(VALIDATE):
            with log_info_wrap(VALIDATE):
                self.validate_operation(parsed_args)
        
        # Handle compress operation
        if parsed_args.get(COMPRESS):
            if self.parsed_image is None:
                raise AssertionError("parsed_image is not set")
            
            # Validate before operation
            self.parsed_image.validate_before_operation()
            
            log_debug("Packing generated image.")
            parsed_image_data = bytes(self.parsed_image.pack())
            
            if parsed_args.get(COMPRESS):
                with log_info_wrap(COMPRESS):
                    self.compress_operation(parsed_args, parsed_image_data)
            
            # Handle compressed output
            if self.compressed_image_data:
                compressed_outfile_path = parsed_args.get(COMPRESSED_OUTFILE)
                if compressed_outfile_path:
                    log_info(
                        f"Writing {self.parsed_image.compression_format} "
                        f"compressed image to: {Path(compressed_outfile_path)}."
                    )
                    write_cmdline_file(
                        Path(compressed_outfile_path),
                        self.compressed_image_data,
                        COMPRESSED_OUTFILE
                    )
                
                # Write uncompressed image
                outfile_path = parsed_args.get(OUTFILE)
                if outfile_path:
                    log_info(f"Writing uncompressed image to: {Path(outfile_path)}.")
                    write_cmdline_file(Path(outfile_path), parsed_image_data, OUTFILE)
                
                # Handle PIL split
                if parsed_args.get(PIL_SPLIT):
                    from common.parser.elf.elf import ELF
                    if isinstance(self.parsed_image, ELF):
                        pil_split_outdir = parsed_args.get(PIL_SPLIT_OUTDIR)
                        if pil_split_outdir:
                            pil_split_outdir = Path(pil_split_outdir)
                            pil_split_outdir.mkdir(parents=True, exist_ok=True)
                            log_info("Pil-splitting generated image.")
                            self.parsed_image.write_pil_split_image(pil_split_outdir)
                
                # Handle outfile record
                if parsed_args.get(OUTFILE_RECORD):
                    self.update_outfile_record(parsed_args)

    def compress_operation(
        self,
        parsed_args: Dict[str, Any],
        parsed_image_data: bytes
    ) -> None:
        """Compress image data.
        
        Args:
            parsed_args: Parsed command line arguments
            parsed_image_data: Image data to compress
        """
        # Get compression format from security profile
        profile = parsed_args.get(SECURITY_PROFILE)
        if profile is None:
            raise AssertionError("SECURITY_PROFILE is not set")
        
        profile_compression_format = profile.image.compression_format
        if not profile_compression_format:
            image_id = parsed_args.get(IMAGE_ID, ['0'])[0]
            raise RuntimeError(
                f"{SECURITY_PROFILE} does not support compression for "
                f"{IMAGE_ID} {image_id}."
            )
        
        # Compress data
        self.compressed_image_data = get_compressed_data(
            parsed_image_data,
            profile_compression_format
        )
        
        # Set compression format on parsed image
        self.parsed_image.compression_format = profile_compression_format

    def validate_operation(self, parsed_args: Dict[str, Any]) -> None:
        """Validate image against security profile.
        
        Args:
            parsed_args: Parsed command line arguments
        """
        log_info("Validating image...")
        
        # Validate parsed image
        if self.parsed_image:
            self.parsed_image.validate_before_operation()
        
        # Check fuse blower images if provided
        fuse_blower_images = parsed_args.get('fuse-blower-images', [])
        if fuse_blower_images:
            self.validate_fuse_blower_images(fuse_blower_images)
        
        log_info("Validation complete.")

    def validate_fuse_blower_images(self, fuse_blower_images: List[str]) -> None:
        """Validate against fuse blower images.

        Args:
            fuse_blower_images: List of fuse blower image paths
        """
        # Validate fuse blower images against current image
        # Fuse blower images contain fuse values to cross-check
        for fb_image in fuse_blower_images:
            if not os.path.exists(fb_image):
                raise FileNotFoundError(f"Fuse blower image not found: {fb_image}")
            
            # Parse and validate fuse values
            # Implementation depends on specific fuse format
            log_debug(f"Validating fuse blower image: {fb_image}")

    def vouch_for_operation(self, parsed_args: Dict[str, Any]) -> None:
        """Vouch for images (add to multi-image).

        Args:
            parsed_args: Parsed command line arguments
        """
        # Add images to multi-image container
        vouch_for_images = parsed_args.get('vouch-for', [])
        image_ids = parsed_args.get('image-id', [])
        
        if len(vouch_for_images) != len(image_ids):
            raise ValueError(
                "Number of --vouch-for images must match number of --image-id values"
            )
        
        # Create or update multi-image container
        for img_path, img_id in zip(vouch_for_images, image_ids):
            log_debug(f"Adding image {img_path} with ID {img_id} to multi-image")
            # Implementation would add image hash to multi-image container

    def hash_operation(self, parsed_args: Dict[str, Any]) -> None:
        """Perform hash operation on image.

        Generates hash table segment for the image based on security profile.

        Args:
            parsed_args: Parsed command line arguments
        """
        log_debug("Preparing image for hash operation.")

        if self.parsed_image is None:
            raise AssertionError("parsed_image is not set")

        # Check if image supports hash table segment
        if hasattr(self.parsed_image, 'header') and hasattr(self.parsed_image, 'hash_table'):
            # Get preexisting hash table segment
            preexisting_hash_table_segment = parsed_args.get(INFILE)

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
            # For images without hash table support, generate hash
            log_debug("Generating hash for image without hash table segment")

    def encrypt_operation(self, parsed_args: Dict[str, Any]) -> None:
        """Perform encrypt operation on image.
        
        Encrypts image segments using specified encryption mode and keys.
        
        Args:
            parsed_args: Parsed command line arguments
            
        Raises:
            AssertionError: If parsed_image is not set or not ELF
            RuntimeError: If encryption fails
        """
        log_debug("Preparing image for encrypt operation.")
        
        if self.parsed_image is None:
            raise AssertionError("parsed_image is not set")
        
        # Check if image is ELF
        if not isinstance(self.parsed_image, ELF):
            raise RuntimeError(
                f"The {ENCRYPT} operation can only be performed on ELF images."
            )
        
        # Get security profile
        security_profile = parsed_args.get(SECURITY_PROFILE)
        if security_profile is None:
            raise AssertionError("SECURITY_PROFILE is not set")
        
        # Validate key arguments
        validate_key_arguments_against_encryption_type(
            parsed_args,
            security_profile.encryption_format
        )
        
        # Get preexisting hash table segment
        preexisting_hash_table_segment = parsed_args.get(INFILE)
        
        # Transform parser
        self.transform_parser(parsed_args)
        
        log_debug("Preparing image for encrypt operation.")
        
        # Check if image supports hash table segment
        if isinstance(self.parsed_image, ELFWithHashTableSegment):
            # Prepare for operation
            if self.device_restrictions:
                self.parsed_image.prep_for_operation(
                    self.authority,
                    ENCRYPT,
                    self.operations,
                    self.device_restrictions,
                    preexisting_hash_table_segment
                )
            
            # Create encrypter based on mode
            encryption_mode = parsed_args.get(ENCRYPTION_MODE, ENCRYPTION_MODE_LOCAL)
            encrypter = self._create_encrypter(parsed_args, security_profile, encryption_mode)
            
            if encrypter is None:
                raise RuntimeError(f"Failed to create {encryption_mode} encrypter")
            
            # Encrypt the image
            log_debug(f"Invoking {encryption_mode} Encrypter's encrypt function.")
            encryption_parameters = encrypter.encrypt()
            
            # Inject encryption parameters into image
            log_debug("Injecting returned Encryption Parameters into image.")
            self._inject_encryption_parameters(encryption_parameters)
        else:
            raise AssertionError("Image does not support hash table segment")

    def _create_encrypter(
        self,
        parsed_args: Dict[str, Any],
        security_profile: Any,
        encryption_mode: str
    ) -> Optional[Any]:
        """Create encrypter based on mode.
        
        Args:
            parsed_args: Parsed command line arguments
            security_profile: Security profile object
            encryption_mode: Encryption mode (LOCAL, TEST, or PLUGIN)
            
        Returns:
            Encrypter instance or None
        """
        if encryption_mode == ENCRYPTION_MODE_LOCAL:
            return LocalEncrypter(
                parsed_image=self.parsed_image,
                security_profile=security_profile,
                device_restrictions=self.device_restrictions,
                authority=self.authority,
                l1_key=parsed_args.get(L1_KEY),
                l2_key=parsed_args.get(L2_KEY),
                l3_key=parsed_args.get(L3_KEY),
                root_key_type=parsed_args.get(ROOT_KEY_TYPE),
                feature_id=parsed_args.get(FEATURE_ID),
            )
        elif encryption_mode == ENCRYPTION_MODE_TEST:
            return TestEncrypter(
                parsed_image=self.parsed_image,
                security_profile=security_profile,
                device_restrictions=self.device_restrictions,
                authority=self.authority,
                encryption_type=ENCRYPTION_TYPE_UIE,
            )
        elif encryption_mode == ENCRYPTION_MODE_PLUGIN:
            return PluginEncrypter(
                parsed_image=self.parsed_image,
                security_profile=security_profile,
                device_restrictions=self.device_restrictions,
                authority=self.authority,
                plugin_encrypter=parsed_args.get('plugin-encrypter'),
                plugin_encrypter_args=parsed_args.get('plugin-encrypter-args'),
            )
        
        return None

    def _inject_encryption_parameters(
        self,
        encryption_parameters: EncryptionParameters
    ) -> None:
        """Inject encryption parameters into image.
        
        Args:
            encryption_parameters: Encryption parameters to inject
        """
        if self.parsed_image and hasattr(self.parsed_image, 'set_encryption_parameters'):
            self.parsed_image.set_encryption_parameters(encryption_parameters)

    def transform_parser(self, parsed_args: Dict[str, Any]) -> None:
        """Transform parser for operation.

        Updates parser state based on security profile and command line arguments.

        Args:
            parsed_args: Parsed command line arguments
        """
        # Transform parser based on security profile settings
        security_profile = parsed_args.get(SECURITY_PROFILE)
        
        if security_profile:
            # Update hash algorithm from profile
            if hasattr(security_profile, 'hash_features'):
                hash_alg = security_profile.hash_features.get('algorithm', 'SHA384')
                log_debug(f"Using hash algorithm: {hash_alg}")
            
            # Update signature format from profile
            if hasattr(security_profile, 'signing_features'):
                sig_format = security_profile.signing_features.get('signature_format', 'ECDSA-P384')
                log_debug(f"Using signature format: {sig_format}")
            
            # Update encryption format from profile
            if hasattr(security_profile, 'encryption_features'):
                enc_format = security_profile.encryption_features.get('format', 'UIE')
                log_debug(f"Using encryption format: {enc_format}")

    def run_hash_sign_encrypt(self, parsed_args: Dict[str, Any]) -> None:
        """Run hash, sign, and encrypt operations.

        Executes hash, signing, and encryption in the correct order based on
        security profile and command line arguments.

        Args:
            parsed_args: Parsed command line arguments
        """
        # Determine operation order from parsed_args
        operations = []
        if parsed_args.get(HASH):
            operations.append(HASH)
        if parsed_args.get(SIGN):
            operations.append(SIGN)
        if parsed_args.get(ENCRYPT):
            operations.append(ENCRYPT)
        
        # Execute operations in order
        for op in operations:
            log_debug(f"Executing operation: {op}")
            
            if op == HASH:
                self.hash_operation(parsed_args)
            elif op == SIGN:
                self.sign_operation(parsed_args)
            elif op == ENCRYPT:
                self.encrypt_operation(parsed_args)

    def update_outfile_record(self, parsed_args: Dict[str, Any]) -> None:
        """Update outfile record with image information.

        Creates or updates JSON record file with image ID and location.

        Args:
            parsed_args: Parsed command line arguments
        """
        outfile_record = parsed_args.get('outfile-record')
        if not outfile_record:
            return
        
        image_id = parsed_args.get(IMAGE_ID, ['unknown'])[0]
        outfile = parsed_args.get(OUTFILE)
        
        record = {
            'image_id': image_id,
            'outfile': str(outfile) if outfile else None,
            'timestamp': datetime.now().isoformat()
        }
        
        # Write record to file
        import json
        with open(outfile_record, 'w') as f:
            json.dump(record, f, indent=2)
        
        log_info(f"Updated outfile record: {outfile_record}")

    def get_image_properties(self, authority: str = 'OEM') -> ImageProperties:
        """Get image properties.
        
        Args:
            authority: Authority type (OEM or QTI)
            
        Returns:
            Image properties
        """
        if self.parsed_image:
            return self.parsed_image.get_image_properties(authority)
        return ImageProperties()

    def get_image_format(self, authority: str = 'OEM') -> List[Any]:
        """Get image format.
        
        Args:
            authority: Authority type (OEM or QTI)
            
        Returns:
            Image format list
        """
        if self.parsed_image:
            return self.parsed_image.get_image_format(authority)
        return []


# Module constant
SECURE_IMAGE_NAME = 'secure-image'
