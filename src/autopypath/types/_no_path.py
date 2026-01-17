"""These are publically exposed special types used by autopypath."""

from pathlib import Path
from typing import NoReturn, final


@final
class _MonkeyWrenchedType:
    """A type to indicate that a type is deliberately broken to prevent use of a method.

    This type is used as a type hint for method parameters in the :class:`NoPath` class
    to indicate that these methods should not be used and will raise a :class:`NotImplemented

    It deliberarily breaks the method signature to prevent accidental usage.

    This helps type checkers identify incorrect usage of these methods before runtime.
    """


@final
class NoPath(Path):
    """A custom Path type representing the absence of a path.

    This class is used to indicate that no valid path is available or applicable.
    It inherits from :class:`~pathlib.Path` to maintain compatibility with path operations,
    but it signifies a 'no path' state and cannot be used to perform actual file system operations.
    """

    def __new__(cls) -> 'NoPath':
        """Create a new instance of NoPath.

        This method ensures that NoPath behaves like a Path object while
        representing the absence of a valid path.

        It cannot be instantiated with any path value and cannot perform any IO operations.

        .. note::
            Because Path is a C extension type rather than a regular Python class,
            we need to call its __new__ method directly on the superclass pathlib.Path
            to insert ourselves into the inheritance chain.

        :return NoPath: An instance of NoPath.
        """
        return super().__new__(cls, '')

    def __str__(self) -> str:
        """String representation of NoPath.

        :return str: A string indicating that this is a NoPath instance.
        """
        return '<NoPath>'

    def __repr__(self) -> str:
        """Official string representation of NoPath.

        :return str: A string representation of the NoPath instance.
        """
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        return isinstance(other, NoPath)

    # --- IO methods overridden to prevent filesystem access ---
    def exists(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def is_file(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def is_dir(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def open(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def read_text(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def read_bytes(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def write_text(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def write_bytes(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def mkdir(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def rmdir(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def unlink(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def rename(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def replace(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def touch(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def stat(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def chmod(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def lstat(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def owner(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def group(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def readlink(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def symlink_to(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def hardlink_to(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def absolute(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def resolve(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def samefile(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def expanduser(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def with_name(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def with_suffix(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def relative_to(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def is_absolute(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def is_reserved(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def joinpath(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def match(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def parent(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def parents(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def parts(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def drive(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def root(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def anchor(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def name(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def suffix(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def suffixes(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def stem(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def as_posix(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def as_uri(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def is_mount(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def is_symlink(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def is_block_device(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def is_char_device(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def is_fifo(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def is_socket(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def iterdir(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def glob(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def rglob(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def cwd(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')

    def home(self, _disabled: _MonkeyWrenchedType) -> NoReturn:  #  type: ignore[override]
        raise NotImplementedError('NoPath does not support IO operations.')
