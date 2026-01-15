"""Validators for configuration parameters.

Use by importing the module and calling the desired validation function.

The validation functions raise `TypeError` or `ValueError` if the input
is invalid.

They return the validated and possibly transformed value if valid."""

from collections.abc import Mapping, Sequence
from pathlib import Path
from types import MappingProxyType
from typing import Any, Union

__all__ = []

from .marker_type import MarkerType
from .load_strategy import LoadStrategy
from .path_resolution import PathResolution


def root_repo_path(value: Any) -> Path:
    """Validates the repository root path.

    :param Any value: The repository root path to validate.
    :return Path: A validated Path object representing the repository root.
    :raises TypeError: If the input is not a Path or string.
    """
    if not isinstance(value, (Path, str)):
        raise TypeError(f'Invalid root_repo_path: expected Path or str, got {type(value)}')
    if isinstance(value, str):
        value = Path(value)
    if not value.exists() or not value.is_dir():
        raise ValueError(f'Repository root path does not exist or is not a directory: {value}')
    return value


def context_file(value: Any) -> Path:
    """Validates the context file path.

    :param Any value: The context file path to validate.
    :return Path: A validated Path object representing the context file.
    :raises TypeError: If the input is not a Path or string.
    """
    if not isinstance(value, (Path, str)):
        raise TypeError(f'Invalid context_file: expected Path or str, got {type(value)}')
    if isinstance(value, str):
        value = Path(value)
    return value


def repo_markers(value: Any) -> Union[MappingProxyType[str, MarkerType], None]:
    """Validates a mapping of repository markers.

    :param Any value: A mapping where keys are filenames or directory names
        that indicate the repository root, and values are of type `MarkerType` or strings.
    :return MappingProxyType[str, MarkerType] | None: A validated immutable mapping of repository markers.
        or None if the input is None.
    :raises TypeError: If the input is not a mapping, keys are not strings,
        or values are not strings.
    :raises ValueError: If any value is not a valid `MarkerType`.
    """
    if value is None:
        return None

    if not isinstance(value, Mapping):
        raise TypeError(f'Invalid repo_markers: expected a mapping, got {type(value)}')
    validated_markers: dict[str, MarkerType] = {}
    for key, val in value.items():
        if not isinstance(key, str):
            raise TypeError(f'Invalid repo_markers key: expected str, got {type(key)}')
        if not isinstance(val, str):
            raise TypeError(f'Invalid repo_markers value: expected str, got {type(val)}')
        try:
            val = MarkerType(val)
        except ValueError as e:
            raise ValueError(f'Invalid MarkerType: {val} is not a valid MarkerType') from e
        validated_markers[key] = val  # type: ignore

    return MappingProxyType(validated_markers)


def paths(value: Any) -> Union[tuple[Path, ...], None]:
    """Validates a sequence of Path objects or strings.

    :param Any value: A sequence of Path objects or strings.
    :return tuple[Path, ...] | None: A validated tuple of :class:`Path` objects or None if the input is None.
    :raises TypeError: If the input is not a sequence or contains non-Path or non-str items
    """
    if value is None:
        return None

    if not isinstance(value, Sequence):
        raise TypeError(f'Invalid paths: expected a sequence, got {type(value)}')

    validated_paths: list[Path] = []
    for item in value:
        if not isinstance(item, (Path, str)):
            raise TypeError(f'Invalid path item: expected Path or str, got {type(item)}')
        if isinstance(item, str):
            item = Path(item)
        validated_paths.append(item)

    return tuple(validated_paths)


def load_strategy(value: Any) -> Union[LoadStrategy, None]:
    """Validates a LoadStrategy value.

    :param Any value: A LoadStrategy value or string matching a LoadStrategy value.
    :return LoadStrategy | None: A validated LoadStrategy value or None if the input is None.
    :raises ValueError: If the input string does not match any LoadStrategy value
    :raises TypeError: If the input is not a LoadStrategy or a string.
    """
    if value is None:
        return None

    load_strategy_indexes: dict[str, LoadStrategy] = {strategy.value: strategy for strategy in LoadStrategy}
    if isinstance(value, str):
        if value not in load_strategy_indexes:
            raise ValueError(
                f'Invalid LoadStrategy: {value} is not a valid LoadStrategy: {list(load_strategy_indexes.keys())}'
            )
        value = load_strategy_indexes[value]
    if not isinstance(value, LoadStrategy):
        raise TypeError(f'Invalid load_strategy: expected LoadStrategy, got {type(value)}')
    return value


def path_resolution_order(value: Any) -> Union[tuple[PathResolution, ...], None]:
    """Validates a sequence of PathResolution values.

    :param Any value: A sequence of PathResolution values or strings matching PathResolution values.
    :return tuple[PathResolution, ...] | None: A validated sequence of PathResolution values or None if the input is None.
    :raises TypeError: If the input is not a sequence or contains non-PathResolution items
    :raises ValueError: If there are duplicate PathResolution values
    """
    if value is None:
        return None

    if isinstance(value, (str, bytes)):
        raise TypeError(f'Invalid path_resolution_order: expected a sequence, got {type(value)}')

    if not isinstance(value, Sequence):
        raise TypeError(f'Invalid path_resolution_order: expected a sequence, got {type(value)}')

    validated_orders: list[PathResolution] = []
    seen_orders: dict[PathResolution, int] = {}
    resolution_indexes: dict[str, PathResolution] = {order.value: order for order in PathResolution}
    for item in value:
        if not isinstance(item, PathResolution) and item not in resolution_indexes:
            raise TypeError(f'Invalid path_resolution_order item: expected PathResolution, got {item}')
        if isinstance(item, str):
            item = resolution_indexes[item]
        validated_orders.append(item)
        seen_orders[item] = seen_orders.get(item, 0) + 1
    if len(seen_orders) != len(validated_orders):
        duplicates = set(order for order in validated_orders if seen_orders[order] > 1)
        raise ValueError(f'Duplicate PathResolution values are not allowed: Duplicated {duplicates}')

    return tuple(validated_orders)
