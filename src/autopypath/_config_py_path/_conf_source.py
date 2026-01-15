"""Module defining configuration sources for sys.path."""

from enum import Enum

__all__ = []


class ConfSource(str, Enum):
    """Sources for configuration of sys.path.

    - MANUAL: Paths provided directly to the configuration function.
    - DEFAULT: Default autopypath configuration.
    - DOTENV: Paths specified in a `.env` file in the repository root.
    - PYPROJECT: Paths specified in `pyproject.toml` in the repository root.
    """

    MANUAL = 'manual'
    DEFAULT = 'default'
    DOTENV = 'dotenv'
    PYPROJECT = 'pyproject'
