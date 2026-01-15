"""Special types used in AutoPyPath.

This module provides compatibility imports for typing features
across different Python versions.

The types provided here include:
- :class:`Literal`
- :class:`Final`
- :class:`TypeAlias`
- :class:`TypeGuard`

"""
# ruff: noqa: F401

__all__ = []

# Compatibility imports for typing features
# This is a 'feature detection' pattern to support multiple Python versions
# without having to know exactly which versions support which features.
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

try:
    from typing import Final
except ImportError:
    from typing_extensions import Final

try:
    from typing import TypeAlias
except ImportError:
    from typing_extensions import TypeAlias

try:
    from typing import TypeGuard
except ImportError:
    from typing_extensions import TypeGuard
