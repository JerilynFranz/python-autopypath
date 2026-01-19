Installation Instructions
=========================

Installing from PyPI
--------------------

The recommended way to install `autopypath` is via `pip`, the Python package
installer. You can install it by running the following command in your terminal:

.. code-block:: shell

   pip install autopypath


Installing from Source
----------------------

If you prefer to install `autopypath` from the source code, you can clone the
repository and install it manually. Here are the steps to do so:

.. code-block:: shell

   git clone https://github.com/JerilynFranz/autopypath.git
   cd autopypath
   pip install .

Development Installation
------------------------
For development purposes, you can install `autopypath` in editable mode.

This allows you to make changes to the source code and have them reflected
immediately without needing to reinstall the package.

To make this easier, a bootstrap script is provided.

You can run the following commands:

.. code-block:: shell

   git clone https://github.com/JerilynFranz/autopypath.git
   cd autopypath
   python3 bootstrap.py
   source .vs

This will set up the development environment and install `autopypath` in
editable mode. It will also setup `tox` and other development dependencies
to help with testing and building the project.

