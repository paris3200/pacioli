"""Tests for cli."""

import locale
import os
import subprocess


def test_entrypoint():
    """Is entrypoint script installed? (setup.py)."""
    exit_status = os.system("pacioli --help")
    assert exit_status == 0


def test_balance_sheet_outputs_to_standard_output():
    """Balance sheet returns a formatted report to standard output."""
    output = subprocess.run(
        [
            "pacioli",
            "-c",
            "tests/resources/sample_config.yml",
            "balance-sheet",
            "-",
            "--end-date",
            "2020/3/31",
        ],
        stdout=subprocess.PIPE,
    )
    report = output.stdout.decode()

    locale.setlocale(locale.LC_ALL, "")
    checking = f"{int(4138):n}"
    savings = f"{int(10030):n}"
    total_longterm = f"{int(325576):n}"
    assert "Acme LLC" in report
    assert f"& Checking  & {checking} \\" in report
    assert f"& Savings  & {savings} \\" in report
    assert f"{{Total Longterm Assets}} & & {total_longterm}" in report


def test_income_statement_outputs_to_standard_output():
    """Balance sheet returns a formatted report to standard output."""
    output = subprocess.run(
        [
            "pacioli",
            "-c",
            "tests/resources/sample_config.yml",
            "income-statement",
            "--begin-date",
            "2020/2/1",
            "--end-date",
            "2020/3/31",
            "-",
        ],
        stdout=subprocess.PIPE,
    )
    locale.setlocale(locale.LC_ALL, "")
    salary = f"{int(4913):n}"
    income = f"{int(4953):n}"
    expenses = f"{int(4162):n}"

    report = output.stdout.decode()
    assert "Acme LLC" in report
    assert f"Salary & {salary} \\" in report
    assert "{Total Income}} & & %s" % income in report
    assert "{Total Expenses}} & & %s \\" % expenses in report


def test_balance_sheet_outputs_to_file(tmp_path):
    """Balance sheet writes to file."""
    # Create a temp directory
    d = tmp_path / "report"
    d.mkdir()

    output_file = d / "report.tex"

    subprocess.run(
        [
            "pacioli",
            "-c",
            "tests/resources/sample_config.yml",
            "balance-sheet",
            output_file,
            "--end-date",
            "2020/3/31",
        ],
        stdout=subprocess.PIPE,
    )
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
    """Balance sheet writes to file."""
    # Create a temp directory
    d = tmp_path / "report"
    d.mkdir()

    output_file = d / "report.tex"

    subprocess.run(
        [
            "pacioli",
            "-c",
            "tests/resources/sample_config.yml",
            "income-statement",
            "--begin-date",
            "2020/2/1",
            "--end-date",
            "2020/3/31",
            output_file,
        ],
        stdout=subprocess.PIPE,
    )
    report = output_file.read_text()

    locale.setlocale(locale.LC_ALL, "")
    salary = f"{int(4913):n}"
    income = f"{int(4953):n}"
    expenses = f"{int(4162):n}"
    assert "Acme LLC" in report
    assert f"Salary & {salary} \\" in report
    assert "{Total Income}} & & %s" % income in report
    assert "{Total Expenses}} & & %s \\" % expenses in report
