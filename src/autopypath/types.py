"""These are publically exposed special types used by autopypath."""

from pathlib import PurePath


class NoPath(PurePath):
    """A special Path type representing the absence of a path.

    This class is used to indicate that no valid path is available or applicable.
    It inherits from :class:`~pathlib.PurePath` to maintain compatibility with path operations,
    but it signifies a 'no path' state and cannot be used to perform actual file system operations.
    """

    def __new__(cls) -> 'NoPath':
        """Create a new instance of NoPath.

        This method ensures that NoPath behaves like a Path object while
        representing the absence of a valid path.

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
