"""Encryption operations for secure image.

Based on decompiled analysis of sectools.exe encrypt_operation.
Supports UIE and QBEC encryption modes with AES-128-XTS.
"""

from typing import Any, Dict, List, Optional, Tuple
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


# Encryption mode constants
ENCRYPTION_MODE_LOCAL = 'LOCAL'
ENCRYPTION_MODE_TEST = 'TEST'
ENCRYPTION_MODE_PLUGIN = 'PLUGIN'

# Encryption type constants
ENCRYPTION_TYPE_UIE = 'UIE'
ENCRYPTION_TYPE_QBEC = 'QBEC'

# Key management feature IDs
FEATURE_ID_SBL = 0x01
FEATURE_ID_AMSS = 0x02
FEATURE_ID_APPSBL = 0x03

# Encryption order constants
ENCRYPTED_THEN_SIGNED = 'ENCRYPTED_THEN_SIGNED'
SIGNED_THEN_ENCRYPTED = 'SIGNED_THEN_ENCRYPTED'


class EncryptionParameters:
    """Encryption parameters container."""

    def __init__(
        self,
        encrypted_segments: Optional[List[bytes]] = None,
        encryption_algorithm: str = 'AES-128-XTS',
        key_id: Optional[bytes] = None,
        nonce: Optional[bytes] = None,
    ) -> None:
        """Initialize encryption parameters.

        Args:
            encrypted_segments: List of encrypted segment data
            encryption_algorithm: Encryption algorithm used
            key_id: Key identifier used for encryption
            nonce: Nonce used for encryption
        """
        self.encrypted_segments = encrypted_segments or []
        self.encryption_algorithm = encryption_algorithm
        self.key_id = key_id
        self.nonce = nonce

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'encrypted_segments': [
                seg.hex() for seg in self.encrypted_segments
            ],
            'encryption_algorithm': self.encryption_algorithm,
            'key_id': self.key_id.hex() if self.key_id else None,
            'nonce': self.nonce.hex() if self.nonce else None,
        }


class BaseEncrypter:
    """Base class for all encrypters."""

    def __init__(
        self,
        parsed_image: Any,
        security_profile: Any,
        device_restrictions: Any,
        authority: str,
    ) -> None:
        """Initialize base encrypter.

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

    def encrypt(self) -> EncryptionParameters:
        """Encrypt the image.

        Returns:
            Encryption parameters with encrypted segments.

        Raises:
            RuntimeError: If encryption fails.
        """
        raise NotImplementedError("Subclasses must implement encrypt")

    def get_encryption_algorithm(self) -> str:
        """Get encryption algorithm.

        Returns:
            Encryption algorithm name.
        """
        raise NotImplementedError(
            "Subclasses must implement get_encryption_algorithm"
        )


class LocalEncrypter(BaseEncrypter):
    """Local encrypter using provided keys."""

    def __init__(
        self,
        parsed_image: Any,
        security_profile: Any,
        device_restrictions: Any,
        authority: str,
        l1_key: Optional[bytes] = None,
        l2_key: Optional[bytes] = None,
        l3_key: Optional[bytes] = None,
        root_key_type: Optional[str] = None,
        feature_id: Optional[int] = None,
    ) -> None:
        """Initialize local encrypter.

        Args:
            parsed_image: Parsed image object
            security_profile: Security profile object
            device_restrictions: Device restrictions object
            authority: Authority type (OEM or QTI)
            l1_key: L1 encryption key
            l2_key: L2 encryption key
            l3_key: L3 encryption key
            root_key_type: Root key type
            feature_id: Feature identifier
        """
        super().__init__(
            parsed_image,
            security_profile,
            device_restrictions,
            authority,
        )

        self.l1_key = l1_key
        self.l2_key = l2_key
        self.l3_key = l3_key
        self.root_key_type = root_key_type
        self.feature_id = feature_id

    def encrypt(self) -> EncryptionParameters:
        """Encrypt the image using local keys.

        Returns:
            Encryption parameters with encrypted segments.
        """
        segments = self._get_segments_to_encrypt()
        key = self._select_encryption_key()

        if not key:
            raise RuntimeError("No encryption key provided")

        encrypted_segments = []
        for segment in segments:
            encrypted = self._encrypt_segment(segment, key)
            encrypted_segments.append(encrypted)

        return EncryptionParameters(
            encrypted_segments=encrypted_segments,
            encryption_algorithm='AES-128-XTS',
            key_id=key[:8] if key else None,
            nonce=b'\x00' * 16,
        )

    def _get_segments_to_encrypt(self) -> List[bytes]:
        """Get segments to encrypt from image.

        Returns:
            List of segment bytes to encrypt.
        """
        if hasattr(self.parsed_image, 'segments'):
            return self.parsed_image.segments()
        elif hasattr(self.parsed_image, 'data'):
            return [self.parsed_image.data]
        return []

    def _select_encryption_key(self) -> Optional[bytes]:
        """Select encryption key (L1/L2/L3).

        Returns:
            Selected key bytes.
        """
        if self.l1_key:
            return self.l1_key
        if self.l2_key:
            return self.l2_key
        if self.l3_key:
            return self.l3_key
        return None

    def _encrypt_segment(self, segment: bytes, key: bytes) -> bytes:
        """Encrypt segment using AES-128-XTS.

        Args:
            segment: Segment data to encrypt
            key: Encryption key (16 bytes for AES-128)

        Returns:
            Encrypted segment bytes.
        """
        # XTS needs 2x key size (256 bits for AES-128-XTS)
        # Keys must be different (XTS uses two independent keys)
        key_16 = key[:16] if len(key) > 16 else key.ljust(16, b'\x00')
        # Create second key by XORing with 0xFF
        key_16_2 = bytes(b ^ 0xFF for b in key_16)
        key_32 = key_16 + key_16_2  # Two independent keys for XTS

        tweak = b'\x00' * 16
        cipher = Cipher(
            algorithms.AES(key_32),
            modes.XTS(tweak),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()

        padded = self._pad_data(segment)
        return encryptor.update(padded) + encryptor.finalize()

    def _pad_data(self, data: bytes) -> bytes:
        """Pad data to 16-byte boundary.

        Args:
            data: Data to pad

        Returns:
            Padded data.
        """
        pad_len = 16 - (len(data) % 16)
        return data + bytes([pad_len] * pad_len)

    def get_encryption_algorithm(self) -> str:
        """Get encryption algorithm.

        Returns:
            Encryption algorithm name.
        """
        return 'AES-128-XTS'


class TestEncrypter(BaseEncrypter):
    """Test encrypter using test keys."""

    def __init__(
        self,
        parsed_image: Any,
        security_profile: Any,
        device_restrictions: Any,
        authority: str,
        encryption_type: str = ENCRYPTION_TYPE_UIE,
    ) -> None:
        """Initialize test encrypter.

        Args:
            parsed_image: Parsed image object
            security_profile: Security profile object
            device_restrictions: Device restrictions object
            authority: Authority type (OEM or QTI)
            encryption_type: Encryption type (UIE or QBEC)
        """
        super().__init__(
            parsed_image,
            security_profile,
            device_restrictions,
            authority,
        )

        self.encryption_type = encryption_type
        self._test_key = bytes.fromhex(
            '000102030405060708090a0b0c0d0e0f'
        )

    def encrypt(self) -> EncryptionParameters:
        """Encrypt the image using test keys.

        Returns:
            Encryption parameters with encrypted segments.
        """
        segments = self._get_segments_to_encrypt()
        encrypted_segments = []

        for segment in segments:
            encrypted = self._encrypt_segment(segment, self._test_key)
            encrypted_segments.append(encrypted)

        return EncryptionParameters(
            encrypted_segments=encrypted_segments,
            encryption_algorithm='AES-128-XTS',
            key_id=self._test_key[:8],
            nonce=b'\x00' * 16,
        )

    def _get_segments_to_encrypt(self) -> List[bytes]:
        """Get segments to encrypt from image.

        Returns:
            List of segment bytes to encrypt.
        """
        if hasattr(self.parsed_image, 'segments'):
            return self.parsed_image.segments()
        elif hasattr(self.parsed_image, 'data'):
            return [self.parsed_image.data]
        return []

    def _encrypt_segment(self, segment: bytes, key: bytes) -> bytes:
        """Encrypt segment using AES-128-XTS.

        Args:
            segment: Segment data to encrypt
            key: Encryption key

        Returns:
            Encrypted segment bytes.
        """
        # XTS needs 2x key size (256 bits for AES-128-XTS)
        # Keys must be different (XTS uses two independent keys)
        key_16 = key[:16] if len(key) > 16 else key.ljust(16, b'\x00')
        # Create second key by XORing with 0xFF
        key_16_2 = bytes(b ^ 0xFF for b in key_16)
        key_32 = key_16 + key_16_2  # Two independent keys for XTS

        tweak = b'\x00' * 16
        cipher = Cipher(
            algorithms.AES(key_32),
            modes.XTS(tweak),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()

        padded = self._pad_data(segment)
        return encryptor.update(padded) + encryptor.finalize()

    def _pad_data(self, data: bytes) -> bytes:
        """Pad data to 16-byte boundary.

        Args:
            data: Data to pad

        Returns:
            Padded data.
        """
        pad_len = 16 - (len(data) % 16)
        return data + bytes([pad_len] * pad_len)

    def get_encryption_algorithm(self) -> str:
        """Get encryption algorithm.

        Returns:
            Encryption algorithm name.
        """
        return 'AES-128-XTS'


class PluginEncrypter(BaseEncrypter):
    """Plugin encrypter using external encryption plugin."""

    def __init__(
        self,
        parsed_image: Any,
        security_profile: Any,
        device_restrictions: Any,
        authority: str,
        plugin_encrypter: Optional[str] = None,
        plugin_encrypter_args: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize plugin encrypter.

        Args:
            parsed_image: Parsed image object
            security_profile: Security profile object
            device_restrictions: Device restrictions object
            authority: Authority type (OEM or QTI)
            plugin_encrypter: Plugin encrypter path
            plugin_encrypter_args: Plugin arguments
        """
        super().__init__(
            parsed_image,
            security_profile,
            device_restrictions,
            authority,
        )

        self.plugin_encrypter = plugin_encrypter
        self.plugin_encrypter_args = plugin_encrypter_args or {}

    def encrypt(self) -> EncryptionParameters:
        """Encrypt the image using external plugin.

        Returns:
            Encryption parameters with encrypted segments.

        Raises:
            RuntimeError: If plugin encryption fails.
        """
        import subprocess
        import json

        if not self.plugin_encrypter:
            raise RuntimeError("Plugin encrypter not specified")

        image_data = self._get_image_data()
        args = self._build_plugin_args()

        try:
            process = subprocess.Popen(
                [self.plugin_encrypter] + args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            stdout, stderr = process.communicate(input=image_data)

            if process.returncode != 0:
                raise RuntimeError(
                    f"Plugin encryption failed: {stderr.decode('utf-8')}"
                )

            return self._parse_plugin_response(stdout)

        except Exception as e:
            raise RuntimeError(f"Plugin encryption failed: {e}")

    def _get_image_data(self) -> bytes:
        """Get image data for encryption.

        Returns:
            Image data bytes.
        """
        if hasattr(self.parsed_image, 'data'):
            return self.parsed_image.data
        return b''

    def _build_plugin_args(self) -> List[str]:
        """Build plugin command line arguments.

        Returns:
            List of arguments.
        """
        args = ['--encrypt']

        for key, value in self.plugin_encrypter_args.items():
            args.append(f'--{key}={json.dumps(value)}')

        return args

    def _parse_plugin_response(self, response: bytes) -> EncryptionParameters:
        """Parse plugin response.

        Args:
            response: Plugin response bytes

        Returns:
            Encryption parameters.

        Raises:
            RuntimeError: If response parsing fails.
        """
        try:
            data = json.loads(response.decode('utf-8'))

            encrypted_segments = [
                bytes.fromhex(seg)
                for seg in data.get('encrypted_segments', [])
            ]

            return EncryptionParameters(
                encrypted_segments=encrypted_segments,
                encryption_algorithm=data.get('algorithm', 'AES-128-XTS'),
                key_id=bytes.fromhex(data['key_id']) if data.get('key_id') else None,
                nonce=bytes.fromhex(data['nonce']) if data.get('nonce') else None,
            )

        except Exception as e:
            raise RuntimeError(f"Failed to parse plugin response: {e}")

    def get_encryption_algorithm(self) -> str:
        """Get encryption algorithm.

        Returns:
            Encryption algorithm name.
        """
        return 'AES-128-XTS'


def get_encryption_format_id(encryption_format: str) -> int:
    """Get encryption format ID from format string.

    Args:
        encryption_format: Encryption format string

    Returns:
        Encryption format ID.
    """
    format_map = {'UIE': 1, 'QBEC': 2}
    return format_map.get(encryption_format, 0)


def get_encryption_order_string(encryption_order: int) -> str:
    """Get encryption order string from ID.

    Args:
        encryption_order: Encryption order ID

    Returns:
        Encryption order string.
    """
    if encryption_order == 1:
        return ENCRYPTED_THEN_SIGNED
    return SIGNED_THEN_ENCRYPTED


def validate_encryption_type_supported(
    encryption_type: str,
    supported_types: List[str]
) -> bool:
    """Validate encryption type is supported.

    Args:
        encryption_type: Encryption type to validate
        supported_types: List of supported types

    Returns:
        True if type is supported.
    """
    return encryption_type in supported_types


def validate_key_arguments_against_encryption_type(
    parsed_args: Dict[str, Any],
    encryption_format: Any
) -> None:
    """Validate key arguments against encryption type.

    Args:
        parsed_args: Parsed command line arguments
        encryption_format: Encryption format from security profile

    Raises:
        ValueError: If key arguments are invalid.
    """
    encryption_type = getattr(encryption_format, 'encryption_type', 'UIE')

    if encryption_type == ENCRYPTION_TYPE_QBEC:
        if parsed_args.get('encryption-mode') == ENCRYPTION_MODE_LOCAL:
            if not parsed_args.get('device-private-key'):
                raise ValueError(
                    "LOCAL mode requires device-private-key for QBEC"
                )
            if not parsed_args.get('device-nonce'):
                raise ValueError(
                    "LOCAL mode requires device-nonce for QBEC"
                )

    uie_only_args = ['l1-key', 'l2-key', 'l3-key', 'root-key-type']
    provided_uie_args = [
        arg for arg in uie_only_args
        if parsed_args.get(arg)
    ]

    if encryption_type == ENCRYPTION_TYPE_QBEC and provided_uie_args:
        raise ValueError(
            f"QBEC incompatible with: {', '.join(provided_uie_args)}"
        )


def get_key_management_feature_id(feature_id: int) -> int:
    """Get key management feature ID.

    Args:
        feature_id: Feature ID

    Returns:
        Key management feature ID.
    """
    feature_map = {
        FEATURE_ID_SBL: 0x01,
        FEATURE_ID_AMSS: 0x02,
        FEATURE_ID_APPSBL: 0x03,
    }
    return feature_map.get(feature_id, 0)


def get_supported_encryption_formats() -> List[str]:
    """Get supported encryption formats.

    Returns:
        List of supported format strings.
    """
    return ['UIE', 'QBEC']


def get_default_encryption_format() -> str:
    """Get default encryption format.

    Returns:
        Default format string.
    """
    return 'UIE'


def get_supported_encryption_algorithms() -> List[str]:
    """Get supported encryption algorithms.

    Returns:
        List of algorithm strings.
    """
    return ['AES-128-XTS']


def get_default_encryption_algorithm() -> str:
    """Get default encryption algorithm.

    Returns:
        Default algorithm string.
    """
    return 'AES-128-XTS'
