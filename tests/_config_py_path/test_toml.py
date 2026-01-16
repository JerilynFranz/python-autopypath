from pathlib import Path

import pytest

from autopypath._config_py_path._config._toml import TomlConfig


def test_toml_config_init(tmp_path: Path) -> None:
    repo_root = tmp_path / 'my_repo'
    repo_root.mkdir()
    marker_file = repo_root / 'filename.txt'
    marker_file.touch()
    marker_dir = repo_root / 'dirname'
    marker_dir.mkdir()
    toml_filename = 'toml_file.toml'
    toml_path = repo_root / toml_filename
    toml_path.write_text("""
[tool.autopypath]
paths = ['src', 'lib']
load_strategy = 'prepend'
path_resolution_order = ['manual', 'autopypath', 'pyproject', 'dotenv']
""")
    try:
        TomlConfig(repo_root_path=repo_root, toml_filename=toml_filename, toml_section='tool.autopypath')
    except Exception as e:
        pytest.fail(f'TOML_001 Initialization of TomlConfig failed with exception: {e}')


def test_toml_missing_section(tmp_path: Path) -> None:
    repo_root = tmp_path / 'my_repo'
    repo_root.mkdir()
    toml_filename = 'toml_file.toml'
    toml_path = repo_root / toml_filename
    toml_path.write_text("""
[tool.other_tool]
paths = ['src', 'lib']
""")

    config = TomlConfig(repo_root_path=repo_root, toml_filename=toml_filename, toml_section='tool.autopypath')
    assert config.load_strategy is None, 'TOML_002 Expected load_strategy to be None when section is missing'
    assert config.paths is None, 'TOML_003 Expected paths to be None when section is missing'
    assert config.path_resolution_order is None, (
        'TOML_004 Expected path_resolution_order to be None when section is missing'
    )
    assert config.repo_markers is None, 'TOML_005 Expected marker_files to be None when section is missing'


def test_toml_missing_file(tmp_path: Path) -> None:
    repo_root = tmp_path / 'my_repo'
    repo_root.mkdir()
    toml_filename = 'non_existent.toml'

    try:
        TomlConfig(repo_root_path=repo_root, toml_filename=toml_filename, toml_section='tool.autopypath')
    except FileNotFoundError:
        return
    pytest.fail('TOML_006 Expected FileNotFoundError when TOML file does not exist')
