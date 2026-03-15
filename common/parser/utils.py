"""Parser utilities."""

from pathlib import Path
from typing import Union, Optional

from common.parser.elf.elf import ELF
from common.parser.elf_with_hash_segment.elf_with_hash_segment import ELFWithHashTableSegment


def get_parsed_image(path: Union[str, Path]) -> Optional[object]:
    """Get parsed image object.
    
    Args:
        path: Image file path
        
    Returns:
        Parsed image object (ELF, MBN, MDT, etc.)
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with open(path, 'rb') as f:
        data = memoryview(f.read())

    if len(data) < 4:
        raise ValueError(f"File too small: {path}")

    if data[:4] == b'\x7fELF':
        elf = ELFWithHashTableSegment()
        try:
            elf.unpack(data)
            return elf
        except Exception:
            elf = ELF()
            elf.unpack(data)
            return elf

    raise ValueError(f"Unknown file format: {path}")


def get_compressed_data(data: Union[memoryview, bytearray, bytes]) -> bytes:
    """Get compressed data."""
    import zlib
    return zlib.compress(bytes(data), level=9)


def get_uncompressed_data(data: Union[memoryview, bytearray, bytes]) -> bytes:
    """Get uncompressed data."""
    import zlib
    return zlib.decompress(bytes(data))
