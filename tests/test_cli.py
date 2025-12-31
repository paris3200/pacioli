"""Tests for cli."""

import locale
import os

from click.testing import CliRunner
from pacioli.cli import cli


def test_entrypoint():
    """Is entrypoint script installed? (setup.py)."""
    exit_status = os.system("pacioli --help")
    assert exit_status == 0


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
    assert f"& Checking  & {checking} \\" in report.output
    assert f"& Savings  & {savings} \\" in report.output
    assert f"{{Total Longterm Assets}} & & {total_longterm}" in report.output


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
    assert "{Total Income}} & & %s" % income in report.output
    assert "{Total Expenses}} & & %s \\" % expenses in report.output


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
    assert f"& Checking  & {checking} \\" in report
    assert f"& Savings  & {savings} \\" in report
    assert f"{{Total Longterm Assets}} & & {total_longterm}" in report


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
    assert "{Total Income}} & & %s" % income in report
    assert "{Total Expenses}} & & %s \\" % expenses in report


def test_income_statement_displays_error_without_dates_or_month() -> None:
    """A error is displayed if a valid month or begin/end date not defined."""
    runner = CliRunner()
    result = runner.invoke(cli, "-c tests/resources/sample_config.yml income-statement - ")
    expected = "Error: Please enter a valid begin-date and end-date or a valid month."
    assert expected in result.output
