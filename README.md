[![Build Status](https://travis-ci.org/paris3200/pacioli.svg?branch=master)](https://travis-ci.org/paris3200/pacioli)

# Pacioli
> Beautiful report creation for plain text accounting.

Pacioli generates financial reports typeset with LaTeX from
[Ledger](http://www.ledger-cli.org) journal files.  The reports can be processed into a PDF using a variety of tools, such as pdflatex.

Reports are generated using customizable templates to meet a variety of needs.


## Usage example
```sh

Usage: pacioli [OPTIONS] COMMAND [ARGS]...

  Pacioli generates LaTeX financial reports from Ledger CLI
  journal files.

Options:
  -c, --config TEXT  Path of config file.
  --help             Show this message and exit.

Commands:
  balance-sheet     Run a balance report using the account mappings defined...
  income-statement  Run a income statement for a set time period.
```


## Development setup

Pacioli uses [Poetry](https://python-poetry.org) to manage packaging and dependencies.  Install Poetry and then fork the project.  Pacioli and the required dependencies can be installed with poetry.

```sh
poetry install
```

## Release History

* 0.2.0
    * Initial Release
* 0.0.1
    * Work in progress

## Meta

Jason Paris – paris3200@gamil.com

Distributed under the MIT license. See ``LICENSE`` for more information.

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->
