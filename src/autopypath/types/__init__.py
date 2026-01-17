"""Public types for autopypath.

This module exposes special types used by autopypath, such as :class:`NoPath`.
"""

# ruff: noqa F401
from typing import TypeAlias, Literal

from ._no_path import NoPath

RepoMarkerLiterals: TypeAlias = Literal['dir', 'file']
"""Type alias for repository marker literals."""

LoadStrategyLiterals: TypeAlias = Literal['prepend', 'prepend_highest_priority', 'replace']
"""Type alias for load strategy literals."""

PathResolutionLiterals: TypeAlias = Literal['manual', 'autopypath', 'pyproject', 'dotenv']
"""Type alias for path resolution order literals."""

__all__ = []
