import os
import subprocess


def test_entrypoint():
    """
    Is entrypoint script installed? (setup.py)
    """
    exit_status = os.system("pacioli --help")
    assert exit_status == 0


def test_balance_sheet_outputs_to_standard_output():
    """
    Balance sheet returns a formatted report to standard output.
    """
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
    assert "Acme LLC" in report
    assert "& Checking  & 4138 \\" in report
    assert "& Savings  & 10030 \\" in report
    assert "{Total Longterm Assets} & & 325576" in report
    assert "{Total Current Assets}} & & 14168\\" in report
    assert "{Total Secured Liabilities} & & 184654\\" in report


def test_balance_sheet_outputs_to_file(tmp_path):
    """
    Balance sheet writes to file.
    """

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
    report = output_file.read_text()
    assert "Acme LLC" in report
    assert "& Checking  & 4138 \\" in report
    assert "& Savings  & 10030 \\" in report
    assert "{Total Longterm Assets} & & 325576" in report
    assert "{Total Current Assets}} & & 14168\\" in report
    assert "{Total Secured Liabilities} & & 184654\\" in report
