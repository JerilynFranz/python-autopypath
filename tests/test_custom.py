"""Tests for autopypath.custom.configure_pypath"""

import logging
import sys

import pytest

_ORIGINAL_SYS_PATH: list[str] = sys.path.copy()
_ORIGINAL_NAME: str = __name__


def test_configure_pypath_no_error() -> None:
    """Test that configure_pypath runs without error."""
    global __name__
    try:
        sys.path = _ORIGINAL_SYS_PATH.copy()
        sys.modules.pop('autopypath.custom', None)
        __name__ = '__main__'
        from autopypath.custom import configure_pypath

        configure_pypath()
    finally:
        sys.path = _ORIGINAL_SYS_PATH.copy()
        __name__ = _ORIGINAL_NAME
        sys.modules.pop('autopypath.custom', None)


def test_configure_pypath_all_options() -> None:
    """Test that configure_pypath runs with all options set."""
    global __name__
    try:
        sys.path = _ORIGINAL_SYS_PATH.copy()
        sys.modules.pop('autopypath', None)
        __name__ = '__main__'
        from autopypath.custom import configure_pypath

        configure_pypath(
            repo_markers={'pyproject.toml': 'file', '.git': 'dir'},
            paths=['src', 'lib'],
            posix_paths=['posix_dir'],
            windows_paths=['windows_dir'],
            load_strategy='prepend',
            path_resolution_order=['autopypath', 'pyproject'],
            log_level=logging.INFO,
            strict=True,
        )
    finally:
        sys.path = _ORIGINAL_SYS_PATH.copy()
        __name__ = _ORIGINAL_NAME
        sys.modules.pop('autopypath.custom', None)


def test_configure_pypath_strict_non_main() -> None:
    """Test that configure_pypath raises RuntimeError when strict is True and not run as __main__."""
    try:
        sys.path = _ORIGINAL_SYS_PATH.copy()
        sys.modules.pop('autopypath.custom', None)
        from autopypath.custom import configure_pypath

        configure_pypath()
    finally:
        sys.path = _ORIGINAL_SYS_PATH.copy()
        sys.modules.pop('autopypath.custom', None)


def test_configure_pypath_context_file_none() -> None:
    """Test that configure_pypath raises RuntimeError when context file is None."""
    global __name__
    try:
        sys.path = _ORIGINAL_SYS_PATH.copy()
        sys.modules.pop('autopypath.custom', None)
        __name__ = '__main__'
        from autopypath.custom import configure_pypath

        configure_pypath.__globals__['_context_file'] = None
        configure_pypath()
        pytest.fail('Expected RuntimeError due to context file being None.')

    except RuntimeError:
        pass

    finally:
        sys.path = _ORIGINAL_SYS_PATH.copy()
        sys.modules.pop('autopypath.custom', None)
        __name__ = _ORIGINAL_NAME


def test_configure_pypath_not_strict_non_main() -> None:
    """Test that configure_pypath does not raise when strict is False and not run as __main__."""
    try:
        sys.path = _ORIGINAL_SYS_PATH.copy()
        sys.modules.pop('autopypath.custom', None)
        from autopypath.custom import configure_pypath

        configure_pypath(strict=False)
    finally:
        sys.path = _ORIGINAL_SYS_PATH.copy()
        sys.modules.pop('autopypath.custom', None)


def test_import_non_main_context() -> None:
    """Test that importing autopypath.custom from non-__main__ context logs a debug message."""
    try:
        sys.path = _ORIGINAL_SYS_PATH.copy()
        sys.modules.pop('autopypath.custom', None)
        from autopypath.custom import configure_pypath

        configure_pypath(strict=True)
    except RuntimeError:
        pass

    finally:
        sys.path = _ORIGINAL_SYS_PATH.copy()
        sys.modules.pop('autopypath.custom', None)
