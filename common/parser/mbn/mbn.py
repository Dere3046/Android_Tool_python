"""MBN parser implementation based on decompiled analysis."""

from typing import Any, Type, Union, Optional, List, Tuple

from common.data.base_parser import DumpDict
from common.data.binary_struct import DetailsTuple, StructDynamic
from common.parser.elf_with_hash_segment.elf_with_hash_segment import HashTableSegmentCommon
from common.parser.elf_with_hash_segment.hash_table_segment_header import HashTableSegmentHeaderCommon
from common.parser.hash_segment.defines import (
    AUTHORITY_OEM,
    HASH_SEGMENT_V3,
    HASH_SEGMENT_V5,
    HASH_SEGMENT_V6,
    HASH_SEGMENT_V7,
    HASH_SEGMENT_V8,
)
from common.parser.mbn.v3.mbn_header import MBNHeaderV3
from common.parser.mbn.v5.mbn_header import MBNHeaderV5
from common.parser.mbn.v6.mbn_header import MBNHeaderV6
from common.parser.mbn.v7.mbn_header import MBNHeaderV7
from common.parser.mbn.v8.mbn_header import MBNHeaderV8
from common.parser.parser_image_info_interface import (
    ImageFormatType,
    ImageInfoInterface,
    ImageProperties,
    MBN_PROPERTIES,
)
from profile.schema import ImageFormat, MBNProperties


MBN_HEADER_CLASSES: dict[int, Type[Union[MBNHeaderV3, MBNHeaderV5, MBNHeaderV6, MBNHeaderV7, MBNHeaderV8]]] = {
    HASH_SEGMENT_V3: MBNHeaderV3,
    HASH_SEGMENT_V5: MBNHeaderV5,
    HASH_SEGMENT_V6: MBNHeaderV6,
    HASH_SEGMENT_V7: MBNHeaderV7,
    HASH_SEGMENT_V8: MBNHeaderV8,
}


class MBN(HashTableSegmentCommon, ImageInfoInterface):
    """MBN image parser."""

    def __init__(self, data: Optional[Union[memoryview, bytearray]] = None, **kwargs: Any) -> None:
        """Initialize MBN parser."""
        self.code: Union[memoryview, bytearray] = memoryview(b'')
        super().__init__(data=data, **kwargs)

    @classmethod
    def hash_segment_type(cls) -> str:
        """Get hash segment type."""
        return "MBN"

    def image_type_string(self) -> str:
        """Get image type string."""
        if self.header is None:
            raise AssertionError("header is not set")
        return f"v{self.header.version} {self.hash_segment_type()}"

    def create_default(
        self,
        mbn_version: int,
        code: Union[memoryview, bytearray],
        **kwargs: Any,
    ) -> None:
        """Create default MBN image."""
        self.code = code
        if self.header is None:
            if mbn_version in MBN_HEADER_CLASSES:
                header_class = MBN_HEADER_CLASSES[mbn_version]
                self.header = header_class()

                if mbn_version == HASH_SEGMENT_V3:
                    self.header.boot_image_id = 0
                    self.header.version = 3
                    self.header.image_src = 0
                    self.header.image_dest_ptr = 0
                    self.header.image_size = len(code)
                    self.header.code_size = len(code)
                    self.header.sig_ptr = len(code)
                    self.header.sig_size = 0
                    self.header.cert_chain_ptr = len(code)
                    self.header.cert_chain_size = 0
                elif mbn_version == HASH_SEGMENT_V5:
                    self.header.image_id = 0
                    self.header.version = 5
                    self.header.image_src = 0
                    self.header.image_dest_ptr = 0
                    self.header.image_size = len(code)
                    self.header.code_size = len(code)
                    self.header.sig_ptr = len(code)
                    self.header.sig_size = 0
                    self.header.cert_chain_ptr = len(code)
                    self.header.cert_chain_size = 0
                elif mbn_version == HASH_SEGMENT_V6:
                    self.header.image_id = 0
                    self.header.version = 6
                    self.header.image_src = 0
                    self.header.image_dest_ptr = 0
                    self.header.image_size = len(code)
                    self.header.code_size = len(code)
                    self.header.sig_ptr = len(code)
                    self.header.sig_size = 0
                    self.header.cert_chain_ptr = len(code)
                    self.header.cert_chain_size = 0
                    self.header.qti_sig_size = 0
                    self.header.qti_cert_chain_size = 0
                elif mbn_version in (HASH_SEGMENT_V7, HASH_SEGMENT_V8):
                    self.header.image_id = 0
                    self.header.version = mbn_version
                    self.header.image_src = 0x18
                    self.header.image_dest_ptr = 0
                    self.header.image_size = 0
                    self.header.code_size = len(code)
                    self.header.sig_ptr = 0
                    self.header.sig_size = 0
                    self.header.cert_chain_ptr = 0
                    self.header.cert_chain_size = 0

                for key, value in kwargs.items():
                    if hasattr(self.header, key):
                        setattr(self.header, key, value)
            else:
                raise RuntimeError(f"Unsupported MBN version: {mbn_version}")

    def unpack(self, data: Union[memoryview, bytearray]) -> None:
        """Unpack MBN data."""
        if len(data) < 8:
            raise ValueError("Data too small for MBN header")

        version = int.from_bytes(data[4:8], 'little')

        if version not in MBN_HEADER_CLASSES:
            raise ValueError(f"Unsupported MBN version: {version}")

        header_class = MBN_HEADER_CLASSES[version]
        self.header = header_class(data)

        if version in (HASH_SEGMENT_V7, HASH_SEGMENT_V8):
            if version == HASH_SEGMENT_V7:
                self.code = data[64:]
            else:
                self.code = data[80:]
        else:
            self.code = data[self.header.size():]

    def pack(self) -> memoryview:
        """Pack MBN data."""
        if self.header is None:
            raise AssertionError("header is not set")

        header_data = self.header.pack()

        if self.header.version in (HASH_SEGMENT_V7, HASH_SEGMENT_V8):
            if self.header.version == HASH_SEGMENT_V7:
                padding_size = 64 - self.header.size()
            else:
                padding_size = 80 - self.header.size()
            padding = b'\x00' * padding_size
            return memoryview(header_data + padding + bytes(self.code))
        else:
            return memoryview(header_data + bytes(self.code))

    def get_image_properties(self, authority: str = AUTHORITY_OEM) -> ImageProperties:
        """Get image properties."""
        props = {}
        if self.header:
            props['version'] = self.header.version
            props['code_size'] = len(self.code)
        return ImageProperties(
            image_type=ImageFormatType.MBN,
            properties=props
        )

    def get_image_format(self, authority: str = AUTHORITY_OEM) -> List[ImageFormat]:
        """Get image format list."""
        return [ImageFormat(format_type=ImageFormatType.MBN)]

    @classmethod
    def is_type(cls, data: Union[memoryview, bytearray]) -> bool:
        """Check if data is MBN format."""
        if len(data) < 8:
            return False

        version = int.from_bytes(data[4:8], 'little')
        return version in (HASH_SEGMENT_V3, HASH_SEGMENT_V5, HASH_SEGMENT_V6, HASH_SEGMENT_V7, HASH_SEGMENT_V8)
