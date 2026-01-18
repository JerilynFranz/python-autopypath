"""Tests for autopypath._config_py_path._config._dotenv module."""

from pathlib import Path

import pytest

from autopypath._config_py_path._config._dotenv import _DotEnvConfig


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
    """Test that DotEnvConfig raises ValueError when provided a non-directory path."""
    bad_path = Path('non_existent_directory')

    try:
        _DotEnvConfig(repo_root_path=bad_path)
        pytest.fail('DOTENV_006 Expected ValueError when initializing DotEnvConfig with non-directory path')
    except ValueError:
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
