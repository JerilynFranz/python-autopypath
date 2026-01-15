"""Validators for configuration parameters.

Use by importing the module and calling the desired validation function.

The validation functions raise `TypeError` or `ValueError` if the input
is invalid.

They return the validated and possibly transformed value if valid."""

from collections.abc import Mapping, Sequence
from pathlib import Path
from posixpath import sep as posix_sep
from ntpath import sep as nt_sep
from os import sep as path_sep
from types import MappingProxyType
from typing import Any, Union

__all__ = []

from .marker_type import MarkerType, resolve_marker_type_literal
from .load_strategy import LoadStrategy, resolve_load_strategy_literal
from .path_resolution import PathResolution, resolve_path_resolution_literal

_MAX_FILE_DIR_NAME_LENGTH: int = 64
"""Maximum length for file or directory names.

Deliberately set to 64 to allow for future flexibility and
avoid issues with filesystems that may have lower limits.
"""


def root_repo_path(value: Any) -> Path:
    """Validates the repository root path.

    :param Any value: The repository root path to validate.
    :return Path: A validated Path object representing the repository root.
    :raises TypeError: If the input is not a Path or string.
    """
    repo_path = validate_path_or_str(value)
    if not repo_path.exists() or not repo_path.is_dir():
        raise ValueError(f'Repository root path does not exist or is not a directory: {repo_path}')
    return repo_path


def context_file(value: Any) -> Path:
    """Validates the context file path.

    :param Any value: The context file path to validate.
    :return Path: A validated Path object representing the context file.
    :raises TypeError: If the input is not a Path or string.
    :raises ValueError: If the file does not exist or is not a file.
    :raises ValueError: If the path is invalid.
    """
    context_file_path = validate_path_or_str(value)
    if not context_file_path.exists() or not context_file_path.is_file():
        raise ValueError(f'Context file does not exist or is not a file: {context_file_path}')
    return context_file_path


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
        if isinstance(val, str):
            resolved_val = resolve_marker_type_literal(val)
            if resolved_val is None:
                raise ValueError(f'Invalid MarkerType: {val} is not a valid MarkerType')
            val = resolved_val
        if not isinstance(val, MarkerType):
            raise TypeError(f'Invalid repo_markers value: expected MarkerType or string, got {type(val)}')
        if not isinstance(key, str):
            raise TypeError(f'Invalid repo_markers key: expected str, got {type(key)}')
        validate_file_or_dir_name(key)
        validated_markers[key] = val

    if len(validated_markers) == 0:
        return None

    return MappingProxyType(validated_markers)


def paths(value: Any) -> Union[tuple[Path, ...], None]:
    """Validates a sequence of Path objects or strings.

    If the input is None, returns None. If the input is a sequence, each item is validated
    to be either a Path or a string (which is converted to a Path).

    If the sequence is empty, returns ``None``

    :param Any value: A sequence of Path objects or strings.
    :return tuple[Path, ...] | None: A validated tuple of :class:`Path` objects or None if the input is None.
    :raises TypeError: If the input is not a sequence or contains non-Path or non-str items
    """
    if value is None:
        return None

    if not isinstance(value, Sequence):
        raise TypeError(f'Invalid paths: expected a sequence, got {type(value)}')

    if len(value) == 0:
        return None

    validated_paths: list[Path] = []
    for item in value:
        validated_paths.append(validate_path_or_str(item))
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

    if isinstance(value, str):
        resolved_value = resolve_load_strategy_literal(value)
        if resolved_value is None:
            raise ValueError(f'Invalid LoadStrategy: {value} is not a valid LoadStrategy: {list(LoadStrategy)}')
        value = resolved_value

    if not isinstance(value, LoadStrategy):
        raise TypeError(f'Invalid load_strategy: expected LoadStrategy, got {type(value)}')
    return value


def path_resolution_order(value: Any) -> Union[tuple[PathResolution, ...], None]:
    """Validates a sequence of PathResolution values.

    :param Any value: A sequence of PathResolution values or strings matching PathResolution values.
    :return tuple[PathResolution, ...] | None: A validated sequence of PathResolution values or None
        if the input is None or empty.
    :raises TypeError: If the input is not a sequence or contains non-PathResolution items
    :raises ValueError: If there are duplicate PathResolution values
    """
    if value is None:
        return None

    if isinstance(value, (str, bytes)):
        raise TypeError(f'Invalid path_resolution_order: expected a sequence, got {type(value)}')

    if not isinstance(value, Sequence):
        raise TypeError(f'Invalid path_resolution_order: expected a sequence, got {type(value)}')

    if len(value) == 0:
        return None

    validated_orders: list[PathResolution] = []
    seen_orders: dict[PathResolution, int] = {}
    for item in value:
        if isinstance(item, str):
            resolved_item = resolve_path_resolution_literal(item)
            if resolved_item is None:
                raise ValueError(
                    f'Invalid PathResolution: {item} is not a valid PathResolution: {list(PathResolution)}'
                )
            item = resolved_item
        if not isinstance(item, PathResolution):
            raise TypeError(f'Invalid path_resolution_order item: expected PathResolution, got {item}')
        validated_orders.append(item)
        seen_orders[item] = seen_orders.get(item, 0) + 1
    if len(seen_orders) != len(validated_orders):
        duplicates = set(order for order in validated_orders if seen_orders[order] > 1)
        raise ValueError(f'Duplicate PathResolution values are not allowed: Duplicated {duplicates}')

    return tuple(validated_orders)


def validate_path_or_str(path: Union[Path, str]) -> Path:
    """Validate a Path object or a string path.

    - Cannot contain null bytes.
    - Cannot be empty or whitespace only.
    - Cannot have leading or trailing whitespace.
    - Cannot be only backslashes or only forward slashes.
    - Each segment cannot be an invalid file or directory name.

    :param Path | str path: The Path object or string path to validate.
    :raises ValueError: If the path is invalid.
    :raises TypeError: If the input is not a Path or string.
    :return Path: The validated Path object.
    """
    if not isinstance(path, (Path, str)):
        raise TypeError(f'Invalid path: expected Path or str, got {type(path)}')
    item_str: str = str(path) if isinstance(path, Path) else path
    if '\000' in item_str:
        raise ValueError('Invalid path item: path cannot contain null byte')
    if item_str.strip() == '':
        raise ValueError('Invalid path item: path cannot be empty or only whitespace')
    if item_str.lstrip() != item_str:
        raise ValueError('Invalid path item: path cannot have leading whitespace ')
    if item_str.rstrip() != item_str:
        raise ValueError('Invalid path item: path cannot have trailing whitespace')
    if item_str.replace('\\', '') == '':
        raise ValueError('Invalid path item: path cannot be only backslashes')
    if item_str.replace('/', '') == '':
        raise ValueError('Invalid path item: path cannot be only forward slashes')
    validated_path = Path(item_str) if isinstance(path, str) else path
    for segment in validated_path.parts:
        validate_file_or_dir_name(segment)
    return validated_path


def validate_file_or_dir_name(name: str) -> None:
    """Check if a given name is forbidden as a file or directory name.

    - Cannot be empty or whitespace only.
    - Cannot have leading or trailing whitespace.
    - Cannot contain path separators.
    - Cannot contain forbidden characters for file/directory names
      (e.g., `<`, `>`, `:`, `"`, `/`, `\\`, `|`, `?`, `*` on Windows
      and `/` on POSIX systems). Characters forbidden on either system are
      always forbidden.
    - Cannot be a reserved name for Windows.
    - Cannot exceed 64 characters in length.

    :param str name: The file or directory name to validate.
    :raises ValueError: If the name is invalid.

    """
    if name.strip() == '':
        raise ValueError('Invalid file/dir name: cannot be empty or whitespace')
    if name.lstrip() != name:
        raise ValueError('Invalid file/dir name: cannot have leading whitespace ')
    if name.rstrip() != name:
        raise ValueError('Invalid file/dir name: cannot have trailing whitespace')
    if posix_sep in name or nt_sep in name or path_sep in name:
        raise ValueError('Invalid file/dir name: cannot contain path separators')
    if has_forbidden_chars(name) or is_windows_reserved(name):
        raise ValueError(f'Invalid file/dir name: {name} is not allowed')
    if len(name) > _MAX_FILE_DIR_NAME_LENGTH:
        message = f'Invalid file/dir name: {name} exceeds maximum length of {_MAX_FILE_DIR_NAME_LENGTH} characters'
        raise ValueError(message)


def has_forbidden_chars(name: str) -> bool:
    forbidden = set('<>:"/\\|?*\0')  # Common forbidden characters on Windows and POSIX
    return any(c in name for c in forbidden)


def is_windows_reserved(name: str) -> bool:
    reserved = {
        'CON',
        'PRN',
        'AUX',
        'NUL',
        *(f'COM{i}' for i in range(1, 10)),
        *(f'LPT{i}' for i in range(1, 10)),
    }
    # Windows ignores case and extension for reserved names
    base = name.split('.')[0].upper()
    return base in reserved
