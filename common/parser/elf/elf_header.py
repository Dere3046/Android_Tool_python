"""ELF header common base class."""


class ELFHeaderCommon:
    """ELF header common base class."""

    def __init__(self, data=None, **kwargs):
        """Initialize ELF header common base class."""
        pass

    def get_ident(self):
        """Get ident field (implemented by subclasses)."""
        raise NotImplementedError
