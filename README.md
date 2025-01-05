# pyproject-to-setup

![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Convert `pyproject.toml` to `setup.py` based on PEP 621 specification.

## Overview

A tool to help maintainers who need to support both modern Python packaging (`pyproject.toml`) and legacy packaging (`setup.py`) simultaneously. It provides flexible conversion modes and follows the PEP 621 specification.

## Installation

```bash
pip install pyproject-to-setup
```

## Quick Start

Basic usage:

```bash
# Convert pyproject.toml in current directory
pyproject-to-setup

# Show help
pyproject-to-setup --help
```

Example conversion:

```toml
# pyproject.toml
[project]
name = "spam-eggs"
version = "2020.0.0"
dependencies = ["httpx"]
requires-python = ">=3.8"
```

```python
# Generated setup.py
import setuptools

setuptools.setup(
    name="spam-eggs",
    version="2020.0.0",
    python_requires=">=3.8",
    install_requires=["httpx"],
)
```

## Features

- Convert between `pyproject.toml` and `setup.py`
- Multiple conversion modes (full, minimal, hybrid)
- Supports PEP 621 fields
- Command line interface and Python API
- Validation of input files

## Development

Requirements:

- Python 3.12+
- Docker (optional)
- Make (optional)

Basic setup:

### Using Docker

```bash
make docker-build
make docker-up
```

### Without Docker

1. Install `uv`: <https://docs.astral.sh/uv/getting-started/installation/>

```bash
uv sync
```

## CONTRIBUTING

For contribution guidelines, please see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
