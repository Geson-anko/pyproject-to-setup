from pathlib import Path

import pytest

from pyproject_to_setup.models import ConversionConfig, SetupMode


@pytest.fixture
def sample_pyproject_path(tmp_path):
    """Create a temporary sample pyproject.toml file."""
    content = '''[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "spam-eggs"
version = "2020.0.0"
dependencies = [
    "httpx",
    "gidgethub[httpx]>4.0.0",
    "django>2.1; os_name != 'nt'",
    "django>2.0; os_name == 'nt'",
]
requires-python = ">=3.8"
authors = [
    {name = "Pradyun Gedam", email = "pradyun@example.com"},
    {name = "Tzu-Ping Chung", email = "tzu-ping@example.com"}
]
description = "Lovely Spam! Wonderful Spam!"'''

    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(content)
    return pyproject


@pytest.fixture
def default_config():
    """Default conversion configuration."""
    return ConversionConfig(
        mode=SetupMode.FULL, include_build_isolation=True, preserve_dynamic=True
    )
