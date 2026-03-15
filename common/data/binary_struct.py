"""Binary structure module."""

from typing import NamedTuple, Any, ClassVar, Tuple, Dict, Optional, Union
import struct


class DetailsTuple(NamedTuple):
    """Details tuple."""
    fields: list
    format_str: str
    field_dict: dict


class StructBase:
    """Base class for binary structures."""

    STRUCT_FORMAT: ClassVar[str] = ''
    STRUCT_FIELDS: ClassVar[Tuple[str, ...]] = ()

    def __init__(self, data: Optional[bytes] = None, check_is_type=None, bypass_validation=False):
        """Initialize structure.
        
        Args:
            data: Optional bytes data to unpack
            check_is_type: Type check parameter
            bypass_validation: Skip validation if True
        """
        for field in self.get_fields():
            setattr(self, field, 0)

        if data is not None:
            self.unpack(data)

        self.ignore = False

    @classmethod
    def get_fields(cls) -> Tuple[str, ...]:
        """Get field names."""
        return cls.STRUCT_FIELDS

    @classmethod
    def get_format(cls) -> str:
        """Get struct format string."""
        return cls.STRUCT_FORMAT

    def unpack(self, data: bytes) -> None:
        """Unpack from bytes."""
        format_str = self.get_format()
        fields = self.get_fields()

        if len(data) < struct.calcsize(format_str):
            raise ValueError(f"Insufficient data, need at least {struct.calcsize(format_str)} bytes")

        values = struct.unpack(format_str, data[:struct.calcsize(format_str)])
        for field, value in zip(fields, values):
            setattr(self, field, value)

    def pack(self) -> bytes:
        """Pack to bytes."""
        format_str = self.get_format()
        fields = self.get_fields()
        values = [getattr(self, field) for field in fields]
        return struct.pack(format_str, *values)

    def size(self) -> int:
        """Get structure size."""
        return struct.calcsize(self.get_format())


class StructDynamic(StructBase):
    """Dynamic structure (MBN compatibility)."""
    pass
