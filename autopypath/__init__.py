"""
autopypath - Automatically configure the Python path for a script in a repo.

This module automatically adds the repository root to the Python path,
making it easier to import modules from anywhere within the repository.
"""

import os
import sys
from pathlib import Path

__version__ = "0.1.0"
__all__ = ["add_repo_to_path", "find_repo_root", "auto_path"]


def find_repo_root(start_path=None, markers=None):
    """
    Find the repository root by looking for marker files.
    
    Args:
        start_path: Path to start searching from (defaults to current file's directory)
        markers: List of marker files/directories that indicate repo root
                (defaults to ['.git', 'setup.py', 'pyproject.toml'])
    
    Returns:
        Path object pointing to repository root, or None if not found
    """
    if start_path is None:
        # Start from the caller's directory
        frame = sys._getframe(1)
        start_path = os.path.dirname(os.path.abspath(frame.f_code.co_filename))
    
    if markers is None:
        markers = ['.git', 'setup.py', 'pyproject.toml', 'tox.ini']
    
    current = Path(start_path).resolve()
    
    # Traverse up the directory tree
    for parent in [current] + list(current.parents):
        for marker in markers:
            if (parent / marker).exists():
                return parent
    
    return None


def add_repo_to_path(repo_root=None):
    """
    Add the repository root to the Python path if not already present.
    
    Args:
        repo_root: Path to repository root (will be auto-detected if not provided)
    
    Returns:
        The repository root path that was added, or None if not found
    """
    if repo_root is None:
        repo_root = find_repo_root()
    
    if repo_root is None:
        return None
    
    repo_root_str = str(repo_root)
    
    if repo_root_str not in sys.path:
        sys.path.insert(0, repo_root_str)
    
    return repo_root


def auto_path():
    """
    Convenience function to automatically configure the Python path.
    
    This is the simplest way to use autopypath - just call this function
    at the top of your script.
    
    Returns:
        The repository root path that was added, or None if not found
    """
    return add_repo_to_path()
