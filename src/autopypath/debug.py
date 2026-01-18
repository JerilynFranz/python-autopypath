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

import logging
from pathlib import Path
from typing import Optional

from ._config_py_path import _ConfigPyPath
from ._context import _context_frameinfo
from ._log import log

__all__ = []

log.setLevel(logging.DEBUG)


_context_file: Optional[Path] = None
"""This is the file path of the script that imported this module, if available."""
_context_name: Optional[str] = None
"""This is the __name__ of the script that imported this module, if available."""
_path_adjusted: bool = False
"""Indicates whether autopypath adjusted sys.path automatically upon import."""

_context_info: Optional[tuple[Path, str]] = _context_frameinfo()
if _context_info is not None:
    _context_file, _context_name = _context_info
    if _context_name != '__main__':
        log.debug(
            'autopypath imported from non-__main__ context (%s); no sys.path changes will be applied.',
            _context_name,
        )
        _path_adjusted = False
    else:  # pragma: no cover  # Untestable branch for coverage: cannot run as __main__ from test frameworks
        _ConfigPyPath(context_file=_context_file)
        log.debug('sys.path adjusted automatically for %s', _context_file)
        _path_adjusted = True
else:  # pragma: no cover  # Wierd case I don't even know how to trigger: could not determine context file at all
    _context_file = None
    _context_name = None
    _path_adjusted = False
    log.warning('could not determine context file; no sys.path changes will be applied.')
