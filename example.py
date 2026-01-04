#!/usr/bin/env python
"""
Example script demonstrating autopypath usage.

This script shows how to use autopypath to automatically configure
the Python path in a repository.
"""

# Import and use autopypath at the top of your script
import autopypath
repo_root = autopypath.auto_path()

print(f"Repository root found: {repo_root}")
print(f"Python path includes: {repo_root in __import__('sys').path}")

# Now you can import from anywhere in your repository
# For example:
# from mypackage import mymodule

# Or use the individual functions for more control
from autopypath import find_repo_root, add_repo_to_path

# Find repo root manually
root = find_repo_root()
print(f"\nManually found root: {root}")

# You can also specify custom marker files
custom_root = find_repo_root(markers=['.git', 'custom_marker.txt'])
print(f"Root with custom markers: {custom_root}")
