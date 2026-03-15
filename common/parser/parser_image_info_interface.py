"""Parser image info interface."""

from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum


class ImageFormatType(Enum):
    """Image format type enumeration."""
    MBN = 'MBN'
    ELF = 'ELF'
    MDT = 'MDT'
    SEC_DAT = 'SEC_DAT'
    SEC_ELF = 'SEC_ELF'


@dataclass
class ImageProperties:
    """Image properties."""
    image_type: ImageFormatType = ImageFormatType.MBN
    properties: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'image_type': self.image_type.value,
            'properties': self.properties
        }


class ImageFormat:
    """Image format."""

    def __init__(self, format_type: ImageFormatType, **kwargs):
        self.format_type = format_type
        self.properties = kwargs

    def __repr__(self) -> str:
        return f"ImageFormat({self.format_type.value}, {self.properties})"


class ImageInfoInterface:
    """Image info interface base class."""

    def __init__(self, data: Optional[Union[memoryview, bytearray]] = None, **kwargs):
        """Initialize image info interface."""
        self.data = data

    def unpack(self, data: Union[memoryview, bytearray]) -> None:
        """Unpack image data."""
        raise NotImplementedError("Subclasses must implement unpack")

    def pack(self) -> Union[memoryview, bytearray]:
        """Pack image data."""
        raise NotImplementedError("Subclasses must implement pack")

    def get_image_properties(self, authority: str = 'OEM') -> ImageProperties:
        """Get image properties."""
        raise NotImplementedError("Subclasses must implement get_image_properties")

    def get_image_format(self, authority: str = 'OEM') -> List[ImageFormat]:
        """Get image format list."""
        raise NotImplementedError("Subclasses must implement get_image_format")

    def class_type_string(self) -> str:
        """Get class type string."""
        return self.__class__.__name__


MBN_PROPERTIES = 'mbn_properties'
ELF_PROPERTIES = 'elf_properties'


class CoreInterface:
    """Core interface base class."""

    def run(self, parsed_args: dict) -> None:
        """Run core operation."""
        raise NotImplementedError("Subclasses must implement run")
