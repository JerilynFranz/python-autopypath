"""Tests for autopypath._config_py_path._config._dotenv module."""

import logging
import os
import unittest.mock
from pathlib import Path, PosixPath, WindowsPath  # noqa: F401  # Needed for repr eval

import pytest

from autopypath._config_py_path._config._dotenv import _DotEnvConfig
from autopypath._exceptions import AutopypathError
from autopypath._log import _log


def test_dotenv_config_init_no_file(tmp_path: Path) -> None:
    """Test that DotEnvConfig initializes correctly when no .env file is present."""
    config = _DotEnvConfig(repo_root_path=tmp_path)

    assert isinstance(config, _DotEnvConfig), 'DOTENV_001 Failed to instantiate DotEnvConfig'
    assert config.paths is None, 'DOTENV_002 Paths should be None when no .env file is present'
    assert config.load_strategy is None, 'DOTENV_003 Load strategy should be None when no .env file is present'
    assert config.repo_markers is None, 'DOTENV_004 Repo markers should be None when no .env file is present'
    assert config.path_resolution_order is None, (
        'DOTENV_005 Path resolution order should be None when no .env file is present'
    )


def test_dotenv_config_init_with_bad_directory() -> None:
    """Test that DotEnvConfig raises AutopypathError when provided a non-directory path."""
    bad_path = Path('non_existent_directory')

    try:
        _DotEnvConfig(repo_root_path=bad_path)
        pytest.fail('DOTENV_006 Expected AutopypathError when initializing DotEnvConfig with non-directory path')
    except AutopypathError:
        pass


def test_dotenv_config_init_with_file(tmp_path: Path) -> None:
    """Test that DotEnvConfig initializes correctly when a .env file is present."""
    dotenv_content = 'PYTHONPATH=src:lib:tests\n'
    dotenv_path = tmp_path / '.env'
    dotenv_path.write_text(dotenv_content)

    config = _DotEnvConfig(repo_root_path=tmp_path)

    assert isinstance(config, _DotEnvConfig), 'DOTENV_007 Failed to instantiate DotEnvConfig with .env file'
    assert config.paths is not None, 'DOTENV_008 Paths should not be None when .env file is present'
    expected_paths = (tmp_path / 'src', tmp_path / 'lib', tmp_path / 'tests')
    assert config.paths == expected_paths, 'DOTENV_009 Paths do not match expected values from .env file'
    assert config.load_strategy is None, 'DOTENV_010 Load strategy should be None when .env file is present'
    assert config.repo_markers is None, 'DOTENV_011 Repo markers should be None when .env file is present'
    assert config.path_resolution_order is None, (
        'DOTENV_012 Path resolution order should be None when .env file is present'
    )


def test_dotenv_config_init_with_no_pythonpath(tmp_path: Path) -> None:
    """Test that DotEnvConfig initializes correctly when .env file has no PYTHONPATH."""
    dotenv_content = 'SOME_OTHER_VAR=value\n'
    dotenv_path = tmp_path / '.env'
    dotenv_path.write_text(dotenv_content)

    config = _DotEnvConfig(repo_root_path=tmp_path)

    assert isinstance(config, _DotEnvConfig), 'DOTENV_013 Failed to instantiate DotEnvConfig with .env file'
    assert config.paths is None, 'DOTENV_014 Paths should be None when PYTHONPATH is not set in .env file'
    assert config.load_strategy is None, 'DOTENV_015 Load strategy should be None when .env file is present'
    assert config.repo_markers is None, 'DOTENV_016 Repo markers should be None when .env file is present'
    assert config.path_resolution_order is None, (
        'DOTENV_017 Path resolution order should be None when .env file is present'
    )


def test_dotenv_config_repr(tmp_path: Path) -> None:
    """Test the __repr__ method of DotEnvConfig."""
    dotenv_content = 'PYTHONPATH=src:lib\n'
    dotenv_path = tmp_path / '.env'
    dotenv_path.write_text(dotenv_content)

    config = _DotEnvConfig(repo_root_path=tmp_path)

    repr_output = repr(config)
    new_config = eval(repr_output)

    assert isinstance(new_config, _DotEnvConfig), 'DOTENV_018 __repr__ did not produce a DotEnvConfig instance'
    assert new_config._repo_root_path == config._repo_root_path, (
        'DOTENV_019 repo_root_path does not match after eval of __repr__'
    )
    assert new_config.paths == config.paths, 'DOTENV_020 paths do not match after eval of __repr__'
    assert new_config.load_strategy == config.load_strategy, (
        'DOTENV_021 load_strategy does not match after eval of __repr__'
    )
    assert new_config.repo_markers == config.repo_markers, 'DOTENV_022 repo_markers do not match after eval of __repr__'
    assert new_config.path_resolution_order == config.path_resolution_order, (
        'DOTENV_023 path_resolution_order does not match after eval of __repr__'
    )


def test_dotenv_config_str(tmp_path: Path) -> None:
    """Test the __str__ method of DotEnvConfig."""
    dotenv_content = 'PYTHONPATH=src:lib\n'
    dotenv_path = tmp_path / '.env'
    dotenv_path.write_text(dotenv_content)

    config = _DotEnvConfig(repo_root_path=tmp_path)
    class_name = config.__class__.__name__
    str_output = str(config)

    expected_str = (
        f'{class_name}:\n'
        '#  repo_markers=None\n'
        f'#  paths=[{str(tmp_path / "src")!r}, {str(tmp_path / "lib")!r}]\n'
        '#  load_strategy=None\n'
        '#  path_resolution_order=None'
    )
    assert str_output == expected_str, 'DOTENV_024 __str__ output does not match expected format'


def test_dotenv_config_with_empty_pythonpath(tmp_path: Path) -> None:
    """Test that DotEnvConfig handles an empty PYTHONPATH in .env file correctly."""
    dotenv_content = 'PYTHONPATH=\n'
    dotenv_path = tmp_path / '.env'
    dotenv_path.write_text(dotenv_content)

    config = _DotEnvConfig(repo_root_path=tmp_path)

    assert isinstance(config, _DotEnvConfig), 'DOTENV_025 Failed to instantiate DotEnvConfig with empty PYTHONPATH'
    assert config.paths is None, 'DOTENV_026 Paths should be None when PYTHONPATH is empty in .env file'
    assert config.load_strategy is None, 'DOTENV_027 Load strategy should be None when .env file is present'
    assert config.repo_markers is None, 'DOTENV_028 Repo markers should be None when .env file is present'
    assert config.path_resolution_order is None, (
        'DOTENV_029 Path resolution order should be None when .env file is present'
    )


def test_dotenv_config_with_not_a_file_dotenv(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    """Test that DotEnvConfig handles a non-file .env path correctly by logging a warning."""
    dotenv_path = tmp_path / '.env'
    dotenv_path.mkdir()  # Create a directory instead of a file

    caplog.clear()
    _DotEnvConfig(repo_root_path=tmp_path)
    warning_messages = [record.message for record in caplog.records if record.levelno == logging.WARNING]
    assert any(message.startswith(_DotEnvConfig._NOT_A_FILE_MESSAGE) for message in warning_messages), (
        'DOTENV_030 Expected a warning about .env path not being a file'
    )

    # Test strict mode raises AutopypathError
    try:
        _DotEnvConfig(repo_root_path=tmp_path, strict=True)
    except AutopypathError as e:
        assert str(e).startswith(_DotEnvConfig._NOT_A_FILE_MESSAGE), (
            'DOTENV_035 Expected AutopypathError about .env path not being a file in strict mode'
        )


def test_non_platform_path_separators_in_dotenv(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    """Test that DotEnvConfig logs appropriate messages for non-native path separators in .env PYTHONPATH."""
    repo_dir = tmp_path / 'repo'
    repo_dir.mkdir()
    dotenv_content = 'PYTHONPATH=src;lib:tests\n'  # Mixed separators
    dotenv_path = repo_dir / '.env'
    dotenv_path.write_text(dotenv_content)

    posix_message = _DotEnvConfig._FOUND_POSIX_SEP_MESSAGE
    windows_message = _DotEnvConfig._FOUND_NT_SEP_MESSAGE

    caplog.clear()
    _log.setLevel(logging.INFO)

    try:
        # Check for expected log messages for this platform

        _DotEnvConfig(repo_root_path=repo_dir)

        log_messages = [record.message for record in caplog.records if record.levelno == logging.INFO]

        expected_message = ''
        if os.name == 'nt':
            expected_message = posix_message
        elif os.name == 'posix':
            expected_message = windows_message
        if expected_message:
            assert any(message == expected_message for message in log_messages), (
                f'DOTENV_031 Expected log message about non-native path separators in .env{caplog.records}'
            )
    finally:
        _log.setLevel(logging.NOTSET)


def test_cross_platform_path_separators_in_dotenv(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    """Test that DotEnvConfig logs appropriate messages for non-native path separators in .env PYTHONPATH
    when os.name is monkeypatched to simulate different platforms.
    """
    repo_dir = tmp_path
    dotenv_content = 'PYTHONPATH=src;lib:tests\n'  # Mixed separators
    dotenv_path = repo_dir / '.env'
    dotenv_path.write_text(dotenv_content)

    # force module loads before monkeypatching os.name
    _DotEnvConfig(repo_root_path=tmp_path)

    os_name = os.name  # Capture the current os.name

    posix_message = _DotEnvConfig._FOUND_POSIX_SEP_MESSAGE
    windows_message = _DotEnvConfig._FOUND_NT_SEP_MESSAGE

    # Patch os.name to the other platform using unittest.mock.patch
    other_os_name = 'nt' if os_name != 'nt' else 'posix'
    try:
        with unittest.mock.patch('os.name', other_os_name):
            caplog.clear()
            _log.setLevel(logging.INFO)

            # Test for cross-platform Path support
            # It is known to fail on CPython < 3.12 and PyPy 3.10 and 3.11
            # It may fail on other platforms or implementations
            try:
                Path('C:\\some\\windows\\path')
                Path('/some/posix/path')
            except Exception:
                pytest.skip('Cross-platform Path creation not supported in this Python version')

            _DotEnvConfig(repo_root_path=tmp_path)

            log_messages = [record.message for record in caplog.records if record.levelno == logging.INFO]

            expected_message = ''
            if other_os_name == 'nt':
                expected_message = posix_message
            elif other_os_name == 'posix':
                expected_message = windows_message
            if expected_message:
                assert any(message == expected_message for message in log_messages), (
                    'DOTENV_032 Expected log message about non-native path separators in .env after os.name monkeypatch'
                )
    finally:
        _log.setLevel(logging.NOTSET)


def test_no_paths_pythonpath_in_dotenv(tmp_path: Path) -> None:
    """Test that DotEnvConfig returns None for paths when PYTHONPATH is not set in .env file."""
    dotenv_content = 'PYTHONPATH=:\n'
    dotenv_path = tmp_path / '.env'
    dotenv_path.write_text(dotenv_content)

    config = _DotEnvConfig(repo_root_path=tmp_path)

    assert config.paths is None, 'DOTENV_033 Paths should be None when PYTHONPATH is not set in .env file'


def test_absolute_and_relative_paths_in_dotenv(tmp_path: Path) -> None:
    """Test that DotEnvConfig correctly resolves absolute and relative paths from PYTHONPATH in .env file."""
    abs_path = tmp_path / 'absolute_path'
    abs_path.mkdir()
    rel_path = 'relative_path'
    (tmp_path / rel_path).mkdir()

    dotenv_content = f'PYTHONPATH={rel_path}\n'
    dotenv_path = tmp_path / '.env'
    dotenv_path.write_text(dotenv_content)

    config = _DotEnvConfig(repo_root_path=tmp_path)

    expected_paths = [(tmp_path / rel_path).resolve(),]
    found_paths = list(config.paths) if config.paths is not None else []
    assert found_paths == expected_paths, (
        'DOTENV_034 Paths do not match expected relative paths from .env file'
    )

    dotenv_content = f'PYTHONPATH={abs_path}\n'
    dotenv_path.write_text(dotenv_content)
    config = _DotEnvConfig(repo_root_path=tmp_path)
    expected_paths = [abs_path.resolve()]
    found_paths = list(config.paths) if config.paths is not None else []
    assert found_paths == expected_paths, (
        'DOTENV_035 Paths do not match expected absolute paths from .env file. '
        f'expected = {expected_paths!r}, found = {found_paths!r},'
        f'dotenv = {dotenv_content}'
    )
