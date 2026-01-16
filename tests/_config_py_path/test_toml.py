from pathlib import Path

import pytest

from autopypath._config_py_path._config._toml import TomlConfig
from autopypath.marker_type import MarkerType


def test_toml_config_init(tmp_path: Path) -> None:
    repo_root = tmp_path / 'my_repo'
    repo_root.mkdir()
    marker_file = repo_root / 'filename.txt'
    marker_file.touch()
    marker_dir = repo_root / 'dirname'
    marker_dir.mkdir()
    (repo_root / 'src').mkdir()  # One of the two default paths so we can test both with and without presence
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


def test_toml_invalid_repo_marker_syntax(tmp_path: Path) -> None:
    repo_root = tmp_path / 'my_repo'
    repo_root.mkdir()
    toml_filename = 'toml_file.toml'
    toml_path = repo_root / toml_filename
    toml_path.write_text("""
[tool.autopypath]
repo_markers = 'should_be_a_table_not_a_string'
""")
    try:
        TomlConfig(repo_root_path=repo_root, toml_filename=toml_filename, toml_section='tool.autopypath')
    except TypeError:
        return
    pytest.fail('TOML_007 Expected TypeError when repo_markers has invalid syntax')


def test_toml_invalid_path_resolution_order_value(tmp_path: Path) -> None:
    repo_root = tmp_path / 'my_repo'
    repo_root.mkdir()
    toml_filename = 'toml_file.toml'
    toml_path = repo_root / toml_filename
    toml_path.write_text("""
[tool.autopypath]
path_resolution_order = ['invalid_value']
""")
    try:
        TomlConfig(repo_root_path=repo_root, toml_filename=toml_filename, toml_section='tool.autopypath')
    except ValueError:
        return
    pytest.fail('TOML_008 Expected ValueError when path_resolution_order has an invalid value')


def test_toml_invalid_load_strategy_value(tmp_path: Path) -> None:
    repo_root = tmp_path / 'my_repo'
    repo_root.mkdir()
    toml_filename = 'toml_file.toml'
    toml_path = repo_root / toml_filename
    toml_path.write_text("""
[tool.autopypath]
load_strategy = 'invalid_strategy'
""")
    try:
        TomlConfig(repo_root_path=repo_root, toml_filename=toml_filename, toml_section='tool.autopypath')
    except ValueError:
        return
    pytest.fail('TOML_009 Expected ValueError when load_strategy has an invalid value')


def test_toml_invalid_load_strategy_syntax(tmp_path: Path) -> None:
    repo_root = tmp_path / 'my_repo'
    repo_root.mkdir()
    toml_filename = 'toml_file.toml'
    toml_path = repo_root / toml_filename
    toml_path.write_text("""
[tool.autopypath]
load_strategy = ['should_be_a_string_not_a_list']
""")
    try:
        TomlConfig(repo_root_path=repo_root, toml_filename=toml_filename, toml_section='tool.autopypath')
    except TypeError:
        return
    pytest.fail('TOML_010 Expected TypeError when load_strategy has invalid syntax')


def test_toml_invalid_paths_syntax(tmp_path: Path) -> None:
    repo_root = tmp_path / 'my_repo'
    repo_root.mkdir()
    toml_filename = 'toml_file.toml'
    toml_path = repo_root / toml_filename
    toml_path.write_text("""
[tool.autopypath]
paths = 'should_be_a_list_not_a_string'
""")
    try:
        TomlConfig(repo_root_path=repo_root, toml_filename=toml_filename, toml_section='tool.autopypath')
    except TypeError:
        return
    pytest.fail('TOML_011 Expected TypeError when paths has invalid syntax')


def test_toml_invalid_repo_markers_value(tmp_path: Path) -> None:
    repo_root = tmp_path / 'my_repo'
    repo_root.mkdir()
    toml_filename = 'toml_file.toml'
    toml_path = repo_root / toml_filename
    toml_path.write_text("""
[tool.autopypath]
repo_markers = {'.git': 'should_be_MarkerType_not_general_string'}
""")
    try:
        TomlConfig(repo_root_path=repo_root, toml_filename=toml_filename, toml_section='tool.autopypath')
    except ValueError:
        return
    pytest.fail('TOML_012 Expected ValueError when repo_markers has an invalid value')


def test_toml_invalid_paths_value(tmp_path: Path) -> None:
    repo_root = tmp_path / 'my_repo'
    repo_root.mkdir()
    toml_filename = 'toml_file.toml'
    toml_path = repo_root / toml_filename
    toml_path.write_text("""
[tool.autopypath]
paths = ['src', 123]
""")
    try:
        TomlConfig(repo_root_path=repo_root, toml_filename=toml_filename, toml_section='tool.autopypath')
    except TypeError:
        return
    pytest.fail('TOML_013 Expected TypeError when paths has an invalid type of value')


def test_toml_invalid_path_resolution_order_syntax(tmp_path: Path) -> None:
    repo_root = tmp_path / 'my_repo'
    repo_root.mkdir()
    toml_filename = 'toml_file.toml'
    toml_path = repo_root / toml_filename
    toml_path.write_text("""
[tool.autopypath]
path_resolution_order = 'should_be_a_list_not_a_string'
""")
    try:
        TomlConfig(repo_root_path=repo_root, toml_filename=toml_filename, toml_section='tool.autopypath')
    except TypeError:
        return
    pytest.fail('TOML_014 Expected TypeError when path_resolution_order has invalid syntax')


def test_toml_invalid_repo_markers_filename_type(tmp_path: Path) -> None:
    repo_root = tmp_path / 'my_repo'
    repo_root.mkdir()
    toml_filename = 'toml_file.toml'
    toml_path = repo_root / toml_filename
    toml_path.write_text("""
[tool.autopypath]
repo_markers = {123='DIR'}
""")
    try:
        TomlConfig(repo_root_path=repo_root, toml_filename=toml_filename, toml_section='tool.autopypath')
    except ValueError:
        return
    pytest.fail('TOML_015 Expected ValueError when repo_markers has an invalid type for the filename')


def test_toml_invalid_repo_markers_filename_value(tmp_path: Path) -> None:
    repo_root = tmp_path / 'my_repo'
    repo_root.mkdir()
    toml_filename = 'toml_file.toml'
    toml_path = repo_root / toml_filename
    toml_path.write_text("""
[tool.autopypath]
repo_markers = {'*invalid*': 'DIR'}
""")
    try:
        TomlConfig(repo_root_path=repo_root, toml_filename=toml_filename, toml_section='tool.autopypath')
    except ValueError:
        return
    pytest.fail('TOML_016 Expected ValueError when repo_markers has an invalid filename value')


def test_toml_misconfigured_section_name(tmp_path: Path) -> None:
    repo_root = tmp_path / 'my_repo'
    repo_root.mkdir()
    toml_filename = 'toml_file.toml'
    toml_path = repo_root / toml_filename
    toml_path.write_text("""
[tool.autopypath]
paths = ['src', 'lib']
""")
    try:
        TomlConfig(repo_root_path=repo_root, toml_filename=toml_filename, toml_section='tool..autopypath')
    except ValueError:
        return
    pytest.fail('TOML_017 Expected ValueError when toml_section has an invalid syntax')


def test_toml_incorrect_section_table_syntax(tmp_path: Path) -> None:
    repo_root = tmp_path / 'my_repo'
    repo_root.mkdir()
    toml_filename = 'toml_file.toml'
    toml_path = repo_root / toml_filename
    toml_path.write_text("""

[tool]

autopypath = 'hello'

""")
    try:
        TomlConfig(repo_root_path=repo_root, toml_filename=toml_filename, toml_section='tool.autopypath')
    except TypeError:
        return
    pytest.fail('TOML_018 Expected ValueError when toml_section is misdefined in the TOML file')


def test_toml_repo_markers_table_syntax(tmp_path: Path) -> None:
    repo_root = tmp_path / 'my_repo'
    repo_root.mkdir()
    toml_filename = 'toml_file.toml'
    toml_path = repo_root / toml_filename
    toml_path.write_text("""
[tool.autopypath]
repo_markers = ['.git', 'DIR', 'setup.py', 'FILE']
""")
    try:
        TomlConfig(repo_root_path=repo_root, toml_filename=toml_filename, toml_section='tool.autopypath')
    except TypeError:
        return
    pytest.fail('TOML_019 Expected TypeError when repo_markers is not a table/dictionary')


def test_toml_repo_markers_table_value_type(tmp_path: Path) -> None:
    repo_root = tmp_path / 'my_repo'
    repo_root.mkdir()
    toml_filename = 'toml_file.toml'
    toml_path = repo_root / toml_filename
    toml_path.write_text("""
[tool.autopypath]
repo_markers = {'.git'=['should_be_string_not_list']}
""")
    try:
        config = TomlConfig(repo_root_path=repo_root, toml_filename=toml_filename, toml_section='tool.autopypath')
        pytest.fail(f'TOML_020 Expected TypeError when repo_markers has non-string value type: {config.repo_markers}')
    except TypeError:
        pass


def test_toml_repr(tmp_path: Path) -> None:
    repo_root = tmp_path / 'my_repo'
    repo_root.mkdir()
    toml_filename = 'toml_file.toml'
    toml_path = repo_root / toml_filename
    toml_path.write_text("""[tool.autopypath]
paths = ['src', 'lib']
""")
    config = TomlConfig(repo_root_path=repo_root, toml_filename=toml_filename, toml_section='tool.autopypath')
    repr_str = repr(config)
    assert 'TomlConfig' in repr_str, 'TOML_021 Expected __repr__ to contain class name'
    assert 'paths' in repr_str, 'TOML_022 Expected __repr__ to contain paths attribute'
    assert 'repo_markers' in repr_str, 'TOML_023 Expected __repr__ to contain repo_markers attribute'
    assert 'load_strategy' in repr_str, 'TOML_024 Expected __repr__ to contain load_strategy attribute'
    assert 'path_resolution_order' in repr_str, 'TOML_025 Expected __repr__ to contain path_resolution_order attribute'
    try:
        round_trip_config = eval(repr_str)
    except Exception as e:
        pytest.fail(f'TOML_026 Expected __repr__ to be evaluable without exception, but got: {e}\nRepr: {repr_str}')
    assert round_trip_config == config, (
        f'TOML_027 Expected __repr__ to be evaluable to the same object value: {repr_str}'
    )


def test_toml_str(tmp_path: Path) -> None:
    repo_root = tmp_path / 'my_repo'
    repo_root.mkdir()
    toml_filename = 'toml_file.toml'
    toml_path = repo_root / toml_filename
    toml_path.write_text("""[tool.autopypath]
paths = ['src', 'lib']
""")
    config = TomlConfig(repo_root_path=repo_root, toml_filename=toml_filename, toml_section='tool.autopypath')
    str_repr = str(config)
    assert 'TomlConfig' in str_repr, 'TOML_028 Expected __str__ to contain class name'
    assert 'paths' in str_repr, 'TOML_029 Expected __str__ to contain paths attribute'
    assert 'repo_markers' in str_repr, 'TOML_030 Expected __str__ to contain repo_markers attribute'
    assert 'load_strategy' in str_repr, 'TOML_031 Expected __str__ to contain load_strategy attribute'
    assert 'path_resolution_order' in str_repr, 'TOML_032 Expected __str__ to contain path_resolution_order attribute'


def test_toml_good_repo_markers(tmp_path: Path) -> None:
    repo_root = tmp_path / 'my_repo'
    repo_root.mkdir()
    toml_filename = 'toml_file.toml'
    toml_path = repo_root / toml_filename
    toml_path.write_text("""
[tool.autopypath]
repo_markers = {'.git'='dir', 'setup.py'='file'}
""")
    try:
        config = TomlConfig(repo_root_path=repo_root, toml_filename=toml_filename, toml_section='tool.autopypath')
    except Exception as e:
        pytest.fail(f'TOML_033 Initialization of TomlConfig with valid repo_markers failed with exception: {e}')
    assert config.repo_markers == {'.git': MarkerType.DIR, 'setup.py': MarkerType.FILE}, (
        f'TOML_034 Expected repo_markers to be correctly parsed, got: {config.repo_markers}'
    )
