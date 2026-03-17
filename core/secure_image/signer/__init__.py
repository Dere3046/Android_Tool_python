"""Signer module for secure image signing.

This module provides different signer implementations based on
decompiled analysis of sectools.exe:
- BaseSigner: Abstract base class
- LocalSigner: Local signing with provided certificates
- TestSigner: Test signing with test certificates
- PluginSigner: External plugin-based signing
"""

from .base_signer import BaseSigner
from .local_signer import LocalSigner
from .test_signer import TestSigner
from .plugin_signer import PluginSigner

__all__ = [
    'BaseSigner',
    'LocalSigner',
    'TestSigner',
    'PluginSigner',
]
