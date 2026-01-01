"""Tests for cli."""

import locale
import os

from click.testing import CliRunner

from pacioli import __version__
from pacioli.cli import cli


def test_entrypoint():
    """Is entrypoint script installed? (setup.py)."""
    exit_status = os.system("pacioli --help")
    assert exit_status == 0


def test_version_option():
    """It displays the version when --version flag is used."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert f"pacioli, version {__version__}" in result.output


def test_balance_sheet_outputs_to_standard_output():
    """Balance sheet returns a formatted report to standard output."""
    runner = CliRunner()
    report = runner.invoke(
        cli, "-c tests/resources/sample_config.yml balance-sheet --end-date 2020/3/31 -"
    )

    locale.setlocale(locale.LC_ALL, "")
    checking = f"{int(4138):n}"
    savings = f"{int(10030):n}"
    total_longterm = f"{int(325576):n}"

    assert "Acme LLC" in report.output
    assert f"\\hspace{{0.25in}}Checking  & {checking} \\" in report.output
    assert f"\\hspace{{0.25in}}Savings  & {savings} \\" in report.output
    assert f"{{Total Long-term Assets}} & " in report.output
    assert total_longterm in report.output


def test_income_statement_outputs_to_standard_output():
    """Balance sheet returns a formatted report to standard output."""
    runner = CliRunner()
    report = runner.invoke(
        cli,
        "-c tests/resources/sample_config.yml income-statement --begin-date 2020/2/1 --end-date 2020/3/31 -",
    )

    locale.setlocale(locale.LC_ALL, "")
    salary = f"{int(4913):n}"
    income = f"{int(4953):n}"
    expenses = f"{int(4162):n}"

    assert "Acme LLC" in report.output
    assert f"Salary & {salary} \\" in report.output
    assert "{Total Revenue} & " in report.output
    assert income in report.output
    assert "{Total Expenses} & " in report.output
    assert expenses in report.output


def test_balance_sheet_outputs_to_file(tmp_path):
    """Balance sheet writes to file."""
    # Create a temp directory
    d = tmp_path / "report"
    d.mkdir()
    output_file = d / "report.tex"

    runner = CliRunner()
    runner.invoke(
        cli,
        f"-c tests/resources/sample_config.yml balance-sheet --end-date 2020/3/31 {output_file}",
    )

    # Format balances
    locale.setlocale(locale.LC_ALL, "")
    checking = f"{int(4138):n}"
    savings = f"{int(10030):n}"
    total_longterm = f"{int(325576):n}"

    report = output_file.read_text()

    assert "Acme LLC" in report
    assert f"\\hspace{{0.25in}}Checking  & {checking} \\" in report
    assert f"\\hspace{{0.25in}}Savings  & {savings} \\" in report
    assert f"{{Total Long-term Assets}} & " in report
    assert total_longterm in report


def test_income_statment_outputs_to_file(tmp_path):
    """income-statement writes to file."""
    # Create a temp directory
    d = tmp_path / "report"
    d.mkdir()

    output_file = d / "report.tex"

    runner = CliRunner()
    runner.invoke(
        cli,
        f"-c tests/resources/sample_config.yml income-statement --begin-date 2020/2/1 --end-date 2020/3/31 {output_file}",
    )
    report = output_file.read_text()

    # Format balances
    locale.setlocale(locale.LC_ALL, "")
    salary = f"{int(4913):n}"
    income = f"{int(4953):n}"
    expenses = f"{int(4162):n}"

    assert "Acme LLC" in report
    assert f"Salary & {salary} \\" in report
    assert "{Total Revenue} & " in report
    assert income in report
    assert "{Total Expenses} & " in report
    assert expenses in report


def test_income_statement_displays_error_without_dates_or_month() -> None:
    """A error is displayed if a valid month or begin/end date not defined."""
    runner = CliRunner()
    result = runner.invoke(cli, "-c tests/resources/sample_config.yml income-statement")
    expected = "Error: Please enter a valid begin-date and end-date, month, or period."
    assert expected in result.output


def test_cash_flow_statement_outputs_to_standard_output():
    """Cash flow statement returns a formatted report to standard output."""
    runner = CliRunner()
    report = runner.invoke(
        cli,
        "-c tests/resources/sample_config.yml cash-flow-statement --begin-date 2020/2/1 --end-date 2020/3/31 -",
    )

    assert report.exit_code == 0
    assert "Acme LLC" in report.output
    assert "Cash Flow Statement" in report.output
    assert "OPERATING ACTIVITIES" in report.output
    assert "INVESTING ACTIVITIES" in report.output
    assert "FINANCING ACTIVITIES" in report.output
    assert "Net Change in Cash" in report.output


def test_cash_flow_statement_outputs_to_file(tmp_path):
    """Cash flow statement writes to file."""
    d = tmp_path / "report"
    d.mkdir()
    output_file = d / "cash_flow.tex"

    runner = CliRunner()
    result = runner.invoke(
        cli,
        f"-c tests/resources/sample_config.yml cash-flow-statement --begin-date 2020/2/1 --end-date 2020/3/31 {output_file}",
    )

    assert result.exit_code == 0
    report = output_file.read_text()

    assert "Acme LLC" in report
    assert "OPERATING ACTIVITIES" in report
    assert "Beginning Cash Balance" in report


def test_cash_flow_statement_requires_dates():
    """Cash flow statement displays error without dates."""
    runner = CliRunner()
    result = runner.invoke(cli, "-c tests/resources/sample_config.yml cash-flow-statement")
    expected = "Error: Please enter a valid begin-date and end-date, month, or period."
    assert expected in result.output


def test_cash_flow_statement_accepts_month_parameter():
    """Cash flow statement can use --month instead of begin/end dates."""
    runner = CliRunner()
    report = runner.invoke(
        cli,
        "-c tests/resources/sample_config.yml cash-flow-statement --month March -",
    )

    assert report.exit_code == 0
    assert "Acme LLC" in report.output
    assert "Cash Flow Statement" in report.output


def test_income_statement_accepts_period_parameter():
    """Income statement can use --period with month range."""
    runner = CliRunner()
    report = runner.invoke(
        cli,
        "-c tests/resources/sample_config.yml income-statement --period 'February 2020 to March 2020' -",
    )

    assert report.exit_code == 0
    assert "Acme LLC" in report.output
    locale.setlocale(locale.LC_ALL, "")
    salary = f"{int(4913):n}"
    assert f"Salary & {salary} \\" in report.output


def test_income_statement_accepts_period_single_month():
    """Income statement can use --period with single month."""
    runner = CliRunner()
    report = runner.invoke(
        cli,
        "-c tests/resources/sample_config.yml income-statement --period 'February 2020' -",
    )

    assert report.exit_code == 0
    assert "Acme LLC" in report.output


def test_cash_flow_statement_accepts_period_parameter():
    """Cash flow statement can use --period with month range."""
    runner = CliRunner()
    report = runner.invoke(
        cli,
        "-c tests/resources/sample_config.yml cash-flow-statement --period 'February 2020 to March 2020' -",
    )

    assert report.exit_code == 0
    assert "Acme LLC" in report.output
    assert "Cash Flow Statement" in report.output


def test_cash_flow_statement_accepts_period_single_month():
    """Cash flow statement can use --period with single month."""
    runner = CliRunner()
    report = runner.invoke(
        cli,
        "-c tests/resources/sample_config.yml cash-flow-statement --period 'February 2020' -",
    )

    assert report.exit_code == 0
    assert "Acme LLC" in report.output


def test_income_statement_period_invalid_format():
    """Income statement shows error with invalid period format."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        "-c tests/resources/sample_config.yml income-statement --period 'invalid format' -",
    )

    assert result.exit_code != 0
    assert "Invalid period format" in result.output
