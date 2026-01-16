"""Tests for the PyProjectConfig class in autopypath._config_py_path._config._pyproject module.

PyProjectConfig is responsible for loading autopypath configuration from pyproject.toml files.

It is a thin subclass of TomlConfig that specifies the correct filename and section for pyproject.toml.

Since the main logic is in TomlConfig, these tests just ensure that PyProjectConfig inherits and
initializes correctly and that __repr__ and __str__ methods work as expected for the subclass.
"""

from pathlib import Path

from autopypath._config_py_path._config._config import Config
from autopypath._config_py_path._config._pyproject import PyProjectConfig
from autopypath._config_py_path._config._toml import TomlConfig


def test_pyproject_config_init(tmp_path: Path) -> None:
    pyproject_path = tmp_path / 'pyproject.toml'
    pyproject_path.write_text("""
[tool.autopypath]
""")
    config = PyProjectConfig(repo_root_path=tmp_path)
    assert isinstance(config, PyProjectConfig), 'PYPROJECT_001 Expected config to be an instance of PyProjectConfig'
    assert isinstance(config, TomlConfig), 'PYPROJECT_002 Expected config to be an instance of TomlConfig'
    assert isinstance(config, Config), 'PYPROJECT_003 Expected config to be an instance of Config'
    assert config.repo_markers is None, 'PYPROJECT_004 Expected repo_markers to be None for empty config'
    assert config.paths is None, 'PYPROJECT_005 Expected paths to be None for empty config'
    assert config.load_strategy is None, 'PYPROJECT_006 Expected load_strategy to be None for empty config'
    assert config.path_resolution_order is None, (
        'PYPROJECT_007 Expected path_resolution_order to be None for empty config'
    )


def test_pyproject_config_repr(tmp_path: Path) -> None:
    pyproject_path = tmp_path / 'pyproject.toml'
    pyproject_path.write_text("""
[tool.autopypath]
""")
    config = PyProjectConfig(repo_root_path=tmp_path)
    expected_repr = f'PyProjectConfig(repo_root_path={str(tmp_path)!r})'
    assert repr(config) == expected_repr, 'PYPROJECT_008 __repr__ output does not match expected format'

    new_config = eval(repr(config))
    assert new_config == config, 'PYPROJECT_009 Evaluated __repr__ output does not produce equal object value'


def test_pyproject_config_str(tmp_path: Path) -> None:
    pyproject_path = tmp_path / 'pyproject.toml'
    pyproject_path.write_text("""
[tool.autopypath]
""")
    config = PyProjectConfig(repo_root_path=tmp_path)
    expected_str = f'PyProjectConfig(repo_root_path={str(tmp_path)!r})'
    assert str(config) == expected_str, 'PYPROJECT_010 __str__ output does not match expected format'
