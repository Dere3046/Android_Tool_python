"""Base parser module."""


class DumpDict(dict):
    """Dictionary with dump capabilities."""
    pass


class BaseParser:
    """Base parser class."""

    def __init__(self, data=None, **kwargs):
        """Initialize base parser."""
        self.data = data

    def unpack(self, data):
        """Unpack data."""
        pass

    def pack(self):
        """Pack data."""
        return b''
