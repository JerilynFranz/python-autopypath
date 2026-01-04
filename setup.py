"""Setup configuration for autopypath."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Read version from the package
version = {}
with open("autopypath/__init__.py") as f:
    for line in f:
        if line.startswith("__version__"):
            exec(line, version)
            break

setup(
    name="autopypath",
    version=version.get("__version__", "0.1.0"),
    author="Jerilyn Franz",
    author_email="",
    description="A small library to automatically configure the Python path for a script in a repo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JerilynFranz/python-autopypath",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        # No external dependencies required for core functionality
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "tox>=3.0",
        ],
    },
    keywords="python path pythonpath automation development",
    project_urls={
        "Bug Reports": "https://github.com/JerilynFranz/python-autopypath/issues",
        "Source": "https://github.com/JerilynFranz/python-autopypath",
    },
)
