"""Custom autopypath configurations.

This module provides functionality to configure :var:`sys.path`
using custom repository markers, paths, load strategies, and resolution orders.
"""
# ruff: noqa: E501

import inspect

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Union, Optional

from .._config_py_path import ConfigPyPath
from .._log import log
from ..types import RepoMarkerLiterals, LoadStrategyLiterals, PathResolutionLiterals


_context_file: Optional[Path] = None
"""This is the file path of the script that imported this module, if available."""

_current_frame = inspect.currentframe()
if _current_frame is not None:
    _parent_frame = _current_frame.f_back
    if _parent_frame and _parent_frame.f_globals.get('__name__') == '__main__':
        _context_file = Path(_parent_frame.f_globals.get('__file__', ''))


def configure_pypath(
    *,
    repo_markers: Optional[Mapping[str, RepoMarkerLiterals]] = None,
    paths: Optional[Sequence[Union[Path, str]]] = None,
    posix_paths: Optional[Sequence[Union[Path, str]]] = None,
    windows_paths: Optional[Sequence[Union[Path, str]]] = None,
    load_strategy: Optional[LoadStrategyLiterals] = None,
    path_resolution_order: Optional[Sequence[PathResolutionLiterals]] = None,
) -> None:
    """Configures the PYTHONPATH according to the provided parameters.

    Configures the :var:`sys.path` according to the provided parameters.

    This function allows customization of how the :var:`sys.path` is set up,
    including repository markers, additional paths, load strategy, and resolution order.

    :param Mapping[str, Literal['dir', 'file']] | None repo_markers: A mapping of file or directory names to their MarkerType
                        used to identify the repository root.
    :param Sequence[Path | str] | None paths: A sequence of paths to include in the :var:`sys.path`.
    :param Sequence[Path | str] | None posix_paths: A sequence of POSIX-specific paths to include in
                        the :var:`sys.path`.
    :param Sequence[Path | str] | None windows_paths: A sequence of Windows-specific paths to include in
                        the :var:`sys.path`.
    :param Literal['prepend', 'prepend_highest_priority', 'replace'] | None load_strategy: The strategy for loading :var:`sys.path` entries.
    :param Sequence[Literal['manual', 'autopypath', 'pyproject', 'dotenv']] | None path_resolution_order: The order in which to
                        resolve :var:`sys.path` sources.
    """
    if _context_file is None:
        log.warning('could not determine context file; no sys.path changes will be applied.')
    else:
        ConfigPyPath(
            context_file=_context_file,
            repo_markers=repo_markers,
            paths=paths,
            posix_paths=posix_paths,
            windows_paths=windows_paths,
            load_strategy=load_strategy,
            path_resolution_order=path_resolution_order,
        )
        log.debug('sys.path adjusted automatically for %s', _context_file)
