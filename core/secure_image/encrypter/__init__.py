"""Encrypter module for secure image encryption.

This module provides encryption functionality based on decompiled
analysis of sectools.exe secure_image_core.pyc.
"""

from .encrypter import (
    # Constants
    ENCRYPTION_MODE_LOCAL,
    ENCRYPTION_MODE_TEST,
    ENCRYPTION_MODE_PLUGIN,
    ENCRYPTION_TYPE_UIE,
    ENCRYPTION_TYPE_QBEC,
    FEATURE_ID_SBL,
    FEATURE_ID_AMSS,
    FEATURE_ID_APPSBL,
    ENCRYPTED_THEN_SIGNED,
    SIGNED_THEN_ENCRYPTED,
    
    # Classes
    EncryptionParameters,
    BaseEncrypter,
    LocalEncrypter,
    TestEncrypter,
    PluginEncrypter,
    
    # Functions
    get_encryption_format_id,
    get_encryption_order_string,
    validate_encryption_type_supported,
    validate_key_arguments_against_encryption_type,
    get_key_management_feature_id,
    get_supported_encryption_formats,
    get_default_encryption_format,
    get_supported_encryption_algorithms,
    get_default_encryption_algorithm,
)

__all__ = [
    # Constants
    'ENCRYPTION_MODE_LOCAL',
    'ENCRYPTION_MODE_TEST',
    'ENCRYPTION_MODE_PLUGIN',
    'ENCRYPTION_TYPE_UIE',
    'ENCRYPTION_TYPE_QBEC',
    'FEATURE_ID_SBL',
    'FEATURE_ID_AMSS',
    'FEATURE_ID_APPSBL',
    'ENCRYPTED_THEN_SIGNED',
    'SIGNED_THEN_ENCRYPTED',
    
    # Classes
    'EncryptionParameters',
    'BaseEncrypter',
    'LocalEncrypter',
    'TestEncrypter',
    'PluginEncrypter',
    
    # Functions
    'get_encryption_format_id',
    'get_encryption_order_string',
    'validate_encryption_type_supported',
    'validate_key_arguments_against_encryption_type',
    'get_key_management_feature_id',
    'get_supported_encryption_formats',
    'get_default_encryption_format',
    'get_supported_encryption_algorithms',
    'get_default_encryption_algorithm',
]
