"""Base command line."""

from typing import Any, Dict, List, Tuple, Optional


class NamespaceWithGet(dict):
    """Namespace with get method."""

    def get(self, key: str, default: Any = None) -> Any:
        return super().get(key, default)

    def __getattr__(self, name: str) -> Any:
        if name in self:
            return self[name]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        self[name] = value


class BaseCMDLine:
    """Base command line class."""
    TOOL_NAME = 'sectools'


CMDLineArgs = Dict[str, Any]
CMDLineGroup = List[Tuple]


def update_cmdline_arg(cmdline_args: CMDLineArgs, *args, **kwargs) -> None:
    """Update command line arguments."""
    pass
