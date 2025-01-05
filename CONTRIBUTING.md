# Contributing to pyproject-to-setup

Thank you for your interest in contributing to pyproject-to-setup! This document provides guidelines and instructions for contributing.

## Development Environment Setup

### Prerequisites

- Python 3.12 or higher
- Docker (recommended)
- Make
- Git

### Setting Up

1. Fork and clone the repository:

   ```bash
   git clone https://github.com/your-username/pyproject-to-setup.git
   cd pyproject-to-setup
   ```

2. Set up the development environment:

   Using Docker (recommended):

   ```bash
   # Build development container
   make docker-build

   # Start container
   make docker-up

   # Attach to development shell
   make docker-attach
   ```

   Without Docker:

   ```bash
   # Install uv package manager
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Create and activate virtual environment
   uv venv
   source .venv/bin/activate

   # Install dependencies
   uv sync
   ```

## Development Workflow

### Code Quality Tools

We use the following tools:

- Ruff: Code formatting and linting
- Pyright: Static type checking
- Pytest: Testing framework

### Common Commands

```bash
# Run all checks (format, test, type check)
make run

# Run specific checks
make format  # Run formatters
make test   # Run tests
make type   # Run type checker
make clean  # Clean generated files
```

### Testing

Tests are located in the `tests/` directory. Please ensure:

- All new features include tests
- All tests pass locally before submitting a pull request
- Test coverage is maintained

Run tests with:

```bash
make test
```

### Type Hints

- Use type hints for all function arguments and return values
- Use the latest Python typing features
- Run type checker with:

```bash
make type
```

## Pull Request Process

1. Create a new branch for your feature:

   ```bash
   git checkout -b feature/name
   ```

2. Make your changes, following our coding standards

3. Run all checks:

   ```bash
   make run
   ```

4. Commit your changes with a clear message:

   ```bash
   git commit -m "Add feature: description of changes"
   ```

5. Push to your fork and submit a pull request

## Coding Standards

- Follow PEP 8 guidelines
- Use clear, descriptive variable and function names
- Write docstrings for all public functions and classes
- Keep functions focused and single-purpose
- Comment complex logic

## Questions and Support

- Open an issue for bugs or feature requests
- Use discussions for general questions

## Code of Conduct

We follow a standard Code of Conduct. Please be respectful and professional in all interactions.
