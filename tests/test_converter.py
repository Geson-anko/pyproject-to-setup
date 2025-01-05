import pytest

from pyproject_to_setup.converter import PyProjectConverter
from pyproject_to_setup.errors import FileError
from pyproject_to_setup.models import ConversionConfig, SetupMode


def test_load_pyproject(sample_pyproject_path, default_config):
    """Test loading pyproject.toml file."""
    converter = PyProjectConverter(default_config)
    data = converter.load_pyproject(sample_pyproject_path)
    assert data["project"]["name"] == "spam-eggs"
    assert data["project"]["version"] == "2020.0.0"


def test_load_nonexistent_file(default_config):
    """Test loading non-existent file."""
    converter = PyProjectConverter(default_config)
    with pytest.raises(FileError, match="File not found"):
        converter.load_pyproject("nonexistent.toml")


def test_convert_minimal_mode(default_config):
    """Test conversion in minimal mode."""
    config = ConversionConfig(mode=SetupMode.MINIMAL)
    converter = PyProjectConverter(config)
    result = converter.convert({"project": {"name": "test"}})
    assert result == {}


def test_convert_full_mode(default_config):
    """Test conversion in full mode."""
    converter = PyProjectConverter(default_config)
    data = {
        "project": {
            "name": "test",
            "version": "1.0.0",
            "dependencies": ["requests"],
            "requires-python": ">=3.8",
        }
    }
    result = converter.convert(data)
    assert result["name"] == "test"
    assert result["version"] == "1.0.0"
    assert result["install_requires"] == ["requests"]
    assert result["python_requires"] == ">=3.8"
