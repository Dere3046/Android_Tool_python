"""
ELF positional data base class.
Based on decompiled analysis.
"""

from typing import Any, Optional, Union


class AbstractPositionalData:
    """Abstract positional data class."""

    def __init__(self, data=None, check_is_type=None, bypass_validation=False):
        """Initialize positional data.

        Args:
            data: Raw data
            check_is_type: Check type
            bypass_validation: Skip validation
        """
        self._data = data
        self.ignore = False

    def offset(self) -> int:
        """Get offset."""
        raise NotImplementedError

    def size(self) -> int:
        """Get size."""
        raise NotImplementedError

    def alignment(self) -> int:
        """Get alignment."""
        raise NotImplementedError

    def address(self) -> int:
        """Get address."""
        raise NotImplementedError

    def mem_size(self) -> int:
        """Get memory size."""
        raise NotImplementedError

    def is_loadable(self) -> bool:
        """Is loadable."""
        return False

    def is_uie_encryptable(self) -> bool:
        """Is UIE encryptable."""
        return False

    def is_qbec_encryptable(self) -> bool:
        """Is QBEC encryptable."""
        return False

    def is_encryptable(self) -> bool:
        """Is encryptable."""
        return self.is_uie_encryptable() or self.is_qbec_encryptable()

    def data_name(self) -> str:
        """Data name."""
        return ""

    def is_to_be_ignored(self) -> bool:
        """Should be ignored."""
        return False

    def validate_before_operation(self, **kwargs) -> None:
        """Validate before operation."""
        pass


class PositionalData(AbstractPositionalData):
    """Positional data implementation."""

    def __init__(self, data=None, check_is_type=None, bypass_validation=False):
        """Initialize positional data.

        Args:
            data: Raw data
            check_is_type: Check type
            bypass_validation: Skip validation
        """
        super().__init__(data, check_is_type, bypass_validation)
        self._offset = 0
        self._size = 0
        self._alignment = 0
        self._address = 0
        self._mem_size = 0

    def offset(self) -> int:
        """Get offset."""
        return self._offset

    def size(self) -> int:
        """Get size."""
        return self._size

    def alignment(self) -> int:
        """Get alignment."""
        return self._alignment

    def address(self) -> int:
        """Get address."""
        return self._address

    def mem_size(self) -> int:
        """Get memory size."""
        return self._mem_size

    def end(self) -> int:
        """Get end offset."""
        return self.offset() + self.size()
