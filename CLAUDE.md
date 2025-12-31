# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Pacioli generates LaTeX-formatted financial reports (Balance Sheets and Income Statements) from Ledger CLI journal files. Reports use customizable Jinja2 templates and can be converted to PDF.

## Project Status

**Last Updated**: 2025-12-30

The project has been modernized to support Python 3.10+ with updated dependencies and modern Python packaging standards. All dependencies have been updated to their latest versions as of 2025, including security updates for PyYAML.

## Development Commands

### Environment Setup
```bash
# Install dependencies (including dev dependencies)
poetry install --with dev

# Update pre-commit hooks
pre-commit install
```

### Testing
```bash
# Run all tests with coverage
poetry run pytest --cov=pacioli

# Run specific test file
poetry run pytest tests/test_balance_sheet.py

# Run tests via nox (runs all quality checks)
nox

# Run only tests session
nox -s tests
```

### Code Quality
```bash
# Run linting
nox -s lint

# Auto-format code with black
nox -s black

# Type checking with mypy
nox -s mypy

# Type checking with pytype
nox -s pytype

# Security audit dependencies
nox -s safety
```

### Pre-commit Hooks
Pre-commit hooks run automatically on commit and include:
- Trailing whitespace removal
- Import reordering
- Black formatting
- Flake8 linting
- Pytest test suite

Install hooks: `pre-commit install`

## Architecture

### Core Design
The codebase follows an object-oriented architecture with inheritance:

1. **Pacioli** (`src/pacioli/pacioli.py`) - Base class providing shared functionality:
   - Executes Ledger CLI commands via subprocess
   - Renders Jinja2 templates with custom delimiters for LaTeX compatibility
   - Formats numbers using locale settings and converts negatives to parenthetical notation
   - Manages configuration and logging

2. **BalanceSheet** and **IncomeStatement** - Inherit from Pacioli:
   - BalanceSheet: Generates point-in-time financial position from categorized account mappings
   - IncomeStatement: Generates period-based income/expense report by parsing Ledger output

3. **CLI** (`src/pacioli/cli.py`) - Click-based command interface that instantiates report classes

### Key Integrations

**Ledger CLI**: All account data is retrieved by running `ledger` commands with subprocess. The tool parses text output using regex to extract balances. Supports flags for effective dates (`--effective`) and cleared transactions (`--cleared`).

**Configuration**: YAML config files define:
- Journal file path
- Template paths for reports
- Account category mappings (Current Assets, Longterm Assets, Secured/Unsecured Liabilities)
- Title and behavior flags

Default config location: `~/.config/pacioli/config.yml` (respects `XDG_CONFIG_HOME`)

**Jinja2 Templates**: Uses custom delimiters to avoid LaTeX conflicts:
- Block: `BLOCK{...}`
- Variable: `\VAR{...}`
- Comment: `\#{...}`
- Line statement: `%%`

Templates receive dictionaries with account short names (derived from final segment of account path) and formatted balances.

### Code Style

- Docstrings follow NumPy convention
- Max line length: 100 characters
- Flake8 enforces complexity max of 10
- Type hints required (checked by mypy)
- Black formatting enforced (version 24.10.0)
- Import sorting with isort (black-compatible profile)
- pyupgrade ensures modern Python 3.10+ syntax

### Python Packaging

The project uses modern Python packaging standards (PEP 621):
- `[project]` table in pyproject.toml for metadata
- `[tool.poetry]` only for Poetry-specific configuration
- Development dependencies in `[tool.poetry.group.dev.dependencies]`
- Supports Python 3.10, 3.11, 3.12, and 3.13

### CI/CD

GitHub Actions runs tests on all supported Python versions (3.10-3.13) with:
- Dependency caching for faster builds
- Code coverage reporting to Codecov
- Separate lint job with flake8, black, and mypy checks
