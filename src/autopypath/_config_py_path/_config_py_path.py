""" "Module to configure Python path"""

from collections.abc import Mapping, Sequence
import os
from pathlib import Path
from posixpath import sep as posix_sep
from ntpath import sep as nt_sep
import sys
from typing import Union, Optional

from dotenv import load_dotenv

from .. import _validate
from .._log import log
from ..marker_type import MarkerType
from ..path_resolution import PathResolution
from ..load_strategy import LoadStrategy
from ._config import DefaultConfig, ManualConfig, PyProjectConfig, DotEnvConfig, Config
from ._conf_source import ConfSource

__all__ = []


class ConfigPyPath:
    """Configures :var:`sys.path` based on manual settings, .env files, and pyproject.toml."""

    def __init__(
        self,
        *,
        context_file: Path,
        repo_markers: Optional[Mapping[str, MarkerType]] = None,
        paths: Optional[Sequence[Union[Path, str]]] = None,
        posix_paths: Union[Sequence[Union[Path, str]], None] = None,
        windows_paths: Union[Sequence[Union[Path, str]], None] = None,
        load_strategy: Union[LoadStrategy, str, None] = None,
        path_resolution_order: Optional[Sequence[Union[PathResolution, str]]] = None,
    ) -> None:
        """Configures :var:`sys.path` based on manual settings, .env files, and pyproject.toml.

        Usage
        -----
        This is the internal function used by autopypath to set up the Python path.

        It is typically called automatically when the module is imported,
        but can also be called manually to customize behavior.

        It is very liberal in what it accepts, but will raise `TypeError` or
        `ValueError` if the inputs are invalid.

        :param Path context_file: The file path of the script that is configuring the Python path.
        :param Mapping[str, MarkerType] | None repo_markers: A dictionary where keys are
            filenames or directory names that indicate the repository root.
            The values should be `file` or `dir`.

            If ``None``, defaults to :var:`~autopypath.defaults.REPO_MARKERS`.

        :param Sequence[Path | str] | None paths: A list of Path objects or strings relative to
            the repo root to add to :var:`sys.path`.

            If ``None``, defaults to :var:`~autopypath.defaults.PATHS`.

        :param Sequence[Path | str] | None posix_paths: A list of Path objects or strings
            relative to the repo root to add to :var:`sys.path` only on POSIX systems.
            These override the paths in `paths` (only on POSIX systems) if provided.

            If ``None``, the paths in `paths` are used on POSIX systems.

        :param Sequence[Path | str] | None windows_paths: A list of Path objects or strings
            relative to the repo root to add to :var:`sys.path` only on Windows systems.
            These override the paths in `paths` (only on Windows systems) if provided.

            If ``None``, the paths in `paths` are used on Windows systems.

        :param LoadStrategy | str | None load_strategy: The strategy for handling multiple :var:`sys.path` sources.

            It is expected to be `merge`, `override`, or `replace` (as defined in :class:`LoadStrategy`).
            It can use either the enum value or its string representation.

            If ``None``, defaults to :var:`~autopypath.defaults.LOAD_STRATEGY`.

        :param PathResolution | str | None path_resolution_order: The order in which to resolve :var:`sys.path` sources.

            It is expected to be a sequence containing any of the following values:
            ``manual``, ``pyproject``, ``dotenv`` as defined in :class:`PathResolution`.
            If ``None``, the default order from :var:`~autopypath.defaults.PATH_RESOLUTION_ORDER` is used.

            It can use either the enum values or their string representations.
        """
        self._context_file: Path = _validate.context_file(context_file)
        """The file path of the script that is configuring the Python path."""

        self._repo_root_path: Path = self._find_repo_root_path()
        """The repository root path based on the configured repo markers."""

        self._manual = ManualConfig(
            repo_markers=repo_markers,
            paths=paths,
            load_strategy=load_strategy,
            path_resolution_order=path_resolution_order,
        )
        """Manual configuration provided directly to the function."""

        self._pyproject = PyProjectConfig(self._repo_root_path)
        """Configuration loaded from pyproject.toml."""

        self._dotenv = DotEnvConfig(self._repo_root_path)
        """Configuration loaded from .env file."""

        self._default = DefaultConfig()
        """Default autopypath configuration."""

        self._path_resolution_order: tuple[PathResolution, ...] = self._determine_path_resolution_order()
        """The order in which to resolve :var:`sys.path` sources."""

    def _determine_path_resolution_order(self) -> tuple[PathResolution, ...]:
        """Determines the order in which to resolve :var:`sys.path` sources.

        :return tuple[PathResolution, ...]: The order in which to resolve :var:`sys.path` sources.
        """
        if self._manual.path_resolution_order is not None:
            order = tuple(PathResolution(item) for item in self._manual.path_resolution_order)
            log.debug('Using manual path resolution order: %s', order)
            return order
        if self._pyproject.path_resolution_order is not None:
            order = tuple(PathResolution(item) for item in self._pyproject.path_resolution_order)
            log.debug('Using pyproject.toml path resolution order: %s', order)
            return order
        log.debug('Using default path resolution order: %s', self._default.path_resolution_order)
        return self._default.path_resolution_order

    def _find_repo_root_path(self) -> Path:
        """Finds the repository root path based on the configured repo markers.

        :return Path: The path to the repository root.
        :raises RuntimeError: If the repository root cannot be found.
        """
        repo_markers = self._manual.repo_markers or self._default.repo_markers
        if repo_markers is None:
            raise RuntimeError('No repository markers defined to find the repo root.')

        current_path = Path(__file__).parent.resolve()
        while True:
            for marker, typ in repo_markers.items():
                test_path = current_path / marker
                if typ == MarkerType.FILE and test_path.exists() and test_path.is_file():
                    log.debug('Repository root found at: %s', current_path)
                    return current_path
                elif typ == MarkerType.DIR and test_path.exists() and test_path.is_dir():
                    log.debug('Repository root found at: %s', current_path)
                    return current_path
            if current_path == current_path.parent:
                break
            current_path = current_path.parent
        raise RuntimeError('Repository root could not be found.')
