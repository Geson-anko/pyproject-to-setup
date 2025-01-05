class ConversionError(Exception):
    """Base exception for conversion errors."""

    pass


class ValidationError(ConversionError):
    """Validation error in pyproject.toml content."""

    pass


class FileError(ConversionError):
    """File operation related errors."""

    pass
