![Build Status](https://github.com/paris3200/pacioli/actions/workflows/main.yml/badge.svg) [![codecov](https://codecov.io/gh/paris3200/pacioli/branch/main/graph/badge.svg?token=8JRRTMR6QO)](https://codecov.io/gh/paris3200/pacioli)

# Pacioli
> *Named after Luca Pacioli, the father of accounting and double-entry bookkeeping.*

**Beautiful financial reports for plain text accounting.**

Transform your [Ledger CLI](http://www.ledger-cli.org) journal files into professionally typeset financial statements. Stop wrestling with spreadsheets—generate publication-ready reports with LaTeX quality typography.

## Why Pacioli?

- **Professional Output**: LaTeX-typeset reports for small businesses, non-profits, grant applications, and tax preparation
- **Customizable Templates**: Adapt reports to match your organization's needs using Jinja2 templates
- **True Cash Flow**: Uses Ledger's `--related` flag for accurate cash-basis reporting required by many small businesses and non-profits
- **Plain Text First**: Works seamlessly with your existing Ledger workflow—no data import/export
- **Complete Picture**: Generate all three core financial statements from your journal file

## Features

**Balance Sheet** - Point-in-time snapshot of financial position
- Categorize accounts into current/long-term assets and liabilities
- See your net worth at any date
- [Example output](https://github.com/paris3200/pacioli/blob/master/src/pacioli/examples/sample_balance_sheet.pdf)

**Income Statement** - Period-based revenue and expense analysis
- Track profitability over any time period
- Support for multi-word account names
- Locale-aware number formatting
- [Example output](https://github.com/paris3200/pacioli/blob/master/src/pacioli/examples/sample_income_statement.pdf)

**Cash Flow Statement** - Cash-basis activity using the direct method
- Operating, Investing, and Financing activities
- Excludes non-cash transactions (credit card purchases)
- Reconciles to your actual cash position
- [Example output](https://github.com/paris3200/pacioli/blob/master/src/pacioli/examples/sample_cash_flow_statement.pdf)

## Quick Start

```bash
# Generate a balance sheet for today
pacioli balance-sheet

# Income statement for last month
pacioli income-statement --period "last month"

# Cash flow for Q1 2024
pacioli cash-flow-statement --period "Jan 2024 to Mar 2024"

# Use custom config
pacioli -c ~/.config/myreports.yml balance-sheet
```

All reports output LaTeX files that can be compiled to PDF with `pdflatex`.

## Documentation

- **Man page**: `man pacioli` (includes shell completion setup)
- **Example templates**: Included in the package
- **Config reference**: See man page for YAML configuration options

## Installation

```bash
pip install pacioli
```

Requires [Ledger CLI](http://www.ledger-cli.org) and a LaTeX distribution (for PDF output).

## Development

Pacioli uses [Poetry](https://python-poetry.org) for dependency management.

```sh
poetry install
poetry run pytest  # Run tests
nox                # Run all quality checks
```

See [CLAUDE.md](CLAUDE.md) for architecture details and development guidelines.

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all quality checks pass (`nox`)
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) for details.

Author: Jason Paris (paris3200@gmail.com)
