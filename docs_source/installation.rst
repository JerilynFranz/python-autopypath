Installation
============

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

   git clone https://github.com/JerilynFranz/python-autopypath.git
   cd python-autopypath
   pip install .

.. _development-installation:

Development Installation
------------------------

For development purposes, you can install `autopypath` in editable mode.

This allows you to make changes to the source code and have them reflected
immediately without needing to reinstall the package.

To make this easier, a bootstrap script is provided.

You can run the following commands:

.. code-block:: shell
   :caption: Setting up the development environment

   git clone https://github.com/JerilynFranz/python-autopypath.git
   cd python-autopypath
   python bootstrap.py

And then activate the virtual environment with:

.. code-block:: shell
   :caption: Activating the virtual environment on Linux/macOS

   source .venv/bin/activate

or on Windows use:

.. code-block:: text
   :caption: Activating the virtual environment on Windows

   .venv\Scripts\activate.bat
   
or if using PowerShell:

.. code-block:: text
   :caption: Activating the virtual environment on Windows PowerShell

   .venv\Scripts\Activate.ps1

This will set up the development environment and install `autopypath` in
editable mode.

It will also setup `uv <https://docs.astral.sh/uv/>`_,
`tox <https://python-basics-tutorial.readthedocs.io/en/latest/test/tox.html>`_,
`sphinx <https://www.sphinx-doc.org/en/master/>`_ and other development dependencies
to help with testing and building the project.

For information on contributing to `autopypath`, please refer to the
:doc:`contributing` section.