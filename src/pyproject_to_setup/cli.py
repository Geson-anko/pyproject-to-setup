import logging
import sys
from pathlib import Path

import click

from .converter import PyProjectConverter
from .errors import ConversionError
from .generator import SetupPyGenerator
from .models import ConversionConfig, SetupMode

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

logger = logging.getLogger(__name__)


@click.command()
@click.argument("pyproject_path", type=click.Path(exists=True))
@click.option(
    "--mode",
    type=click.Choice(["full", "minimal", "hybrid"]),
    default="hybrid",
    help="Conversion mode",
)
@click.option("--output", type=click.Path(), default="setup.py", help="Output path")
def main(pyproject_path: str, mode: str, output: str) -> None:
    """Convert pyproject.toml to setup.py."""
    try:
        config = ConversionConfig(
            mode=SetupMode[mode.upper()],
            include_build_isolation=True,
            preserve_dynamic=True,
        )

        converter = PyProjectConverter(config)
        generator = SetupPyGenerator(config)

        # Load and convert
        pyproject_data = converter.load_pyproject(pyproject_path)
        setup_kwargs = converter.convert(pyproject_data)

        # Generate and save
        content = generator.generate(setup_kwargs)
        Path(output).write_text(content, encoding="utf-8")

        logger.info(f"Generated {output} successfully")

    except ConversionError as e:
        logger.error(str(e))
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)
