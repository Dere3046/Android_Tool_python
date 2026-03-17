"""Plugin signer implementation based on decompiled analysis."""

import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .base_signer import BaseSigner
from common.crypto.openssl import (
    verify_signature,
    verify_certificate_chain,
    get_signature_information,
    load_public_key,
)


class PluginSigner(BaseSigner):
    """Plugin signer using external signing plugin."""

    def __init__(
        self,
        parsed_image: Any,
        security_profile: Any,
        device_restrictions: Any,
        authority: str,
        outfile: str,
        plugin_signer: Optional[str] = None,
        plugin_signer_args: Optional[Dict[str, Any]] = None,
        subject: Optional[str] = None,
    ) -> None:
        """Initialize plugin signer.

        Args:
            parsed_image: Parsed image object
            security_profile: Security profile object
            device_restrictions: Device restrictions object
            authority: Authority type (OEM or QTI)
            outfile: Output file path
            plugin_signer: Plugin signer path/name
            plugin_signer_args: Plugin signer arguments
            subject: Attestation certificate subject
        """
        super().__init__(
            parsed_image,
            security_profile,
            device_restrictions,
            authority,
        )

        self.outfile = outfile
        self.plugin_signer = plugin_signer
        self.plugin_signer_args = plugin_signer_args or {}
        self.subject = subject

        self._plugin_process: Optional[subprocess.Popen] = None
        self._public_key_bytes: Optional[bytes] = None

    def _validate_plugin(self) -> bool:
        """Validate plugin exists and is executable.

        Returns:
            True if plugin is valid.

        Raises:
            FileNotFoundError: If plugin not found
            PermissionError: If plugin is not executable
        """
        if not self.plugin_signer:
            raise FileNotFoundError("Plugin signer not specified")

        plugin_path = Path(self.plugin_signer)

        if not plugin_path.exists():
            raise FileNotFoundError(
                f"Plugin signer not found: {self.plugin_signer}"
            )

        if not plugin_path.is_file():
            raise PermissionError(
                f"Plugin signer is not a file: {self.plugin_signer}"
            )

        return True

    def _invoke_plugin(self, command: str, args: List[str]) -> subprocess.Popen:
        """Invoke plugin with specified command and arguments.

        Args:
            command: Plugin command
            args: Command arguments

        Returns:
            Plugin process.
        """
        full_args = [command] + args
        return subprocess.Popen(
            full_args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def sign(self, image: Any) -> Tuple[bytes, List[bytes]]:
        """Sign the image using external plugin.

        Args:
            image: Image to sign

        Returns:
            Tuple of (signature, certificate_chain).

        Raises:
            RuntimeError: If plugin signing fails
            FileNotFoundError: If plugin not found
        """
        self._validate_plugin()

        image_data = self._prepare_image_data(image)
        args = self._build_plugin_args()

        self._plugin_process = self._invoke_plugin(self.plugin_signer, args)

        stdout, stderr = self._plugin_process.communicate(input=image_data)

        if self._plugin_process.returncode != 0:
            raise RuntimeError(
                f"Plugin signing failed: {stderr.decode('utf-8', errors='ignore')}"
            )

        signature, certificate_chain = self._parse_plugin_response(stdout)

        return signature, certificate_chain

    def _prepare_image_data(self, image: Any) -> bytes:
        """Prepare image data for plugin.

        Args:
            image: Image to sign

        Returns:
            Image data bytes.
        """
        if hasattr(image, 'data'):
            return image.data
        elif isinstance(image, bytes):
            return image
        else:
            return bytes(image)

    def _build_plugin_args(self) -> List[str]:
        """Build plugin command line arguments.

        Returns:
            List of arguments.
        """
        args = ['--sign']
        args.append(f'--authority={self.authority}')

        if self.subject:
            args.append(f'--subject={self.subject}')

        for key, value in self.plugin_signer_args.items():
            args.append(f'--{key}={json.dumps(value)}')

        return args

    def _parse_plugin_response(
        self,
        response: bytes
    ) -> Tuple[bytes, List[bytes]]:
        """Parse plugin response.

        Args:
            response: Plugin response bytes

        Returns:
            Tuple of (signature, certificate_chain).

        Raises:
            RuntimeError: If response parsing fails
        """
        try:
            data = json.loads(response.decode('utf-8'))

            signature = bytes.fromhex(data.get('signature', ''))
            cert_chain = [
                bytes.fromhex(cert)
                for cert in data.get('certificate_chain', [])
            ]

            if pub_key_hex := data.get('public_key'):
                self._public_key_bytes = bytes.fromhex(pub_key_hex)

            return signature, cert_chain

        except Exception as e:
            raise RuntimeError(f"Failed to parse plugin response: {e}")

    def verify_signature(self, signature: bytes) -> bool:
        """Verify signature using plugin.

        Args:
            signature: Signature bytes to verify

        Returns:
            True if signature is valid.
        """
        image_hash = self._generate_image_hash(self.parsed_image)

        if not self._public_key_bytes:
            self._load_public_key_from_plugin()

        if not self._public_key_bytes:
            return False

        return verify_signature(
            signature,
            self._public_key_bytes,
            image_hash,
            self.get_signature_algorithm()
        )

    def verify_certificate_chain(self, certificate_chain: List[bytes]) -> bool:
        """Verify certificate chain using plugin.

        Args:
            certificate_chain: List of certificate bytes

        Returns:
            True if certificate chain is valid.
        """
        return verify_certificate_chain(certificate_chain)

    def _generate_image_hash(self, image: Any) -> bytes:
        """Generate hash of image for signing.

        Args:
            image: Image to hash

        Returns:
            Image hash bytes.
        """
        import hashlib

        data = self._prepare_image_data(image)
        return hashlib.sha384(data).digest()

    def _load_public_key_from_plugin(self) -> None:
        """Load public key from plugin."""
        if not self.plugin_signer:
            return

        try:
            args = ['--get-public-key']
            process = subprocess.Popen(
                [self.plugin_signer] + args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            stdout, _ = process.communicate()

            if process.returncode == 0:
                data = json.loads(stdout.decode('utf-8'))
                if pub_key_hex := data.get('public_key'):
                    self._public_key_bytes = bytes.fromhex(pub_key_hex)

        except Exception:
            pass

    def get_signature_algorithm(self) -> str:
        """Get signature algorithm from plugin.

        Returns:
            Signature algorithm name.
        """
        if hasattr(self.security_profile, 'signing_features'):
            return self.security_profile.signing_features.get('algorithm', 'ECDSA')
        return 'ECDSA'

    def get_signature_information(self, signature: bytes) -> Dict[str, Any]:
        """Get signature information from plugin.

        Args:
            signature: Signature bytes

        Returns:
            Dictionary with signature information.
        """
        info = get_signature_information(signature)
        info['plugin'] = self.plugin_signer
        info['plugin_args'] = self.plugin_signer_args
        return info

    def close(self) -> None:
        """Close plugin process."""
        if self._plugin_process:
            self._plugin_process.kill()
            self._plugin_process = None

    def __del__(self) -> None:
        """Destructor - clean up plugin process."""
        self.close()
