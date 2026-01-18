"""Tests for :mod:`autopypath._config_py_path._config_py_path`."""

from collections.abc import Sequence
import logging
from pathlib import Path
import sys

import pytest

from autopypath._config_py_path._config_py_path import _ConfigPyPath, _EMPTY_AUTOPYPATH_CONFIG
from autopypath.types._no_path import _NoPath
from autopypath import _defaults as defaults

_ORIGINAL_SYS_PATH: list[str] = sys.path.copy()
_ORIGINAL_NAME: str = __name__


def setup_function() -> None:
    """Setup function to reset sys.path before each test."""
    sys.path = _ORIGINAL_SYS_PATH.copy()


def teardown_function() -> None:
    """Teardown function to reset sys.path after each test."""
    sys.path = _ORIGINAL_SYS_PATH.copy()


def test_empty_autopypath_config() -> None:
    """Tests the special empty AutopypathConfig instance."""
    assert isinstance(_EMPTY_AUTOPYPATH_CONFIG.toml_filepath, _NoPath), (
        'EMPTY_AUTO_001 _EMPTY_AUTOPYPATH_CONFIG.toml_filepath should be a _NoPath instance'
    )
    assert _EMPTY_AUTOPYPATH_CONFIG.repo_markers is None, (
        'EMPTY_AUTO_002 _EMPTY_AUTOPYPATH_CONFIG.repo_markers should be None'
    )
    assert _EMPTY_AUTOPYPATH_CONFIG.paths is None, 'EMPTY_AUTO_003 _EMPTY_AUTOPYPATH_CONFIG.paths should be None'
    assert _EMPTY_AUTOPYPATH_CONFIG.load_strategy is None, (
        'EMPTY_AUTO_004 _EMPTY_AUTOPYPATH_CONFIG.load_strategy should be None'
    )
    assert _EMPTY_AUTOPYPATH_CONFIG.path_resolution_order is None, (
        'EMPTY_AUTO_005 _EMPTY_AUTOPYPATH_CONFIG.path_resolution_order should be None'
    )


def test_configured_autopypath_config(tmp_path: Path) -> None:
    """Tests that _ConfigPyPath.autopypath_config returns the correct configuration
    when an autopypath.toml file exists in the root of the repository.

    We want to test various combinations of existing and non-existing paths
    specified in the autopypath.toml file.

    'src' exists, 'tests' does not exist.

    Uses a temporary directory to simulate a repository with an autopypath.toml file.
    """
    root_path = tmp_path / 'repo'
    root_path.mkdir()
    root_path.joinpath('some_file.txt').write_text('Just a test file.')
    src_path = root_path / 'src'
    src_path.mkdir()
    git_path = root_path / '.git'
    git_path.mkdir()
    autopypath_path = root_path / 'autopypath.toml'
    # Note: only "src" exists, "tests" does not exist
    autopypath_path.write_text("""
[tool.autopypath]
load_strategy = "replace"
path_resolution_order = ["manual", "autopypath", "pyproject", "dotenv"]
repo_markers = {".git" = "dir", "setup.py" = "file"}
paths=["src", "tests"]
""")
    config = _ConfigPyPath(
        context_file=str(root_path / 'some_file.txt'),
        dry_run=True,
    )
    autopypath_config = config.autopypath_config
    assert autopypath_config.load_strategy == 'replace', (
        'AUTOPYPATH_CONFIGURED_001 autopypath_config.load_strategy should be LoadStrategy.REPLACE'
    )
    assert autopypath_config.path_resolution_order == (
        'manual',
        'autopypath',
        'pyproject',
        'dotenv',
    ), (
        'AUTOPYPATH_CONFIGURED_002 autopypath_config.path_resolution_order should match the configured '
        ' path resolution order: ["manual", "autopypath", "pyproject", "dotenv"]'
    )
    assert autopypath_config.repo_markers == {'.git': 'dir', 'setup.py': 'file'}, (
        'AUTOPYPATH_CONFIGURED_003 autopypath_config.repo_markers should match the configured repo markers'
    )
    if isinstance(autopypath_config.paths, Sequence):
        assert len(autopypath_config.paths) == 2, (
            'AUTOPYPATH_CONFIGURED_004 autopypath_config.paths should '
            'have length 2 because src and tests were configured'
        )
        assert str(autopypath_config.paths[0].name) == 'src', (
            'AUTOPYPATH_CONFIGURED_005 autopypath_config.paths should match the configured paths'
        )
        assert autopypath_config.paths[0].is_dir(), (
            'AUTOPYPATH_CONFIGURED_006 autopypath_config.paths[0] should be match the path to src directory'
        )
        assert src_path.resolve() == autopypath_config.paths[0].resolve(), (
            'AUTOPYPATH_CONFIGURED_007 autopypath_config.paths[0] should resolve to the src directory path'
        )
    else:
        pytest.fail('AUTOPYPATH_CONFIGURED_008 autopypath_config.paths should be a list')


def test_default_config(tmp_path: Path) -> None:
    """Tests that _ConfigPyPath.autopypath_config returns the special empty config when appropriate.
    Uses a temporary directory to simulate a repository without any autopypath configuration
    and a pyproject.toml file to mark the root.
    """
    root_path = tmp_path / 'repo'
    root_path.mkdir()
    root_path.joinpath('some_file.txt').write_text('Just a test file.')
    pyproject_path = root_path / 'pyproject.toml'
    pyproject_path.write_text("""
[tool.some_other_tool]
""")

    config = _ConfigPyPath(
        context_file=str(root_path / 'some_file.txt'),
        dry_run=True,
    )

    default_config = config.default_config
    assert default_config.load_strategy == defaults._LOAD_STRATEGY, (
        'DEFAULT_CONFIG_001 default_config.load_strategy should match defaults._LOAD_STRATEGY'
    )
    assert default_config.path_resolution_order == defaults._PATH_RESOLUTION_ORDER, (
        'DEFAULT_CONFIG_002 default_config.path_resolution_order should match defaults._PATH_RESOLUTION_ORDER'
    )
    assert default_config.repo_markers == defaults._REPO_MARKERS, (
        'DEFAULT_CONFIG_003 default_config.repo_markers should match defaults._REPO_MARKERS'
    )
    assert default_config.paths == defaults._PATHS


def test_no_pyproject_toml_file(tmp_path: Path) -> None:
    """Tests that _ConfigPyPath.pyproject_config returns an empty config when
    no pyproject.toml configuration file exists

    Uses a temporary directory to simulate a repository with an empty autopypath config in pyproject.toml.
    """
    root_path = tmp_path / 'repo'
    root_path.mkdir()
    root_path.joinpath('some_file.txt').write_text('Just a test file.')
    git_path = root_path / '.git'
    git_path.mkdir()

    config = _ConfigPyPath(
        context_file=str(root_path / 'some_file.txt'),
        dry_run=True,
    )

    pyproject_config = config.pyproject_config
    assert pyproject_config.load_strategy is None, 'NO_PYPROJECT_FILE_001 pyproject_config.load_strategy should be None'
    assert pyproject_config.path_resolution_order is None, (
        'NO_PYPROJECT_FILE_002 pyproject_config.path_resolution_order should be None'
    )
    assert pyproject_config.repo_markers is None, 'NO_PYPROJECT_FILE_003 pyproject_config.repo_markers should be None'
    assert pyproject_config.paths is None, 'NO_PYPROJECT_FILE_004 pyproject_config.paths should be None'


def test_empty_pyproject_config(tmp_path: Path) -> None:
    """Tests that _ConfigPyPath.pyproject_config returns an empty config when pyproject.toml
    exists but has no autopypath configuration.

    Uses a temporary directory to simulate a repository with an empty autopypath config in pyproject.toml.
    """
    root_path = tmp_path / 'repo'
    root_path.mkdir()
    root_path.joinpath('some_file.txt').write_text('Just a test file.')
    pyproject_path = root_path / 'pyproject.toml'
    pyproject_path.write_text("""
[tool.some_other_tool]
""")
    config = _ConfigPyPath(
        context_file=str(root_path / 'some_file.txt'),
        dry_run=True,
    )

    pyproject_config = config.pyproject_config
    assert pyproject_config.load_strategy is None, (
        'EMPTY_PYPROJECT_CONFIG_001 pyproject_config.load_strategy should be None'
    )
    assert pyproject_config.path_resolution_order is None, (
        'EMPTY_PYPROJECT_CONFIG_002 pyproject_config.path_resolution_order should be None'
    )
    assert pyproject_config.repo_markers is None, (
        'EMPTY_PYPROJECT_CONFIG_003 pyproject_config.repo_markers should be None'
    )
    assert pyproject_config.paths is None, 'EMPTY_PYPROJECT_CONFIG_004 pyproject_config.paths should be None'


def test_configured_pyproject_config(tmp_path: Path) -> None:
    """Tests that _ConfigPyPath.pyproject_config returns the correct configuration
    when a pyproject.toml file exists in the root of the repository.

    We want to test various combinations of existing and non-existing paths
    specified in the autopypath.toml file.

    'src' exists, 'tests' does not exist.

    Uses a temporary directory to simulate a repository with an autopypath.toml file.
    """
    root_path = tmp_path / 'repo'
    root_path.mkdir()
    root_path.joinpath('some_file.txt').write_text('Just a test file.')
    src_path = root_path / 'src'
    src_path.mkdir()
    git_path = root_path / '.git'
    git_path.mkdir()
    pyproject_path = root_path / 'pyproject.toml'
    # Note: only "src" exists, "tests" does not exist
    pyproject_path.write_text("""
[tool.autopypath]
load_strategy = "prepend_highest_priority"
path_resolution_order = ["manual", "autopypath", "pyproject", "dotenv"]
repo_markers = {".git" = "dir", "setup.py" = "file"}
paths=["src", "tests"]
""")
    config = _ConfigPyPath(
        context_file=str(root_path / 'some_file.txt'),
        dry_run=True,
    )
    pyproject_config = config.pyproject_config
    assert pyproject_config.load_strategy == 'prepend_highest_priority', (
        'PYPROJECT_CONFIGURED_001 pyproject_config.load_strategy should be LoadStrategy.PREPEND_HIGHEST_PRIORITY'
    )
    assert pyproject_config.path_resolution_order == (
        'manual',
        'autopypath',
        'pyproject',
        'dotenv',
    ), (
        'PYPROJECT_CONFIGURED_002 pyproject_config.path_resolution_order should match the configured '
        ' path resolution order: ["manual", "autopypath", "pyproject", "dotenv"]'
    )
    assert pyproject_config.repo_markers == {'.git': 'dir', 'setup.py': 'file'}, (
        'PYPROJECT_CONFIGURED_003 pyproject_config.repo_markers should match the configured repo markers'
    )
    if isinstance(pyproject_config.paths, Sequence):
        assert len(pyproject_config.paths) == 2, (
            'PYPROJECT_CONFIGURED_004 pyproject_config.paths should have length 2 because src and tests were configured'
        )
        assert str(pyproject_config.paths[0].name) == 'src', (
            'PYPROJECT_CONFIGURED_005 pyproject_config.paths should match the configured paths'
        )
        assert str(pyproject_config.paths[1].name) == 'tests', (
            'PYPROJECT_CONFIGURED_006 pyproject_config.paths should match the configured paths'
        )
        assert pyproject_config.paths[0].is_dir(), (
            'PYPROJECT_CONFIGURED_007 pyproject_config.paths[0] should be match the path to src directory'
        )
        assert src_path.resolve() == pyproject_config.paths[0].resolve(), (
            'PYPROJECT_CONFIGURED_008 pyproject_config.paths[0] should resolve to the src directory path'
        )
    else:
        pytest.fail('PYPROJECT_CONFIGURED_009 pyproject_config.paths should be a list')


def test_no_autopypath_toml_file(tmp_path: Path) -> None:
    """Tests that _ConfigPyPath.autopypath_config returns the special empty config when
    no autopypath.toml configuration file exists

    Uses a temporary directory to simulate a repository with an empty autopypath config in pyproject.toml.
    """
    root_path = tmp_path / 'repo'
    root_path.mkdir()
    root_path.joinpath('some_file.txt').write_text('Just a test file.')
    pyproject_path = root_path / 'pyproject.toml'
    pyproject_path.write_text("""
[tool.some_other_tool]
""")
    config = _ConfigPyPath(
        context_file=str(root_path / 'some_file.txt'),
        dry_run=True,
    )

    autopypath_config = config.autopypath_config
    assert autopypath_config.load_strategy is None, (
        'NO_AUTOPYPATH_FILE_001 autopypath_config.load_strategy should be None'
    )
    assert autopypath_config.path_resolution_order is None, (
        'NO_AUTOPYPATH_FILE_002 autopypath_config.path_resolution_order should be None'
    )
    assert autopypath_config.repo_markers is None, (
        'NO_AUTOPYPATH_FILE_003 autopypath_config.repo_markers should be None'
    )
    assert autopypath_config.paths is None, 'NO_AUTOPYPATH_FILE_004 autopypath_config.paths should be None'


def test_no_dotenv_file(tmp_path: Path) -> None:
    """Tests that _ConfigPyPath.dotenv_config returns an empty config when
    no .env configuration file exists

    Uses a temporary directory to simulate a repository without a .env file.
    """
    root_path = tmp_path / 'repo'
    root_path.mkdir()
    root_path.joinpath('some_file.txt').write_text('Just a test file.')
    pyproject_path = root_path / 'pyproject.toml'
    pyproject_path.write_text("""
[tool.some_other_tool]
""")
    config = _ConfigPyPath(
        context_file=str(root_path / 'some_file.txt'),
        dry_run=True,
    )
    dotenv_config = config.dotenv_config
    assert dotenv_config.load_strategy is None, 'NO_DOTENV_FILE_001 dotenv_config.load_strategy should be None'
    assert dotenv_config.path_resolution_order is None, (
        'NO_DOTENV_FILE_002 dotenv_config.path_resolution_order should be None'
    )
    assert dotenv_config.repo_markers is None, 'NO_DOTENV_FILE_003 dotenv_config.repo_markers should be None'
    assert dotenv_config.paths is None, 'NO_DOTENV_FILE_004 dotenv_config.paths should be None'


def test_empty_dotenv_config(tmp_path: Path) -> None:
    """Tests that _ConfigPyPath.dotenv_config returns an empty config when .env
    exists but has no PYTHONPATH configuration.

    Uses a temporary directory to simulate a repository with an empty autopypath config in .env.
    """
    root_path = tmp_path / 'repo'
    root_path.mkdir()
    root_path.joinpath('some_file.txt').write_text('Just a test file.')
    pyproject_path = root_path / 'pyproject.toml'
    pyproject_path.write_text("""
[tool.some_other_tool]
""")
    dotenv_path = root_path / '.env'
    dotenv_path.write_text("""
SOME_OTHER_ENV_VAR=some_value
""")
    config = _ConfigPyPath(
        context_file=str(root_path / 'some_file.txt'),
        dry_run=True,
    )
    dotenv_config = config.dotenv_config
    assert dotenv_config.load_strategy is None, 'EMPTY_DOTENV_CONFIG_001 dotenv_config.load_strategy should be None'
    assert dotenv_config.path_resolution_order is None, (
        'EMPTY_DOTENV_CONFIG_002 dotenv_config.path_resolution_order should be None'
    )
    assert dotenv_config.repo_markers is None, 'EMPTY_DOTENV_CONFIG_003 dotenv_config.repo_markers should be None'
    assert dotenv_config.paths is None, 'EMPTY_DOTENV_CONFIG_004 dotenv_config.paths should be None'


def test_configured_dotenv_config(tmp_path: Path) -> None:
    """Tests that _ConfigPyPath.dotenv_config returns the correct configuration
    when a .env file exists in the root of the repository.

    We want to test various combinations of existing and non-existing paths
    specified in the .env file.

    'src' exists, 'tests' does not exist.

    Uses a temporary directory to simulate a repository with an autopypath.toml file.
    """
    root_path = tmp_path / 'repo'
    root_path.mkdir()
    root_path.joinpath('some_file.txt').write_text('Just a test file.')
    src_path = root_path / 'src'
    src_path.mkdir()
    git_path = root_path / '.git'
    git_path.mkdir()
    dotenv_path = root_path / '.env'
    # Note: only "src" exists, "tests" does not exist
    dotenv_path.write_text("""
PYTHONPATH=src:tests
""")
    config = _ConfigPyPath(
        context_file=str(root_path / 'some_file.txt'),
        dry_run=True,
    )
    dotenv_config = config.dotenv_config
    assert dotenv_config.load_strategy is None, 'DOTENV_CONFIGURED_001 dotenv_config.load_strategy should be None'
    assert dotenv_config.path_resolution_order is None, (
        'DOTENV_CONFIGURED_002 dotenv_config.path_resolution_order should be None'
    )
    assert dotenv_config.repo_markers is None, 'DOTENV_CONFIGURED_003 dotenv_config.repo_markers should be None'
    if isinstance(dotenv_config.paths, Sequence):
        assert len(dotenv_config.paths) == 2, (
            'DOTENV_CONFIGURED_004 dotenv_config.paths should have length 2 '
            f'because src and tests were configured: {dotenv_config.paths}'
        )
        assert str(dotenv_config.paths[0].name) == 'src', (
            'DOTENV_CONFIGURED_005 dotenv_config.paths should match the configured paths'
        )
        assert str(dotenv_config.paths[1].name) == 'tests', (
            'DOTENV_CONFIGURED_006 dotenv_config.paths should match the configured paths'
        )
        assert dotenv_config.paths[0].is_dir(), (
            'DOTENV_CONFIGURED_007 dotenv_config.paths[0] should be match the path to src directory'
        )
        assert src_path.resolve() == dotenv_config.paths[0].resolve(), (
            'DOTENV_CONFIGURED_008 dotenv_config.paths[0] should resolve to the src directory path'
        )
    else:
        pytest.fail('DOTENV_CONFIGURED_009 dotenv_config.paths should be a list')


def test_manual_config(tmp_path: Path) -> None:
    """Tests that _ConfigPyPath.manual_config returns an empty config when no manual
    configuration is provided.

    Uses a temporary directory to simulate a repository without any manual configuration.
    """
    root_path = tmp_path / 'repo'
    root_path.mkdir()
    root_path.joinpath('some_file.txt').write_text('Just a test file.')
    hg_path = root_path / '.hg'
    hg_path.mkdir()

    config = _ConfigPyPath(
        context_file=str(root_path / 'some_file.txt'),
        dry_run=True,
        load_strategy='prepend',
        path_resolution_order=['manual', 'autopypath'],
        paths=['src', 'tests'],
        repo_markers={'.hg': 'dir'},
    )

    manual_config = config.manual_config
    assert manual_config.load_strategy, 'MANUAL_CONFIG_001 manual_config.load_strategy should not be None'
    assert manual_config.path_resolution_order, (
        'MANUAL_CONFIG_002 manual_config.path_resolution_order should not be None'
    )
    assert isinstance(manual_config.paths, Sequence), 'MANUAL_CONFIG_003 manual_config.paths should be a Sequence'
    assert manual_config.repo_markers == {'.hg': 'dir'}, (
        'MANUAL_CONFIG_004 manual_config.repo_markers should match the provided manual configuration'
    )

    if isinstance(manual_config.paths, Sequence):
        assert len(manual_config.paths) == 2, (
            'MANUAL_CONFIG_005 manual_config.paths should have length 2 because src and tests were provided'
        )
        assert str(manual_config.paths[0].name) == 'src', (
            'MANUAL_CONFIG_006 manual_config.paths should match the provided manual configuration paths'
        )
        assert str(manual_config.paths[1].name) == 'tests', (
            'MANUAL_CONFIG_007 manual_config.paths should match the provided manual configuration paths'
        )
    else:
        pytest.fail('MANUAL_CONFIG_008 manual_config.paths should be a list')


def test_replace_strategy_live(tmp_path: Path) -> None:
    """
    Performs live tests of the 'replace' load strategy.

    Default sys.path is preserved and restored after the test.

    :param Path tmp_path: Path to a temporary directory for testing.
    """
    root_path = tmp_path / 'repo'
    root_path.mkdir()
    context_file = root_path / 'some_file.txt'
    context_file.write_text('Just a test file.')
    vcs_path = root_path / '.vcs'
    vcs_path.mkdir()

    # src and tests do not exist - expect RuntimeError
    sys_path_before: list[str] = sys.path.copy()
    try:
        _ConfigPyPath(
            context_file=str(root_path / 'some_file.txt'),
            load_strategy='replace',
            path_resolution_order=['manual'],
            paths=['src', 'tests'],
            repo_markers={'.vcs': 'dir'},
        )
        pytest.fail('REPLACE_STRATEGY_LIVE_001 Expected RuntimeError because no paths exist to replace sys.path')

    except RuntimeError:
        pass  # Expected because paths do not exist at all
    finally:
        sys.path = sys_path_before

    # Create the 'src' directory so one of the paths exists
    try:
        src_path = root_path / 'src'
        src_path.mkdir()

        _ConfigPyPath(
            context_file=str(root_path / 'some_file.txt'),
            load_strategy='replace',
            path_resolution_order=['manual'],
            paths=['src', 'tests'],
            repo_markers={'.vcs': 'dir'},
        )

        assert len(sys.path) == 1, (
            'REPLACE_STRATEGY_LIVE_002 sys.path should have length 1 after replace strategy is applied'
        )
        assert sys.path[0] == str(src_path.resolve()), (
            'REPLACE_STRATEGY_LIVE_003 sys.path[0] should be the src directory path'
        )
    finally:
        sys.path = sys_path_before


def test_strict(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    """Tests that _ConfigPyPath raises RuntimeError in strict mode
    when no valid paths are found to add to sys.path for non-replace
    load strategies.

    Uses a temporary directory to simulate a repository with an autopypath.toml file.
    """
    root_path = tmp_path / 'repo'
    root_path.mkdir()
    root_path.joinpath('some_file.txt').write_text('Just a test file.')
    git_path = root_path / '.git'
    git_path.mkdir()
    autopypath_path = root_path / 'autopypath.toml'
    # Note: both "src" and "tests" do not exist
    autopypath_path.write_text("""
[tool.autopypath]
load_strategy = "prepend"
path_resolution_order = ["manual", "autopypath", "pyproject", "dotenv"]
repo_markers = {".git" = "dir"}
paths=["src", "tests"]
""")
    try:
        _ConfigPyPath(
            context_file=str(root_path / 'some_file.txt'),
            dry_run=True,
            strict=True,
        )
        pytest.fail('STRICT_001 Expected RuntimeError because no paths exist and strict mode is enabled')
    except RuntimeError:
        pass  # Expected because paths do not exist

    # Now test that a warning is logged for non-strict mode
    caplog.clear()
    _ConfigPyPath(
        context_file=str(root_path / 'some_file.txt'),
        dry_run=True,
        strict=False,
    )
    warning_messages = [record.message for record in caplog.records if record.levelno == logging.WARNING]
    assert any(
        'autopypath: No valid paths to add to sys.path after processing.' in message for message in warning_messages
    ), 'STRICT_002 Expected a warning about no valid paths to add to sys.path in non-strict mode'
