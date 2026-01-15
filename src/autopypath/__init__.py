"""Module providing autopypath functionality.

It allows automatic management of Python paths for project scripts so that
they can be run directly without manual path adjustments or reliance on IDE features.

It is **NOT** meant to replace normal package management or virtual environments,
but to facilitate running scripts directly during development and testing when
the build breaks due to import errors in unrelated code that prevent the normal test
runner from executing at all.

It detects the project root by looking for specific marker files or directories
(such as `pyproject.toml`, `.git`, or `.hg`) and adjusts `sys.path` to include
relevant subdirectories based on configurations found in `pyproject.toml`,
`.env` files, and `PYTHONPATH` environment variables.

If no valid project root or paths are found, it does not modify `sys.path` at all
but instead logs warnings to inform the user. It only makes adjustments when it can
confidently determine the correct paths to add and has been explicitly invoked
directly from a script being run as `__main__`. It will not add paths to non-existent
directories.

If there is any doubt about whether to adjust the path, the module opts to do nothing.

This is to avoid interfering with normal development workflows and to 'fail to safe'
by preventing accidentally breaking the environment. A 'if in doubt, do nothing' approach.

.. note::

   The automatic configuration only occurs when the module is imported
   at the top level of a script that is run directly (i.e., `__name__ == "__main__"`).

   It cannot be used from inside functions or class definitions. If the module is imported
   in any other context, it will log debug information but will not adjust `sys.path`.

   It should be imported before any other imports that depend on the adjusted Python path.

   The custom configuration function also only works when called directly
   from the top level of a script being executed as `__main__` - not from within
   functions or classes.

   Again, the function should be called before any other imports that depend on the adjusted Python path.

Modes of Operation
==================

**Fully Automatic Mode**
------------------------

When imported from a script, it automatically adjusts `sys.path` based on the
`pyproject.toml` file, `.env` file, and `PYTHONPATH` environment variables.
found in the project root. This ensures that modules can be imported
correctly when running scripts directly.

.. code-block:: python
    import autopypath
    # sys.path is now adjusted automatically

**Fully Automatic Debug Mode**
------------------------------

By importing the :module:`autopypath.debug` submodule,
detailed debug logging is enabled to trace how the project root is determined,
which paths are added to `sys.path`, and any issues encountered along the way.

This is useful for troubleshooting and understanding the internal workings of autopypath.

.. code-block:: python
    import autopypath.debug
    # sys.path is now adjusted automatically with debug logging enabled

**Custom Configured Mode**
--------------------------

Users can call the :func:`autopypath.custom.configure_pypath`
function to specify custom repository markers, manual paths, and loading strategies.
This provides flexibility for different project structures and requirements.

The path is **NOT** adjusted automatically on import in this mode; the user must call the
:func:`configure_pypath` function explicitly.

.. code-block:: python
    from autopypath.custom import configure_pypath

    configure_pypath(
        repo_markers={'setup.py': MarkerType.FILE, '.git': MarkerType.DIR},
        manual_paths=[Path('src'), Path('lib')],
        load_strategy=LoadStrategy.OVERRIDE,
    )
    # sys.path is now adjusted based on custom configuration

**Custom Configured Debug Mode**
--------------------------------

By importing the :module:`autopypath.custom.debug` submodule,
users can enable detailed debug logging while using custom configuration options.

The path is **NOT** adjusted automatically on import; the user must call the
:func:`configure_pypath` function explicitly.

.. code-block:: python
    from autopypath.custom.debug import configure_pypath

    configure_pypath(
        repo_markers={'setup.py': MarkerType.FILE, '.git': MarkerType.DIR},
        manual_paths=[Path('src'), Path('lib')],
        load_strategy=LoadStrategy.OVERRIDE,
    )
    # sys.path is now adjusted based on custom configuration

"""

import inspect
from pathlib import Path
from typing import Optional

from ._log import log
from ._config_py_path import ConfigPyPath

# Only run if directly imported by a script being executed as __main__
# If there is any doubt, do not run automatically


_context_file: Optional[Path] = None
"""This is the file path of the script that imported this module, if available."""

_current_frame = inspect.currentframe()
if _current_frame is not None:
    _parent_frame = _current_frame.f_back
    if _parent_frame and _parent_frame.f_globals.get('__name__') == '__main__':
        _context_file = Path(_parent_frame.f_globals.get('__file__', ''))

if _context_file is None:
    log.debug('could not determine context file; no sys.path changes will be applied.')
else:
    ConfigPyPath(context_file=_context_file)
    log.debug('sys.path adjusted automatically for %s', _context_file)
