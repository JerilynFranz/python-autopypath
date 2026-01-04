# python-autopypath

A small library to automatically configure the Python path for a script in a repo.

## Overview

`autopypath` is a lightweight Python library that automatically adds your repository root to the Python path. This eliminates the need for complex relative imports or manual sys.path manipulation when working with Python projects.

## Installation

Install from PyPI:

```bash
pip install autopypath
```

Or install from source:

```bash
git clone https://github.com/JerilynFranz/python-autopypath.git
cd python-autopypath
pip install -e .
```

## Usage

The simplest way to use autopypath is to call `auto_path()` at the top of your script:

```python
import autopypath
autopypath.auto_path()

# Now you can import from anywhere in your repo
from mypackage import mymodule
```

### Advanced Usage

Find the repository root:

```python
from autopypath import find_repo_root

repo_root = find_repo_root()
print(f"Repository root: {repo_root}")
```

Add repository to path with custom markers:

```python
from autopypath import find_repo_root, add_repo_to_path

# Find repo root using custom marker files
repo_root = find_repo_root(markers=['.git', 'setup.py', 'MyCustomMarker.txt'])
add_repo_to_path(repo_root)
```

## How It Works

`autopypath` searches for common repository marker files (`.git`, `setup.py`, `pyproject.toml`, `tox.ini`) starting from the current script's directory and traversing up the directory tree. Once found, it adds the repository root to `sys.path`.

## Development

This project uses tox for testing and development automation.

### Running Tests

```bash
# Run tests for all Python versions
tox

# Run tests for specific Python version
tox -e py311

# Run tests with coverage
tox -e cov
```

### Code Quality

```bash
# Run linting
tox -e lint

# Format code
tox -e format

# Type checking
tox -e type
```

### Building

```bash
# Build package
tox -e build

# Or use build directly
pip install build
python -m build
```

## Requirements

- Python 3.7 or higher
- No external dependencies for core functionality

## License

Apache License 2.0 - See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
