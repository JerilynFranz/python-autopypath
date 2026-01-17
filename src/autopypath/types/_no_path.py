"""These are publically exposed special types used by autopypath."""

from pathlib import PurePath
from typing import NoReturn, final


class NotSupported(NotImplementedError):
    """Exception raised when an unsupported operation is attempted on NoPath.

    This exception indicates that the attempted operation is not supported"""


@final
class _UsagePreventedType:
    """A type to indicate that a type is deliberately broken to prevent use of a method.

    This type is used as a type hint for method parameters in the :class:`NoPath` class
    to indicate that these methods should not be used and will raise a :class:`NotImplemented

    It deliberarily breaks the method signature to prevent accidental usage.

    This helps type checkers identify incorrect usage of these methods before runtime.
    """


_PathType: type[PurePath] = type(PurePath())
"""A type alias for the pathlib.PurePath type.

Generally, you cannot directly inherit from pathlib.PurePath because it is a C extension type.
This alias allows us to work around that limitation.
"""


@final
class _NoPath(_PathType):  # type: ignore[valid-type,misc]  # Magic to inherit from pathlib.PurePath
    """A custom Path type representing the absence of a path.

    This class is used to indicate that no valid path is available or applicable.

    It inherits from :class:`~pathlib.PurePath` to maintain compatibility with path operations
    and type checking, but it signifies a 'no path' state and cannot be used to perform any
    file system operations.
    """

    def __new__(cls) -> '_NoPath':
        """Create a new instance of NoPath.

        This method ensures that NoPath types as as a :class:`~pathlib.Path` subclass while
        representing the absence of a valid path.

        It cannot be instantiated with any path value and cannot perform any IO operations.

        .. note::
            Because PurePath is a C extension type rather than a regular Python class,
            we need to call its __new__ method directly on the superclass pathlib.PurePath
            to insert ourselves into the inheritance chain.

        :return NoPath: An instance of NoPath.
        """
        return super().__new__(cls, '')  # type: ignore[arg-type]

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
        return isinstance(other, _NoPath)

    # --- IO methods overridden to prevent filesystem access ---
    def exists(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def is_file(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def is_dir(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def open(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def read_text(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def read_bytes(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def write_text(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def write_bytes(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def mkdir(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def rmdir(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def unlink(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def rename(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def replace(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def touch(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def stat(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def chmod(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def lstat(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def owner(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def group(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def readlink(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def symlink_to(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def hardlink_to(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def absolute(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def resolve(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def samefile(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def expanduser(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def with_name(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def with_suffix(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def relative_to(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def is_absolute(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def is_reserved(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def joinpath(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def match(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def parent(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def parents(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def parts(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def drive(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def root(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def anchor(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def name(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def suffix(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def suffixes(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def stem(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def as_posix(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def as_uri(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def is_mount(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def is_symlink(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def is_block_device(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def is_char_device(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def is_fifo(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def is_socket(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def iterdir(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def glob(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def rglob(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def cwd(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')

    def home(self, _disabled: _UsagePreventedType) -> NoReturn:  #  type: ignore[override]
        raise NotSupported('NoPath does not support IO operations.')
