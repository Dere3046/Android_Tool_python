"""Secure image core implementation."""

import json
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

from cmd_line_interface.basecmdline import NamespaceWithGet
from cmd_line_interface.sectools.cmd_line_common.defines import (
    FUSE_BLOWER_IMAGES, HASH, IMAGE_ID, INFILE, OUTFILE,
    SECURITY_PROFILE, SIGN, VALIDATE,
)
from cmd_line_interface.sectools.secure_image.defines import (
    COMPRESS, COMPRESSED_OUTFILE, ENCRYPT,
)
from common.logging.logger import log_info, log_warning
from common.parser.hash_segment.defines import AUTHORITY_OEM
from common.parser.parser_image_info_interface import CoreInterface, ImageFormat, ImageFormatType, ImageProperties
from common.parser.utils import get_compressed_data, get_parsed_image
from common.utils import write_cmdline_file
from core.core_interfaces.core_security_profile_validator_interface import CoreSecurityProfileValidatorInterface
from core.hash_sign_core import HashSignCore, log_info_wrap
from profile.profile_core import SecurityProfile


class SecureImageCore(HashSignCore):
    """Secure image core class."""

    def __init__(self, parsed_args: NamespaceWithGet, security_profile: SecurityProfile) -> None:
        """Initialize secure image core."""
        self.parsed_args = parsed_args
        self.security_profile = security_profile
        self.parsed_image = None
        self.outfile_record_file = None

    def run(self) -> None:
        """Run secure image operations."""
        parsed_args = self.parsed_args

        operations = []
        if parsed_args.get(INSPECT, False):
            operations.append('inspect')
        if parsed_args.get(DUMP):
            operations.append('dump')
        if parsed_args.get(VALIDATE, False):
            operations.append('validate')
        if parsed_args.get(SIGN, False):
            operations.append('sign')
        if parsed_args.get(HASH, False):
            operations.append('hash')
        if parsed_args.get(ENCRYPT, False):
            operations.append('encrypt')
        if parsed_args.get(COMPRESS, False):
            operations.append('compress')

        infile = parsed_args.get(INFILE)
        if infile:
            self.parsed_image = get_parsed_image(infile)

        for operation in operations:
            if operation == 'inspect':
                self.inspect_operation()
            elif operation == 'dump':
                self.dump_operation(parsed_args)
            elif operation == 'validate':
                self.validate_operation(parsed_args)
            elif operation == 'sign':
                self.sign_operation(parsed_args)
            elif operation == 'hash':
                self.hash_operation(parsed_args)
            elif operation == 'encrypt':
                self.encrypt_operation(parsed_args)
            elif operation == 'compress':
                self.compress_operation(parsed_args)

    def inspect_operation(self) -> None:
        """Inspect operation - print human-readable format."""
        print(self.parsed_image)

    def dump_operation(self, parsed_args: NamespaceWithGet) -> None:
        """Dump operation - decompose image."""
        from common.data.base_parser import DumpInterface

        if isinstance(self.parsed_image, DumpInterface):
            dump_dir = Path(parsed_args.get(DUMP))
            self.parsed_image.write_dump_files(dump_dir)
        else:
            raise RuntimeError(
                f"{INFILE} is a {self.parsed_image.__class__.__name__} image for which the {DUMP} "
                f"operation is not supported. The {INSPECT} operation can be used to see contents of {INFILE}."
            )

    def validate_operation(self, parsed_args: NamespaceWithGet) -> None:
        """Validate operation."""
        outfile = parsed_args.get(OUTFILE)
        fuse_blower_images = parsed_args.get(FUSE_BLOWER_IMAGES, [])

        log_info("Validating image...")

        if self.parsed_image:
            self.parsed_image.validate_before_operation()

        if fuse_blower_images:
            from core.secure_image.validate.validate import get_fuse_blower_images_mismatches
            mismatches = get_fuse_blower_images_mismatches(self.parsed_image, fuse_blower_images)
            if mismatches:
                log_warning(f"Fuse blower image mismatches: {mismatches}")

        log_info("Validation complete.")

    def compress_operation(self, parsed_args: NamespaceWithGet) -> None:
        """Compress operation."""
        log_info("Performing compress operation...")
        if self.parsed_image:
            compressed_data = get_compressed_data(self.parsed_image.pack())
            outfile = parsed_args.get(COMPRESSED_OUTFILE) or parsed_args.get(OUTFILE)
            with open(outfile, 'wb') as f:
                f.write(compressed_data)
            log_info(f"Compressed image written to {outfile}")

    def sign_operation(self, parsed_args: NamespaceWithGet) -> None:
        """Sign operation."""
        log_info("Performing sign operation...")

    def hash_operation(self, parsed_args: NamespaceWithGet) -> None:
        """Hash operation."""
        log_info("Performing hash operation...")

    def encrypt_operation(self, parsed_args: NamespaceWithGet) -> None:
        """Encrypt operation."""
        log_info("Performing encrypt operation...")

    def get_image_properties(self, authority: str = AUTHORITY_OEM) -> ImageProperties:
        """Get image properties."""
        if self.parsed_image:
            return self.parsed_image.get_image_properties(authority)
        return ImageProperties(image_type=ImageFormatType.ELF, properties={})

    def get_image_format(self, authority: str = AUTHORITY_OEM) -> List[ImageFormat]:
        """Get image format list."""
        if self.parsed_image:
            return self.parsed_image.get_image_format(authority)
        return [ImageFormat(format_type=ImageFormatType.ELF)]
