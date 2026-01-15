"""Config from pyproject.toml for autopypath."""

import datetime
from pathlib import Path
from types import MappingProxyType
from typing import Union, Any

import tomli

from ._config import Config
from ...load_strategy import LoadStrategy
from ...marker_type import MarkerType
from ... import _validate
from ..._log import log

__all__ = ['PyProjectConfig']


_TOML_TYPES: dict[type, str] = {
    dict: 'table',
    list: 'array',
    str: 'string',
    int: 'int',
    float: 'float',
    bool: 'boolean',
    datetime.date: 'date',
    datetime.datetime: 'datetime',
    datetime.time: 'time',
}
"""Mapping of Python types to TOML types for error messages."""


class PyProjectConfig(Config):
    """Configuration for autopypath using pyproject.toml files."""

    __slots__ = ('_repo_root_path',)

    def __init__(self, repo_root_path: Path) -> None:
        """Configuration for autopypath using pyproject.toml files.

        :param Path repo_root_path: The root path of the repository containing pyproject.toml.
            resolve :func:`sys.path` sources. Specified as a sequence of :class:`PathResolution` enums.
        :raises TypeError: If any configuration value is of an invalid type (ex. string instead of table).
        :raises ValueError: If any configuration value is invalid.
        """
        self._repo_root_path = _validate.root_repo_path(repo_root_path)

        # pyproject.toml data
        pyproject_data = self._pyproject_data()
        if not pyproject_data:
            super().__init__(repo_markers=None, paths=None, load_strategy=None, path_resolution_order=None)
            return

        # [tool.autopypath]
        autopypath_config = self._pyproject_autopypath(pyproject_data)
        if not autopypath_config:
            super().__init__(repo_markers=None, paths=None, load_strategy=None, path_resolution_order=None)
            return

        # example: repo_markers = { '.git' = 'dir', 'setup.py' = 'file' }
        repo_markers = self._pyproject_repo_markers(autopypath_config)

        # example: paths = ['src', 'tests']
        paths = self._pyproject_paths(autopypath_config)

        # example: load_strategy = 'merge'
        load_strategy = self._pyproject_load_strategy(autopypath_config)

        # example: path_resolution_order = ['manual', 'pyproject', 'dotenv']
        path_resolution_order = self._pyproject_path_resolution_order(autopypath_config)

        super().__init__(
            repo_markers=repo_markers,
            paths=paths,
            load_strategy=load_strategy,
            path_resolution_order=path_resolution_order,
        )

    def _pyproject_data(self) -> dict[str, Any]:
        """Loads and returns the pyproject.toml data as a dictionary.

        :return dict[str, Any]: The parsed pyproject.toml data or an empty dictionary if the file does not exist.
        """
        pyproject_path = self._repo_root_path / 'pyproject.toml'
        if not pyproject_path.exists() or not pyproject_path.is_file():
            log.debug(f'No pyproject.toml file found at {pyproject_path}.')
            return {}

        with pyproject_path.open('rb') as f:
            pyproject_data = tomli.load(f)
        return pyproject_data

    def _pyproject_autopypath(self, pyproject_data: dict[str, Any]) -> dict[str, Any]:
        """Returns the [tool.autopypath] section from pyproject.toml
        if it exists, otherwise returns an empty dictionary.


        Example
        -------
        .. code-block:: toml
            [tool.autopypath]
            repo_markers = { '.git' = 'dir', 'setup.py' = 'file' }
            paths = ['src', 'tests']
            path_resolution_order = ['manual', 'pyproject', 'dotenv']

        :param dict[str, Any] pyproject_data: The parsed pyproject.toml data.
        :return dict[str, Any]: The autopypath configuration section.
        :raises TypeError: If the configuration for [tool.autopypath] is invalid.
        """
        autopypath_config = pyproject_data.get('tool', {}).get('autopypath', {})
        if not isinstance(autopypath_config, dict):
            toml_type = _TOML_TYPES.get(type(autopypath_config), 'unknown')
            raise TypeError(
                'Invalid [tool.autopypath] section in pyproject.toml: expected table, '
                f'got {toml_type}: {autopypath_config}'
            )
        if not autopypath_config:
            log.debug('No [tool.autopypath] configuration section found in pyproject.toml.')
            return {}

        return autopypath_config

    def _pyproject_repo_markers(self, autopypath_config: dict) -> Union[MappingProxyType[str, MarkerType], None]:
        """Collects repository markers from the [tool.autopypath] section of pyproject.toml.

        Example
        -------
        .. code-block:: toml
            [tool.autopypath]
            repo_markers = { 'custom_marker.txt' = 'file', '.git' = 'dir' }

        :param autopypath_config: The autopypath configuration section from pyproject.toml.
        :return MappingProxyType[str, MarkerType] | None: A mapping of repository markers or ``None``.
        :raises TypeError: If the configuration is invalid.
        :raises ValueError: If any marker type is invalid (not 'file' or 'dir').
        """
        raw_repo_markers = autopypath_config.get('repo_markers', None)
        if not isinstance(raw_repo_markers, (type(None), dict)):
            toml_type = _TOML_TYPES.get(type(raw_repo_markers), 'unknown')
            raise TypeError(
                f'Invalid repo_markers in pyproject.toml: expected table, got {toml_type}: {raw_repo_markers}'
            )
        collected_repo_markers: dict[str, MarkerType] = {}
        if raw_repo_markers is not None:
            for key, value in raw_repo_markers.items():
                if not isinstance(value, str):
                    toml_type = _TOML_TYPES.get(type(raw_repo_markers), 'unknown')
                    raise TypeError(f'Invalid repo_marker value for {key}: expected string, got {toml_type}: {value}')
                try:
                    collected_repo_markers[key] = MarkerType(value)
                except ValueError as e:
                    raise ValueError(f'Invalid repo_marker type value for {key}: {value}') from e
        repo_markers = _validate.repo_markers(collected_repo_markers)
        return repo_markers

    def _pyproject_paths(self, autopypath_config: dict[str, Any]) -> Union[tuple[Path, ...], None]:
        """Collects paths from pyproject.toml.

        Example
        -------
        .. code-block:: toml
            [tool.autopypath]
            paths = ['src', 'tests']

        :param autopypath_config: The autopypath configuration section from pyproject.toml.
        :return tuple[Path, ...] | None: A tuple of paths or ``None``.
        :raises TypeError: If the configuration is invalid.
        """
        # example: paths = ['src', 'tests']
        raw_paths = autopypath_config.get('paths', None)
        if not isinstance(raw_paths, (type(None), list)):
            toml_type = _TOML_TYPES.get(type(raw_paths), 'unknown')
            raise TypeError(f'Invalid paths in pyproject.toml: expected array, got {toml_type}: {raw_paths}')
        requested_paths = _validate.paths(raw_paths)
        filtered_paths: list[Path] = []
        if requested_paths is not None:
            for p in requested_paths:
                target_path = self._repo_root_path / p
                if not target_path.exists():
                    log.warning(
                        f'Path specified in pyproject.toml configuration does not exist: {target_path} - skipping.'
                    )
                else:
                    filtered_paths.append(target_path)
        paths = tuple(filtered_paths) if filtered_paths else None
        return paths

    def _pyproject_load_strategy(self, autopypath_config: dict[str, Any]) -> Union[LoadStrategy, None]:
        """Collects load strategy from pyproject.toml.

        Example
        -------
        .. code-block:: toml
            [tool.autopypath]
            load_strategy = 'append'

        :param autopypath_config: The autopypath configuration section from pyproject.toml.
        :return LoadStrategy | None: The load strategy or ``None``.
        :raises TypeError: If the configuration is invalid.
        """
        raw_load_strategy = autopypath_config.get('load_strategy', None)
        if not isinstance(raw_load_strategy, (type(None), str)):
            toml_type = _TOML_TYPES.get(type(raw_load_strategy), 'unknown')
            raise TypeError(
                f'Invalid load_strategy in pyproject.toml: expected string, got {toml_type}: {raw_load_strategy}'
            )
        if raw_load_strategy is None:
            return None
        try:
            load_strategy = LoadStrategy(raw_load_strategy)
        except ValueError as e:
            raise ValueError(f'Invalid load_strategy: {raw_load_strategy}') from e

        return load_strategy

    def _pyproject_path_resolution_order(self, autopypath_config: dict[str, Any]) -> Union[tuple[str, ...], None]:
        """Collects path resolution order from pyproject.toml.

        Example
        -------
        .. code-block:: toml
            [tool.autopypath]
            path_resolution_order = ['manual', 'pyproject', 'dotenv']

        :param autopypath_config: The autopypath configuration section from pyproject.toml.
        :return tuple[str, ...] | None: The path resolution order or ``None``.
        :raises TypeError: If the configuration is invalid.
        """
        raw_order = autopypath_config.get('path_resolution_order', None)
        if not isinstance(raw_order, (type(None), list)):
            toml_type = _TOML_TYPES.get(type(raw_order), 'unknown')
            raise TypeError(
                f'Invalid path_resolution_order in pyproject.toml: expected array, got {toml_type}: {raw_order}'
            )
        path_resolution_order = _validate.path_resolution_order(raw_order)
        return path_resolution_order

    def __repr__(self) -> str:
        """String representation of the PyprojectConfig object.

        :return str: A string representation of the PyprojectConfig instance.
        """
        return (
            f'{self.__class__.__name__}(repo_root_path={self._repo_root_path!r})\n'
            f'#  repo_markers={self.repo_markers!r}\n'
            f'#  paths={self.paths!r}\n'
            f'#  load_strategy={self.load_strategy!r}\n'
            f'#  path_resolution_order={self.path_resolution_order!r}'
        )

    def __str__(self) -> str:
        """String representation of the PyProjectConfig instance."""
        return (
            f'{self.__class__.__name__}:\n'
            f'  repo_markers={self.repo_markers!r}\n'
            f'  paths={self.paths!r}\n'
            f'  load_strategy={self.load_strategy!r}\n'
            f'  path_resolution_order={self.path_resolution_order!r}'
        )
