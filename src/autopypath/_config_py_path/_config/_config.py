"""Base class for python path sources"""

from collections.abc import Mapping, Sequence
from pathlib import Path
from types import MappingProxyType
from typing import Union, Optional


from ..._log import log
from ...load_strategy import LoadStrategy
from ...marker_type import MarkerType
from ...path_resolution import PathResolution
from ... import _validate

__all__ = []


class NotPresent:
    """Sentinel class to represent a value that is not present."""


NOT_PRESENT = NotPresent()


class Config:
    """Base configuration class for python path sources.


    :property repo_markers: Mapping of repository markers to their MarkerType.
    :property paths: Additional paths to include in :var:`sys.path`.
    :property load_strategy: The load strategy for handling multiple :var:`sys.path` sources.
    :property path_resolution_order: The order in which to resolve :var:`sys.path` sources.
    """

    __slots__ = ('_repo_markers', '_paths', '_load_strategy', '_path_resolution_order')

    def __init__(
        self,
        *,
        repo_markers: Optional[Mapping[str, MarkerType]] = None,
        paths: Optional[Sequence[Union[Path, str]]] = None,
        load_strategy: Optional[Union[LoadStrategy, str]] = None,
        path_resolution_order: Optional[Sequence[Union[PathResolution, str]]] = None,
    ) -> None:
        """
        :param Mapping[str, MarkerType] | None repo_markers: Markers to identify the repository root.
            Mapping of file or directory names to their MarkerType.

        :param Sequence[Path | str] | Nonepaths: Additional paths to include in :var:`sys.path`.
            Sequence of paths relative to the repository root to be added to :var:`sys.path`.

        :param LoadStrategy | str | Noneload_strategy: The strategy for loading from :func:`sys.path` sources.
            The strategy to use when handling multiple sys.path sources.

            It is expected to be one of `merge`, `override`, or `replace` (as defined in :class:`LoadStrategy`).
            It can use either the enum value or its string representation.

        :param Sequence[PathResolution | str] | None path_resolution_order: The order in which to
            resolve :func:`sys.path` sources.

            It is expected to be a sequence containing any of the following values:
            `manual`, `pyproject`, `dotenv` as defined in :class:`PathResolution`.
            It can use either the enum values or their string representations.
        """
        self._repo_markers: Union[MappingProxyType[str, MarkerType], None] = _validate.repo_markers(repo_markers)
        self._paths: Union[tuple[Path, ...], None] = _validate.paths(paths)
        self._load_strategy: Union[LoadStrategy, None] = _validate.load_strategy(load_strategy)
        self._path_resolution_order: Union[tuple[PathResolution, ...], None] = _validate.path_resolution_order(
            path_resolution_order
        )

        cls = self.__class__.__name__
        log.debug(
            f'{cls} initialized with repo_markers={self._repo_markers}, '
            f'paths={self.paths}, load_strategy={self.load_strategy}, '
            f'path_resolution_order={self.path_resolution_order}'
        )

    @property
    def repo_markers(self) -> Union[MappingProxyType[str, MarkerType], None]:
        """Mapping of repository markers to their MarkerType.

        :return MappingProxyType[str, MarkerType] | None: A mapping where keys are filenames or directory names
            that indicate the repository root, and values are of type `MarkerType`.
            ``None`` if no custom repo markers are set.
        """
        return self._repo_markers

    @property
    def load_strategy(self) -> Union[LoadStrategy, None]:
        """The load strategy for handling multiple :func:`sys.path` sources.

        :return LoadStrategy | None: The strategy used when handling multiple sys.path sources.
            ``None`` if no custom load strategy is set.
        """
        return self._load_strategy

    @property
    def path_resolution_order(self) -> Union[tuple[PathResolution, ...], None]:
        """The order in which to resolve :func:`sys.path` sources.

        :return tuple[PathResolution, ...] | None: A tuple defining the order of resolution for sys.path sources.
            ``None`` if no custom resolution order is set.
        """
        return self._path_resolution_order

    @property
    def paths(self) -> Union[tuple[Path, ...], None]:
        """Additional paths to include in :var:`sys.path`.

        :return tuple[Path, ...] | None: A tuple of additional paths relative to the repository root
            to be added to :var:`sys.path`. ``None`` if no additional paths are set.
        """
        return self._paths

    def __repr__(self) -> str:
        """String representation of the Config object.

        :return str: A string representation of the Config instance.
        """
        cls = self.__class__.__name__
        return (
            f'{cls}(repo_markers={self._repo_markers}, '
            f'paths={self.paths}, load_strategy={self.load_strategy}, '
            f'path_resolution_order={self.path_resolution_order})'
        )

    def __str__(self) -> str:
        """String representation of the Config instance."""
        return (
            f'{self.__class__.__name__}:\n'
            f'  repo_markers={self.repo_markers!r}\n'
            f'  paths={self.paths!r}\n'
            f'  load_strategy={self.load_strategy!r}\n'
            f'  path_resolution_order={self.path_resolution_order!r}'
        )

    def __eq__(self, other: object) -> bool:
        """Equality comparison for Config objects.

        :param object other: Another object to compare with.
        :return bool: True if both Config instances are equal, False otherwise.
        """
        if not isinstance(other, Config):
            return NotImplemented
        return (
            self.repo_markers == other.repo_markers
            and self.paths == other.paths
            and self.load_strategy == other.load_strategy
            and self.path_resolution_order == other.path_resolution_order
        )

    def __hash__(self) -> int:
        """Hash for Config objects."""
        repo_markers: MappingProxyType[str, MarkerType] = self.repo_markers or MappingProxyType({})
        return hash(
            (frozenset(sorted(repo_markers.items())), self.paths, self.load_strategy, self.path_resolution_order)
        )

    def replace(
        self,
        *,
        repo_markers: Union[Mapping[str, MarkerType], None, NotPresent] = NOT_PRESENT,
        paths: Union[Sequence[Union[Path, str]], None, NotPresent] = NOT_PRESENT,
        load_strategy: Union[LoadStrategy, str, None, NotPresent] = NOT_PRESENT,
        path_resolution_order: Union[Sequence[Union[PathResolution, str]], None, NotPresent] = NOT_PRESENT,
    ) -> 'Config':
        """Creates a copy of the current Config instance with specified attributes replaced.

        If an attribute is not provided, the value from the current instance is used.

        The default value for each parameter is a sentinel `NotPresent` instance,
        which indicates that the current value should be retained.

        :param Mapping[str, MarkerType] | None | NotPresent repo_markers: New repo_markers value.
        :param Sequence[Path | str] | None | NotPresent paths: New paths value.
        :param LoadStrategy | str | None | NotPresent load_strategy: New load_strategy value.
        :param Sequence[PathResolution | str] | None | NotPresent path_resolution_order: New path_resolution_order
            value.

        :return Config: A new Config instance with selected attributes replaced.
        """

        new_repo_markers = self.repo_markers if isinstance(repo_markers, NotPresent) else repo_markers
        new_paths = self.paths if isinstance(paths, NotPresent) else paths
        new_load_strategy = self.load_strategy if isinstance(load_strategy, NotPresent) else load_strategy
        new_path_resolution_order = (
            self.path_resolution_order if isinstance(path_resolution_order, NotPresent) else path_resolution_order
        )
        return Config(
            repo_markers=new_repo_markers,
            paths=new_paths,
            load_strategy=new_load_strategy,
            path_resolution_order=new_path_resolution_order,
        )
