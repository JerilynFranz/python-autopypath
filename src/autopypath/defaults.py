"""Default configuration values for autopypath package."""

from pathlib import Path
from types import MappingProxyType
from typing import Final

from .marker_type import MarkerType
from .path_resolution import PathResolution
from .load_strategy import LoadStrategy

__all__ = []

REPO_MARKERS: Final[MappingProxyType[str, MarkerType]] = MappingProxyType(
    {
        'pyproject.toml': MarkerType.FILE,
        '.git': MarkerType.DIR,  # Git repository marker
        '.hg': MarkerType.DIR,  # Mercurial repository marker
        '.svn': MarkerType.DIR,  # Subversion repository marker
        '.bzr': MarkerType.DIR,  # Bazaar repository marker
        '.cvs': MarkerType.DIR,  # CVS repository marker
        '_darcs': MarkerType.DIR,  # Darcs repository marker
        '.fossil': MarkerType.DIR,  # Fossil repository marker
    }
)
"""Default repository markers used to identify the repository root. The presence of
any of these files or directories indicates the root of the project repository.

Default markers are:
- ``pyproject.toml``: Indicates the repository root by the presence of this file.
- ``.git``: Indicates a Git repository root by the presence of this directory.
- ``.hg``: Indicates a Mercurial repository root by the presence of this directory.
- ``.svn``: Indicates a Subversion repository root by the presence of this directory.
- ``.bzr``: Indicates a Bazaar repository root by the presence of this directory.
- ``.cvs``: Indicates a CVS repository root by the presence of this directory.
- ``_darcs``: Indicates a Darcs repository root by the presence of this directory.
- ``.fossil``: Indicates a Fossil repository root by the presence of this directory.

These can be overridden by the `repo_markers` parameter to :func:`configure_pypath`.
They can also be configured in the `pyproject.toml` file under the
`[tool.autopypath]` section.

The order for checking these markers is as follows. Resolution stops
at the first level the markers are defined.

If manual repo markers are provided via :func:`configure_pypath`, those are the only markers checked.

If no manual repo markers are provided but `pyproject.toml` defines `repo_markers`, those are used instead.

If neither manual repo markers nor `pyproject.toml` defines `repo_markers`, the default markers listed above are used

The order is:

manual paths
------------
.. code-block:: python
    from autopypath.custom import configure_pypath, MarkerType
    configure_pypath(
        repo_markers={'custom_marker.txt': MarkerType.FILE}
    )

pyproject.toml
--------------

.. code-block:: toml
    [tool.autopypath]
    repo_markers = { 'pyproject.toml' = 'file', '.git' = 'dir' }

default markers
-----------------

The default markers as defined above.

"""

PATH_RESOLUTION_ORDER: Final[tuple[PathResolution, ...]] = (
    PathResolution.MANUAL,
    PathResolution.PYPROJECT,
    PathResolution.DOTENV,
)

"""Default resolution order for :func:`sys.path` sources.

This is used if there is no specific resolution order provided in pyproject.toml
or other configuration.

It be overridden by the `path_resolution_order` parameter to `configure_pypath()`
or by configuring it in `pyproject.toml` under the
`[tool.autopypath]` section.

If overridden, it should be provided as a sequence of strings or
:class:`PathResolution` enum members. The overrides will replace the entire default order
and define a new order for resolving :func:`sys.path` sources.


Overrides can use any combination of the following values.
- `manual`: Paths provided directly via the `paths` parameter to `configure_pypath()`.
- `pyproject`: Paths specified in the `pyproject.toml` file in the repository root.
- `dotenv`: Paths specified in the `.env` file in the repository root.
- `env`: Paths from the shell environment's `:func:`sys.path`` variable.

Override Examples
-----------------

Manual
~~~~~~

.. code-block:: python
    from autopypath.custom import configure_pypath, PathResolution
    configure_pypath(
        path_resolution_order=[PathResolution.ENV, PathResolution.MANUAL]
    )

pyproject.toml
~~~~~~~~~~~~~~

You can specify the resolution order in `pyproject.toml` under the `[tool.autopypath]` section

Omitted path resolution types will not be used for resolution at runtime.

.. code-block:: toml
    [tool.autopypath]
    path_resolution_order = ['manual', 'pyproject', 'dotenv', 'env']

This order applies prioritization in the following way:

1. `paths` specified in the :func:`~autopypath.custom.configure_pypath` call (highest priority)
2. Paths specified in `pyproject.toml` in the repository root
3. Paths from PYTHONPATH specified in `.env` file in the repository root
4. Paths from the shell environment's PYTHONPATH variable (lowest priority)
"""

LOAD_STRATEGY: LoadStrategy = LoadStrategy.MERGE
"""Default load strategy for :func:`sys.path` sources.

This is used if there is no specific load strategy provided in pyproject.toml
or other configuration.

The available load strategies are defined as follows:

- **merge** (default)

    Combines paths from all sources.

    This allows a developer's local shell environment to supplement the
    paths defined in the project's configuration files. Paths are added
    to the front of `sys.path` in the order of priority.

- **override**

    Uses paths from the most specific source found (highest priority) only,
    ignoring others. This ensures a predictable path environment.

- **replace**
    Replaces the entire `sys.path` with the merged paths from all sources.
    This may break standard library and installed package imports,
    so it should be used with caution.


These can be overridden by the `load_strategy` parameter to :func:`configure_pypath`.
They can also be configured in the `pyproject.toml` file under the
`[tool.autopypath]` section.

The order for defining these load strategies is as follows. Definition stops
at the first level the strategies are defined at.

If a manual load strategies is provided via :func:`configure_pypath`, that is the stragegy used.

If no manual load strategy is provided but `pyproject.toml` defines `load_strategy`, that is used instead.

If `load_strategy` is not defined either manually or via `pyproject.toml`, the default strategy listed above is used

The order is:

manual strategy
---------------
.. code-block:: python
    from autopypath.custom import configure_pypath, MarkerType
    configure_pypath(
        load_strategy=LoadStrategy.OVERRIDE
    )

pyproject.toml
--------------

.. code-block:: toml
    [tool.autopypath]
    load_strategy = "override"

default markers
-----------------

The default strategy as defined above.

"""

PATHS: Final[tuple[Path, ...]] = (Path('src'), Path('tests'))
"""Default paths to add to sys.path relative to the repository root.

These directories are added to :var:`sys.path` if they exist in the repository root.

They can be overridden by the `paths` parameter to `configure_pypath()`.

They can also be configured in `pyproject.toml` under the
`[tool.autopypath]` section.

If a configured path does not exist or is not a directory, it will be logged at 'INFO' level

.. code-block:: toml
    [tool.autopypath]
    paths = ['src', 'tests']

"""
