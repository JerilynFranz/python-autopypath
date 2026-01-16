"""autopypath.toml configuration module for autopypath."""

from pathlib import Path

from ._toml import TomlConfig


class AutopypathConfig(TomlConfig):
    """Configuration for autopypath using autopypath.toml files."""

    def __init__(self, repo_root_path: 'Path') -> None:
        """Configuration for autopypath using autopypath.toml files.

        If a ``autopypath.toml`` file is not found in the provided repository root path,
        the configuration will have all attributes set to ``None``.

        If the ``autopypath.toml`` file is found, it will parse the relevant
        autopypath configuration under the ``[tool.autopypath]`` section.

        :param Path repo_root_path: The root path of the repository containing a autopypath.toml file.
        :raises ValueError: If the provided repo_root_path is not a valid directory.
        """
        super().__init__(repo_root_path=repo_root_path, toml_filename='autopypath.toml', toml_section='tool.autopypath')

    def __repr__(self) -> str:
        """String representation of the AutopypathConfig object.

        :return str: A string representation of the AutopypathConfig instance.
        """
        return f'{self.__class__.__name__}(repo_root_path={str(self._repo_root_path)!r})'
