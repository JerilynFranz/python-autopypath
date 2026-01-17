"""These are publically exposed special types used by autopypath."""
# mypy: disable-error-code=override
# pyright: reportIncompatibleMethodOverride=false

from pathlib import Path
from typing import TYPE_CHECKING, final

from .._typing import Never, TypeAlias


class NotSupported(NotImplementedError):
    """Exception raised when an unsupported operation is attempted on NoPath.

    This exception indicates that the attempted operation is not supported.
    """


if TYPE_CHECKING:
    # During static analysis, make the "disabled" parameter un-callable:
    # nothing can ever satisfy a Never-typed argument.
    _UsagePreventedType: TypeAlias = Never
else:

    @final
    class _UsagePreventedType:
        """A type to indicate that a type is deliberately broken to prevent use of a method.

        This type is used as a type hint for method parameters in the :class:`NoPath` class
        to indicate that these methods should not be used and will raise a :class:`NotImplemented`
        exception if called.

        It deliberarily breaks the method signature to prevent accidental usage.

        This helps type checkers identify incorrect usage of these methods before runtime.
        """


_PathType: type[Path] = type(Path())
"""A type alias for the pathlib.Path type.

Generally, you cannot directly inherit from pathlib.Path because it is a C extension type.
This alias allows us to work around that limitation.
"""


_NOT_SUPPORTED_ERR: str = 'NoPath does not support this operation.'


@final
class _NoPath(_PathType):  # type: ignore[valid-type,misc]  # Magic to inherit from pathlib.Path
    """A custom Path type representing the absence of a path.

    This class is used to indicate that no valid path is available or applicable.

    It inherits from :class:`~pathlib.Path` to maintain compatibility with path operations
    and type checking, but it signifies a 'no path' state and cannot be used to perform any
    file system operations.
    """

    def __hash__(self) -> int:
        """Hash for NoPath objects always returns 0."""
        return 0

    def __repr__(self) -> str:
        """Representation of NoPath."""
        return '<NoPath>'

    def __str__(self) -> str:
        """String representation of NoPath."""
        return '<NoPath>'

    def __eq__(self, other: object) -> bool:
        """Equality comparison for NoPath objects.

        :param object other: Another object to compare with.
        :return bool: True if both are NoPath instances, False otherwise.
        """
        return isinstance(other, _NoPath)

    def __fspath__(self) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def __truediv__(self, key: object) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def __rtruediv__(self, key: object) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    # --- IO methods overridden to prevent filesystem access ---
    def exists(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def is_file(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def is_dir(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def open(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def read_text(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def read_bytes(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def write_text(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def write_bytes(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def mkdir(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def rmdir(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def unlink(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def rename(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def replace(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def touch(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def stat(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def chmod(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def lstat(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def owner(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def group(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def readlink(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def symlink_to(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def hardlink_to(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def absolute(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def resolve(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def samefile(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def expanduser(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def with_name(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def with_suffix(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def relative_to(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def is_absolute(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def is_reserved(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def joinpath(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def match(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    @property
    def parent(self) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    @property
    def parents(self) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    @property
    def parts(self) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    @property
    def drive(self) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    @property
    def root(self) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    @property
    def anchor(self) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    @property
    def name(self) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    @property
    def suffix(self) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    @property
    def suffixes(self) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    @property
    def stem(self) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def as_posix(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def as_uri(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def is_mount(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def is_symlink(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def is_block_device(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def is_char_device(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def is_fifo(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def is_socket(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def iterdir(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def glob(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    def rglob(self, _disabled: _UsagePreventedType) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    @classmethod
    def cwd(cls) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)

    @classmethod
    def home(cls) -> Never:
        raise NotSupported(_NOT_SUPPORTED_ERR)
