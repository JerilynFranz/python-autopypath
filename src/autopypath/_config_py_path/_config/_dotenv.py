"""Config from dotenv files for autopypath."""

import os
from ntpath import pathsep as nt_pathsep
from pathlib import Path
from posixpath import pathsep as posix_pathsep
from typing import Union

import dotenv

from ... import _validate
from ..._log import log
from ._config import _Config

__all__ = ['_DotEnvConfig']


class _DotEnvConfig(_Config):
    """Configuration for autopypath using dotenv files."""

    _FOUND_POSIX_SEP_MESSAGE: str = "Detected POSIX-style path separator ':' in .env PYTHONPATH on Windows platform."
    _FOUND_NT_SEP_MESSAGE: str = "Detected Windows-style path separator ';' in .env PYTHONPATH on POSIX platform."
    _NOT_A_FILE_MESSAGE: str = '.env path is not a file'

    def __init__(self, repo_root_path: 'Path', strict: bool = False) -> None:
        """Configuration for autopypath using dotenv files.

        If a ``.env`` file is not found in the provided repository root path,
        the configuration will have all attributes set to ``None``.

        If the ``.env`` file is found, it will parse the ``PYTHONPATH`` variable
        if present, and set :property:`paths` accordingly.

        Because ``.env`` files do not natively support repository markers, load strategy,
        or path resolution order, these values are set to ``None``. The only supported
        configuration from ``.env`` files is the list of paths specified in the ``PYTHONPATH``
        environment variable.

        :param Path repo_root_path: The root path of the repository containing a .env file.
        :param bool strict: (default: ``False``) Indicates whether strict mode is enabled for error handling.
        :raises ValueError: If the provided repo_root_path is not a valid directory.
        """
        log.debug('Initializing DotEnvConfig with repo_root_path: %s', repo_root_path)
        self._repo_root_path = _validate.root_repo_path(repo_root_path)

        log.debug('Looking for .env file in repo_root_path: %s', self._repo_root_path)
        dotenv_path = self._repo_root_path / '.env'
        log.debug('.env file path resolved to: %s', dotenv_path)
        if not dotenv_path.exists():
            log.info('No .env file found at path: %s', dotenv_path)
            super().__init__(
                repo_markers=None, paths=None, load_strategy=None, path_resolution_order=None, strict=strict
            )
            return

        if not dotenv_path.is_file():
            message = f'{self._NOT_A_FILE_MESSAGE}: %s'
            if strict:
                formatted_message = self._NOT_A_FILE_MESSAGE.format(dotenv_path)
                log.error(formatted_message)
                raise ValueError(formatted_message)
            log.warning(message, dotenv_path)
            super().__init__(
                repo_markers=None, paths=None, load_strategy=None, path_resolution_order=None, strict=strict
            )
            return

        self._dotenv_path = dotenv_path

        paths = self._dotenv_pythonpaths(repo_root=self._repo_root_path, dotenv_path=self._dotenv_path)
        super().__init__(repo_markers=None, paths=paths, load_strategy=None, path_resolution_order=None, strict=strict)

    def _dotenv_pythonpaths(self, *, repo_root: Path, dotenv_path: Path) -> Union[tuple[Path, ...], None]:
        """Parses PYTHONPATH from the .env file and returns the list of directory paths as a tuple.

        If PYTHONPATH is not set in the .env file, returns None.

        :param Path dotenv_path: The path to the .env file.
        :return Union[tuple[Path], None]: A tuple of Path objects representing the directories
            in PYTHONPATH, or None if PYTHONPATH is not set in the .env file.
        """
        pythonpath_value = dotenv.get_key(dotenv_path, 'PYTHONPATH', encoding='utf-8')
        log.info('Read PYTHONPATH from .env file at %s: PYTHONPATH=%s', dotenv_path, pythonpath_value)
        if pythonpath_value is None:
            log.info('PYTHONPATH not set in .env file at %s', dotenv_path)
            return None
        has_posix_pathsep: bool = posix_pathsep in pythonpath_value
        has_nt_pathsep: bool = nt_pathsep in pythonpath_value
        is_nt: bool = os.name == 'nt'
        is_posix: bool = os.name == 'posix'

        if is_nt and has_posix_pathsep:
            log.info(self._FOUND_POSIX_SEP_MESSAGE)
        elif is_posix and has_nt_pathsep:
            log.info(self._FOUND_NT_SEP_MESSAGE)

        python_path_str = pythonpath_value.strip()

        subdirs_to_add = []
        if python_path_str:
            log.debug('PYTHONPATH from environment: %s', python_path_str)
            normalized_path = python_path_str.replace(posix_pathsep, os.pathsep).replace(nt_pathsep, os.pathsep)
            subdirs_to_add = [p.strip() for p in normalized_path.split(os.pathsep) if p]

        paths: list[Path] = []
        for subdir in subdirs_to_add:
            subdir_path = Path(subdir)
            if not subdir_path.is_absolute():
                subdir_path = repo_root / subdir_path
            paths.append(subdir_path.resolve())
        log.debug('Resolved PYTHONPATH directories from .env: %s', paths)
        if not paths:
            return None
        return tuple(paths)

    def __repr__(self) -> str:
        """String representation of the DefaultConfig object.

        :return str: A string representation of the DefaultConfig instance.
        """
        return f'{self.__class__.__name__}(repo_root_path={str(self._repo_root_path)!r})\n'

    def __str__(self) -> str:
        """String representation of the DotEnvConfig instance."""
        paths_str = ', '.join(f'{str(p)!r}' for p in self.paths) if self.paths else 'None'
        return (
            f'{self.__class__.__name__}:\n'
            f'#  repo_markers={self.repo_markers!r}\n'
            f'#  paths=[{paths_str}]\n'
            f'#  load_strategy={self.load_strategy!r}\n'
            f'#  path_resolution_order={self.path_resolution_order!r}'
        )
