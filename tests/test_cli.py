import os


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
    report = os.system("pacioli -c tests/resources/sample_config.yml --balance-sheet")
    assert report == 0
