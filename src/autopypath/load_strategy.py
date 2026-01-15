"""Load strategy definitions for autopypath."""

from enum import Enum
from types import MappingProxyType

from ._doc_utils import enum_docstrings
from ._typing import Literal, TypeAlias, Final, TypeGuard

__all__ = ['LoadStrategy']


@enum_docstrings
class LoadStrategy(str, Enum):
    """Defines the strategy for loading :func:`sys.path` from multiple sources.

    - MERGE: Combine paths from all sources in priority order.

        Default priority order is:
            1. `manual_paths` (highest priority)
            2. `pyproject.toml` in repository root
            3. `.env` file in repository root
            4. Shell environment (`:func:`sys.path`` environment variable, lowest priority)

    - OVERRIDE: Use only the paths from the highest priority source.
    - REPLACE: Replace `sys.path` entirely with the merged :func:`sys.path` sources.
               This may break standard library and installed package imports.

    Example
    -------
    .. code-block:: python
        from autopypath.load_strategy import LoadStrategy

        strategy = LoadStrategy.MERGE
    """

    MERGE = 'merge'
    """Use paths from all sources, combining them in priority order."""
    USE_HIGHEST_PRIORITY = 'override'
    """Use paths from the highest priority source only."""
    REPLACE = 'replace'
    """Replace sys.path entirely with the merged paths from all sources."""


LoadStrategyLiteral: TypeAlias = Literal['merge', 'override', 'replace']
"""Literal type for LoadStrategy values."""


LOAD_STRATEGY_MAP: Final[MappingProxyType[LoadStrategyLiteral, LoadStrategy]] = MappingProxyType(
    {strategy.value: strategy for strategy in LoadStrategy}
)
"""Mapping from literal strings to LoadStrategy enum members.

Example
-------

.. code-block:: python

    from autopypath.load_strategy import LOAD_STRATEGY_MAP, LoadStrategy

    strategy = LOAD_STRATEGY_MAP['merge']
    assert strategy == LoadStrategy.MERGE
"""


def is_load_strategy_literal(value: str) -> TypeGuard[LoadStrategyLiteral]:
    """Checks if the given string is a valid LoadStrategy literal.

    Example
    -------

    .. code-block:: python
        from autopypath.load_strategy import is_load_strategy_literal

        assert is_load_strategy_literal('merge') is True
        assert is_load_strategy_literal('override') is True
        assert is_load_strategy_literal('replace') is True
        assert is_load_strategy_literal('invalid') is False

    :param str value: The string to check.
    :return bool: ``True`` if the string is a valid ``LoadStrategy`` literal, ``False`` otherwise.
    """
    return value in LOAD_STRATEGY_MAP


def resolve_load_strategy_literal(value: str) -> LoadStrategy | None:
    """Resolves a string literal to its corresponding :class:`LoadStrategy` enum member
    or returns ``None`` if the literal is invalid.

    Example
    -------

    .. code-block:: python
        from autopypath.path_resolution_order import resolve_load_strategy_literal, LoadStrategy

        assert resolve_load_strategy_literal('merge') == LoadStrategy.MERGE
        assert resolve_load_strategy_literal('override') == LoadStrategy.OVERR IDE
        assert resolve_load_strategy_literal('replace') == LoadStrategy.REPLACE
        assert resolve_load_strategy_literal('invalid') is None

    :param str value: The string literal to resolve.
    :return LoadStrategy | None: The corresponding LoadStrategy enum member,
                               or ``None`` if the literal is invalid.
    """
    if is_load_strategy_literal(value):
        return LOAD_STRATEGY_MAP.get(value)
    return None
