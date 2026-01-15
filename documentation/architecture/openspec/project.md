# Project Context

## Purpose
A Python library package which provides **accretive data structures** - collections which can grow but never shrink. It aims to make programs safer by encouraging immutability and preventing unwanted state tampering, while acknowledging the limitations of Python's dynamic nature.

## Tech Stack
- **Language**: Python 3.10+
- **Build System**: Hatch
- **Linting**: Ruff, Vibelinter
- **Type Checking**: Pyright (Mypy is explicitly avoided)
- **Testing**: Pytest, Sphinx (for doctests)
- **Documentation**: Sphinx
- **Dependencies**: `absence`, `classcore`, `dynadoc`, `typing-extensions`

## Project Conventions

### Filesystem Organization
See `documentation/architecture/filesystem.rst` (relative: `../filesystem.rst`) for detailed filesystem organization.
- **Root**: Standard Python project structure (`pyproject.toml`, `sources/`, `tests/`, `documentation/`).
- **Source**: `sources/accretive/` with a centralized import hub (`__/`) pattern.

### Code Style
- **Line Length**: 79 characters.
- **Linting**: Enforced by Ruff and Vibelinter. See `pyproject.toml` for enabled rules.
- **Import Pattern**: Uses a `__` directory for centralized imports (`imports.py`, `exceptions.py`, etc.).
- **Type Hints**: Extensive use of type hints, checked by Pyright.

### Architecture Patterns
- **Common Architecture**: Follows patterns from [python-project-common](https://github.com/emcd/python-project-common).
- **Accretive Data Structures**: Classes that allow addition but not removal or modification of existing entries/attributes.
- **Centralized Imports**: Uses `sources/accretive/__/` to manage internal and external imports.
- **Exception Hierarchy**: Centralized in `sources/accretive/exceptions.py`.

### Testing Strategy
- **Framework**: Pytest for unit tests.
- **Doctests**: Run via Sphinx (Pytest configuration explicitly excludes them).
- **Conventions**:
    - Test files located in `tests/`.
    - Test functions follow `test_[0-9][0-9][0-9]_*` pattern.
    - Long-running tests marked with `@pytest.mark.slow`.

### Git Workflow
- **Changelog**: Uses `towncrier` with fragments in `.auxiliary/data/towncrier`.
- **CI**: GitHub Actions (`tester.yaml`).

## Domain Context
- **Immutability**: The library provides "accretive" collections (dictionaries, namespaces) that allow growth but prevent shrinkage or mutation of existing elements.
- **Limitations**: Python cannot truly enforce immutability; the library provides safety mechanisms that can be circumvented by determined users.
- **Key Classes**:
    - `Dictionary`: Accretive dictionary.
    - `Namespace`: Accretive namespace (like `SimpleNamespace`).
    - `@accretive` / `@with_standard_behaviors`: Decorators for creating accretive objects.

## Important Constraints
- **Python Version**: Must support Python 3.10 through 3.14 (and PyPy).
- **Type Checker**: Use Pyright, not Mypy.
- **Doctests**: Must be run with Sphinx, not Pytest.

## External Dependencies
- **Core**: `absence`, `classcore`, `dynadoc`.
- **Dev**: `hatch`, `ruff`, `pyright`, `pytest`, `sphinx`.
