"""PyProject.toml configuration module for autopypath."""

from pathlib import Path

from ._toml import TomlConfig


class PyProjectConfig(TomlConfig):
    """Configuration for autopypath using pyproject.toml files."""

    def __init__(self, repo_root_path: 'Path') -> None:
        """Configuration for autopypath using pyproject.toml files.

        If a ``pyproject.toml`` file is not found in the provided repository root path,
        the configuration will have all attributes set to ``None``.

        If the ``pyproject.toml`` file is found, it will parse the relevant
        autopypath configuration under the ``[tool.autopypath]`` section.

        :param Path repo_root_path: The root path of the repository containing a pyproject.toml file.
        :raises ValueError: If the provided repo_root_path is not a valid directory.
        """
        super().__init__(repo_root_path=repo_root_path, toml_filename='pyproject.toml', toml_section='tool.autopypath')

    def __repr__(self) -> str:
        """String representation of the PyProjectConfig object.

        :return str: A string representation of the PyProjectConfig instance.
        """
        return f'{self.__class__.__name__}(repo_root_path={str(self._repo_root_path)!r})'
