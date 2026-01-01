# Pacioli Example Files

This directory contains example configuration and template files to help you get started with Pacioli.

## Quick Start

1. **Create your config directory:**
   ```bash
   mkdir -p ~/.config/pacioli/templates
   ```

2. **Copy the example files:**

   After installing Pacioli, you can find these example files in your Python site-packages directory. To locate them:
   ```bash
   python -c "import pacioli; import os; print(os.path.join(os.path.dirname(pacioli.__file__), 'examples'))"
   ```

   Copy the files to your config directory:
   ```bash
   # Copy the config file
   cp config.yml ~/.config/pacioli/config.yml

   # Copy the templates
   cp templates/*.tex ~/.config/pacioli/templates/
   ```

3. **Customize the configuration:**

   Edit `~/.config/pacioli/config.yml` to:
   - Set the path to your Ledger journal file
   - Map your Ledger accounts to the appropriate categories
   - Adjust the report title
   - Configure other options as needed

4. **Customize the templates (optional):**

   The LaTeX templates in `~/.config/pacioli/templates/` can be customized to match your preferred formatting and style.

## Files Included

- **config.yml** - Example configuration file with all available options
- **templates/balance_sheet.tex** - LaTeX template for balance sheet reports
- **templates/income_statement.tex** - LaTeX template for income statement reports
- **templates/cash_flow_statement.tex** - LaTeX template for cash flow statement reports

## Template Variables

The templates use Jinja2 with custom delimiters compatible with LaTeX:

- Variables: `\VAR{variable_name}`
- Blocks: `BLOCK{ for item in items }` ... `BLOCK{ endfor }`
- Comments: `\#{comment}`

See the example templates for usage patterns.

## More Information

For detailed documentation, visit: https://github.com/paris3200/pacioli
