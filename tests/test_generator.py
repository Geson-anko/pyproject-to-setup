from pyproject_to_setup.generator import SetupPyGenerator
from pyproject_to_setup.models import ConversionConfig, SetupMode


def test_generate_minimal(default_config):
    """Test generating minimal setup.py."""
    config = ConversionConfig(mode=SetupMode.MINIMAL)
    generator = SetupPyGenerator(config)
    content = generator.generate({})
    assert "setuptools.setup()" in content


def test_generate_with_arguments(default_config):
    """Test generating setup.py with arguments."""
    generator = SetupPyGenerator(default_config)
    setup_kwargs = {
        "name": "test",
        "version": "1.0.0",
        "install_requires": ["requests"],
    }
    content = generator.generate(setup_kwargs)
    assert "name='test'" in content
    assert "version='1.0.0'" in content
    assert "install_requires=['requests']" in content
