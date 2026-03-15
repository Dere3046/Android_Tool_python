"""Profile schema definitions."""

from typing import Any, Dict


class MBNProperties:
    """MBN properties."""

    def __init__(self, version, metadata_version, common_metadata_version):
        self.version = version
        self.metadata_version = metadata_version
        self.common_metadata_version = common_metadata_version


class ImageFormat:
    """Image format."""

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class ELFProperties:
    """ELF properties."""

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
