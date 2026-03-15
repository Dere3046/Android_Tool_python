"""Common utilities."""

import os
from pathlib import Path
from typing import Union


def write_cmdline_file(path: Union[str, Path], data: bytes, description: str = "") -> None:
    """Write cmdline file.
    
    Args:
        path: File path
        data: Data to write
        description: File description for logging
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def delete_file(path: Union[str, Path]) -> None:
    """Delete file.
    
    Args:
        path: File path
    """
    path = Path(path)
    if path.exists():
        path.unlink()
