"""Load strategy definitions for autopypath."""

from enum import Enum
from types import MappingProxyType
from typing import Union

from ._doc_utils import enum_docstrings
from ._typing import Final, Literal, TypeAlias, TypeGuard

__all__ = ['LoadStrategy']


@enum_docstrings
class LoadStrategy(str, Enum):
    """Defines the strategy for loading :func:`sys.path` from multiple sources.

    - PREPEND: Combine paths from all sources in priority order and prepend them to :func:`sys.path`.

        Default priority order is:
            1. `manual_paths` (highest priority)
            2. `autopypath.toml`
            2. `pyproject.toml` in repository root
            3. `.env` file in repository root

    - PREPEND_HIGHEST_PRIORITY: Use only the paths from the highest priority source
        and prepend them to :func:`sys.path`.

    - REPLACE: Replace `sys.path` entirely with the merged :func:`sys.path` sources.
        .. warning:: This may break standard library and installed package imports

            Not recommended unless you understand the implications. This strategy
            is generally discouraged: It can lead to missing standard library modules
            and installed packages, causing runtime errors.

            This is only suitable for very advanced use cases where you have
            full control over the environment. In short, *'if you don't know exactly
            why you need this, you probably shouldn't use it.'*

    Example
    -------
    .. code-block:: python
        from autopypath.load_strategy import LoadStrategy

        strategy = LoadStrategy.PREPEND
    """

    PREPEND = 'prepend'
    """Use paths from all sources, merging and prepending them in priority order."""
    PREPEND_HIGHEST_PRIORITY = 'prepend_highest_priority'
    """Use paths from the highest priority source only."""
    REPLACE = 'replace'
    """Replace sys.path entirely with the merged paths from all sources."""


LoadStrategyLiteral: TypeAlias = Literal['prepend', 'prepend_highest_priority', 'replace']
"""Literal type for LoadStrategy values."""


LOAD_STRATEGY_MAP: Final[MappingProxyType[LoadStrategyLiteral, LoadStrategy]] = MappingProxyType(
    {strategy.value: strategy for strategy in LoadStrategy}
)
"""Mapping from literal strings to LoadStrategy enum members.

Example
-------

.. code-block:: python

    from autopypath.load_strategy import LOAD_STRATEGY_MAP, LoadStrategy

    strategy = LOAD_STRATEGY_MAP['prepend']
    assert strategy == LoadStrategy.MERGE
"""


def is_load_strategy_literal(value: str) -> TypeGuard[LoadStrategyLiteral]:
    """Checks if the given string is a valid LoadStrategy literal.

    Example
    -------

    .. code-block:: python
        from autopypath.load_strategy import is_load_strategy_literal

        assert is_load_strategy_literal('prepend') is True
        assert is_load_strategy_literal('override') is True
        assert is_load_strategy_literal('replace') is True
        assert is_load_strategy_literal('invalid') is False

    :param str value: The string to check.
    :return bool: ``True`` if the string is a valid ``LoadStrategy`` literal, ``False`` otherwise.
    """
    return value in LOAD_STRATEGY_MAP


def resolve_load_strategy_literal(value: str) -> Union[LoadStrategy, None]:
    """Resolves a string literal to its corresponding :class:`LoadStrategy` enum member
    or returns ``None`` if the literal is invalid.

    Example
    -------

    .. code-block:: python
        from autopypath.path_resolution_order import resolve_load_strategy_literal, LoadStrategy

        assert resolve_load_strategy_literal('prepend') == LoadStrategy.MERGE
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
