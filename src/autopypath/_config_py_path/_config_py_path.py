""" "Module to configure Python path"""

from collections.abc import Mapping, Sequence
from pathlib import Path
import sys
from typing import Union, Optional

from .. import _validate
from .._log import log
from ..marker_type import MarkerType
from ..path_resolution import PathResolution
from ..load_strategy import LoadStrategy
from ._config import DefaultConfig, ManualConfig, PyProjectConfig, DotEnvConfig
from ._conf_source import ConfSource

__all__ = []


class ConfigPyPath:
    """Configures :var:`sys.path` based on manual settings, pyproject.toml, and .env files."""

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

        self._load_strategy: LoadStrategy = self._determine_load_strategy()
        """The strategy for handling multiple :var:`sys.path` sources."""

        self._paths: tuple[Path, ...] = self._determine_paths()
        """The final resolved paths to be added to :var:`sys.path`."""

    def _determine_paths(self) -> tuple[Path, ...]:
        """Determines the final resolved paths to be added to :var:`sys.path`.

        It follows the configured path resolution order and load strategy to
        combine paths from manual settings, pyproject.toml, and .env files.

        Paths that are already in :var:`sys.path` are not duplicated.

        :return tuple[Path, ...]: The final resolved paths to be added to :var:`sys.path`.
        """

        existing_paths = sys.path
        known_paths: set[Path] = set()
        for p in existing_paths:
            try:
                path_obj = Path(p).resolve()
                if path_obj not in known_paths:
                    known_paths.add(path_obj)
            except Exception:
                log.warning('Could not resolve existing sys.path entry: %s', p)

        raw_paths: list[Path] = []
        for source in self._path_resolution_order:
            match source:
                case PathResolution.MANUAL:
                    source_paths = self._manual.paths
                    log.debug('Resolving paths from MANUAL source: %s', source_paths)
                case PathResolution.PYPROJECT:
                    source_paths = self._pyproject.paths
                    log.debug('Resolving paths from PYPROJECT source: %s', source_paths)
                case PathResolution.DOTENV:
                    source_paths = self._dotenv.paths
                    log.debug('Resolving paths from DOTENV source: %s', source_paths)
                case _:
                    log.warning('Unknown path resolution source: %s', source)
                    continue

            if not source_paths:
                continue

            match self._load_strategy:
                case LoadStrategy.REPLACE:
                    raw_paths.extend(source_paths)
                    log.debug('Load strategy REPLACE: Appending paths %s from %s', source_paths, source)
                    break
                case LoadStrategy.USE_HIGHEST_PRIORITY:
                    log.debug('Load strategy USE_HIGHEST_PRIORITY: Using paths %s from %s', source_paths, source)
                    raw_paths = list(source_paths)
                    break
                case LoadStrategy.MERGE:
                    log.debug('Load strategy MERGE: Appending paths %s from %s', source_paths, source)
                    raw_paths.extend(source_paths)
                case _:  # pragma: no cover  # should never happen due to earlier validation
                    raise ValueError(f'Unknown load strategy: {self._load_strategy}')

            # Remove duplicates while preserving order
            unique_paths: list[Path] = []
            for path in raw_paths:
                resolved_path = path.resolve()
                if resolved_path not in known_paths:
                    unique_paths.append(resolved_path)
                    known_paths.add(resolved_path)

            match self._load_strategy:
                case LoadStrategy.REPLACE:
                    sys.path = [str(p) for p in unique_paths]
                    log.debug('sys.path replaced with: %s', sys.path)
                case LoadStrategy.USE_HIGHEST_PRIORITY:
                    sys.path = [str(p) for p in unique_paths] + sys.path
                    log.debug('sys.path updated with highest priority paths: %s', sys.path)
                case LoadStrategy.MERGE:
                    sys.path = [str(p) for p in unique_paths] + sys.path
                    log.debug('sys.path updated with merged paths: %s', sys.path)

        # Process default paths if no paths have been set yet
        if not raw_paths:
            default_paths = self._default.paths
            log.debug('Processing default paths: %s', default_paths)
            for path in default_paths:
                raw_paths.append(path)

        return tuple(raw_paths)

    def _determine_load_strategy(self) -> LoadStrategy:
        """Determines the load strategy for handling multiple :var:`sys.path` sources.

        It looks for the strategy in the following precedence:
        1. Manual configuration provided directly to the function.
        2. Configuration loaded from pyproject.toml.
        3. Default autopypath configuration.

        The first source that provides a non-None strategy is used.

        :return LoadStrategy: The strategy for handling multiple :var:`sys.path` sources.
        """
        if self._manual.load_strategy is not None:
            strategy = LoadStrategy(self._manual.load_strategy)
            log.debug('Using manual load strategy: %s', strategy)
            return strategy
        if self._pyproject.load_strategy is not None:
            strategy = LoadStrategy(self._pyproject.load_strategy)
            log.debug('Using pyproject.toml load strategy: %s', strategy)
            return strategy
        log.debug('Using default load strategy: %s', self._default.load_strategy)
        return self._default.load_strategy

    def _determine_path_resolution_order(self) -> tuple[PathResolution, ...]:
        """Determines the order in which to resolve :var:`sys.path` sources.

        It looks for the order in the following precedence:
        1. Manual configuration provided directly to the function.
        2. Configuration loaded from pyproject.toml.
        3. Default autopypath configuration.

        The first source that provides a non-None order is used.

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
