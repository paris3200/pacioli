![Build Status](https://github.com/paris3200/pacioli/actions/workflows/main.yml/badge.svg) [![codecov](https://codecov.io/gh/paris3200/pacioli/branch/main/graph/badge.svg?token=8JRRTMR6QO)](https://codecov.io/gh/paris3200/pacioli)

# Pacioli
> *Named after Luca Pacioli, the father of accounting and double-entry bookkeeping.*

**Beautiful financial reports for plain text accounting.**

Pacioli transforms your [Ledger CLI](http://www.ledger-cli.org) journal files into professionally typeset financial statements using LaTeX. Generate publication-ready balance sheets, income statements, and cash flow reports with customizable templates.

Pacioli supports three core financial statements:
- **Balance Sheet** - Point-in-time snapshot of assets, liabilities, and equity
- **Income Statement** - Period-based revenue and expense summary
- **Cash Flow Statement** - Cash-basis cash inflows and outflows using the direct method

Reports are generated using customizable templates to meet a variety of needs.  An example Balance Sheet using the default template can be seen [here](https://github.com/paris3200/pacioli/blob/master/tests/resources/sample_balance_sheet.pdf)


## Usage example
```

Usage: pacioli [OPTIONS] COMMAND [ARGS]...

  Pacioli generates LaTeX financial reports from Ledger CLI
  journal files.

Options:
  -c, --config TEXT  Path of config file.
  --help             Show this message and exit.

Commands:
  balance-sheet        Run a balance report using the account mappings defined...
  income-statement     Run a income statement for a set time period.
  cash-flow-statement  Run a cash flow statement for a set time period.
```

For detailed documentation, a comprehensive man page is included in the repository. To install it:
```sh
# From the repository directory
sudo cp man/pacioli.1 /usr/local/share/man/man1/
sudo mandb
man pacioli
```

Or view it directly without installation:
```sh
man ./man/pacioli.1
```

Note: Man pages are not automatically installed by pip. Distribution packages (Debian, Homebrew, etc.) typically handle man page installation.

### Cash Flow Statement

The cash flow statement uses the **direct method** and leverages Ledger's `--related` flag to ensure only **cash-basis transactions** are included. This means:

- Credit card purchases are excluded (they're liabilities, not cash flows)
- Only transactions that directly affect your cash accounts are included
- The statement reconciles: Beginning Cash + Net Change = Ending Cash

The statement categorizes cash flows into three activities:
- **Operating Activities**: Day-to-day business operations (income and expenses)
- **Investing Activities**: Long-term asset purchases and sales
- **Financing Activities**: Debt and equity transactions

Configure these categories in your config file by specifying which accounts belong to each category.

## Development setup

Pacioli uses [Poetry](https://python-poetry.org) to manage packaging and dependencies.  Install Poetry and then fork the project.  Pacioli and the required dependencies can be installed with poetry.

```sh
poetry install
```

## Release History

* 0.4.0
    * Add Cash Flow Statement support using the direct method
    * Leverage Ledger's --related flag for true cash-basis reporting
    * Add comprehensive test coverage (97% overall)
    * Support Python 3.10, 3.11, 3.12, and 3.13
* 0.3.4
    * Fix issue with effective and cleared flags not working when false.
    * Fix template not found error.
    * Fix issue with liability accounts with a positive balance being displayed as negative balance.
    * Add feature to use month names for income-statement time period.
* 0.3.3
    * Add support for Python 3.10
* 0.3.2
    * Code refactoring with increased documentation.
* 0.3.1
    * Add support for two word account names on the Income Statement
* 0.3.0
    * Add support for locale formatting of balances
* 0.2.0
    * Initial Release
* 0.0.1
    * Work in progress

## Meta

Jason Paris – paris3200@gmail.com

Distributed under the MIT license. See ``LICENSE`` for more information.

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->
