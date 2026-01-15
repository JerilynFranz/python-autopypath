==========
autopypath
==========
  
autopypath is a Python library that simplifies the management of the Python module search path (`sys.path`)
for testing and development environments. It automatically finds and adds relevant directories to `sys.path`
based on configuration files such as `pyproject.toml` and `.env`. 

It is not a replacement for virtual environments but rather a tool to dynamically adjust `sys.path` in tests
or scripts, making it easier to work with possibly broken build or development setups where
the testing framework cannot be run because it attempts to import modules that are not yet installed
or where other tests cannot be loaded due to breakage from ongoing development.

It is designed to be lightweight and easy to integrate into existing testing setups, providing a seamless experience
for developers working on Python projects and "just working" with their code without worrying about
the intricacies of path resolution and IDE or test runner configurations.

Usage
=====

This is an example of how to use autopypath in your test scripts
so that a single test can be run directly from the command line
without requiring the entire test suite to be executed even
if the project is not fully built or installed.

Even if your test script is located deep in a subdirectory, you can still use autopypath
to ensure that the necessary paths are added to :var:`sys.path` without any manual intervention.

Here is an example test script named `my_test_script.py`:

.. code-block:: python

   import autopypath
   import pytest

   import mypackage.my_module
   from mypackage import my_other_module

   ### tests
   ...

   if __name__ == '__main__':
       pytest.main([__file__])

It can then be run directly *without having to install the package first
or manually munge :var:`sys.path`, or `PYTHONPATH` to make it work*.

.. note::

   While autopypath is primarily designed to be used in test scripts,
   it can also be utilized in other Python scripts where dynamic
   adjustment of :var:`sys.path` is needed based on project configuration.

It automatically resolves the paths based on the configuration files in the root directory
of the project and adds them to 'sys.path' before running the tests.

Because you can run the test script directly, it is easy to integrate into IDEs
or other development tools that may not be aware of the project's build system.

It has pyproject.toml and .env support out of the box, so if your project
uses those files for configuration, autopypath can automatically pick them up
and adjust :var:`sys.path` accordingly.

If you already use pyproject.toml to define your project structure, autopypath has
first-class support for configuring paths based on that file.

.. code-block:: bash

   python my_test_script.py


.. toctree::
   :name: contents
   :maxdepth: 2
   :caption: Table of Contents

   installation
   usage
   tutorials
   command_line_options
