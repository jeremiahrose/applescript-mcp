"""Tools package for macOS control functionality."""

from . import macos

# Expose macos functions at the tools level for convenience
from .macos import get_tools, handle_tool_call

__all__ = ["macos", "get_tools", "handle_tool_call"]