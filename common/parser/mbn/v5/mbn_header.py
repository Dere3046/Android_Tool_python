"""MBN v5 header implementation."""

import struct
from dataclasses import dataclass
from typing import ClassVar, Tuple, Optional

from common.data.binary_struct import StructDynamic


@dataclass
class MBNHeaderV5(StructDynamic):
    """MBN version 5 header - 40 bytes format."""

    STRUCT_FORMAT: ClassVar[str] = '<IIIIIIIIII'
    STRUCT_FIELDS: ClassVar[Tuple[str, ...]] = (
        'image_id',
        'version',
        'image_src',
        'image_dest_ptr',
        'image_size',
        'code_size',
        'sig_ptr',
        'sig_size',
        'cert_chain_ptr',
        'cert_chain_size',
    )

    image_id: int = 0
    version: int = 5
    image_src: int = 0
    image_dest_ptr: int = 0
    image_size: int = 0
    code_size: int = 0
    sig_ptr: int = 0
    sig_size: int = 0
    cert_chain_ptr: int = 0
    cert_chain_size: int = 0

    def __init__(self, data: Optional[bytes] = None, **kwargs):
        """Initialize MBN v5 header."""
        self.image_id = 0
        self.version = 5
        self.image_src = 0
        self.image_dest_ptr = 0
        self.image_size = 0
        self.code_size = 0
        self.sig_ptr = 0
        self.sig_size = 0
        self.cert_chain_ptr = 0
        self.cert_chain_size = 0

        if data is not None:
            if len(data) < self.size():
                raise ValueError(f"Insufficient data, need at least {self.size()} bytes")
            values = struct.unpack(self.STRUCT_FORMAT, data[:self.size()])
            for field, value in zip(self.STRUCT_FIELDS, values):
                setattr(self, field, value)

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @classmethod
    def unpack(cls, data: bytes) -> 'MBNHeaderV5':
        """Unpack from bytes."""
        return cls(data)

    def pack(self) -> bytes:
        """Pack to bytes."""
        if self.sig_ptr == 0 and self.code_size != 0:
            self.sig_ptr = self.image_dest_ptr + self.code_size

        if self.cert_chain_ptr == 0 and self.sig_ptr != 0:
            self.cert_chain_ptr = self.sig_ptr + self.sig_size

        if self.image_size == 0:
            self.image_size = self.code_size + self.sig_size + self.cert_chain_size

        values = [getattr(self, field) for field in self.STRUCT_FIELDS]
        return struct.pack(self.STRUCT_FORMAT, *values)

    def size(self) -> int:
        """Get header size."""
        return struct.calcsize(self.STRUCT_FORMAT)
