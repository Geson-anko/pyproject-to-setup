from pyproject_to_setup.converter import PyProjectConverter
from pyproject_to_setup.generator import SetupPyGenerator


def test_full_conversion_pipeline(sample_pyproject_path, default_config, tmp_path):
    """Test the full conversion pipeline with sample pyproject.toml."""
    # Convert pyproject.toml to setup() arguments
    converter = PyProjectConverter(default_config)
    pyproject_data = converter.load_pyproject(sample_pyproject_path)
    setup_kwargs = converter.convert(pyproject_data)

    # Verify conversion results
    assert setup_kwargs["name"] == "spam-eggs"
    assert setup_kwargs["version"] == "2020.0.0"
    assert "httpx" in setup_kwargs["install_requires"]
    assert setup_kwargs["python_requires"] == ">=3.8"

    # Generate setup.py
    generator = SetupPyGenerator(default_config)
    setup_py_content = generator.generate(setup_kwargs)

    # Verify generated content
    assert "import setuptools" in setup_py_content
    assert "name='spam-eggs'" in setup_py_content
    assert "version='2020.0.0'" in setup_py_content

    # Write and verify file
    output_path = tmp_path / "setup.py"
    output_path.write_text(setup_py_content)
    assert output_path.exists()
    assert output_path.read_text().strip() == setup_py_content.strip()


def test_entry_points_conversion(default_config):
    """Test conversion of entry points."""
    converter = PyProjectConverter(default_config)
    data = {
        "project": {
            "name": "test",
            "version": "1.0.0",
            "scripts": {"cli-command": "package:main"},
            "gui-scripts": {"gui-command": "package:gui"},
        }
    }
    setup_kwargs = converter.convert(data)
    assert "entry_points" in setup_kwargs
    assert "console_scripts" in setup_kwargs["entry_points"]
    assert "gui_scripts" in setup_kwargs["entry_points"]
    assert setup_kwargs["entry_points"]["console_scripts"] == [
        "cli-command = package:main"
    ]
    assert setup_kwargs["entry_points"]["gui_scripts"] == ["gui-command = package:gui"]


def test_dynamic_fields_handling(default_config):
    """Test handling of dynamic fields."""
    converter = PyProjectConverter(default_config)
    data = {
        "project": {
            "name": "test",
            "version": "1.0.0",
            "dynamic": ["dependencies", "optional-dependencies"],
        }
    }
    setup_kwargs = converter.convert(data)
    assert "install_requires" not in setup_kwargs
    assert "extras_require" not in setup_kwargs
