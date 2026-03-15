"""Core interface module."""

from typing import Any, Dict


class CoreInterface:
    """Core interface base class."""

    def run(self, parsed_args: Dict[str, Any]) -> None:
        """Run core operation.
        
        Args:
            parsed_args: Parsed command line arguments
        """
        raise NotImplementedError("Subclasses must implement run")
