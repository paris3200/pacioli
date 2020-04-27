import os
import subprocess


def test_entrypoint():
    """
    Is entrypoint script installed? (setup.py)
    """
    exit_status = os.system("pacioli --help")
    assert exit_status == 0


def test_config_file():
    """
    Config file can be passed via cli.
    """
    report = os.system("pacioli -c tests/resources/sample_config.yml")
    assert report == 0


def test_balance_sheet():
    """
    Balance sheet returns a formatted report to standard output.
    """
    output = subprocess.run(
        ["pacioli", "-c", "tests/resources/sample_config.yml", "--balance-sheet"],
        stdout=subprocess.PIPE,
    )
    report = output.stdout.decode()
    assert "Acme LLC" in report
    assert "& Checking  & 3648 \\" in report
    assert "& Savings  & 10030 \\" in report
    assert "{Total Longterm Assets} & & 325576" in report
    assert "{Total Current Assets}} & & 13678\\" in report
    assert "{Total Secured Liabilities} & & 184654\\" in report
