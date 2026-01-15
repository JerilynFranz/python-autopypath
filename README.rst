==========
autopypath
==========

A small library to automatically configure the Python path for a test script in a repo.


Overview
========

When writing test scripts for Python projects, it's not uncommon to encounter problems preventing
pytest from running normally because of errors preventing it from completing imports due to
broken code in unrelated modules. This can be especially problematic in monorepos or projects
with complex directory structures.

To make it easier to run a specific test script without worrying about import errors, autopypath
automatically adjusts the Python path to include the necessary directories, allowing tests
to be run directly from the file without pytest attempting to import unrelated modules.

By default, autopypath looks for a `src/` and a `tests` directory in the project repo root and adds
them to the Python path.

This is customizable.

Installation
============

You can install the package via pip:

.. code-block:: shell

    pip install autopypath

Usage
=====

To use autopypath with pytest, simply import it at the beginning of your test scripts and call the
`configure()` function. For example, at the top of your test script, add:

.. code-block:: python

    import autopypath


and add the following at the bottom of the script:

.. code-block:: python

    if __name__ == "__main__":
        pytest.main()


This will automatically adjust the Python path to include the necessary directories
to ensure your tests can find the modules they need without looking at unrelated code.

If you run the test script directly, autopypath will configure the Python path
before executing the tests. It will not interfere with normal pytest runs or
change the environment except when run directly.

Customization
=============

For more detailed usage instructions and examples, please refer to the documentation
in the `docs/` directory or visit the project's GitHub page.

