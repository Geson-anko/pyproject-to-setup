import logging
import sys
from pathlib import Path

import click

from . import __version__
from .converter import PyProjectConverter
from .errors import ConversionError
from .generator import SetupPyGenerator
from .models import ConversionConfig, SetupMode

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


@click.command()
@click.version_option(version=__version__, prog_name="pyproject-to-setup")
@click.argument(
    "pyproject_path",
    type=click.Path(exists=True, path_type=Path),
    default="pyproject.toml",
)
@click.option(
    "-m",
    "--mode",
    type=click.Choice(["full", "minimal", "hybrid"], case_sensitive=False),
    default="hybrid",
    help="Conversion mode [default: hybrid]",
    show_default=True,
)
@click.option(
    "-o",
    "--output",
    type=click.Path(path_type=Path),
    default="setup.py",
    help="Output path [default: setup.py]",
    show_default=True,
)
@click.option(
    "-q",
    "--quiet",
    is_flag=True,
    help="Suppress output except for errors",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Show debug information",
)
def main(
    pyproject_path: Path,
    mode: str,
    output: Path,
    quiet: bool,
    verbose: bool,
) -> None:
    """Convert pyproject.toml to setup.py.

    If PYPROJECT_PATH is not specified, looks for pyproject.toml in the current
    directory and its parents. Fails if no pyproject.toml is found.

    Examples:
        # Convert pyproject.toml in current directory
        $ pyproject-to-setup

        # Convert specific file with minimal mode
        $ pyproject-to-setup path/to/pyproject.toml -m minimal

        # Convert and output to different location
        $ pyproject-to-setup -o path/to/setup.py
    """
    # Configure logging based on verbosity
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    elif quiet:
        logging.getLogger().setLevel(logging.WARNING)

    try:
        if not pyproject_path.is_file():
            raise ConversionError(
                f"Could not find pyproject.toml in {pyproject_path.parent} or its parents"
            )

        logger.debug(f"Converting {pyproject_path} to {output}")
        logger.debug(f"Using mode: {mode}")

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
        output.write_text(content, encoding="utf-8")

        if not quiet:
            logger.info(f"Generated {output} successfully")

    except ConversionError as e:
        logger.error(str(e))
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        if verbose:
            logger.exception("Detailed traceback:")
        sys.exit(1)


if __name__ == "__main__":
    main()
