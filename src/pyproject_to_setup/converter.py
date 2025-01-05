import logging
import tomllib
from pathlib import Path
from typing import Any

from .errors import ConversionError, FileError, ValidationError
from .models import ConversionConfig, ProjectMetadata, SetupMode
from .validation import validate_project_data

logger = logging.getLogger(__name__)


class PyProjectConverter:
    """Convert pyproject.toml to setup.py parameters."""

    def __init__(self, config: ConversionConfig):
        self.config = config

    def load_pyproject(self, path: str | Path) -> dict[str, Any]:
        """Load and parse pyproject.toml file.

        Args:
            path: Path to pyproject.toml

        Returns:
            Parsed TOML content

        Raises:
            FileError: If file cannot be read
            ValidationError: If content is invalid
        """
        try:
            path = Path(path)
            with path.open("rb") as f:
                data = tomllib.load(f)
            validate_project_data(data)
            return data
        except FileNotFoundError:
            raise FileError(f"File not found: {path}")
        except tomllib.TOMLDecodeError as e:
            raise ValidationError(f"Invalid TOML syntax: {e}")
        except Exception as e:
            raise ConversionError(f"Unexpected error: {e}")

    def convert(self, pyproject_data: dict[str, Any]) -> dict[str, Any]:
        """Convert pyproject.toml data to setup() arguments.

        Args:
            pyproject_data: Parsed pyproject.toml content

        Returns:
            Dictionary of setup() arguments
        """
        if self.config.mode == SetupMode.MINIMAL:
            return {}

        project_data: ProjectMetadata = pyproject_data["project"]
        setup_kwargs: dict[str, Any] = {"name": project_data["name"]}

        # Handle dynamic fields
        dynamic_fields = set(project_data.get("dynamic", []))

        # Core metadata
        if "version" not in dynamic_fields:
            setup_kwargs["version"] = project_data.get("version")

        if "requires-python" not in dynamic_fields:
            setup_kwargs["python_requires"] = project_data.get("requires-python")

        # Dependencies
        if "dependencies" not in dynamic_fields:
            setup_kwargs["install_requires"] = project_data.get("dependencies", [])

        if "optional-dependencies" not in dynamic_fields:
            setup_kwargs["extras_require"] = project_data.get(
                "optional-dependencies", {}
            )

        # Entry points
        entry_points = self._convert_entry_points(project_data, dynamic_fields)
        if entry_points:
            setup_kwargs["entry_points"] = entry_points

        # URLs
        if "urls" not in dynamic_fields:
            urls = project_data.get("urls", {})
            if urls:
                setup_kwargs["project_urls"] = urls
                if "Homepage" in urls:
                    setup_kwargs["url"] = urls["Homepage"]

        return setup_kwargs

    def _convert_entry_points(
        self, project_data: ProjectMetadata, dynamic_fields: set
    ) -> dict[str, list[str]]:
        """Convert entry points configuration."""
        entry_points = {}

        if "scripts" not in dynamic_fields:
            scripts = project_data.get("scripts", {})
            if scripts:
                entry_points["console_scripts"] = [
                    f"{name} = {target}" for name, target in scripts.items()
                ]

        if "gui-scripts" not in dynamic_fields:
            gui_scripts = project_data.get("gui-scripts", {})
            if gui_scripts:
                entry_points["gui_scripts"] = [
                    f"{name} = {target}" for name, target in gui_scripts.items()
                ]

        return entry_points
