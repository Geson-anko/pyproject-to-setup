from typing import Any

from .errors import ValidationError


def validate_project_data(data: dict[str, Any]) -> None:
    """Validate pyproject.toml content against PEP 621 requirements.

    Args:
        data: Parsed pyproject.toml content

    Raises:
        ValidationError: If validation fails
    """
    if "project" not in data:
        raise ValidationError("Missing [project] table")

    project = data["project"]
    if "name" not in project:
        raise ValidationError("Missing required field: project.name")

    if "version" not in project and "version" not in project.get("dynamic", []):
        raise ValidationError(
            "Version must be specified statically or marked as dynamic"
        )
