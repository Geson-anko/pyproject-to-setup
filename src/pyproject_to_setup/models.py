from dataclasses import dataclass
from enum import Enum, auto
from typing import Required, TypedDict


class SetupMode(Enum):
    """Conversion mode for setup.py generation."""

    FULL = auto()  # Complete conversion
    MINIMAL = auto()  # Minimal setup.py
    HYBRID = auto()  # Keep dynamic values in setup.py


class AuthorInfo(TypedDict, total=False):
    """Author information structure."""

    name: str
    email: str


class ProjectMetadata(TypedDict, total=False):
    """Project metadata structure based on PEP 621."""

    name: Required[str]
    version: str
    description: str
    readme: dict[str, str]
    requires_python: str
    license: dict[str, str]
    authors: list[AuthorInfo]
    maintainers: list[AuthorInfo]
    keywords: list[str]
    classifiers: list[str]
    urls: dict[str, str]
    scripts: dict[str, str]
    gui_scripts: dict[str, str]
    entry_points: dict[str, dict[str, str]]
    dependencies: list[str]
    optional_dependencies: dict[str, list[str]]
    dynamic: list[str]


@dataclass
class ConversionConfig:
    """Configuration for the conversion process."""

    mode: SetupMode
    include_build_isolation: bool = True
    preserve_dynamic: bool = True
    error_on_unknown: bool = False
