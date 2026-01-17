"""Enables debug logging for autopypath when imported.

**Automatic Debug Mode**
------------------------
By importing the :module:`autopypath.debug` submodule,
detailed debug logging is enabled to trace how the project root is determined,
which paths are added to `sys.path`, and any issues encountered along the way.

Otherwise, it is functionally equivalent to importing :mod:`autopypath`.

This is useful for troubleshooting and understanding the internal workings of autopypath.

.. code-block:: python
    import autopypath.debug
    # sys.path is now adjusted automatically with debug logging enabled

"""

import inspect
from pathlib import Path
from typing import Optional

from ._config_py_path import _ConfigPyPath
from ._log import log

__all__ = []

log.setLevel('DEBUG')

# Only run if imported directly by a script being executed as __main__

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
    _ConfigPyPath(context_file=_context_file)
    log.debug('sys.path adjusted automatically for %s', _context_file)
