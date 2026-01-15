"""Tests for autopypath._config_py_path._config."""

import pytest

from testspec import TestSpec, idspec, TestAction

from autopypath._config_py_path._config import Config
from autopypath.marker_type import MarkerType

# fmt: off

@pytest.mark.parametrize(
    'testspec', [
        idspec('MARKER_001', TestAction(
            name='Create Config with valid repo_markers',
            action=Config,
            kwargs={'repo_markers': {'.git': MarkerType.DIR, 'pyproject.toml': MarkerType.FILE}},
            validate_result=lambda result: (
                result.repo_markers == {'.git': MarkerType.DIR, 'pyproject.toml': MarkerType.FILE}))),
        idspec('MARKER_002', TestAction(
            name='Create Config with empty repo_markers',
            action=Config,
            kwargs={'repo_markers': {}},
            validate_result=lambda result: result.repo_markers == {})),
        idspec('MARKER_003', TestAction(
            name='Create Config with single repo_marker',
            action=Config,
            kwargs={'repo_markers': {'setup.py': MarkerType.FILE}},
            validate_result=lambda result: result.repo_markers == {'setup.py': MarkerType.FILE})),
        idspec('MARKER_004', TestAction(
            name='Create Config with string repo_markers',
            action=Config,
            kwargs={'repo_markers': {'.git': 'dir', 'setup.py': 'file'}},
            validate_result=lambda result: (
                result.repo_markers == {'.git': MarkerType.DIR, 'setup.py': MarkerType.FILE}))),
        idspec('MARKER_005', TestAction(
            name='Create Config with mixed type repo_markers',
            action=Config,
            kwargs={'repo_markers': {'.git': MarkerType.DIR, 'setup.py': 'file'}},
            validate_result=lambda result: (
                result.repo_markers == {'.git': MarkerType.DIR, 'setup.py': MarkerType.FILE}))),
        idspec('MARKER_006', TestAction(
            name='Create Config with invalid repo_marker',
            action=Config,
            kwargs={'repo_markers': {'.git': 'DIR'}},
            exception=ValueError)),
        idspec('MARKER_007', TestAction(
            name='Create Config with invalid repo_marker type',
            action=Config,
            kwargs={'repo_markers': {'.git': 123}},
            exception=TypeError)),
        idspec('MARKER_008', TestAction(
            name='Create Config with None repo_markers',
            action=Config,
            kwargs={'repo_markers': None},
            validate_result=lambda result: result.repo_markers is None)),
        idspec('MARKER_009', TestAction(
            name='Create Config with no repo_markers',
            action=Config,
            kwargs={},
            validate_result=lambda result: result.repo_markers is None)),
    ],
)
def test_repo_markers_valid(testspec: TestSpec) -> None:
    """Test Config with valid repo_markers."""
    testspec.run()

# fmt: on

if __name__ == '__main__':
    pytest.main()
