"""Tests for autopypath._config_py_path._config._manual module.

The Manual config class is just no changes subclass of
the base Config class, so this test just verifies that the
class can be instantiated as ManualConfig and is a subclass
of Config.

All the real logic is tested in tests/_config_py_path/test_config.py
"""

from autopypath._config_py_path._config import _Config, _DefaultConfig
from autopypath import _defaults


def test_default_config_init() -> None:
    """Test that DefaultConfig can be instantiated with default parameters."""
    config = _DefaultConfig()

    assert isinstance(config, _DefaultConfig), 'DEFAULT_001 Failed to instantiate DefaultConfig'
    assert issubclass(_DefaultConfig, _Config), 'DEFAULT_002 DefaultConfig is not a subclass of Config'
    assert config.load_strategy == _defaults._LOAD_STRATEGY, 'DEFAULT_003 Load strategy does not match default'
    assert config.paths == _defaults._PATHS, 'DEFAULT_004 Paths do not match default'
    assert config.repo_markers == _defaults._REPO_MARKERS, 'DEFAULT_005 Repo markers do not match default'
    assert config.path_resolution_order == _defaults._PATH_RESOLUTION_ORDER, (
        'DEFAULT_006 Path resolution order does not match default'
    )
