"""Default config instance for autopypath."""

from pathlib import Path
from types import MappingProxyType

from ... import defaults
from ..._log import log
from ..._load_strategy import LoadStrategy
from ..._path_resolution import PathResolution
from ..._marker_type import MarkerType
from ._config import Config


class DefaultConfig(Config):
    """Default configuration for autopypath."""

    def __init__(self) -> None:
        """Default configuration for autopypath.

        The default configuration uses the default values defined in
        :mod:`autopypath.defaults`. It validates that these defaults are not None
        or empty where applicable and initializes the class with these default values.
        :raises ValueError: If any of the default values are None or empty where not allowed.
        """

        log.debug('Initializing DefaultConfig with default values from autopypath.defaults')

        # Override types for slots because they are guaranteed to be non-None/non-empty
        # from the DefaultConfig module because we double check them above.
        # This let us avoid mypy errors about possible None values when accessing the
        # the default properties.
        self._load_strategy: LoadStrategy  # type: ignore
        self._paths: tuple[Path, ...]  # type: ignore
        self._repo_markers: MappingProxyType[str, MarkerType]  # type: ignore
        self._path_resolution_order: tuple[PathResolution, ...]  # type: ignore

        super().__init__(
            repo_markers=defaults.REPO_MARKERS,
            paths=defaults.PATHS,
            load_strategy=defaults.LOAD_STRATEGY,
            path_resolution_order=defaults.PATH_RESOLUTION_ORDER,
        )

    @property
    def repo_markers(self) -> MappingProxyType[str, MarkerType]:
        """Mapping of repository markers to their MarkerType.

        :return MappingProxyType[str, MarkerType] | None: A mapping where keys are filenames or directory names
            that indicate the repository root, and values are of type `MarkerType`.
            ``None`` if no custom repo markers are set.
        """
        return self._repo_markers

    @property
    def load_strategy(self) -> LoadStrategy:
        """The load strategy for handling multiple :func:`sys.path` sources.

        :return LoadStrategy | None: The strategy used when handling multiple sys.path sources.
            ``None`` if no custom load strategy is set.
        """
        return self._load_strategy

    @property
    def path_resolution_order(self) -> tuple[PathResolution, ...]:
        """The order in which to resolve :func:`sys.path` sources.

        :return tuple[PathResolution, ...] | None: A tuple defining the order of resolution for sys.path sources.
            ``None`` if no custom resolution order is set.
        """
        return self._path_resolution_order

    @property
    def paths(self) -> tuple[Path, ...]:
        """Additional paths to include in :var:`sys.path`.

        :return tuple[Path, ...] | None: A tuple of additional paths relative to the repository root
            to be added to :var:`sys.path`. ``None`` if no additional paths are set.
        """
        return self._paths

    def __repr__(self) -> str:
        """String representation of the DefaultConfig object.

        :return str: A string representation of the DefaultConfig instance.
        """
        return (
            f'{self.__class__.__name__}()\n'
            f'#  repo_markers={self.repo_markers!r}\n'
            f'#  paths={self.paths!r}\n'
            f'#  load_strategy={self.load_strategy!r}\n'
            f'#  path_resolution_order={self.path_resolution_order!r}'
        )
