"""Config from dotenv files for autopypath."""

import re
from ntpath import pathsep as nt_pathsep
from pathlib import Path
from posixpath import pathsep as posix_pathsep
from typing import Union

import dotenv

from ... import _validate
from ..._exceptions import AutopypathError
from ..._log import _log
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
        :raises AutopypathError: If the provided repo_root_path is not a valid directory.
        """
        _log.debug('Initializing DotEnvConfig with repo_root_path: %s', repo_root_path)
        self._repo_root_path = _validate.root_repo_path(repo_root_path)

        _log.debug('Looking for .env file in repo_root_path: %s', self._repo_root_path)
        dotenv_path = self._repo_root_path / '.env'
        _log.debug('.env file path resolved to: %s', dotenv_path)
        if not dotenv_path.exists():
            _log.info('No .env file found at path: %s', dotenv_path)
            super().__init__(
                repo_markers=None, paths=None, load_strategy=None, path_resolution_order=None, strict=strict
            )
            return

        if not dotenv_path.is_file():
            message = f'{self._NOT_A_FILE_MESSAGE}: %s'
            if strict:
                formatted_message = self._NOT_A_FILE_MESSAGE.format(dotenv_path)
                _log.error(formatted_message)
                raise AutopypathError(formatted_message)
            _log.warning(message, dotenv_path)
            super().__init__(
                repo_markers=None, paths=None, load_strategy=None, path_resolution_order=None, strict=strict
            )
            return

        self._dotenv_path = dotenv_path

        paths = self._dotenv_pythonpaths(repo_root=self._repo_root_path, dotenv_path=self._dotenv_path)
        super().__init__(repo_markers=None, paths=paths, load_strategy=None, path_resolution_order=None, strict=strict)

    def _determine_separator(self, value: str) -> Union[str, None]:
        """
        Heuristically determines the path separator in a PYTHONPATH string by scoring patterns.
        This is platform-agnostic.

        :param str value: The PYTHONPATH string from the .env file.
        :return: The determined separator (';' or ':'), None for a single path,
                 or a sentinel object for an ambiguous path.
        """
        # Scores for nt (;) vs posix (:) separators
        nt_score = 0
        posix_score = 0

        # Pattern matching to adjust scores
        # `C:\` at the start is a very strong indicator of a windows path component.

        nt_drive_letter_list_count: int = 0
        if re.search(r"^[a-zA-Z]:[\\/]", value):
            nt_drive_letter_list_count += 1

        # Count `;` followed by a drive letter as a strong indicator of a windows path list.
        nt_drive_letter_list_count += len(re.findall(r";[a-zA-Z]:[\\/]", value))

        # Adjust scores based on found nt drive letter patterns
        nt_score += nt_drive_letter_list_count * 4

        posix_score -= nt_drive_letter_list_count  # Correct for colon in drive letter

        # `/` at the start is a strong indicator of a posix path.
        posix_absolute_path_count: int = 0
        if value.startswith('/'):
            posix_absolute_path_count += 1

        # Count `:/` as a strong indicator of a posix path list.
        posix_absolute_path_count += len(re.findall(r":/", value))

        # Adjust scores based on found posix absolute path patterns
        posix_score += posix_absolute_path_count * 4

        # Count backslashes as a strong indicator of an NT path, but avoid double-counting.
        # Subtract backslashes that are already part of the scored drive-letter patterns.
        backslash_count = value.count('\\') - nt_drive_letter_list_count

        # Adjust score based on corrected backslash count
        nt_score += max(0, backslash_count) * 2

        # Presence of separators as a weaker indicator
        nt_count = value.count(nt_pathsep)
        posix_count = value.count(posix_pathsep)

        if nt_count > 0:
            nt_score += 1
        if posix_count > 0:
            posix_score += 1

        _log.debug('Separator determination scores: NT=%d, POSIX=%d', nt_score, posix_score)

        # Determine the winner
        if nt_score > posix_score:
            return nt_pathsep
        if posix_score > nt_score:
            # If we think it's posix, but it looks like a single windows path, it's not a separator.
            if re.match(r"^[a-zA-Z]:[\\/]", value) and posix_count == 1:
                return None
            return posix_pathsep

        # Handle ties or ambiguity
        if nt_score > 0 and nt_score == posix_score:
            _log.warning(
                'Ambiguous PYTHONPATH in .env: contains patterns for both Windows (;) and POSIX (:) separators. '
                'Falling back to separator count to break the tie. PYTHONPATH="%s"',
                value,
            )
            # As a final tie-breaker, prefer the separator that appears more often.
            return nt_pathsep if value.count(nt_pathsep) > value.count(posix_pathsep) else posix_pathsep

        # If scores are both 0, it's likely a single path with no separator.
        return None

    def _dotenv_pythonpaths(self, *, repo_root: Path, dotenv_path: Path) -> Union[tuple[Path, ...], None]:
        """Parses PYTHONPATH from the .env file and returns the list of directory paths as a tuple.

        If PYTHONPATH is not set in the .env file, returns None.

        :param Path dotenv_path: The path to the .env file.
        :return Union[tuple[Path], None]: A tuple of Path objects representing the directories
            in PYTHONPATH, or None if PYTHONPATH is not set in the .env file.
        """
        pythonpath_value = dotenv.get_key(dotenv_path, 'PYTHONPATH', encoding='utf-8')
        _log.info('Read PYTHONPATH from .env file at %s: PYTHONPATH=%s', dotenv_path, pythonpath_value)
        if not pythonpath_value:
            _log.info('PYTHONPATH not set or is empty in .env file at %s', dotenv_path)
            return None

        separator: Union[str, None] = self._determine_separator(pythonpath_value)
        _log.debug('Determined path separator to be %r', separator)

        segments = pythonpath_value.split(separator) if separator is not None else [pythonpath_value]

        paths: list[Path] = []
        for seg in segments:
            seg = seg.strip()
            if not seg:
                continue

            if re.search(r'["\']', seg):
                _log.warning(
                    'Quotes detected in PYTHONPATH segment: %r. '
                    'Quotes are not typically used in .env files and may indicate incorrect path parsing.',
                    seg,
                )

            seg_path = Path(seg)
            if seg_path.is_absolute():
                _log.warning(
                    'Absolute path detected in PYTHONPATH segment: %r. '
                    'Absolute paths are not supported. Skipping.',
                    seg,
                )
                continue

            # Path is relative, resolve it against the repo root.
            full_path = (repo_root / seg_path).resolve()
            paths.append(full_path)

        _log.debug('Resolved PYTHONPATH directories from .env: %s', paths)
        return tuple(paths) if paths else None

    def __repr__(self) -> str:
        """String representation of the DefaultConfig object.

        :return str: A string representation of the DefaultConfig instance.
        """
        return f'{self.__class__.__name__}(repo_root_path={self._repo_root_path!r})\n'

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
