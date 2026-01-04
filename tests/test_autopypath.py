"""Tests for autopypath module."""

import os
import sys
import tempfile
from pathlib import Path
import pytest

import autopypath


def test_version():
    """Test that version is defined."""
    assert hasattr(autopypath, '__version__')
    assert isinstance(autopypath.__version__, str)


def test_find_repo_root_with_git(tmp_path):
    """Test finding repo root with .git marker."""
    # Create a fake repo structure
    repo_root = tmp_path / "myrepo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()
    
    subdir = repo_root / "src" / "submodule"
    subdir.mkdir(parents=True)
    
    # Test from subdirectory
    found_root = autopypath.find_repo_root(str(subdir))
    assert found_root == repo_root


def test_find_repo_root_with_setup_py(tmp_path):
    """Test finding repo root with setup.py marker."""
    repo_root = tmp_path / "myproject"
    repo_root.mkdir()
    (repo_root / "setup.py").touch()
    
    subdir = repo_root / "src"
    subdir.mkdir()
    
    found_root = autopypath.find_repo_root(str(subdir))
    assert found_root == repo_root


def test_find_repo_root_with_pyproject_toml(tmp_path):
    """Test finding repo root with pyproject.toml marker."""
    repo_root = tmp_path / "myproject"
    repo_root.mkdir()
    (repo_root / "pyproject.toml").touch()
    
    subdir = repo_root / "lib" / "module"
    subdir.mkdir(parents=True)
    
    found_root = autopypath.find_repo_root(str(subdir))
    assert found_root == repo_root


def test_find_repo_root_with_tox_ini(tmp_path):
    """Test finding repo root with tox.ini marker."""
    repo_root = tmp_path / "myproject"
    repo_root.mkdir()
    (repo_root / "tox.ini").touch()
    
    subdir = repo_root / "tests"
    subdir.mkdir()
    
    found_root = autopypath.find_repo_root(str(subdir))
    assert found_root == repo_root


def test_find_repo_root_not_found(tmp_path):
    """Test when repo root cannot be found."""
    subdir = tmp_path / "random" / "dir"
    subdir.mkdir(parents=True)
    
    found_root = autopypath.find_repo_root(str(subdir))
    # Should return None when no markers found
    assert found_root is None


def test_find_repo_root_custom_markers(tmp_path):
    """Test finding repo root with custom markers."""
    repo_root = tmp_path / "myproject"
    repo_root.mkdir()
    (repo_root / "custom.marker").touch()
    
    subdir = repo_root / "src"
    subdir.mkdir()
    
    found_root = autopypath.find_repo_root(str(subdir), markers=["custom.marker"])
    assert found_root == repo_root


def test_add_repo_to_path(tmp_path):
    """Test adding repo to path."""
    repo_root = tmp_path / "myrepo"
    repo_root.mkdir()
    
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        result = autopypath.add_repo_to_path(repo_root)
        assert result == repo_root
        assert str(repo_root) in sys.path
        # Should be at the beginning
        assert sys.path[0] == str(repo_root)
    finally:
        # Restore original sys.path
        sys.path[:] = original_path


def test_add_repo_to_path_already_present(tmp_path):
    """Test that path isn't duplicated if already present."""
    repo_root = tmp_path / "myrepo"
    repo_root.mkdir()
    
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Add once
        autopypath.add_repo_to_path(repo_root)
        path_len_1 = len(sys.path)
        
        # Add again
        autopypath.add_repo_to_path(repo_root)
        path_len_2 = len(sys.path)
        
        # Length should be the same
        assert path_len_1 == path_len_2
    finally:
        # Restore original sys.path
        sys.path[:] = original_path


def test_add_repo_to_path_none_root():
    """Test add_repo_to_path when root cannot be found."""
    # This will try to auto-detect, which should work for this test file
    # since we're in a repo with setup.py
    result = autopypath.add_repo_to_path()
    # Should find the repo root
    assert result is not None


def test_auto_path():
    """Test the convenience auto_path function."""
    original_path = sys.path.copy()
    
    try:
        result = autopypath.auto_path()
        # Should return a path (this test is in a repo)
        assert result is not None
    finally:
        sys.path[:] = original_path


def test_module_exports():
    """Test that expected functions are exported."""
    assert 'find_repo_root' in autopypath.__all__
    assert 'add_repo_to_path' in autopypath.__all__
    assert 'auto_path' in autopypath.__all__
